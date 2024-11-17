import numpy as np
from scipy.signal import butter, filtfilt, find_peaks
import time
import matplotlib as plt
import pyfirmata
import threading


class Filter:
    def __init__(self):

        # Band-pass filter parameters
        self.LOW_CUTOFF = 74.5     # Low cutoff frequency in Hz
        self.HIGH_CUTOFF = 149.5   # High cutoff frequency in Hz
        self.SAMPLING_RATE = 500   # Sampling rate in Hz (update to your actual rate)
        self.BUFFER_TIME = 0.2     # Buffer time for the live sampling

        # Envelope filter parameters
        self.ENVELOPE_CUTOFF = 7  # Low-pass filter cutoff for envelope extraction (in Hz)
        self.ENVELOPE_PROMINENCE = 0.005 # Promonience for the envelope peak detection
        self.ENVELOPE_HEIGHT = 2.5 # Height is the thing to adjust in order to get the right peaks Misbah 0.5
        self.ENVELOPE_WIDTH = 0.0025 # Misbah: 1

        self.time_points = []
        #self.data = {"0": [], "1": [], "2": [], "3": [], "4": []}
        
        


    # Band-pass filter design and application
    def butter_bandpass(self, lowcut, highcut, fs, order=4):
        nyquist = 0.5 * fs
        low = lowcut / nyquist
        high = highcut / nyquist
        b, a = butter(order, [low, high], btype='band')
        return b, a

    def apply_bandpass_filter(self, data, lowcut, highcut, fs, order=4):
        b, a = self.butter_bandpass(lowcut, highcut, fs, order)
        return filtfilt(b, a, data)

    # Function to calculate the envelope of the EMG signal  
    def calculate_envelope(self, emg_signal, sampling_rate, cutoff_freq=5.0):
        rectified_signal = np.abs(emg_signal)
        nyquist_freq = sampling_rate / 2.0
        normalized_cutoff = cutoff_freq / nyquist_freq
        b, a = butter(4, normalized_cutoff, btype='low')
        envelope = filtfilt(b, a, rectified_signal)
        return envelope

    def plot(self):
            
        # Convert collected data for plotting
        data = np.array(self.data)
        time_points = np.array(self.time_points)

        # Final Processing
        filtered_data = self.apply_bandpass_filter(data, self.LOW_CUTOFF, self.HIGH_CUTOFF, self.SAMPLING_RATE)
        envelope = self.calculate_envelope(filtered_data, self.SAMPLING_RATE, self.ENVELOPE_CUTOFF)
        envelope_peaks, _ = find_peaks(envelope, prominence=self.ENVELOPE_PROMINENCE, height=self.ENVELOPE_HEIGHT, width=self.ENVELOPE_WIDTH)

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


    def filter(self, value, start_time):
        
        buffer = []
        buffer_size = int(self.SAMPLING_RATE * self.BUFFER_TIME)  # 0.2 seconds buffer
        if value is not None:
            value = int(value)
            self.time_points.append(time.time() - start_time)
            buffer.append(value)
        if time.time() - start_time >= 12:
            
            if len(buffer) >= buffer_size:
                buffer_array = np.array(buffer)

                # Apply filters and detect peaks
                filtered = self.apply_bandpass_filter(buffer_array, self.LOW_CUTOFF, self.HIGH_CUTOFF, self.SAMPLING_RATE)
                envelope = self.calculate_envelope(filtered, self.SAMPLING_RATE, self.ENVELOPE_CUTOFF)
                envelope_peaks, properties = find_peaks(
                    envelope, 
                    prominence=self.ENVELOPE_PROMINENCE,  # Adjust for your signal strength
                    width=self.ENVELOPE_WIDTH, 
                    height= self.ENVELOPE_HEIGHT 
                )
                
                # Check and print detected peaks
                if envelope_peaks.size > 0 and i >= 0:
                    print(f"Detected peaks at: {np.array(self.time_points)[-len(buffer) + envelope_peaks]}")
                    #keyboard.HawkTuah()
                i += 1

                # Clear the buffer
                buffer = []