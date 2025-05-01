import odrive  # 导入 ODrive 库，用于控制 ODrive 电机驱动器
import time  # 导入时间库，用于延时操作
from odrive.utils import dump_errors  # 导入 dump_errors 函数

odrv0 = odrive.find_any()  # 查找并连接到任意可用的 ODrive 设备
odrv0.axis0.controller.config.control_mode = odrive.utils.ControlMode.POSITION_CONTROL  # 设置控制模式为位置控制
odrv0.axis0.controller.config.input_mode = odrive.utils.InputMode.TRAP_TRAJ  # 设置输入模式为T形轨迹模式
odrv0.axis0.requested_state = odrive.utils.AxisState.CLOSED_LOOP_CONTROL  # 将轴的状态设置为闭环控制

dump_errors(odrv0, True)  # 打印整体错误状态
odrv0.clear_errors()  # 清除任何现有错误
odrv0.axis0.encoder.set_linear_count(0)  # 将当前位置设置为零位

# 设置T形轨迹工作模式下的梯形速度和加速度限制
odrv0.axis0.trap_traj.config.vel_limit =0.5# 设置梯形速度限制500.0
odrv0.axis0.trap_traj.config.accel_limit = 0.5# 设置梯形加速度限制400.0
odrv0.axis0.trap_traj.config.decel_limit =0.5# 设置梯形减速度限制400.0
time.sleep(0.5)  # 等待设置生效

# 运行正反转1圈
full_rotation = 8  #电机转8圈，整体转1圈
error=0.1  # 设置误差范围#增大误差可以提高运行速度
# 循环10次执行正反转1圈
for i in range(3):# 循环10次执行正反转1圈
    odrv0.axis0.controller.input_pos = full_rotation  # 设置目标位置为正转1圈
    print("正转1圈")  # 打印正转信息
    while abs(odrv0.axis0.encoder.pos_estimate - full_rotation) > error:  # 等待到达目标位置#增大误差可以提高运行速度
        time.sleep(0.05)
    
    odrv0.axis0.controller.input_pos = 0  # 设置目标位置为反转回零位
    print("反转1圈")  # 打印反转信息
    while abs(odrv0.axis0.encoder.pos_estimate) > error:  # 等待回到零位
        time.sleep(0.05)

print("The motor has stopped.")  # 打印停止信息

odrv0.axis0.requested_state = odrive.utils.AxisState.IDLE  # 将轴的状态设置为IDLE，退出位置模式