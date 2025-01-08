# RoBottle - The Smart Drinking IoT Device

## Project Overview
Robottle is a Smart Drinking IoT device designed to encourage healthy hydration habits. Using a Raspberry Pi Zero 2W and a range of sensors, the device monitors water quality, water levels, and user drinking behavior. It delivers real-time updates and reminders through a LINE bot interface, ensuring users stay hydrated. Additionally, the system prompts users to drink water after extended periods of inactivity, helping to maintain regular hydration throughout the day.

## Features
Water Intake Tracking: Monitors water consumption using an ultrasonic sensor.
Water Quality Monitoring: Measures Total Dissolved Solids (TDS) using a TDS sensor.
Hydration Reminders: LED reminders to prompt drinking after an hour of inactivity.
Web Interface: Displays data via LINE Bot.
Tilt Detection: Detects when the bottle is tilted using an accelerometer to infer drinking activity.

## Required Components
### Hardware Requirements
- Raspberry Pi Zero 2W
- AJ-SR04M Ultrasonic Sensor
- Grove TDS Sensor
- ADXL345 Accelerometer
- LED
- Resistors
- Breadboard and Jumper Wires

### Sofeware Requirements
- Raspbian Buster OS
- Python 3
- Libraries:
  - RPi.GPIO: Controls GPIO pins.
  - Flask: Hosts a local server for the LINE Bot.
  - line-bot-sdk: Integrates with LINE messaging.
  - Adafruit_ADS1x15: Reads analog data from the TDS sensor.
  - adxl345: Interfaces with the accelerometer.
- Platforms:
  - LINE Messaging API: Notifies users with water data.
 
## Circuit Diagram

## System Architecture
Sensors collect data (water level, water quality, tilt).
Raspberry Pi Pico processes the data and controls the LED.
Flask Server communicates with the LINE Bot for user notifications.

## Step-by-Step Implementation
1. SetUp Raspberry Pi
   



