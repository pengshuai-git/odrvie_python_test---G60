import odrive
import time
import datetime
import matplotlib.pyplot as plt
from collections import deque

# 连接ODrive
drv = odrive.find_any()
time.sleep(1)

max_points = 100  # 显示最近100个点
motor_temps = deque(maxlen=max_points)
fet_temps = deque(maxlen=max_points)
timestamps = deque(maxlen=max_points)

plt.ion()
fig, ax = plt.subplots()
line1, = ax.plot([], [], label='Motor Temp (°C)')
line2, = ax.plot([], [], label='FET Temp (°C)')
ax.set_xlabel('Time')
ax.set_ylabel('Temperature (°C)')
ax.legend()

start_time = time.time()

while True:
    now_sec = int(time.time() - start_time)
    motor_temp = drv.axis0.motor.motor_thermistor.temperature
    fet_temp = drv.axis0.motor.fet_thermistor.temperature
    timestamps.append(now_sec)
    motor_temps.append(motor_temp)
    fet_temps.append(fet_temp)

    line1.set_data(timestamps, motor_temps)
    line2.set_data(timestamps, fet_temps)
    ax.set_xticks(list(timestamps)[::max(1, len(timestamps)//10)])
    ax.set_xticklabels([str(x) for x in list(timestamps)[::max(1, len(timestamps)//10)]], rotation=0, fontsize=8)
    ax.set_xlim(max(0, now_sec - max_points + 1), now_sec)
    ax.set_ylim(min(min(motor_temps, default=0), min(fet_temps, default=0)) - 5,
                max(max(motor_temps, default=50), max(fet_temps, default=50)) + 5)
    plt.tight_layout()
    plt.pause(1)
