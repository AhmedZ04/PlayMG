import time
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import butter, filtfilt, find_peaks
import pyfirmata
import threading
from queue import Queue

# Serial Port Configuration
SERIAL_PORT = 'COM4'  # Replace with your Arduino's port
BAUD_RATE = 9600      # Match the Arduino's serial rate

# Filter Parameters
LOW_CUTOFF = 74.5     # Low cutoff frequency in Hz
HIGH_CUTOFF = 149.5   # High cutoff frequency in Hz
SAMPLING_RATE = 500   # Sampling rate in Hz
ENVELOPE_CUTOFF = 7   # Low-pass filter cutoff for envelope extraction (in Hz)
ENVELOPE_PROMINENCE = 0.005  # Prominence for peak detection
ENVELOPE_HEIGHT = 3          # Minimum height for peak detection
ENVELOPE_WIDTH = 0.0025      # Minimum width for peak detection

PORT_TOTAL = 8

# Initialize queue for processed data
data_queue = Queue()

# Band-pass filter design
def butter_bandpass(lowcut, highcut, fs, order=4):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return b, a

# Apply band-pass filter
def apply_bandpass_filter(data, lowcut, highcut, fs, order=4):
    b, a = butter_bandpass(lowcut, highcut, fs, order)
    return filtfilt(b, a, data)

# Envelope calculation
def calculate_envelope(emg_signal, sampling_rate, cutoff_freq=5.0):
    rectified_signal = np.abs(emg_signal)
    nyquist_freq = sampling_rate / 2.0
    normalized_cutoff = cutoff_freq / nyquist_freq
    b, a = butter(4, normalized_cutoff, btype='low')
    envelope = filtfilt(b, a, rectified_signal)
    return envelope

# Worker thread to process EMG data from a port
def process_emg_data(port, board, start_time):
    buffer = []
    buffer_size = int(SAMPLING_RATE * 0.5)  # 0.5 seconds buffer
    time_points = []

    while True:
        value = board.analog[port].read()
        if value is not None:
            new_value = int(value * 1000)
            buffer.append(new_value)
            time_points.append(time.time() - start_time)

            if len(buffer) >= buffer_size:
                buffer_array = np.array(buffer)

                # Apply filters and detect peaks
                filtered = apply_bandpass_filter(buffer_array, LOW_CUTOFF, HIGH_CUTOFF, SAMPLING_RATE)
                envelope = calculate_envelope(filtered, SAMPLING_RATE, ENVELOPE_CUTOFF)
                envelope_peaks, _ = find_peaks(
                    envelope, 
                    prominence=ENVELOPE_PROMINENCE, 
                    width=ENVELOPE_WIDTH, 
                    height=ENVELOPE_HEIGHT
                )

                # Send filtered data to the queue
                data_queue.put((port, time_points[-len(buffer):], filtered, envelope, envelope_peaks))

                # Save plot for this port
                save_plot(port, time_points[-len(buffer):], filtered, envelope)

                buffer = []  # Clear buffer after processing
        time.sleep(0.001)

# Save plots for each port
def save_plot(port, time_points, filtered, envelope):
    plt.figure(figsize=(10, 6))
    plt.subplot(2, 1, 1)
    plt.plot(time_points, filtered, label="Filtered Data", color="green")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.title(f"Port {port}: Band-Pass Filtered Signal")
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(time_points, envelope, label="Envelope", color="purple")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.title(f"Port {port}: Envelope Signal")
    plt.legend()

    plt.tight_layout()
    filename = f"port_{port}_signal_plot.png"
    plt.savefig(filename)
    plt.close()
    print(f"Saved plot for port {port} as {filename}")

# Main function
def main():
    # Initialize the Arduino board
    try:
        board = pyfirmata.ArduinoMega(SERIAL_PORT, baudrate=BAUD_RATE)
        it = pyfirmata.util.Iterator(board)
        it.start()
        for i in range(PORT_TOTAL + 1):
            board.get_pin(f'a:{i}:i')
    except Exception as e:
        print(f"Error: {e}")
        exit()

    start_time = time.time()

    # Launch threads for each port
    threads = []
    for port in range(PORT_TOTAL + 1):  # Ports A0 to A8
        thread = threading.Thread(target=process_emg_data, args=(port, board, start_time))
        thread.daemon = True
        threads.append(thread)
        thread.start()

    # Run until interrupted
    try:
        while True:
            time.sleep(0.1)  # Main thread sleeps to let worker threads run
    except KeyboardInterrupt:
        print("Stopping data collection...")

if __name__ == "__main__":
    main()
