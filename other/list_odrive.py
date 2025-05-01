
#PYTHON3.9.1
import odrive
import time
from odrive.enums import AXIS_STATE_FULL_CALIBRATION_SEQUENCE, AXIS_STATE_IDLE, ENCODER_MODE_INCREMENTAL,MOTOR_TYPE_HIGH_CURRENT,CONTROL_MODE_POSITION_CONTROL,INPUT_MODE_TRAP_TRAJ  # 导入所需的枚举常量

# 查找连接的 ODrive 设备
print("正在查找 ODrive 设备...")
odrv0 = odrive.find_any()  # 自动查找并连接到 ODrive 设备
print("ODrive 设备已连接。")
# 列出 ODrive 配置参数

def list_odrive_config(odrv):
    print("ODrive 配置参数:")
    print("主板配置:")
    print(f"  Brake Resistance: {odrv.config.brake_resistance}")
    print(f"  DC Bus Undervoltage Trip Level: {odrv.config.dc_bus_undervoltage_trip_level}")
    print(f"  DC Bus Overvoltage Trip Level: {odrv.config.dc_bus_overvoltage_trip_level}")
    print(f"  DC Max Positive Current: {odrv.config.dc_max_positive_current}")
    print(f"  DC Max Negative Current: {odrv.config.dc_max_negative_current}")
    print(f"  Max Regen Current: {odrv.config.max_regen_current}")
    
    print("\n电机配置:")
    print(f"  Pole Pairs: {odrv.axis0.motor.config.pole_pairs}")
    print(f"  Calibration Current: {odrv.axis0.motor.config.calibration_current}")
    print(f"  Resistance Calib Max Voltage: {odrv.axis0.motor.config.resistance_calib_max_voltage}")
    print(f"  Motor Type: {odrv.axis0.motor.config.motor_type}")
    print(f"  Current Limit: {odrv.axis0.motor.config.current_lim}")
    print(f"  Requested Current Range: {odrv.axis0.motor.config.requested_current_range}")
    
    print("\n编码器配置:")
    print(f"  Mode: {odrv.axis0.encoder.config.mode}")
    print(f"  CPR: {odrv.axis0.encoder.config.cpr}")
    print(f"  Bandwidth: {odrv.axis0.encoder.config.bandwidth}")
    
    print("\n控制器配置:")
    print(f"  Control Mode: {odrv.axis0.controller.config.control_mode}")
    print(f"  Velocity Limit: {odrv.axis0.controller.config.vel_limit}")
    print(f"  Position Gain: {odrv.axis0.controller.config.pos_gain}")
    print(f"  Velocity Gain: {odrv.axis0.controller.config.vel_gain}")
    print(f"  Velocity Integrator Gain: {odrv.axis0.controller.config.vel_integrator_gain}")
    print(f"  Input Mode: {odrv.axis0.controller.config.input_mode}")
    
    print("\n梯形轨迹配置:")
    print(f"  Velocity Limit: {odrv.axis0.trap_traj.config.vel_limit}")
    print(f"  Acceleration Limit: {odrv.axis0.trap_traj.config.accel_limit}")
    print(f"  Deceleration Limit: {odrv.axis0.trap_traj.config.decel_limit}")

# 调用函数列出配置
list_odrive_config(odrv0)