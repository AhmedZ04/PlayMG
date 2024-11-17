import serial
import time
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import butter, lfilter, find_peaks, filtfilt

# Configure serial port
SERIAL_PORT = 'COM3'  # Replace with your Arduino's port
BAUD_RATE = 9600      # Match the Arduino's serial rate

# Band-pass filter parameters
LOW_CUTOFF = 74.5     # Low cutoff frequency in Hz
HIGH_CUTOFF = 149.5   # High cutoff frequency in Hz
SAMPLING_RATE = 500   # Sampling rate in Hz (update to your actual rate)

# Envelope filter parameters
ENVELOPE_CUTOFF = 3  # Low-pass filter cutoff for envelope extraction (in Hz)

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

# Function to calculate the envelope of the EMG signal
def calculate_envelope(emg_signal, sampling_rate, cutoff_freq=5.0):
    # Step 1: Rectify the signal (take the absolute value)
    rectified_signal = np.abs(emg_signal)

    # Step 2: Apply a low-pass filter to get the envelope
    nyquist_freq = sampling_rate / 2.0
    normalized_cutoff = cutoff_freq / nyquist_freq
    b, a = butter(4, normalized_cutoff, btype='low')

    # Apply the filter
    envelope = filtfilt(b, a, rectified_signal)

    return envelope

# Function to detect muscle contraction based on filtered signal
def detect_contraction(filtered_data, threshold=0.5):
    # Find peaks in the filtered signal
    peaks, _ = find_peaks(filtered_data, height=threshold, distance=SAMPLING_RATE // 2)
    
    # If more than a certain number of peaks are detected in a reasonable timeframe, muscle contraction is likely
    contraction_detected = len(peaks) > 5  # Adjust the threshold based on your data
    return contraction_detected, peaks

# Main program
sampling_time = 20  # seconds
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

processingTimeStart = time.time()

if not data:
    print("No valid data received. Exiting.")
    exit()

# Convert data to NumPy array
data = np.array(data)

# Apply band-pass filter
filtered_data = apply_bandpass_filter(data, LOW_CUTOFF, HIGH_CUTOFF, SAMPLING_RATE)

# Ignore values greater than ±5 in the filtered data
filtered_data = np.clip(filtered_data, -20, 20)

# Calculate the envelope of the EMG signal
envelope = calculate_envelope(filtered_data, SAMPLING_RATE, ENVELOPE_CUTOFF)

# Detect muscle contraction
contraction_detected, peaks = detect_contraction(filtered_data)

# Detect local maxima (peaks) in the envelope
envelope_peaks, _ = find_peaks(envelope)

# Print the time and amplitude values of the detected peaks
for i in envelope_peaks:
    print(f"Peak at time {time_points[i]:.3f} s with amplitude {envelope[i]:.3f}")

print(f"Time to process data: {time.time() - processingTimeStart}")

# Plot the original, filtered data, and envelope with peaks
plt.figure(figsize=(10, 8))

plt.subplot(3, 1, 1)
plt.plot(time_points, data, label="Original Data", color="blue")
plt.xlabel("Time (s)")
plt.ylabel("Value")
plt.title("Original Data")
plt.grid(True)
plt.legend()

plt.subplot(3, 1, 2)
plt.plot(time_points, filtered_data, label="Filtered Data", color="green")
plt.xlabel("Time (s)")
plt.ylabel("Value (Filtered)")
plt.title("Data After Band-Pass Filter")
plt.grid(True)
plt.legend()

plt.subplot(3, 1, 3)
plt.plot(time_points, envelope, label="Envelope", color="purple", linewidth=2)
plt.plot(np.array(time_points)[envelope_peaks], envelope[envelope_peaks], "x", color="red", label="Local Maxima")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.title("Envelope of the Filtered Data with Local Maxima")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()

# Print contraction detection result
if contraction_detected:
    print("Muscle contraction detected!")
else:
    print("No muscle contraction detected.")
