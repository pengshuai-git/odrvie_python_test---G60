import odrive  # 导入 ODrive 库
import time  # 导入时间库
from odrive.enums import AXIS_STATE_CLOSED_LOOP_CONTROL, CONTROL_MODE_POSITION_CONTROL, CONTROL_MODE_TORQUE_CONTROL  # 导入所需的枚举值
from odrive.utils import dump_errors  # 导入 dump_errors 函数

def calculate_gravity_torque(mass, arm_length, gravity=9.81):
    """
    计算重力补偿所需的力矩。
    :param mass: 重物的质量（kg）
    :param arm_length: 力臂长度（m）
    :param gravity: 重力加速度，默认为 9.81 m/s^2
    :return: 所需的力矩值
    """
    return mass * gravity * arm_length

def detect_torque_change(axis, threshold=0.6):
    """
    检测力矩的突变，用于判断是否挂上重物。
    :param axis: 选择的轴 (axis0 或 axis1)
    :param threshold: 力矩突变的阈值
    :return: 检测到的反力矩值
    """
    print("等待挂重物，请挂上重物...")
    previous_torque = axis.motor.current_control.Iq_measured * axis.motor.config.torque_constant
    while True:
        current_torque = axis.motor.current_control.Iq_measured * axis.motor.config.torque_constant
        if abs(current_torque - previous_torque) > threshold:  # 检测力矩突变
            print(f"检测到力矩突变，当前力矩为：{current_torque:.4f} Nm")
            time.sleep(1)  # 稳定 1 秒
            return current_torque
        previous_torque = current_torque
        time.sleep(0.1)

def set_gravity_compensation(axis, torque):
    """
    设置电机的重力补偿效果。
    :param axis: 选择的轴 (axis0 或 axis1)
    :param torque: 重力补偿所需的力矩值
    """
    axis.controller.config.control_mode = CONTROL_MODE_TORQUE_CONTROL  # 设置控制模式为力矩控制
    axis.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL  # 设置为闭环控制模式
    axis.controller.input_torque = torque  # 设置补偿力矩

def main():
    print("正在查找 ODrive 设备...")
    odrv0 = odrive.find_any()  # 查找并连接到任何可用的 ODrive 设备
    print("ODrive 已连接！")
    dump_errors(odrv0, True)  # 打印整体错误状态
    odrv0.clear_errors()  # 清除任何现有错误
    odrv0.axis0.encoder.set_linear_count(0)  # 将当前位置设置为零位

    # 进入位置模式以保持重物位置
    odrv0.axis0.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL
    odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
    odrv0.axis0.controller.input_pos = odrv0.axis0.encoder.pos_estimate  # 设置当前位置为目标位置

    # 检测力矩突变作为挂重物的切换点
    torque = detect_torque_change(odrv0.axis0)

    # 切换到力矩模式并设置重力补偿
    print("切换到重力补偿模式...")
    set_gravity_compensation(odrv0.axis0, torque)

    print("重力补偿已设置。按 Ctrl+C 退出程序。")
    try:
        while True:
            time.sleep(1)  # 保持程序运行
    except KeyboardInterrupt:
        print("程序已终止，停止电机。")
        odrv0.axis0.controller.input_torque = 0  # 停止电机，清除力矩

if __name__ == "__main__":
    main()
