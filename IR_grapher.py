""" Read 2.5D IR scanner data (yaw, pitch, distance) from an Arduino and
    plot it as a 2D image where color = distance. """

import csv
import time

import numpy as np
import serial
import matplotlib.pyplot as plt

ARDUINO_PORT = 'COM5'   # Replace with your Arduino's port
BAUD_RATE = 9600        # Must match Serial.begin() in the Arduino sketch
IDLE_TIMEOUT_S = 10     # Stop if no valid data arrives for this long
SAVE_CSV = 'scan_data.csv'

# Expected line format from the Arduino:  yaw,pitch,distance
# e.g. "90,45,0.63"  (Serial.print(yaw); Serial.print(","); ... Serial.println(dist);)
# Optionally, have the Arduino send the line "DONE" when the scan finishes.


def read_scan():
    """Collect (yaw, pitch, distance) rows until DONE, Ctrl+C, or idle timeout."""
    rows = []
    ser = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)            # Arduino resets when the port opens; give it a moment
    ser.reset_input_buffer()

    last_data = time.time()
    print("Listening... (Ctrl+C to stop early)")
    try:
        while time.time() - last_data < IDLE_TIMEOUT_S:
            line = ser.readline().decode(errors='ignore').strip()
            if not line:
                continue
            if line.upper() == 'DONE':
                break
            try:
                yaw, pitch, dist = (float(x) for x in line.split(','))
            except ValueError:
                print("Skipping bad line:", repr(line))
                continue
            rows.append((yaw, pitch, dist))
            last_data = time.time()
            print(f"yaw = {yaw}, pitch = {pitch}, distance = {dist}")
    except KeyboardInterrupt:
        print("\nStopped by user.")
    finally:
        ser.close()
    return rows


def make_grid(rows):
    """Turn (yaw, pitch, dist) rows into a 2D array indexed [pitch, yaw]."""
    data = np.array(rows)
    yaws = np.unique(data[:, 0])
    pitches = np.unique(data[:, 1])
    total = np.zeros((len(pitches), len(yaws)))
    count = np.zeros_like(total)

    y_idx = np.searchsorted(yaws, data[:, 0])
    p_idx = np.searchsorted(pitches, data[:, 1])
    np.add.at(total, (p_idx, y_idx), data[:, 2])
    np.add.at(count, (p_idx, y_idx), 1)

    # Average repeat visits to the same angle; untouched cells become NaN (blank)
    grid = np.where(count > 0, total / np.maximum(count, 1), np.nan)
    return pitches, yaws, grid


def plot_scan(pitches, yaws, grid):
    fig, ax = plt.subplots()
    mesh = ax.pcolormesh(yaws, pitches, grid, shading='nearest', cmap='viridis')
    fig.colorbar(mesh, ax=ax, label='distance (m)')
    ax.set_xlabel('yaw (degrees)')
    ax.set_ylabel('pitch (degrees)')
    ax.set_title('2.5D IR Scanner Data')
    plt.show()


def main():
    rows = read_scan()
    if not rows:
        print("No data received. Check the port name, baud rate, and data format.")
        return

    with open(SAVE_CSV, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['yaw', 'pitch', 'distance'])
        writer.writerows(rows)
    print(f"Saved {len(rows)} readings to {SAVE_CSV}")

    pitches, yaws, grid = make_grid(rows)
    plot_scan(pitches, yaws, grid)


if __name__ == '__main__':
    main()