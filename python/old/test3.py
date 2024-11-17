import serial
import time
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import butter, lfilter, find_peaks

# Configure serial port
SERIAL_PORT = 'COM3'  # Replace with your Arduino's port
BAUD_RATE = 9600      # Match the Arduino's serial rate

# Band-pass filter parameters
LOW_CUTOFF = 74.5     # Low cutoff frequency in Hz
HIGH_CUTOFF = 149.5   # High cutoff frequency in Hz
SAMPLING_RATE = 500   # Sampling rate in Hz (update to your actual rate)

# Rolling buffer size (enough to cover a short window for analysis)
BUFFER_SIZE = SAMPLING_RATE * 2  # 2 seconds of data

# Initialize serial connection
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Connected to {SERIAL_PORT}")
except Exception as e:
    print(f"Error: {e}")
    exit()

# Band-pass filter design
def butter_bandpass(lowcut, highcut, fs, order=4):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return b, a

def apply_bandpass_filter(data, lowcut, highcut, fs, order=4):
    b, a = butter_bandpass(lowcut, highcut, fs, order)
    y = lfilter(b, a, data)
    return y

# Function to detect muscle contraction
def detect_contraction(filtered_data, threshold=None):
    if threshold is None:
        # Dynamically set the threshold as a fraction of the signal's max amplitude
        threshold = 0.2 * np.max(np.abs(filtered_data))  # Lower threshold for more sensitivity
    
    # Detect peaks
    peaks, _ = find_peaks(filtered_data, height=threshold, distance=SAMPLING_RATE // 2)
    return len(peaks) > 0, peaks

# Update y-axis range dynamically based on signal
def update_y_axis(ax, data):
    signal_min = np.min(data)
    signal_max = np.max(data)
    margin = 0.1 * (signal_max - signal_min)  # Add a 10% margin
    ax.set_ylim(signal_min - margin, signal_max + margin)

# Initialize data buffer
data_buffer = np.zeros(BUFFER_SIZE)
time_buffer = np.linspace(-BUFFER_SIZE / SAMPLING_RATE, 0, BUFFER_SIZE)

# Real-time processing
print("Reading data in real-time...")
muscle_contractions = []  # Store time points when contractions are detected
time_points = []  # Store the time of each reading
filtered_data_history = []  # Store filtered data for later plotting

try:
    while True:
        try:
            # Read data from the serial port
            line = ser.readline().decode('utf-8').strip()
            value = float(line)

            # Shift buffer and append the new value
            data_buffer = np.roll(data_buffer, -1)
            data_buffer[-1] = value
            time_points.append(time.time())

            # Apply band-pass filter
            filtered_data = apply_bandpass_filter(data_buffer, LOW_CUTOFF, HIGH_CUTOFF, SAMPLING_RATE)

            # Debugging: Print filtered data to check if peaks are present
            print(f"Filtered data (last few values): {filtered_data[-10:]}")

            # Detect contraction
            contraction_detected, peaks = detect_contraction(filtered_data)

            # If a contraction is detected, store the time and print a message
            if contraction_detected:
                contraction_time = time.time()
                muscle_contractions.append(contraction_time)
                print(f"Muscle contraction detected at time(s): {contraction_time}")

            # Store filtered data for later plotting
            filtered_data_history.append(filtered_data)

        except ValueError:
            continue  # Skip invalid lines
except KeyboardInterrupt:
    print("Exiting and plotting data...")

# Close the serial connection
ser.close()

# Plot the data after exiting the loop
plt.figure(figsize=(10, 6))

# Plot the filtered data over time
plt.subplot(2, 1, 1)
for i, filtered_data in enumerate(filtered_data_history):
    plt.plot(time_points[i:i+len(filtered_data)], filtered_data, label="Filtered Data", color="green")
plt.xlabel("Time (s)")
plt.ylabel("Filtered Signal")
plt.title("Filtered EMG Data")
plt.grid(True)

# Plot the detected muscle contractions
plt.subplot(2, 1, 2)
plt.plot(time_points, np.concatenate(filtered_data_history), label="Filtered Data", color="green")
for contraction_time in muscle_contractions:
    plt.axvline(contraction_time, color="red", linestyle="--", label="Contraction Detected")
plt.xlabel("Time (s)")
plt.ylabel("Filtered Signal")
plt.title("Filtered EMG Data with Muscle Contractions")
plt.grid(True)

plt.tight_layout()
plt.legend(loc="upper right")
plt.show()
