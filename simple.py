import time
import serial
import matplotlib.pyplot as plt 

# interactive mode on
plt.ion()

# =========================================================
# === BEÁLLÍTÁSOK ===
# =========================================================
log_filename = "data\\meres_1.txt"

colors = ["#AF0", "#A0F", "#0AF", "#FA0", "#F0A", "#0FA", 
          "#A00", "#0A0", "#00A", "#AA0", "#A0A", "#0AA", 
          "#F00", "#0F0", "#00F", "#FF0", "#F0F", "#0FF", 
          "#000"]

measurements = {}
sensors = []
sensor_colors = {}
timestamps = []
plots = []

log_initialized = False
log_counter = 1

# =========================================================
# === KÉT PLOT EGYMÁS MELLETT ===
# =========================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

ax1.set_title("Szenzorok (idő)")
ax1.set_xlabel("idő (s)")
ax1.set_ylabel("hőmérséklet")

ax2.set_title("Szenzor vs referencia")
ax2.set_xlabel("Referencia hőmérséklet")
ax2.set_ylabel("Szenzor hőmérséklet")

sensor_port = serial.Serial("/dev/cu.usbmodem2101", 115200, timeout=0)
# sensor_port = serial.Serial("COM6", 115200, timeout=0)

# =========================================================
# === FEJLÉC OLVASÁS ===
# =========================================================
line = sensor_port.readline()
while True:

    if line == b"":
        time.sleep(0.1)
        line = sensor_port.readline()
        continue

    raw_measurement = line.decode("utf-8").strip()
    values = raw_measurement.split("\t")

    if values[0] == "N" and values[1] == "Millis":
        sensors = values[2:]
        print("Sensors:", sensors)

        for sensor in sensors:
            measurements[sensor] = []
            sensor_colors[sensor] = colors.pop()

        # ✅ referencia = első szenzor (3. oszlop)
        ref_sensor = sensors[0]

        # ✅ log fájl fejléc
        with open(log_filename, "wt", encoding="utf-8") as f:
            header = ["N", "Millis"] + sensors
            f.write("\t".join(header) + "\n")

        log_initialized = True
        log_counter = 1
        break

    time.sleep(0.1)
    line = sensor_port.readline()

# =========================================================
# === FŐ MÉRÉSI CIKLUS ===
# =========================================================
while True:
    line = sensor_port.readline()
    while line != b"":
        raw_measurement = line.decode("utf-8").strip()
        values = raw_measurement.split("\t")

        # fejléc átugrása
        if values[0] == "N" and values[1] == "Millis":
            break

        # régi plotok törlése
        for plot in plots:
            plot.remove()
        plots.clear()

        # =================================================
        # --- MÉRÉSEK KIOLVASÁSA ---
        # =================================================
        for i, raw in enumerate(values[2:]):
            sensor_name = sensors[i]
            measurement_value = float(raw[:-1])
            measurements[sensor_name].append(measurement_value)
        
        millis_val = int(values[1])
        time_sec = millis_val / 1000   # ✅ MÁSODPERC
        timestamps.append(time_sec)

        # =================================================
        # ✅ AZONNALI MENTÉS MINDEN ÚJ SORNÁL
        # =================================================
        if log_initialized:
            row = [str(log_counter), values[1]]

            for sensor in sensors:
                row.append(f"{measurements[sensor][-1]:.3f}")

            with open(log_filename, "at", encoding="utf-8") as f:
                f.write("\t".join(row) + "\n")

            log_counter += 1

        # --- REFERENCIA AKTUÁLIS ÉRTÉKEI ---
        ref_vals = measurements[ref_sensor]

        # =================================================
        # === PLOTTOLÁS ===
        # =================================================
        for sensor in sensors:
            current_measurements = measurements[sensor]

            # ✅ referencia dupla vastag
            lw = 3 if sensor == ref_sensor else 1.5

            # --- BAL: idő (s) vs szenzor ---
            p1, = ax1.plot(timestamps, current_measurements,
                           color=sensor_colors[sensor],
                           linewidth=lw)
            plots.append(p1)

            # --- JOBB: szenzor vs referencia ---
            if len(ref_vals) == len(current_measurements):
                p2, = ax2.plot(ref_vals, current_measurements,
                               color=sensor_colors[sensor],
                               linewidth=lw)
                plots.append(p2)

        # --- JOBB OLDAL: referencia átló (y = x) ---
        if len(ref_vals) > 1:
            p_ref, = ax2.plot(ref_vals, ref_vals, "k--", linewidth=3)
            plots.append(p_ref)

        ax1.grid(True)
        ax2.grid(True)

        line = sensor_port.readline()

    plt.pause(0.25)
