import odrive  # 导入 ODrive 库
import time  # 导入时间库
from odrive.enums import AXIS_STATE_MOTOR_CALIBRATION, AXIS_STATE_ENCODER_OFFSET_CALIBRATION, AXIS_STATE_IDLE, CONTROL_MODE_VELOCITY_CONTROL, INPUT_MODE_VEL_RAMP, AXIS_STATE_CLOSED_LOOP_CONTROL  # 导入所需的枚举值
from odrive.utils import dump_errors  # 导入 dump_errors 函数

odrv0 = odrive.find_any()  # 查找并连接到任何可用的 ODrive 设备
odrv0.axis0.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL  # 设置控制模式为速度控制
odrv0.axis0.controller.config.input_mode = INPUT_MODE_VEL_RAMP  # 设置输入模式为速度斜坡
odrv0.axis0.controller.config.vel_ramp_rate = 5  # 设置速度斜坡的变化率
odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL  # 将轴状态设置为闭环控制

dump_errors(odrv0, True)  # 打印整体错误状态
odrv0.clear_errors()  # 清除任何现有错误
odrv0.axis0.encoder.set_linear_count(0)  # 将当前位置设置为零位

odrv0.axis0.controller.input_vel =1# 设置目标速度为 150
time.sleep(100) #待 5 秒以保持速度
odrv0.axis0.controller.input_vel = 0  # 将目标速度设置为 0（停止电机）
print("The motor has stopped.")  # 打印停止信息
# 代码结束