import os
import time
import odrive
from odrive.enums import AXIS_STATE_CLOSED_LOOP_CONTROL

# 切换到指定路径
os.chdir(r'F:\00_Odrive\odrvie_python_test - G60\Read_velocity')

# 连接odrive
print('正在查找odrive...')
odrv = odrive.find_any()
print('已连接odrive')

axis = odrv.axis0  # 假设使用axis0

# 进入速度模式
axis.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
axis.controller.config.control_mode = 2  # 2为速度模式

# 初始速度为0
set_rpm = 0
axis.controller.input_vel = set_rpm / 60.0  # 转为RPS
print('初始速度为0')

# 等待1秒
start_time = time.time()
while time.time() - start_time < 1:
    feedback_rpm = axis.encoder.vel_estimate * 60.0
    error = feedback_rpm - set_rpm
    print(f'[{feedback_rpm:+.2f}；{set_rpm:+.2f}；{error:+.2f}]')
    time.sleep(0.05)

# 设定速度为10RPM
set_rpm = 100
axis.controller.input_vel = set_rpm / 60.0
print('设定速度为10RPM')

# 5秒后停止
start_time = time.time()
while time.time() - start_time < 5:
    feedback_rpm = axis.encoder.vel_estimate * 60.0
    error = feedback_rpm - set_rpm
    print(f'[{feedback_rpm:+.2f}；{set_rpm:+.2f}；{error:+.2f}]')
    time.sleep(0.05)

# 停止
set_rpm = 0
axis.controller.input_vel = set_rpm / 60.0
print('停止')

# 再打印一段停止后的反馈
'''
for _ in range(20):
    feedback_rpm = axis.encoder.vel_estimate * 60.0
    error = feedback_rpm - set_rpm
    print(f'[{feedback_rpm:.2f}；{set_rpm:.2f}；{error:.2f}]')
    time.sleep(0.05)
'''