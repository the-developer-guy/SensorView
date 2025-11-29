import serial
import numpy as np 
import matplotlib.pyplot as plt 

# interactive mode on
plt.ion()

measurements = [1, 2, 3]
meas2 = [2, 4, 6]
timestamps = [1, 2, 3]

plt.title("Szenzorok") 
plt.xlabel("idő") 
plt.ylabel("hőmérséklet") 

line1, = plt.plot(timestamps, measurements, color="#500")
line2, = plt.plot(timestamps, meas2, color="#0F0")

for i in range(4, 100):
    measurements.append(i)
    meas2.append(i*2)
    timestamps.append(i)

    line1.remove()
    line2.remove()
    line1, = plt.plot(timestamps, measurements, color="#500")
    line2, = plt.plot(timestamps, meas2, color="#0F0")

    plt.pause(0.25)