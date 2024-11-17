import serial
import time
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import butter, filtfilt, find_peaks
import pyfirmata

import keyboard

# Configure serial port
SERIAL_PORT = 'COM4'  # Replace with your Arduino's port
BAUD_RATE = 9600      # Match the Arduino's serial rate

# Band-pass filter parameters
LOW_CUTOFF = 74.5     # Low cutoff frequency in Hz
HIGH_CUTOFF = 149.5   # High cutoff frequency in Hz
SAMPLING_RATE = 500   # Sampling rate in Hz (update to your actual rate)

# Envelope filter parameters
ENVELOPE_CUTOFF = 7  # Low-pass filter cutoff for envelope extraction (in Hz)
ENVELOPE_PROMINENCE = 0.005 # Promonience for the envelope peak detection
ENVELOPE_HEIGHT = 5 # Height is the thing to adjust in order to get the right peaks Misbah 0.5
ENVELOPE_WIDTH = 0.0025 # Misbah: 1

# Initialize serial connection
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Connected to {SERIAL_PORT}")
except Exception as e:
    print(f"Error: {e}")
    exit()



def read_serial_data():
    try:
        beg = time.time()
        line = int(ser.readline().decode('utf-8').strip())
        #print(f"Time to process data: {time.time() - beg}")
        return line
    except Exception:
        return None  # Ignore invalid lines

# Band-pass filter design and application
def butter_bandpass(lowcut, highcut, fs, order=4):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return b, a

def apply_bandpass_filter(data, lowcut, highcut, fs, order=4):
    b, a = butter_bandpass(lowcut, highcut, fs, order)
    return filtfilt(b, a, data)

# Function to calculate the envelope of the EMG signal
def calculate_envelope(emg_signal, sampling_rate, cutoff_freq=5.0):
    rectified_signal = np.abs(emg_signal)
    nyquist_freq = sampling_rate / 2.0
    normalized_cutoff = cutoff_freq / nyquist_freq
    b, a = butter(4, normalized_cutoff, btype='low')
    envelope = filtfilt(b, a, rectified_signal)
    return envelope

# Main program
data = []
buffer = []
buffer_size = int(SAMPLING_RATE * 0.2)  # 0.2 seconds buffer
time_points = []
start_time = time.time()

i = 0
j = 0
try:

    while True:
        value = read_serial_data()  

        if value is not None:
            value = int(value*1000)
            
            data.append(value)
            time_points.append(time.time() - start_time)
            buffer.append(value)
            #print(f"Time to process: {time.time() - beg}")
    
        if time.time() - start_time >= 12:
            if j == 0:
                print("Initilization Finished")
                j += 1
            if len(buffer) >= buffer_size:
                buffer_array = np.array(buffer)

                # Apply filters and detect peaks
                filtered = apply_bandpass_filter(buffer_array, LOW_CUTOFF, HIGH_CUTOFF, SAMPLING_RATE)
                envelope = calculate_envelope(filtered, SAMPLING_RATE, ENVELOPE_CUTOFF)
                envelope_peaks, properties = find_peaks(
                    envelope, 
                    prominence=ENVELOPE_PROMINENCE,  # Adjust for your signal strength
                    width=ENVELOPE_WIDTH, 
                    height= ENVELOPE_HEIGHT 
                )
                
                # Check and print detected peaks
                if envelope_peaks.size > 0 and i >= 0:
                    keyboard.PressW()
                    print(f"Detected peaks at: {np.array(time_points)[-len(buffer) + envelope_peaks]}")
                        
                i += 1
                buffer = []
                

                

except KeyboardInterrupt:
    print("Stopping data collection and plotting results.")
    

# Convert collected data for plotting
data = np.array(data)

time_points = np.array(time_points)

# Final Processing
filtered_data = apply_bandpass_filter(data, LOW_CUTOFF, HIGH_CUTOFF, SAMPLING_RATE)
envelope = calculate_envelope(filtered_data, SAMPLING_RATE, ENVELOPE_CUTOFF)
envelope_peaks, _ = find_peaks(envelope, prominence=ENVELOPE_PROMINENCE, height=ENVELOPE_HEIGHT, width=ENVELOPE_WIDTH)

# Plot data
plt.figure(figsize=(10, 8))
plt.subplot(3, 1, 1)
plt.plot(time_points, data, label="Raw Data", color="blue")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.title("Raw EMG Signal")
plt.legend()

plt.subplot(3, 1, 2)
plt.plot(time_points, filtered_data, label="Filtered Data", color="green")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.title("Band-Pass Filtered Signal")
plt.legend()

plt.subplot(3, 1, 3)
plt.plot(time_points, envelope, label="Envelope", color="purple")
plt.plot(time_points[envelope_peaks], envelope[envelope_peaks], "x", color="red", label="Peaks")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.title("Envelope with Detected Peaks")
plt.legend()

plt.tight_layout()
plt.show()
