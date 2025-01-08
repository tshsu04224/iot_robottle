# **RoBottle - The Smart Drinking IoT Device**

## **Project Overview**
RoBottle is a Smart Drinking IoT device designed to promote healthy hydration habits. Utilizing a Raspberry Pi Zero 2W and various sensors, the device monitors water quality, water levels, and user drinking behavior. It provides real-time updates and hydration reminders through a LINE bot interface, ensuring users stay hydrated. Additionally, the system prompts users to drink water after extended periods of inactivity, helping maintain regular hydration throughout the day.

## **Features**
- **Water Intake Tracking:** Monitors water consumption using an ultrasonic sensor.
- **Water Quality Monitoring:** Measures Total Dissolved Solids (TDS) using a TDS sensor.
- **Hydration Reminders:** LED reminders prompt drinking after an hour of inactivity.
- **Web Interface:** Displays data via LINE Bot.
- **Tilt Detection:** Detects when the bottle is tilted using an accelerometer to infer drinking activity.

## **Required Components**

### **Hardware Requirements**
- Raspberry Pi Zero 2W
- AJ-SR04M Ultrasonic Sensor
- Grove TDS Sensor
- ADXL345 Accelerometer
- LED
- Resistors
- Breadboard and Jumper Wires

### **Software Requirements**
- Raspbian Buster OS
- Python 3
- Libraries:
  - RPi.GPIO: Controls GPIO pins.
  - Flask: Hosts a local server for the LINE Bot.
  - line-bot-sdk: Integrates with LINE messaging.
  - Adafruit_ADS1x15: Reads analog data from the TDS sensor.
  - adxl345: Interfaces with the accelerometer.
- Platforms:
  - LINE Messaging API: Sends water data notifications to users.

## **Circuit Diagram**
- (Include your circuit diagram here)

## **System Architecture**
1. **Sensors** collect data on water level, water quality, and tilt.
2. **Raspberry Pi Zero 2W** processes the data and controls the LED.
3. **Flask Server** communicates with the LINE Bot for user notifications.

## **Step-by-Step Implementation**

### **1. Set Up Raspberry Pi**

#### **1.1 Follow the Raspberry Pi Setup Guide**
Follow the instructions from the official Raspberry Pi website to set up your Raspberry Pi:
[Getting Started with Raspberry Pi](https://www.raspberrypi.com/documentation/computers/getting-started.html)

#### **1.2 Enable Interfaces (SSH / I2C / VNC)**
- Open the Raspberry Pi Configuration tool from the "Preferences" menu in the desktop environment.
- Go to the "Interfaces" tab and enable the following options:
  - **SSH**
  - **I2C**
  - **VNC**
- Click "OK" to apply these changes.

Alternatively, you can enable them using terminal commands:

##### **Enable SSH:**
1. Open the terminal.
2. Run the following commands:
   ```bash
   sudo systemctl enable ssh
   sudo systemctl start ssh
   ```
3. To check if SSH is running, use:
   ```bash
   sudo systemctl status ssh
   ```

##### **Enable I2C:**
1. Open the terminal.
2. Run the following command to open the configuration tool:
   ```bash
   sudo raspi-config
   ```
3. In the `raspi-config` menu, go to **Interfacing Options** → **I2C**, then choose **Yes** to enable I2C.
4. After completion, select **Finish** and reboot the Raspberry Pi:
   ```bash
   sudo reboot
   ```

##### **Enable VNC:**
1. Open the terminal.
2. Run the following command to open the VNC configuration tool:
   ```bash
   sudo raspi-config
   ```
3. In the `raspi-config` menu, go to **Interfacing Options** → **VNC**, then choose **Yes** to enable VNC.
4. After completion, select **Finish** and reboot the Raspberry Pi:
   ```bash
   sudo reboot
   ```

Once completed, SSH, I2C, and VNC will be enabled on your Raspberry Pi.

### **2. Set Up Hardware**
- (Include detailed steps and diagrams for wiring sensors, LEDs, etc.)

### **3. Install Required Libraries**

#### **3.1 Update the Raspberry Pi System**
Before installing any libraries, update your Raspberry Pi system:
```bash
sudo apt update
sudo apt upgrade -y
```

#### **3.2 Install Python 3 and pip**
Ensure Python 3 and pip are installed, along with the latest version of pip:
```bash
sudo apt install python3 python3-pip -y
pip3 install --upgrade pip
```

#### **3.3 Set Up a Python Virtual Environment (Optional but Recommended)**
For isolating project dependencies, it is recommended to create a virtual environment:
```bash
sudo apt-get install python3-venv -y
python3 -m venv myenv
source myenv/bin/activate
```

#### **3.4 Install Required Libraries**

Below are the steps to install all necessary libraries for the project:

##### **3.4.1 Install Flask**
Flask is used to create a web server for the LINE Bot.
```bash
pip3 install Flask
```
- **Description:** Flask is a micro web framework that allows you to build a web server for your LINE Bot API.

##### **3.4.2 Install line-bot-sdk**
This SDK allows communication between your Raspberry Pi and the LINE Bot API.
```bash
pip3 install line-bot-sdk
```
- **Description:** This library enables LINE messaging integration for sending hydration reminders to users.

##### **3.4.3 Install RPi.GPIO**
RPi.GPIO is required for controlling GPIO pins on the Raspberry Pi.
```bash
pip3 install RPi.GPIO
```
- **Description:** The RPi.GPIO library enables interaction with hardware components like LEDs and sensors.

##### **3.4.4 Install Adafruit-ADS1x15**
This library supports reading data from the TDS sensor via the ADS1115 ADC.
```bash
pip3 install adafruit-ads1x15
```
- **Description:** Required for interfacing with the ADS1115 ADC, which reads analog data from the TDS sensor.

##### **3.4.5 Install adxl345**
This library helps interface with the ADXL345 accelerometer.
```bash
pip3 install adxl345
```
- **Description:** Used to detect tilt via the accelerometer, which is used to infer drinking behavior.

#### **3.5 Verify Installation**

After installation, verify the libraries:
```bash
pip3 freeze
```
You should see:
- Flask
- line-bot-sdk
- RPi.GPIO
- adafruit-ads1x15
- adxl345

Alternatively, for a virtual environment:
```bash
pip list
```

#### **3.6 Verify I2C Interface**
Ensure I2C is enabled.

##### **3.6.1 Check I2C Devices**
To check if I2C devices are connected correctly:
```bash
sudo apt-get install i2c-tools -y
i2cdetect -y 1
```

You should see:
- `0x48` (ADS1115 module address)
- `0x53` (ADXL345 accelerometer address)

### **4. LINE Bot Setup**

#### **4.1 Install LINE Bot SDK**

First, install the **line-bot-sdk**, which is the Python package for communicating with the LINE Bot API.

```bash
pip3 install line-bot-sdk
```

- **Description:** The `line-bot-sdk` is the official SDK for interacting with the LINE API, allowing you to send messages to users or receive messages from LINE users.

After installation, you can verify the installation with the following command:

```bash
pip3 show line-bot-sdk
```

#### **4.2 Set Up LINE Bot Developer Account**

To interact with the LINE Bot, you need to create a LINE Bot and obtain the `Access Token` and `Channel Secret`. These steps are done in the **LINE Developers Console**.

##### **4.2.1 Access LINE Developers Console**
1. Go to the [LINE Developers Console](https://developers.line.biz/en/).
2. Log in with your LINE account. If you don’t have an account, register one first.

##### **4.2.2 Create a New Channel (Bot)**
1. In the LINE Developers Console, click **Create New Provider** and name your provider (e.g., RoBottle).
2. Create a new **Channel**, selecting **Messaging API** as the type.
3. Fill in the necessary information:
   - **Channel name:** Name your bot.
   - **Channel description:** Describe your bot.
   - **Channel icon:** Upload an icon for your bot (optional).
4. After filling out the information, click **Create**.

##### **4.2.3 Obtain LINE Channel Access Token and Secret**
1. On your Channel settings page, find the **Channel Access Token** and **Channel Secret**.
2. Copy and save these values, as they will be used in the script later.

#### **4.3 Set Up Webhook URL**

To enable your LINE Bot to receive messages, you need to set up a Webhook URL. This URL is used to receive messages from LINE users.

##### **4.3.1 Use ngrok to Create a Public URL**

If your Raspberry Pi doesn’t have a public IP address, you can use **ngrok** to create a temporary public URL for testing.

1. Install ngrok:
   ```bash
   sudo apt install ngrok
   ```

2. Register and download ngrok
   - Go to the [ngrok website](https://ngrok.com/), register an account, and download the appropriate version.

3. Start ngrok on your Raspberry Pi:
   - Run the following command to start ngrok and expose your local port (for example, your Flask server is running on port 5000):
     ```bash
     ngrok http 5000
     ```

4. You will receive a public URL, such as:
   ```
   https://xxxxxxxx.ngrok.io
   ```

5. Use this public URL to set your LINE Bot Webhook URL. Copy this URL and set it in the **LINE Developers Console**:
   - In the **Messaging API** settings, find the **Webhook URL** and set it to `https://xxxxxxxx.ngrok.io`.

6. Click **Verify** to ensure the Webhook is set up correctly.

##### **4.3.2 Set Up Webhook URL (Local Flask Server) and Test LINE Bot**

You can copy the codes from `linebot.py` to test if your bot works or not.
Make sure to replace `YOUR_CHANNEL_ACCESS_TOKEN` and `YOUR_CHANNEL_SECRET` with the actual values you obtained from the LINE Developers Console.
