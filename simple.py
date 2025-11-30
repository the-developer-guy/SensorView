import time
import serial
import matplotlib.pyplot as plt 

# interactive mode on
plt.ion()

colors = ["#AF0", "#A0F", "#0AF", "#FA0", "#F0A", "#0FA", 
          "#A00", "#0A0", "#00A", "#AA0", "#A0A", "#0AA", 
          "#F00", "#0F0", "#00F", "#FF0", "#F0F", "#0FF", 
          "#000"]

measurements = {}
sensors = []
sensor_colors = {}
timestamps = []
plots = []

plt.title("Szenzorok") 
plt.xlabel("idő") 
plt.ylabel("hőmérséklet") 

sensor_port = serial.Serial("/dev/cu.usbmodem2101", 115200, timeout=0)

# warmup for header
line = sensor_port.readline()
while line != b"":
    raw_measurement = line.decode("utf-8").strip()
    values = raw_measurement.split("\t")
    if values[0] == "nr" and values[1] == "time":
        sensors = values[2:-1]
        print("Sensors: ", sensors)
        for sensor in sensors:
            measurements[sensor] = []
            sensor_colors[sensor] = colors.pop()
        break
    time.sleep(0.1)
    line = sensor_port.readline()

while True:
    line = sensor_port.readline()
    while line != b"":
        raw_measurement = line.decode("utf-8").strip()
        values = raw_measurement.split("\t")

        # skip header
        if values[0] == "nr" and values[1] == "time":
            continue

        for plot in plots:
            plot.remove()
        plots.clear()

        for i, raw in enumerate(values[2:-1]):
            sensor_name = sensors[i]
            measurement_value = float(raw[:-1])
            measurements[sensor_name].append(measurement_value)
        
        timestamps.append(int(values[1]))

        for sensor in sensors:
            current_measurements = measurements[sensor]
            timestamps = [meas["timestamp"] for meas in current_measurements]
            p, = plt.plot(timestamps, current_measurements, color=sensor_colors[sensor])
            plots.append(p)

        line = sensor_port.readline()

    plt.pause(0.25)
    