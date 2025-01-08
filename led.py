import RPi.GPIO as GPIO
import time

# 設定 GPIO 模式
GPIO.setmode(GPIO.BCM)

# 定義 GPIO 引腳，假設 LED 接到 Physical Pin 11 (GPIO 17)
LED_PIN = 12

# 設定 LED 引腳為輸出模式
GPIO.setup(LED_PIN, GPIO.OUT)

# 打開 LED（設置為 HIGH）
GPIO.output(LED_PIN, GPIO.HIGH)

# 保持 3 秒，讓 LED 亮起來
time.sleep(3)

# 關閉 LED（設置為 LOW）
GPIO.output(LED_PIN, GPIO.LOW)

# 清理 GPIO 設定
GPIO.cleanup()
