import time
import serial
import matplotlib.pyplot as plt 

# interactive mode on
plt.ion()

colors = ["#C00", "#0C0", "#00C", "#CC0", "#C0C", "#0CC", "#000"]

measurements = {}
sensors = []
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
    values = raw_measurement.split(";")
    if values[0] == "name":
        sensors = values[2:-1]
        print("Sensors: ", sensors)
        for sensor in sensors:
            measurements[sensor] = []
        break
    time.sleep(0.1)
    line = sensor_port.readline()

while True:
    line = sensor_port.readline()
    while line != b"":
        raw_measurement = line.decode("utf-8").strip()
        values = raw_measurement.split(";")

        # skip header
        if values[0] == "name":
            continue

        for plot in plots:
            plot.remove()
        plots.clear()

        for i, raw in enumerate(values[2:-1]):
            sensor_name = sensors[i]
            measurement_value = float(raw)
            measurements[sensor_name].append(measurement_value)
        
        timestamps.append(int(values[1]))

        for sensor in sensors:
            current_measurements = measurements[sensor]
            timestamps = [meas["timestamp"] for meas in current_measurements]
            p, = plt.plot(timestamps, current_measurements)
            plots.append(p)

        line = sensor_port.readline()

    plt.pause(0.25)
    