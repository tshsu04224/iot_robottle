import RPi.GPIO as GPIO
import time

# GPIO 腳位定義（Physical）
TRIG = 7   # 超音波 Trig 腳位 -> Pin 7
ECHO = 11  # 超音波 Echo 腳位 -> Pin 11

# 水壺高度設定（單位：cm）
WATER_BOTTLE_HEIGHT = 20.0  # 假設水壺總高度為 20 cm

# 初始化 GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def measure_distance():
    """測量水位與感測器的距離"""
    # 發送超音波信號
    GPIO.output(TRIG, True)
    time.sleep(0.00001)  # 發送 10µs 的脈衝
    GPIO.output(TRIG, False)

    # 等待 Echo 信號
    pulse_start = time.time()
    timeout = pulse_start + 0.02  # 超時時間 20ms

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
        if pulse_start > timeout:
            return None  # 等待回波信號超時

    pulse_end = time.time()
    timeout = pulse_end + 0.02  # 超時時間 20ms

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
        if pulse_end > timeout:
            return None  # 等待回波結束信號超時

    # 計算距離（單位：cm）
    pulse_duration = pulse_end - pulse_start
    distance = (pulse_duration * 17150) - 15  # 超音波速度：34300 cm/s
    return round(distance, 2)

def calculate_water_level(distance):
    """根據測量距離計算剩餘水量百分比"""
    if distance > WATER_BOTTLE_HEIGHT or distance is None:
        return 0  # 水壺中無水或測量失敗
    remaining_height = WATER_BOTTLE_HEIGHT - distance
    water_level_percent = (remaining_height / WATER_BOTTLE_HEIGHT) * 100
    return round(water_level_percent, 2)

try:
    while True:
        distance = measure_distance()
        if distance is not None:
            water_level = calculate_water_level(distance)
            print(f"水位距離: {distance} cm")
            print(f"剩餘水量: {water_level}%\n")
        else:
            print("測量失敗，請檢查感測器連接。\n")
        time.sleep(2)  # 每隔 2 秒測量一次
except KeyboardInterrupt:
    print("結束程式")
    GPIO.cleanup()
