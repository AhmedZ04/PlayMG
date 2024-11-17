# HawkDuam

## Overview
**HawkDuam** is an Electromyography (EMG)-based project that uses the Bioamp EXG Pill to map forearm muscle gestures to computer keyboard inputs. By detecting muscle contractions through EMG signals, gestures can trigger actions, such as pressing specific keys on a computer.

## Features
- Processes EMG signals from forearm muscle gestures.
- Maps gestures to keyboard inputs (e.g., clenching a fist to press Spacebar).
- Real-time signal processing using band-pass filtering, envelope detection, and peak analysis.
- Customizable gesture-to-key mapping.

---

## Setup

### Hardware Requirements
- **Bioamp EXG Pill** (or compatible EMG sensor).
- **Arduino board** (e.g., Uno, Mega).
- Wires and a breadboard for connections.
- Computer with USB connectivity.

### Software Requirements
- **Python** (version 3.6 or later).
- **Arduino IDE** for uploading the script to the Arduino.
- Python libraries: `serial`, `time`, `matplotlib`, `numpy`, `asyncio`, `scipy`.

---

## Procedure

### 1. Data Collection
1. Connect the Bioamp EXG Pill to the Arduino to capture analog signals for muscle gestures.
2. Upload the provided Arduino sketch to the Arduino board to transmit EMG data to the computer.

### 2. Signal Processing
1. EMG signals are filtered using a band-pass filter to remove noise.
2. The filtered signal is rectified and smoothed to detect muscle contractions.

### 3. Key Mapping
1. Processed signals are analyzed for distinct patterns (e.g., envelope peaks).
2. Map these patterns to keyboard inputs for real-time actions.

---

## Gesture Mapping

| **Gesture**           | **Keyboard Key** |
|------------------------|------------------|
| Fist Clenching        | Spacebar         |
| Wrist Flexion         | Enter            |
| [Insert Gesture Here] | [Insert Key Here]|
| [Insert Gesture Here] | [Insert Key Here]|

*Edit this table to customize gestures and their mapped keys.*

---

## Challenges Faced
- Detecting peaks accurately in noisy EMG data.
- Reducing processing delays for real-time interaction.
- Initial signal spikes causing false positives.
- Synchronizing multiple channels effectively.
- Debugging hardware misconfigurations (e.g., wrong Arduino pin connections).

---

## Libraries Used

### Python Libraries
- `serial`: For reading data from the Arduino.
- `time`: For timing and sampling.
- `matplotlib`: For data visualization and plotting.
- `numpy`: For numerical computations and array handling.
- `asyncio`: For handling asynchronous tasks.
- `scipy`: For signal processing (e.g., filtering, peak detection).

### Arduino Libraries
- Standard C++ libraries for serial communication.

---

## License
This project is open-source and available for customization. Feel free to modify it for your use case.

---
