import odrive  # 导入 ODrive 库
import time  # 导入时间库
from odrive.enums import AXIS_STATE_CLOSED_LOOP_CONTROL, CONTROL_MODE_POSITION_CONTROL  # 导入所需的枚举值
from odrive.utils import dump_errors  # 导入 dump_errors 函数

def set_switch_simulation(axis, positions, stiffness, threshold):
    """
    设置电机的开关模拟功能。
    :param axis: 选择的轴 (axis0 或 axis1)
    :param positions: 档位位置列表
    :param stiffness: 档位的刚度（弹力系数）
    :param threshold: 档位切换的阈值范围
    """
    axis.controller.config.control_mode = CONTROL_MODE_POSITION_CONTROL  # 设置控制模式为位置控制
    axis.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL  # 设置为闭环控制模式
    axis.controller.config.pos_gain = stiffness  # 设置位置增益为刚度

    print("开关模拟已启动。按 Ctrl+C 退出程序。")
    current_target = None  # 当前目标档位位置
    try:
        while True:
            current_position = axis.encoder.pos_estimate  # 获取当前电机位置
            for i, target_position in enumerate(positions):
                if abs(current_position - target_position) < threshold:  # 判断是否接近某档位
                    if current_target != target_position:  # 仅在目标位置改变时更新
                        axis.controller.input_pos = target_position  # 设置目标位置为档位位置
                        current_target = target_position
                        print(f"已切换到第 {i + 1} 档，目标位置：{target_position}")
                    break
            time.sleep(0.1)  # 稍作延迟，避免过于频繁的检测
    except KeyboardInterrupt:
        print("程序已终止，停止电机。")
        axis.controller.input_pos = axis.encoder.pos_estimate  # 停止电机，保持当前位置

def main():
    print("正在查找 ODrive 设备...")
    odrv0 = odrive.find_any()  # 查找并连接到任何可用的 ODrive 设备
    print("ODrive 已连接！")
    dump_errors(odrv0, True)  # 打印整体错误状态
    odrv0.clear_errors()  # 清除任何现有错误
    odrv0.axis0.encoder.set_linear_count(0)  # 将当前位置设置为零位

    total_turns = 8  # 电机总共转 8 圈
    steps_per_turn = 16384  # 每圈对应的编码器计数
    num_positions = 5  # 分为 5 档
    positions = []  # 初始化档位位置列表
    for i in range(num_positions):
        positions.append(i * (total_turns / num_positions) * steps_per_turn)  # 计算每档位置

    stiffness = float(input("请输入卡顿感（刚度，建议范围 10.0 - 50.0）："))  # 用户输入刚度
    threshold = float(input("请输入档位切换阈值（建议范围 100 - 500）："))  # 用户输入档位切换的阈值范围

    set_switch_simulation(odrv0.axis0, positions, stiffness, threshold)  # 启动开关模拟

if __name__ == "__main__":
    main()
