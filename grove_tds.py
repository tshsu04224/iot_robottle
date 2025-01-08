import time
from Adafruit_ADS1x15 import ADS1115

# 初始化 ADS1115 類別
adc = ADS1115(address=0x48)
GAIN = 1  # 設置增益

# TDS 檢測範圍定義（ppm）
SAFE_TDS_THRESHOLD = 500  # 安全飲用水的 TDS 最大值

def read_tds(channel=0):
    """
    讀取 TDS 感測器的數值並計算 TDS 值。
    :param channel: ADS1115 的通道，默認為 0。
    :return: TDS 值（ppm）。
    """
    raw_value = adc.read_adc(channel, gain=GAIN)
    voltage = abs(raw_value * (4.096 / 32768.0))  # 轉換為電壓並取絕對值
    tds_value = (133.42 * voltage**3 - 255.86 * voltage**2 + 857.39 * voltage) * 0.5  # TDS公式
    return max(0, tds_value)  # 確保返回值為正

def main():
    print("Starting TDS monitoring system...")

    while True:
        tds_value = read_tds()
        print(f"Current TDS value: {tds_value:.2f} ppm")

        if tds_value > SAFE_TDS_THRESHOLD:
            print("Warning: Water quality is poor, consider replacing the water!")
        else:
            print("Water quality is good, safe to drink.")

        time.sleep(5)  # 每隔 5 秒測量一次

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting TDS monitoring...")
