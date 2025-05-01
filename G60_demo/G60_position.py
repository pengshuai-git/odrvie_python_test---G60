import odrive  # 导入 ODrive 库，用于控制 ODrive 电机驱动器
import time  # 导入时间库，用于延时操作

odrv0 = odrive.find_any()  # 查找并连接到任意可用的 ODrive 设备
odrv0.axis0.controller.config.control_mode = odrive.utils.ControlMode.POSITION_CONTROL  # 设置控制模式为位置控制
odrv0.axis0.controller.config.input_mode = odrive.utils.InputMode.POS_FILTER  # 设置输入模式为位置过滤模式
odrv0.axis0.requested_state = odrive.utils.AxisState.CLOSED_LOOP_CONTROL  # 将轴的状态设置为闭环控制

# 设置当前位置为 0
odrv0.axis0.encoder.set_linear_count(0)

# 读取并打印编码器的 CPR 值
encoder_cpr = odrv0.axis0.encoder.config.cpr  # 获取编码器每转计数 (CPR) 的配置值
print(f"编码器每转计数 (CPR): {encoder_cpr}")  # 打印编码器的 CPR 值

# 运行正反转1圈
full_rotation = 16384  # 假设1圈对应的编码器计数为16384

odrv0.axis0.controller.input_pos = 8  # 设置目标位置为10（正转1圈）
time.sleep(5)  # 等待5秒以确保电机完成动作

odrv0.axis0.controller.input_pos = 0  # 设置目标位置为100（进一步移动）