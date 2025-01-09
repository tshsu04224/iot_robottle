import time
import math
import RPi.GPIO as GPIO
from flask import Flask, request, jsonify
import json
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.exceptions import InvalidSignatureError
from Adafruit_ADS1x15 import ADS1115
from adxl345 import ADXL345

# Line Bot 設定
LINE_CHANNEL_ACCESS_TOKEN = "Your Channel Access Token"
LINE_CHANNEL_SECRET = "Your Channel Secret"

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# Flask 伺服器
app = Flask(__name__)

# GPIO 腳位設定
TRIG = 7
ECHO = 11
LED_PIN = 32
WATER_BOTTLE_HEIGHT = 15.0  # 水壺高度 (cm)
SAFE_TDS_THRESHOLD = 500  # TDS 安全飲用水的最大值 (ppm)

# 初始化感測器
adc = ADS1115(address=0x48)
GAIN = 1  # 設置增益
accelerometer = ADXL345()

# 初始化 GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.OUT)  # 設定 LED 腳位為輸出模式

# 讀取 TDS 值
def read_tds(channel=0):
    try:
        raw_value = adc.read_adc(channel, gain=GAIN)
        voltage = abs(raw_value * (4.096 / 32768.0))
        tds_value = (133.42 * voltage**3 - 255.86 * voltage**2 + 857.39 * voltage)
        return max(0, tds_value)  # 確保返回值為正數
    except Exception as e:
        print(f"Error reading TDS sensor: {e}")
        return None

# 檢測水壺傾斜
def detect_tilt():
    axes = accelerometer.getAxes(True)
    x, y, z = axes['x'], axes['y'], axes['z']
    magnitude = math.sqrt(x**2 + y**2 + z**2)
    if magnitude == 0:
        return False
    x_angle = x / magnitude
    y_angle = y / magnitude

    # 設定傾斜關值和最小間隔
    MIN_INTERVAL = 10  # 喝水檢測的最小間隔秒數
    global last_drink_time
    if (abs(x_angle) > 0.5 or abs(y_angle) > 0.5) and (time.time() - last_drink_time > MIN_INTERVAL):
        return True
    return False

# 測量水位距離
def measure_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    pulse_start = time.time()
    timeout = pulse_start + 0.02
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
        if pulse_start > timeout:
            return None
    pulse_end = time.time()
    timeout = pulse_end + 0.02
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
        if pulse_end > timeout:
            return None
    pulse_duration = pulse_end - pulse_start
    return (pulse_duration * 17150) - 14

# 計算水位百分比
def calculate_water_level(distance):
    """
    根據測量的距離計算剩餘水量百分比。
    水壺高度: 15 cm，測距感測器安裝在水壺頂部。
    """
    if distance is None or distance > WATER_BOTTLE_HEIGHT:
        return 0  # 超出水壺高度範圍，水量為 0%

    # 剩餘水位高度 = 水壺總高度 - 測量距離
    remaining_height = WATER_BOTTLE_HEIGHT - distance

    # 計算剩餘水量百分比
    water_percentage = (remaining_height / WATER_BOTTLE_HEIGHT) * 100
    return round(water_percentage, 2)

# LED 閃爍
def blink_led(duration=5):
    end_time = time.time() + duration
    while time.time() < end_time:
        GPIO.output(LED_PIN, True)  # 開燈
        time.sleep(0.5)
        GPIO.output(LED_PIN, False)  # 關燈
        time.sleep(0.5)

# 保存上次喝水時間
last_drink_time = time.time()
last_water_level = 0
reminder_enabled = False  # 提醒功能是否啟動

# Flask 路由
@app.route("/", methods=["POST"])
def linebot():
    global last_drink_time, last_water_level, reminder_enabled
    body = request.get_data(as_text=True)
    try:
        json_data = json.loads(body)
        signature = request.headers['X-Line-Signature']
        handler.handle(body, signature)

        if not json_data['events']:
            return 'OK'

        tk = json_data['events'][0]['replyToken']
        user_id = json_data['events'][0]['source']['userId']
        msg = json_data['events'][0]['message']['text']

        if msg == "水質檢測":
            tds_value = read_tds()
            if tds_value is None:
                reply = "Error: 無法讀取水質數據，請檢查感測器。"
            elif tds_value > SAFE_TDS_THRESHOLD:
                reply = f"水質檢測結果: {tds_value:.2f} ppm\n警告: 水質不佳，請更換水源！"
            else:
                reply = f"水質檢測結果: {tds_value:.2f} ppm\n水質良好，適合飲用。"
        elif msg == "目前資訊":
            distance = measure_distance()
            if distance is None:
                distance_str = "無法測量"
                water_level = "無法讀取水位距離，請檢查感測器。"
            else:
                distance_str = f"{distance:.3f}"
                water_level = f"{calculate_water_level(distance)}%"

                # 檢測水量是否減少，如果減少，更新上次喝水時間
                current_water_level = calculate_water_level(distance)
                if current_water_level < last_water_level:
                    last_drink_time = time.time()
                    last_water_level = current_water_level

            tds_value = read_tds()
            last_drink = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(last_drink_time))
            water_quality = (
                f"水質: {tds_value:.2f} ppm"
                if tds_value is not None else "無法讀取水質數據，請檢查感測器。"
            )
            reply = (
                f"目前資訊:\n"
                f"水位距離: {distance_str} cm\n"
                f"剩餘水量: {water_level}\n"
                f"{water_quality}\n"
                f"上次喝水時間: {last_drink}"
            )
        elif msg == "提醒我喝水":
            reminder_enabled = True
            reply = "已啟動喝水提醒功能。當超過一小時未喝水時將提醒您。"
        elif msg == "取消提醒":
            reminder_enabled = False
            reply = "已關閉喝水提醒功能。"
        else:
            reply = "未知的指令，請輸入有效指令。"

        line_bot_api.reply_message(tk, TextSendMessage(text=reply))

        if reminder_enabled:
# and (time.time() - last_drink_time > 3600):
            blink_led(5)
            line_bot_api.push_message(
                user_id, TextSendMessage(text="已經超過一小時未喝水，請記得補充水分！")
            )

    except Exception as e:
        print(f"Error: {e}")
    return 'OK'

# 主程序
def main():
    global last_drink_time, last_water_level
    while True:
        if detect_tilt():
            print("水壺傾斜，檢查水量變化...")
            initial_distance = measure_distance()
            if initial_distance is not None:
                time.sleep(3)  # 等待測量穩定
                final_distance = measure_distance()
                if final_distance is not None:
                    initial_level = calculate_water_level(initial_distance)
                    final_level = calculate_water_level(final_distance)
                    if final_level < initial_level - 1:
                        print("喝水行為檢測成功，更新記錄...")
                        last_drink_time = time.time()
                        last_water_level = final_level
        time.sleep(3)

if __name__ == "__main__":
    import threading
    threading.Thread(target=main, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)
