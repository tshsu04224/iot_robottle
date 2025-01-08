import math 
import time  
from adxl345 import ADXL345

# 初始化 ADXL345 加速度計
accelerometer = ADXL345()

# 檢測傾斜
def detect_tilt():
    axes = accelerometer.getAxes(True)
    x, y, z = axes['x'], axes['y'], axes['z']
    magnitude = math.sqrt(x**2 + y**2 + z**2)
    if magnitude == 0:
        return False  # 避免除以零錯誤

    x_angle = x / magnitude
    y_angle = y / magnitude

    # 如果傾斜角度超過 50%，認定為發生傾斜
    if abs(x_angle) > 0.5 or abs(y_angle) > 0.5:
        return True
    return False

# 主程序
def main():
    print("Starting smart bottle system...")
    last_drink_time = time.time()

    while True:
        # 檢測是否傾斜
        if detect_tilt():
            print("Bottle tilted: User is drinking water")
            last_drink_time = time.time()
        else:
            # 檢查距上次喝水的時間
            elapsed_time = time.time() - last_drink_time
            if elapsed_time > 3600:  # 超過1小時未喝水
                print("Reminder: It's been over an hour since the last drink!")

        time.sleep(3)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting program...")

