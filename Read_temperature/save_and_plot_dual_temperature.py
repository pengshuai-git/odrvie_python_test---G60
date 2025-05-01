import odrive
import time
import csv
import matplotlib.pyplot as plt
from collections import deque

# 连接ODrive
drv = odrive.find_any()
time.sleep(1)

max_points = 100  # 滚动窗口点数
motor_temps = []
fet_temps = []
timestamps = []

scroll_motor_temps = deque(maxlen=max_points)
scroll_fet_temps = deque(maxlen=max_points)
scroll_timestamps = deque(maxlen=max_points)

csv_file = 'temperature_log.csv'
with open(csv_file, mode='w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Time(s)', 'Motor_Temp(°C)', 'FET_Temp(°C)'])
    plt.ion()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    line1, = ax1.plot([], [], label='Motor Temp (°C)')
    line2, = ax1.plot([], [], label='FET Temp (°C)')
    line3, = ax2.plot([], [], label='Motor Temp (°C)')
    line4, = ax2.plot([], [], label='FET Temp (°C)')
    ax1.set_title('live_temperature')
    ax2.set_title('full_temperature')
    ax1.set_xlabel('Time (s)')
    ax2.set_xlabel('Time (s)')
    ax1.set_ylabel('Temperature (°C)')
    ax2.set_ylabel('Temperature (°C)')
    ax1.legend()
    ax2.legend()
    start_time = time.time()
    print('Time(s), Motor_Temp(°C), FET_Temp(°C)')
    while True:
        now_sec = int(time.time() - start_time)
        motor_temp = drv.axis0.motor.motor_thermistor.temperature
        fet_temp = drv.axis0.motor.fet_thermistor.temperature
        timestamps.append(now_sec)
        motor_temps.append(motor_temp)
        fet_temps.append(fet_temp)
        scroll_timestamps.append(now_sec)
        scroll_motor_temps.append(motor_temp)
        scroll_fet_temps.append(fet_temp)
        writer.writerow([now_sec, f'{motor_temp:.2f}', f'{fet_temp:.2f}'])
        f.flush()
        print(f'{now_sec}, {motor_temp:.2f}, {fet_temp:.2f}')
        # 滚动窗口图
        line1.set_data(scroll_timestamps, scroll_motor_temps)
        line2.set_data(scroll_timestamps, scroll_fet_temps)
        ax1.set_xlim(max(0, now_sec - max_points + 1), now_sec)
        ax1.set_ylim(min(min(scroll_motor_temps, default=0), min(scroll_fet_temps, default=0)) - 5,
                    max(max(scroll_motor_temps, default=50), max(scroll_fet_temps, default=50)) + 5)
        # 全程图
        line3.set_data(timestamps, motor_temps)
        line4.set_data(timestamps, fet_temps)
        ax2.set_xlim(0, now_sec)
        ax2.set_ylim(min(min(motor_temps, default=0), min(fet_temps, default=0)) - 5,
                    max(max(motor_temps, default=50), max(fet_temps, default=50)) + 5)
        for ax in (ax1, ax2):
            ax.relim()
            ax.autoscale_view()
        plt.tight_layout()
        plt.pause(1)
