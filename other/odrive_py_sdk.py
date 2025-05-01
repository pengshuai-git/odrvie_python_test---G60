import odrive
from odrive.utils import dump_errors  # 修复导入错误
import time

# 查找连接的 ODrive 设备
odrv0 = odrive.find_any()

# 检查直流母线电压
if (odrv0.vbus_voltage < 20):  # 假设 20V 是最低安全电压
    print(f"警告: 直流母线电压过低 ({odrv0.vbus_voltage}V)，请检查电源！")
else:
    print(f"直流母线电压正常: {odrv0.vbus_voltage}V")

# 配置控制模式为速度控制
odrv0.axis0.controller.config.control_mode = 2  # 2 表示 VELOCITY_CONTROL

# 配置输入模式为速度斜坡
odrv0.axis0.controller.config.input_mode = 1  # 1 表示 VEL_RAMP

# 设置速度斜坡速率
odrv0.axis0.controller.config.vel_ramp_rate = 5

# 设置最大速度限制
odrv0.axis0.controller.config.vel_limit = 150  # 设置最大速度为 2000 counts/s
print(f"最大速度限制已设置为: {odrv0.axis0.controller.config.vel_limit} counts/s")

# 设置电机的最大电流限制
odrv0.axis0.motor.config.current_lim = 10  # 设置最大电流限制为 10A
print(f"电机最大电流限制已设置为: {odrv0.axis0.motor.config.current_lim}A")

# 清除错误并检查电机状态
print("清除错误...")
odrv0.axis0.error = 0
odrv0.axis0.motor.error = 0
odrv0.axis0.encoder.error = 0
odrv0.axis0.controller.error = 0
odrv0.axis1.error = 0
odrv0.axis1.motor.error = 0
odrv0.axis1.encoder.error = 0
odrv0.axis1.controller.error = 0
dump_errors(odrv0)  # 打印清除后的错误信息

# 设置轴的状态为闭环控制
odrv0.axis0.requested_state = 8  # 8 表示 CLOSED_LOOP_CONTROL

# 确保电机已进入闭环控制状态
if odrv0.axis0.current_state != 8:  # 8 表示 CLOSED_LOOP_CONTROL
    print(f"警告: 电机未进入闭环控制状态，当前状态为 {odrv0.axis0.current_state}")
    odrv0.axis0.requested_state = 8
    time.sleep(1)  # 等待状态切换

# 再次检查是否存在错误
print("检查电机状态...")
dump_errors(odrv0)
if odrv0.axis0.error != 0 or odrv0.axis0.motor.error != 0:
    print("错误: 电机存在问题，无法进入闭环控制状态。请检查硬件连接或配置！")
    exit(1)  # 退出程序以避免进一步操作

# 打印电机当前状态以便调试
print(f"电机当前状态: {odrv0.axis0.current_state}")

# 设置目标速度
odrv0.axis0.controller.input_vel = 150
time.sleep(2)
odrv0.axis0.controller.input_vel = -150

# 实时读取速度值
print("实时速度值:")
for _ in range(10):  # 循环 10 次，每次间隔 0.5 秒
    print(f"当前速度: {odrv0.axis0.encoder.vel_estimate:.2f} counts/s")
    time.sleep(0.5)

# 打印错误信息（如果有）
dump_errors(odrv0)  # 使用正确的导入函数

# 等待 5 秒
time.sleep(5)

# 停止电机
odrv0.axis0.controller.input_vel = 0