import odrive  # 导入 ODrive 库
import time  # 导入时间库
from odrive.enums import AXIS_STATE_CLOSED_LOOP_CONTROL, CONTROL_MODE_POSITION_CONTROL  # 导入所需的枚举值
from odrive.utils import dump_errors  # 导入 dump_errors 函数

def set_spring(axis, spring_coefficient, target_position):
    """
    设置电机的弹簧效果。
    :param axis: 选择的轴 (axis0 或 axis1)
    :param spring_coefficient: 弹力系数
    :param target_position: 弹簧的目标位置
    """
    axis.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL  # 设置控制模式为位置控制
    axis.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL  # 设置为闭环控制模式
    axis.controller.config.pos_gain = spring_coefficient  # 设置位置增益为弹力系数
    axis.controller.input_pos = target_position  # 设置目标位置

def main():
    print("正在查找 ODrive 设备...")
    odrv0 = odrive.find_any()  # 查找并连接到任何可用的 ODrive 设备
    print("ODrive 已连接！")
    dump_errors(odrv0, True)  # 打印整体错误状态
    odrv0.clear_errors()  # 清除任何现有错误
    odrv0.axis0.encoder.set_linear_count(0)  # 将当前位置设置为零位

    print("请输入弹力系数（建议范围 1.0 - 20.0）：")
    spring_coefficient = float(input())  # 获取用户输入的弹力系数
    print("请输入目标位置（单位：编码器计数）：")
    target_position = float(input())  # 获取用户输入的目标位置

    set_spring(odrv0.axis0, spring_coefficient, target_position)  # 设置轴 0 的弹簧效果

    print("弹簧效果已设置。按 Ctrl+C 退出程序。")
    try:
        while True:
            time.sleep(1)  # 保持程序运行
    except KeyboardInterrupt:
        print("程序已终止，停止电机。")
        odrv0.axis0.controller.input_pos = odrv0.axis0.encoder.pos_estimate  # 停止电机，保持当前位置

if __name__ == "__main__":
    main()
