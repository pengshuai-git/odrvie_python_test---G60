import odrive  # 导入 ODrive 库
import time  # 导入时间库
from odrive.enums import AXIS_STATE_CLOSED_LOOP_CONTROL, CONTROL_MODE_VELOCITY_CONTROL  # 导入所需的枚举值
from odrive.utils import dump_errors  # 导入 dump_errors 函数

def set_damping(axis, damping_coefficient):
    """
    设置电机的阻尼效果。
    :param axis: 选择的轴 (axis0 或 axis1)
    :param damping_coefficient: 阻尼系数
    """
    axis.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL  # 设置控制模式为速度控制
    axis.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL  # 设置为闭环控制模式
    axis.controller.input_vel = 0  # 初始速度为 0
    axis.controller.config.vel_gain = damping_coefficient  # 设置速度增益为阻尼系数

def main():
    print("正在查找 ODrive 设备...")
    odrv0 = odrive.find_any()  # 查找并连接到任何可用的 ODrive 设备
    print("ODrive 已连接！")
    dump_errors(odrv0, True)  # 打印整体错误状态
    odrv0.clear_errors()  # 清除任何现有错误
    odrv0.axis0.encoder.set_linear_count(0)  # 将当前位置设置为零位
    #print("请输入阻尼系数（建议范围 0.1 - 1.0）：")
    damping_coefficient = float(0.5) # 获取用户输入的阻尼系数damping_coefficient = float(input()) 
    set_damping(odrv0.axis0, damping_coefficient)  # 设置轴 0 的阻尼

    print("阻尼已设置。按 Ctrl+C 退出程序。")
    try:
        while True:
            time.sleep(1)  # 保持程序运行
    except KeyboardInterrupt:
        print("程序已终止，停止电机。")
        odrv0.axis0.controller.input_vel = 0  # 停止电机

if __name__ == "__main__":
    main()
