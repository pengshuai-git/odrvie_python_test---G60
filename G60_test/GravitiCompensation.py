import odrive
from odrive.enums import (
    AXIS_ERROR_NONE,
    AXIS_STATE_CLOSED_LOOP_CONTROL,
    AXIS_STATE_IDLE
)
from odrive.enums import AXIS_STATE_CLOSED_LOOP_CONTROL, CONTROL_MODE_POSITION_CONTROL, CONTROL_MODE_TORQUE_CONTROL  # 导入所需的枚举值
import time
import math
import keyboard  # 需要安装：pip install keyboard

# 重力加速度常数 (m/s²)
GRAVITY = 9.81
# 负载质量 (kg)
LOAD_MASS = 5
# 力臂长度 (m)
ARM_LENGTH = 0.2  # 200mm转换为米
# 电机转矩常数 (Nm/A)
KT = 0.47
#减速比
gear_i = 7.75  # 减速比7.75:1
def find_odrive():
    """查找并连接到ODrive设备"""
    print("正在查找ODrive设备...")
    odrv = odrive.find_any()
    # 设置初始位置为 0
    odrv.axis0.encoder.set_linear_count(0)
    #print(f"已连接到ODrive: {odrv.serial_number}")
    return odrv

def setup_motor(odrv):
    """设置电机为电流控制模式"""
    # 选择电机轴（假设使用axis0）
    axis = odrv.axis0
    # 设置为电流控制模式
    axis.controller.config.control_mode = CONTROL_MODE_TORQUE_CONTROL  # 电流控制模式
    print("电机已设置为电流控制模式")
    
    return axis

def calculate_torque(angle_deg):
    """计算所需的力矩 (Nm)"""
    # 将角度从度转换为弧度
    angle_rad = math.radians(angle_deg)
    
    # 计算力矩公式：τ = m * g * l * sin(α)
    torque = LOAD_MASS * GRAVITY * ARM_LENGTH * math.sin(angle_rad)
    torque = torque / gear_i  # 考虑减速比
    return torque

def torque_to_current(torque):
    """将力矩转换为电流 (A)"""
    # 使用电机的转矩常数 (Nm/A)
    current = torque / KT
    return current

def clear_odrive_errors(odrv0):
    """检查并清除ODrive的错误"""
    # 检查错误
    if odrv0.axis0.error != AXIS_ERROR_NONE:
        print(f"检测到错误: {odrv0.axis0.error}")
        # 清除错误
        odrv0.axis0.error = AXIS_ERROR_NONE
        print("错误已清除")
    else:
        pass
        #print("没有检测到错误")

def main():
    # 查找并连接ODrive
    odrv = find_odrive()
    # 清除ODrive错误
    clear_odrive_errors(odrv)
    # 设置电机为电流控制模式
    axis = setup_motor(odrv)
    odrv.axis0.requested_state = AXIS_STATE_IDLE

    # 提示用户设置零位
    print("请手动将电机移动到零位，然后按 Enter 键继续...")
    input()  # 等待用户按下 Enter 键确认
    odrv.axis0.encoder.set_linear_count(0)  # 设置当前位置为零位
    print("零位已设置完成，程序开始运行。")

    # 初始化变量
    A_in = 0.0  # 用户输入的调整值
    A_step = 0.1  # 每次调整的步长
    motor_enabled = False  # 电机是否启用
    
    try:
        while True:
            # 清除ODrive错误
            
            clear_odrive_errors(odrv)
            # 获取当前角度 (假设从ODrive或传感器获取)
            # 这里用模拟值代替，实际使用时替换为真实数据
            #angle_deg = float(input("请输入当前角度 (度): "))
            # 获取当前角度 (从编码器读取实际数据)
            encoder_cpr = odrv.axis0.encoder.config.cpr  # 获取编码器每转计数
            encoder_cpr = gear_i   # 考虑减速比
            #print(f"编码器每转计数: {encoder_cpr}")
            pos_estimate = odrv.axis0.encoder.pos_estimate  # 获取当前位置（编码器计数）
            #print(f"当前位置: {pos_estimate:.2f}电机圈 ",end="")
            pos_gearbox_estimate= pos_estimate / gear_i  # 计算减速器输出位置
            #print(f"当前位置: {pos_gearbox_estimate:.2f}整机圈 ",end="")
            angle_deg = (pos_estimate / encoder_cpr) * 360.0  # 将编码器计数转换为角度
            #print(f"当前角度: {angle_deg:.2f} 度")
            
            # 按键控制逻辑
            if keyboard.is_pressed('up'):
                A_in += A_step
                print(f"A_in 增加: {A_in:.3f}")
                time.sleep(0.1)  # 防止按键抖动
            if keyboard.is_pressed('down'):
                A_in -= A_step
                print(f"A_in 减少: {A_in:.3f}")
                time.sleep(0.1)  # 防止按键抖动
            if keyboard.is_pressed('right'):
                motor_enabled = True
                odrv.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
                print("电机已启用")
                time.sleep(0.1)
            if keyboard.is_pressed('left'):
                motor_enabled = False
                odrv.axis0.requested_state = AXIS_STATE_IDLE
                print("电机已禁用")
                time.sleep(0.1)
            
            if motor_enabled:
                # 计算所需的力矩
                torque = calculate_torque(angle_deg)
                print(f"所需力矩: {torque:.2f} Nm", end="")
                # 设置电机力矩
                torque2=torque*4 #5KG is 4   0.8kg is 3.8
                axis.controller.input_torque = torque2
                print(f"力矩已设置为: {torque2:.2f} Nm")
            
            # 等待一段时间
            time.sleep(0.1)
    
    except KeyboardInterrupt:
        # 捕获Ctrl+C，安全停止电机
        axis.controller.current_setpoint = 0
        odrv.axis0.requested_state = AXIS_STATE_IDLE
        print("\n电机已停止")


if __name__ == "__main__":
    main()
    