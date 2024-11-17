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

# Initialize serial connection
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Connected to {SERIAL_PORT}")
except Exception as e:
    print(f"Error: {e}")
    exit()

# Function to read data from the serial port
def read_serial_data():
    try:
        line = ser.readline().decode('utf-8').strip()
        return float(line)  # Convert the string to a float
    except Exception:
        return None  # Ignore invalid lines

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

# Function to detect muscle contraction based on filtered signal
def detect_contraction(filtered_data, threshold=0.5):
    # Find peaks in the filtered signal
    peaks, _ = find_peaks(filtered_data, height=threshold, distance=SAMPLING_RATE // 2)
    
    # If more than a certain number of peaks are detected in a reasonable timeframe, muscle contraction is likely
    contraction_detected = len(peaks) > 5  # Adjust the threshold based on your data
    return contraction_detected, peaks

# Main program
sampling_time = 5  # seconds
start_time = time.time()
data = []

time_points = []

print("Reading data...")
while time.time() - start_time < sampling_time:
    value = read_serial_data()
    if value is not None:
        data.append(value)
        time_points.append(time.time() - start_time)  # Record the timestamp

# Close the serial connection
ser.close()
print("Sampling complete.")

if not data:
    print("No valid data received. Exiting.")
    exit()

# Convert data to NumPy array
data = np.array(data)

# Apply band-pass filter
filtered_data = apply_bandpass_filter(data, LOW_CUTOFF, HIGH_CUTOFF, SAMPLING_RATE)

# Detect muscle contraction
contraction_detected, peaks = detect_contraction(filtered_data)
print(len(peaks))
# Plot the original and filtered data
plt.figure(figsize=(10, 6))

plt.subplot(2, 1, 1)
plt.plot(time_points, data, label="Original Data", color="blue")
plt.xlabel("Time (s)")
plt.ylabel("Value")
plt.title("Original Data")
plt.grid(True)
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(time_points, filtered_data, label="Filtered Data", color="green")
plt.plot(np.array(time_points)[peaks], filtered_data[peaks], "x", color="red", label="Detected Peaks")
plt.xlabel("Time (s)")
plt.ylabel("Value (Filtered)")
plt.title("Data After Band-Pass Filter")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()

print(len(peaks))

# Print contraction detection result
if contraction_detected:
    print("Muscle contraction detected!")
else:
    print("No muscle contraction detected.")
