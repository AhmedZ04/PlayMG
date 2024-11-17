import serial
import time
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import butter, filtfilt, find_peaks

import keyboard

# Configure serial port
SERIAL_PORT = 'COM4'  # Replace with your Arduino's port
BAUD_RATE = 9600 

# Initialize serial connection
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Connected to {SERIAL_PORT}")
except Exception as e:
    print(f"Error: {e}")
    exit()

data = []


for i in range(0, 200):
    beg = time.time()
    line = ser.readline().decode()
    
    data.append(float(time.time() - beg))

    '''A0 = line // 10**12
    A1 = (line % 10**12) // 10**9
    A2 = (line % 10**9) // 10**6
    A3 = (line % 10**6) // 10**3
    A4 = line % 10**3'''

print(np.mean(np.array(data)))

    