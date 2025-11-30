import time
import serial
import numpy as np 
import matplotlib.pyplot as plt 

# interactive mode on
plt.ion()

measurements = {}
plots = []

plt.title("Szenzorok") 
plt.xlabel("idő") 
plt.ylabel("hőmérséklet") 

sensor_port = serial.Serial("/dev/cu.usbmodem2101", 115200, timeout=0)
while True:
    line = sensor_port.readline()
    while line != b"":
        raw_measurement = line.decode("utf-8").strip()
        print(raw_measurement)
        values = raw_measurement.split(";")
        
        try:
            raw = int(values[3])
        except:
            raw = 0
        
        try:
            corrected = int(values[4])
        except:
            corrected = 0

        measurement = {
            "type": values[0],
            "number": int(values[1]),
            "timestamp": int(values[2]),
            "raw": raw,
            "corrected": corrected
        }

        if measurement["type"] not in measurements:
            measurements[measurement["type"]] = []
        measurements[measurement["type"]].append(measurement)

        for plot in plots:
            plot.remove()
        plots.clear()

        for name in measurements:
            current_measurements = measurements[name]
            raw_values = [meas["raw"] for meas in current_measurements]
            corrected_values = [meas["corrected"] for meas in current_measurements]
            timestamps = [meas["timestamp"] for meas in current_measurements]

            if len(raw_values) == len(timestamps):
                p, = plt.plot(timestamps, raw_values)
                plots.append(p)
            
            if len(corrected_values) == len(timestamps):
                p, = plt.plot(timestamps, corrected_values)
                plots.append(p)

        line = sensor_port.readline()

    plt.pause(0.25)
    