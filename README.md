<img width="1024" height="733" alt="Screenshot 2025-07-27 at 6 05 34 PM" src="https://github.com/user-attachments/assets/885c551f-2745-4c56-a243-ccc1345522f1" />
# Sound-Controlled Nerf Turret | EE14N Final Project — Kuzey Kantarcıoğlu and Chisa Ogaki

## Overview

This project explores how sound input from a live trumpet can directly control physical hardware in real time. The final system is a rotating turret that detects musical notes, rotates accordingly, and fires a Nerf gun all controlled purely by pitch detection.

## System Breakdown

### 1. Rotating Platform

- **Function**: Allows the turret to pan left or right.
- **Mechanism**: A Lazy Susan bearing mounted to a wood base.
- **Actuation**: Controlled via a stepper motor connected to a DRV8825 motor driver.
- **Logic**: 
  - Trumpet note **G (700 Hz)** → rotate clockwise  
  - Trumpet note **B (830 Hz)** → rotate counterclockwise
- **Precision**: Steps controlled via pulse width modulation using the Raspberry Pi’s GPIO.

### 2. Shooting Mechanism

- **Weapon**: Modified Nerf Elite blaster.
- **Trigger**: Pulled by a metal wire connected to a solenoid actuator.
- **Firing Logic**: 
  - Trumpet note **D (525 Hz)** → activate solenoid to fire.
- **Control**: Raspberry Pi sends voltage to the solenoid using a transistor or relay circuit.

### 3. Sound Recognition and Control

- **Input**: USB microphone connected to Raspberry Pi 5.
- **Signal Processing**:
  - 2048-sample FFT with Hamming window
  - Bandpass filtered to 60–1000 Hz
  - Peak frequency matched to note ranges
- **Software Stack**:
  - Python with `PyAudio`, `NumPy`, `SciPy`, and `lgpio`
- **Performance**: Real-time detection with under 100ms latency.

## Components & Tools

| Component                  | Role                                 |
|---------------------------|--------------------------------------|
| Raspberry Pi 5            | Central controller                   |
| USB Microphone            | Audio input                          |
| DRV8825 Driver            | Stepper motor driver                 |
| NEMA 17 Stepper Motor     | Platform rotation                    |
| Solenoid Actuator         | Firing mechanism                     |
| Nerf Blaster              | Projectile system                    |
| Relay/Transistor          | Solenoid control                     |
| Lazy Susan Bearing        | Rotating mount                       |
| 3D-Printed Clamp          | Gun stabilization                    |
| Wooden Base               | Physical support                     |

## CAD Files & Reference Links

- Rail Option 1: https://www.thingiverse.com/thing:3060828  
- Rail Option 2: https://www.thingiverse.com/thing:5873867  
- Solenoid Inspiration: https://www.youtube.com/watch?v=67hDDnlqaKc  
- DRV8825 Motor Driver: https://www.pololu.com/product/2133  

## Project Timeline

| Task | Description | Status |
|------|-------------|--------|
| Stepper Motor Control | Code + wiring test on Pi | ✅ |
| Solenoid Setup | Mounting, control circuit | ✅ |
| Audio Analysis | Real-time FFT & note detection | ✅ |
| Integration | Map notes to hardware actions | ✅ |
| Mobile Controller | RaspiController phone control | WIP |
| Assembly | Clamp, base, wiring | ✅ |
| Final Demo | Fully functional system | ✅ |

## Summary

This project combines signal processing, embedded hardware control, and mechanical design to create a responsive, sound-controlled turret. By leveraging real-time audio frequency detection and precise GPIO-based actuation, the system bridges music and robotics in an interactive and engaging way.
