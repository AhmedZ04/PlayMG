import serial
import time
import numpy as np
from scipy.signal import butter, lfilter

# Serial configuration
PORT = 'COM3'  # Replace with your Arduino's port
BAUD_RATE = 9600  # Match the Arduino baud rate
THRESHOLD = 200  # Threshold for muscle contraction detection (after filtering)
SAMPLING_RATE = 500  # Adjust to match Arduino's data sampling rate (in Hz)

# Bandpass filter parameters
LOW_CUTOFF = 49.5  # Lower cutoff frequency in Hz
HIGH_CUTOFF = 149.5  # Upper cutoff frequency in Hz

def butter_bandpass(lowcut, highcut, fs, order=4):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return b, a

def bandpass_filter(data, lowcut, highcut, fs, order=4):
    b, a = butter_bandpass(lowcut, highcut, fs, order)
    return lfilter(b, a, data)

def main():
    try:
        # Initialize serial connection
        with serial.Serial(PORT, BAUD_RATE, timeout=1) as arduino:
            print(f"Connected to Arduino on {PORT} at {BAUD_RATE} baud.")
            time.sleep(2)  # Wait for the connection to stabilize
            
            # Prepare data buffer for filtering
            buffer_size = SAMPLING_RATE  # Buffer to hold one second of data
            data_buffer = np.zeros(buffer_size)
            buffer_index = 0

            # Continuously read data
            while True:
                if arduino.in_waiting > 0:
                    try:
                        # Read and decode data from Arduino
                        raw_data = arduino.readline().decode('utf-8').strip()
                        emg_value = int(raw_data)
                        
                        # Update buffer
                        data_buffer[buffer_index] = emg_value
                        buffer_index = (buffer_index + 1) % buffer_size

                        # Apply bandpass filter
                        if buffer_index == 0:  # Process buffer once it's full
                            filtered_data = bandpass_filter(
                                data_buffer, LOW_CUTOFF, HIGH_CUTOFF, SAMPLING_RATE
                            )

                            # Detect muscle contraction in filtered data
                            max_filtered_value = np.max(np.abs(filtered_data))
                            if max_filtered_value > THRESHOLD:
                                print("Muscle contraction detected!")
                            else:
                                print(f"Filtered Max Value: {max_filtered_value:.2f}")
                    except ValueError:
                        print("Invalid data received.")
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
    except KeyboardInterrupt:
        print("Program interrupted. Exiting.")

if __name__ == "__main__":
    main()
