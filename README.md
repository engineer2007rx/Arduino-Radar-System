# Arduino  Radar System

This is a beginner-friendly Arduino project that I built using an ultrasonic sensor and a servo motor. It scans the surroundings, detects nearby objects, and displays their positions on a radar-style interface using Python.

## Features
- Scans from 0° to 180° using a servo motor.
- Measures object distance using an HC-SR04 sensor.
- Uses two LEDs to indicate object detection.
- Displays sensor readings through a Python radar interface.

## Components
- Arduino Uno
- HC-SR04 Ultrasonic Sensor
- SG90 Servo Motor
- 2 LEDs and 220Ω resistors
- Jumper wires

## Technologies Used
- Arduino IDE (C++)
- Python
- Pygame
- PySerial

## How to Run
1. Upload the Arduino sketch from the `Arduino` folder.
2. Install dependencies:
   ```bash
   python -m pip install -r requirement.txt
   ```
3. Set the correct COM port in `radar.py`.
4. Close Arduino Serial Monitor.
5. Run:
   ```bash
   python radar.py
   ```

## What I Learned

This project helped me understand basic electronics, sensor interfacing, servo control, serial communication, and Python-based visualization.

*This is an ultrasonic radar demonstration, not an actual electromagnetic radar.*
