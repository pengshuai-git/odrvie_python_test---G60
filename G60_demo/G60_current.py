import odrive  # 导入 ODrive 库，用于控制 ODrive 电机驱动器
import time  # 导入时间库，用于延时操作

odrv0 = odrive.find_any()  # 查找并连接到任意可用的 ODrive 设备
odrv0.axis0.controller.config.control_mode = odrive.utils.CONTROL_MODE_TORQUE_CONTROL   # 设置控制模式为力矩控制
odrv0.axis0.controller.config.input_mode = odrive.utils.INPUT_MODE_PASSTHROUGH # 设置输入模式为直通模式
odrv0.axis0.requested_state = odrive.utils.AxisState.CLOSED_LOOP_CONTROL  # 将轴的状态设置为闭环控制

# 设置当前位置为 0
odrv0.axis0.encoder.set_linear_count(0)

#电机控制测试：
odrv0.axis0.controller.input_torque = 0.1	#改变转矩大小，可以用尝试阻挡电机转动，体会转矩的改变
time.sleep(1)
odrv0.axis0.controller.input_torque = -0.1
time.sleep(1)
odrv0.axis0.controller.input_torque = 0.01	
time.sleep(1)
odrv0.axis0.controller.input_torque = 1
time.sleep(1)
odrv0.axis0.controller.input_torque = 0
print("电机转矩控制测试完成")
# 设置目标电流（单位：安培）
odrv0.axis0.controller.input_torque = 0
#电机电流和转矩估算,查看指令电机电流
#odrv0.axis0.motor.current_control.Iq_setpoint

#查看测量的电机电流
#odrv0.axis0.motor.current_control.Iq_measured

#根据已知的电机KV、测得的电机电流，可以用以下公式来估算电机转矩：
#Torque [N.m] = 8.27 * Current [A] / KV.

# 其中，8.27是一个常数，用于将电流转换为转矩，KV是电机的KV值（单位：RPM/V）。
# 计算转矩
Torque = 8.27 * 0.1 / 600  # 假设电机KV为600
print(f"Estimated Torque: {Torque} N.m")  # 打印估算的转矩值