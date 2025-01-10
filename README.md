# **RoBottle - The Smart Drinking IoT Device**

## **Overview 📜**
RoBottle is a Smart Drinking IoT device designed to promote healthy hydration habits. Utilizing a Raspberry Pi Zero 2W and various sensors, the device monitors water quality, water levels, and user drinking behavior. It provides real-time updates and hydration reminders through a LINE bot interface, ensuring users stay hydrated. Additionally, the system prompts users to drink water after extended periods of inactivity, helping maintain regular hydration throughout the day.

## **Features ✨**
1. **Water Quality Monitoring (TDS Sensor)**  
  Measures the Total Dissolved Solids (TDS) value in the water and determines whether it meets safe drinking standards.

2. **Water Volume Detection (Ultrasonic Sensor)**  
  Uses an ultrasonic sensor to measure the remaining water volume in the bottle and calculates the water level percentage.

3. **Drinking Behavior Detection (Accelerometer)**  
  Utilizes an accelerometer to detect the tilt of the bottle, determining whether drinking behavior has occurred.

4. **Drinking Reminder (LED + LINE Bot)**  
  Sends reminders through LED flashing and LINE Bot notifications when there is a prolonged period of inactivity in drinking.

5. **LINE Bot Integration**  
  Interacts with the user via LINE Bot, including features like checking water quality, monitoring water levels, and enabling or disabling drinking reminders.

## **System Architecture 🖥️**
![system architecture](https://github.com/tshsu04224/iot_robottle/blob/main/images/architecture.png)

- The system integrates hardware, software, and external services for a smart drinking IoT device.
  
- Sensors (ultrasonic, accelerometer, and TDS) collect data on water level, drinking behavior, and water quality, which are processed by respective functions.
    
- The Flask server acts as the central hub, receiving data, processing user requests, and sending notifications.  

- Users interact via a LINE Bot API for real-time updates and commands, while the GPIO controls an LED for hydration reminders.

## **Required Components 🛠️**

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

## **Circuit Diagram 🔌**
 ![circuit diagram](https://github.com/tshsu04224/iot_robottle/blob/main/images/circuit_diagram.png)

## **Step-by-Step Implementation 📝**

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

#### **2.1 Grove TDS sensor and ADS1115 ADC module**
The GPIO pins on the Raspberry Pi cannot directly handle analog signals, so an additional ADC module, ADS1115, is needed to convert analog signals into digital signals.
1. First, connect ADS1115 ADC module to Raspberry Pi as follows:
   ![ads](https://github.com/tshsu04224/iot_robottle/blob/main/images/ads.png)
  - Wire the GND pin of the ADC module to Physical Pin 6 (GND) on the Raspberry Pi.  
  - Wire the VDD pin of the ADC module to Physical Pin 1 (3v3) on the Raspberry Pi.  
  - Wire the SDA pin of the ADC module to Physical Pin 3 (SDA) on the Raspberry Pi.
  - Wire the SCL pin of the ADC module to Physical Pin 5 (SCL) on the Raspberry Pi.
    
2. Then, connect Grove TDS sensor to ADC module as follows:
   ![tds](https://github.com/tshsu04224/iot_robottle/blob/main/images/tds.png)
  - Wire the GND pin of the TDS sensor to the GND pin on the ADC module.  
  - Wire the VCC pin of the TDS sensor to the VDD pin on the ADC module.
  - Wire the SID pin of the TDS sensor to the A0 pin on the ADC module.
 
#### **2.2 ADXL345 accelerometer sensor**
  ![adxl](https://github.com/tshsu04224/iot_robottle/blob/main/images/adxl.png)
- Wire the GND pin of the Accelerometer to Physical Pin 14 (GND) on the Raspberry Pi.  
- Wire the VCC pin of the Accelerometer to Physical Pin 17 (3v3) on the Raspberry Pi.  
- Wire the SDA pin of the Accelerometer to Physical Pin 3 (SDA) on the Raspberry Pi.  
- Wire the SCL pin of the Accelerometer to Physical Pin 5 (SCL) on the Raspberry Pi. 

#### **2.3 AJ-SR04M Ultrasonic Distance Sensor**
  ![ajsr04m](https://github.com/tshsu04224/iot_robottle/blob/main/images/ajsr04m.png)
- Wire the GND pin of the Ultrasonic Sensor to Physical Pin 39 (GND) on the Raspberry Pi.  
- Wire the 5V pin of the Ultrasonic Sensor to Physical Pin 2 (5V) on the Raspberry Pi.
- Wire the Trig pin of the Ultrasonic Sensor to Physical Pin 7 (GPIO4) on the Raspberry Pi. 
- Wire the Echo pin of the Ultrasonic Sensor to Physical Pin 11 (GPIO17) on the Raspberry Pi.  

#### **2.4 LED**
  ![led](https://github.com/tshsu04224/iot_robottle/blob/main/images/led.png)
- Connect the positive leg (+) of the LED to physical pin 32 (GPIO12) on the Raspberry Pi through a 220-ohm resistor.  
- Connect the negative leg (-) of the LED directly to physical pin 34 (GND) on the Raspberry Pi.  

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
First, ensure I2C is enabled, then:

##### **3.6.1 Check I2C Devices**
To check if I2C devices are connected correctly:
```bash
sudo apt-get install i2c-tools -y
i2cdetect -y 1
```

You should see:
```bash
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:                         -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: -- -- -- -- -- -- -- -- 48 -- -- -- -- -- -- --
50: -- -- -- 53 -- -- -- -- -- -- -- -- -- -- -- --
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: -- -- -- -- -- -- -- --
```
- `0x48` (ADS1115 module address)
- `0x53` (ADXL345 accelerometer address)

#### **3.7 Test the sensors**
If you want to test the functionality of these sensors, you can copy my code files `accelerometer.py`, `grove_tds.py`, and `ultraDis.py`, and try running them.

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

### **5. Code Structure and Implementation**

#### **5.1. Hardware Initialization**
#### GPIO Pin Configuration
- **TRIG/ECHO (Ultrasonic Sensor)**: Used to measure the water level distance.
- **LED_PIN (LED Reminder Light)**: Controls the LED flashing for reminders.
```python
GPIO.setmode(GPIO.BOARD)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.OUT)
```

#### Sensor Initialization
- **ADS1115 (TDS Sensor)**: Configures the gain value `GAIN`, reads analog voltage values, and converts them to TDS.
- **ADXL345 (Accelerometer)**: Used to detect the tilt of the bottle.
```python
adc = ADS1115(address=0x48)
GAIN = 1
accelerometer = ADXL345()
```

#### **5.2. Feature Implementation**
#### Water Quality Monitoring
Reads values from the TDS sensor, converts them to ppm, and checks if they exceed the safe threshold.
```python
def read_tds(channel=0):
    raw_value = adc.read_adc(channel, gain=GAIN)
    voltage = abs(raw_value * (4.096 / 32768.0))
    tds_value = (133.42 * voltage**3 - 255.86 * voltage**2 + 857.39 * voltage)
    return max(0, tds_value)
```

#### Water Level Measurement and Calculation
The ultrasonic sensor measures distance and calculates the remaining water level percentage:
```python
def measure_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    # Calculates pulse duration and converts it to distance (cm)
    pulse_duration = pulse_end - pulse_start
    return (pulse_duration * 17150) - 14

def calculate_water_level(distance):
    remaining_height = WATER_BOTTLE_HEIGHT - distance
    return round((remaining_height / WATER_BOTTLE_HEIGHT) * 100, 2)
```

#### Drinking Behavior Detection
Uses the accelerometer to detect bottle tilt, determining drinking actions:
```python
def detect_tilt():
    axes = accelerometer.getAxes(True)
    x, y, z = axes['x'], axes['y'], axes['z']
    magnitude = math.sqrt(x**2 + y**2 + z**2)
    x_angle = x / magnitude
    y_angle = y / magnitude
    return abs(x_angle) > 0.5 or abs(y_angle) > 0.5
```

#### Drinking Reminder
Controls LED flashing and sends reminder notifications via LINE Bot.
```python
def blink_led(duration=5):
    end_time = time.time() + duration
    while time.time() < end_time:
        GPIO.output(LED_PIN, True)
        time.sleep(0.5)
        GPIO.output(LED_PIN, False)
        time.sleep(0.5)
```

#### **5.3. LINE Bot Integration**
Starts a web server using the Flask framework to handle LINE Bot Webhook requests.
- **Command Detection**:
  - `水質檢測`: Check water quality.
  - `目前資訊`: Measure water level and percentage.
  - `提醒我喝水` / `取消提醒`: Enable or disable the reminder function.
```python
@app.route("/", methods=["POST"])
def linebot():
    body = request.get_data(as_text=True)
    signature = request.headers['X-Line-Signature']
    handler.handle(body, signature)

    msg = json_data['events'][0]['message']['text']
    if msg == "水質檢測":
        tds_value = read_tds()
        # Return water quality results
    elif msg == "目前資訊":
        distance = measure_distance()
        water_level = calculate_water_level(distance)
        # Return water level information
    elif msg == "提醒我喝水":
        reminder_enabled = True
    elif msg == "取消提醒":
        reminder_enabled = False
```

#### **5.4. Main Program Logic**
- Continuously monitors the tilt and water level of the bottle.
- Updates the last drinking time and water level when drinking behavior is detected.
```python
def main():
    global last_drink_time, last_water_level
    while True:
        if detect_tilt():
            initial_distance = measure_distance()
            time.sleep(3)
            final_distance = measure_distance()
            if final_level < initial_level - 1:
                last_drink_time = time.time()
                last_water_level = final_level
        time.sleep(3)
```

The complete code file is in `robottle.py`. You can refer to that file for detailed code or try executing it.

## **[Demo Video](https://youtube.com/shorts/RiBYk9MDmnA?si=cT1atlD9fJNi6Rfa)🎥**

## **Reference 📚**
- [Raspberry Pi Accelerometer using the ADXL345](https://pimylifeup.com/raspberry-pi-accelerometer-adxl345/)
