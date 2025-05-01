import odrive
import time
from odrive.utils import dump_errors  # 正确导入 dump_errors 函数



# 查找连接的 ODrive 设备
odrv0 = odrive.find_any()

# 配置控制模式为速度控制
odrv0.axis0.controller.config.control_mode = 2  # 2 表示 VELOCITY_CONTROL

# 配置输入模式为速度斜坡
odrv0.axis0.controller.config.input_mode = 1  # 1 表示 VEL_RAMP

# 设置速度斜坡速率
odrv0.axis0.controller.config.vel_ramp_rate = 5

# 设置轴的状态为闭环控制
odrv0.axis0.requested_state = 8  # 8 表示 CLOSED_LOOP_CONTROL
time.sleep(0.1)  # 等待状态切换完成

# 检查状态是否成功切换
if odrv0.axis0.current_state != 8:
    print("Failed to switch to CLOSED_LOOP_CONTROL. Please check configuration or hardware.")
    dump_errors(odrv0, True)
    exit()

# 设置目标速度
odrv0.axis0.controller.input_vel = 15

# 打印错误信息（如果有）
dump_errors(odrv0, True)  # 使用 dump_errors 打印设备错误信息

# 设置控制模式为位置控制
odrv0.axis0.controller.config.control_mode = 3  # 3 表示 POSITION_CONTROL

# 获取当前位置并设置为目标位置
current_position = odrv0.axis0.encoder.pos_estimate
odrv0.axis0.controller.input_pos = current_position


# 等待 5 秒
time.sleep(5)

# 停止电机
odrv0.axis0.controller.input_vel = 0
