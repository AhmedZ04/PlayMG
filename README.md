# PlayMG

## Overview

PlayMG is an Electromyography (EMG)-based project leveraging the Bioamp EXG Pill to map forearm muscle activity to computer keyboard inputs. By detecting muscle contractions and finger movements through EMG signals, specific gestures can trigger keyboard actions, such as pressing the Spacebar.

## Features

- Real-time processing of EMG signals to detect forearm muscle activity and finger movements.
- Gesture-to-key mapping for seamless interaction (e.g., clenching a fist to press Spacebar).
- Advanced signal processing techniques, including band-pass filtering, envelope detection, and peak analysis.
- Easily customizable gesture-to-key mappings.

## Procedure

### Data Collection
- Connect the Bioamp EXG Pill to the Arduino to capture analog signals corresponding to different muscle movements and finger gestures.
- Upload the provided Arduino sketch to enable communication between the Arduino and the computer.

### Signal Processing
- EMG signals are filtered using a band-pass filter to remove noise.
- Filtered signals are then enveloped to further reduce noise.
- Envelopes are parameterized and muscle contractions are detected with high certainty.

### Gesture Mapping
- Processed EMG signals are analyzed to recognize specific gestures, which are then mapped to keyboard inputs.

## Gesture Keybinds

| **Gesture**           | **Keyboard Key**   |
|-----------------------|--------------------|
| Left Fist Clenching   | Left Input         |
| Right Fist Clenching  | Right Input        |

## Challenges Faced and Solutions

1. **Detecting Highs and Lows in Envelope Peaks**
   - Fine-tuned filter parameters and adjusted peak detection thresholds.

2. **Hardware Misconfigurations**
   - Corrected Arduino pin connections and verified channel assignments (e.g., wrong channel initially used).

3. **Asynchronous Channel Processing**
   - Optimized the script to handle all five EMG channels efficiently.

4. **Processing Delays**
   - Reduced signal processing runtime for near-instantaneous feedback.

5. **Initial Signal Spikes**
   - Ignored early noise to avoid false positives during system initialization.

6. **Muscle Contraction Detection**
   - Achieved real-time responsiveness by improving the detection algorithm.

## Libraries Used

### Python Libraries
- `serial`: Communicates with the Arduino for real-time data acquisition.
- `time`: Handles time-based sampling and delays.
- `matplotlib`: Visualizes raw, filtered, and processed EMG data.
- `numpy`: Performs numerical computations and array manipulations.
- `asyncio`: Supports asynchronous signal processing tasks.
- `scipy`: Provides filtering and peak detection tools.

### Arduino Libraries
- Standard C libraries for serial communication.
