import odrive
from odrive.enums import AXIS_STATE_CLOSED_LOOP_CONTROL
import time
import math

# 查找连接的 ODrive 设备
print("正在查找 ODrive 设备...")
odrv0 = odrive.find_any()  # 自动查找并连接到 ODrive 设备
print("ODrive 设备已连接。")

# 清除错误
print("清除错误...")
odrv0.axis0.error = 0  # 清除 axis0 的错误
odrv0.axis0.controller.error = 0  # 清除控制器的错误
odrv0.axis0.motor.error = 0  # 清除电机的错误
odrv0.axis0.encoder.error = 0  # 清除编码器的错误

# 进入闭环控制模式
print("进入闭环控制模式...")
odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
time.sleep(1)

# 设置正弦轨迹参数
amplitude = 1  # 正弦波的振幅（单位：圈）
frequency = 10  # 正弦波的频率（单位：Hz）
duration = 0.1    # 运动持续时间（单位：秒）
update_interval = 0.001  # 更新频率（单位：秒）

# 开始正弦轨迹运动
print("开始正弦轨迹运动...")
start_time = time.time()
while time.time() - start_time < duration:
    elapsed_time = time.time() - start_time
    # 计算正弦波目标位置
    target_position = amplitude * math.sin(2 * math.pi * frequency * elapsed_time)
    # 设置目标位置
    odrv0.axis0.controller.input_pos = target_position
    # 打印当前目标位置
    print(f"时间: {elapsed_time:.2f} 秒, 目标位置: {target_position:.4f} 圈")
    time.sleep(update_interval)  # 控制更新频率

# 停止运动
print("停止运动...")
odrv0.axis0.controller.input_pos = 0
time.sleep(1)

print("正弦轨迹运动完成。")