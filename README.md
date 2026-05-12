# Face Recognition Based Electronic Voting Machine

A hybrid security system using **Python (OpenCV)** for biometric authentication and **Arduino Uno** for hardware voting logic.

## 🛠 Hardware Components
* Arduino Uno
* I2C LCD Display (16x2)
* USB Webcam
* Push Buttons & Buzzer

## How it Works
1. Python Layer:Uses `face_recognition` to identify the voter. Sends a 'U' signal via USART to Arduino if verified.
2. Arduino Layer: Receives the serial signal, unlocks the buttons, and records the vote.
3. Security: Uses EEPROM to prevent double-voting.

## 📁 Folder Structure
* `Python_Scripts/`: Contains the logic and Serial communication.
* `Arduino_Code/`: Contains the '.ino' sketch for the microcontroller.

## 📄 Documentation
Full project details can be found in the `Documentation/` folder:
* Project Proposal: Initial scope and objectives.
* Research Paper: Detailed literature review and methodology.
* Final Presentation: PPT used for the final defense.
