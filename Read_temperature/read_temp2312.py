import odrive
import time
import datetime

# 重新连接
odrv0 = odrive.find_any()
time.sleep(1)

print("电机热敏电阻配置:", odrv0.axis0.motor_thermistor.config)
print("FET热敏电阻配置:", odrv0.axis0.fet_thermistor.config)
print("-------------------------------------------------------")

while True:
    motor_temp = odrv0.axis0.motor_thermistor.temperature-44.38
    fet_temp = odrv0.axis0.fet_thermistor.temperature
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{now}] 电机热敏电阻温度: {motor_temp:.2f} °C ,FET热敏电阻温度: {fet_temp:.2f} °C")
    time.sleep(1)