import numpy as np
import matplotlib.pyplot as plt

# === SZÍNEK (simple.py kompatibilis) ===
COLORS = ["#AF0", "#A0F", "#0AF", "#FA0", "#F0A", "#0FA",
          "#A00", "#0A0", "#00A", "#AA0", "#A0A", "#0AA",
          "#F00", "#0F0", "#00F", "#FF0", "#F0F", "#0FF",
          "#000"]


# ============================================================
# 1) FILE BEOLVASÁS
# ============================================================
def load_measurements(filename):
    sensors = []
    data_rows = []

    with open(filename, "rt", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        parts = line.strip().split("\t")

        if parts[0] == "N" and parts[1] == "Millis":
            sensors = parts[2:]   # szenzor nevek
            continue

        if parts[0].isdigit():
            data_rows.append(parts)

    # referencia = 3. oszlop = első szenzor
    ref_sensor = sensors[0]

    ref_temps = []
    measurements = {s: [] for s in sensors}

    for row in data_rows:
        ref_val = float(row[2])   # referencia
        ref_temps.append(ref_val)

        for i, sensor in enumerate(sensors):
            measurements[sensor].append(float(row[i + 2]))

    return np.array(ref_temps), sensors, measurements, ref_sensor


# ============================================================
# 2) FITTELÉS: F = A + B*Tref + C*Tref²
# ============================================================
def fit_sensors(ref_temps, sensors, measurements):
    fit_params = {}

    for sensor in sensors:
        y = np.array(measurements[sensor])
        C, B, A = np.polyfit(ref_temps, y, 2)
        fit_params[sensor] = (A, B, C)

    return fit_params


# ============================================================
# 3) PLOTTOLÁS: 3 EGYMÁS MELLETTI ÁBRA
# ============================================================
def plot_results(ref_temps, sensors, measurements, fit_params, ref_sensor):
    sensor_colors = {}
    colors = COLORS.copy()

    for sensor in sensors:
        sensor_colors[sensor] = colors.pop()

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20, 5))

    # --- Címek ---
    ax1.set_title("Mérés + fitt")
    ax2.set_title("Nem korrigált hiba (mért - referencia)")
    ax3.set_title("Korrigált hiba (mért - fitt)")

    for ax in [ax1, ax2, ax3]:
        ax.set_xlabel("Referencia hőmérséklet (°C)")
        ax.grid(True)

    ax1.set_ylabel("Hőmérséklet (°C)")
    ax2.set_ylabel("Hiba (°C)")
    ax3.set_ylabel("Hiba (°C)")
    ax2.axhline(0, linestyle="--")
    ax3.axhline(0, linestyle="--")

    # --- Referencia vastag vonal mindháromon ---
    ax1.plot(ref_temps, ref_temps, linewidth=4, label=f"{ref_sensor} (referencia)")
    ax2.plot(ref_temps, np.zeros_like(ref_temps), linewidth=4, label="Referencia")
    ax3.plot(ref_temps, np.zeros_like(ref_temps), linewidth=4, label="Referencia")

    # --- Szenzorok ---
    for sensor in sensors:
        y = np.array(measurements[sensor])
        A, B, C = fit_params[sensor]

        x_fit = np.linspace(ref_temps.min(), ref_temps.max(), 500)
        y_fit_smooth = A + B * x_fit + C * x_fit * x_fit
        y_fit = A + B * ref_temps + C * ref_temps * ref_temps

        error_uncorrected = y - ref_temps
        error_corrected = y - y_fit

        lw = 4 if sensor == ref_sensor else 1.5

        # 1) mérés + fitt
        ax1.plot(ref_temps, y, color=sensor_colors[sensor], linewidth=lw, label=sensor)
        ax1.plot(x_fit, y_fit_smooth, "--", color=sensor_colors[sensor])

        # 2) nem korrigált hiba
        ax2.plot(ref_temps, error_uncorrected,
                 color=sensor_colors[sensor], linewidth=lw)

        # 3) korrigált hiba
        ax3.plot(ref_temps, error_corrected,
                 color=sensor_colors[sensor], linewidth=lw)

    ax1.legend()
    plt.tight_layout()
    plt.show()


# ============================================================
# 4) KALIBRÁCIÓS EGYÜTTHATÓK KIÍRÁSA (C FORMÁTUM)
# ============================================================
def print_c_calibration(fit_params, ref_sensor):
    print("\n--- KALIBRÁCIÓS EGYÜTTHATÓK (REFERENCIÁHOZ FITTELVE) ---\n")

    for sensor in fit_params:
        A, B, C = fit_params[sensor]

        print(
            f"float\t{sensor}_0 = {A:.6f};\t"
            f"float\t{sensor}_1 = {B:.6f};\t"
            f"float\t{sensor}_2 = {C:.6f};\t"
            f"// A {sensor} szenzor kalibracios parameterei ({ref_sensor} referencia)"
        )


# ============================================================
# 5) MAIN
# ============================================================
def main():
    # filename = "data\szobahofok_20C_120C.txt"
    filename = "data\meres_1.txt"

    ref_temps, sensors, measurements, ref_sensor = load_measurements(filename)
    fit_params = fit_sensors(ref_temps, sensors, measurements)
    plot_results(ref_temps, sensors, measurements, fit_params, ref_sensor)
    print_c_calibration(fit_params, ref_sensor)


if __name__ == "__main__":
    main()
