import odrive  # 导入 ODrive 库
import numpy as np  # 导入 NumPy 库
import time  # 导入时间库
from odrive.utils import dump_errors  # 导入 dump_errors 函数

def initialize_odrive():
    """初始化 ODrive 设备并清除错误"""
    odrv0 = odrive.find_any()
    dump_errors(odrv0, True)  # 打印整体错误状态
    odrv0.clear_errors()  # 清除任何现有错误
    odrv0.axis0.encoder.set_linear_count(0)  # 将当前位置设置为 0
    print("当前位置已设置为 0")
    return odrv0

def collect_data(odrv0, target_position):
    """采集电机电流和编码器位置数据"""
    data = []
    odrv0.axis0.requested_state = odrive.enums.AXIS_STATE_CLOSED_LOOP_CONTROL  # 设置电机进入闭环控制模式
    odrv0.axis0.controller.input_pos = target_position  # 设置目标位置

    start_time = time.time()
    while odrv0.axis0.encoder.pos_estimate < target_position:
        current_time = time.time()
        elapsed_time = current_time - start_time

        # 采集时间、位置、速度、力矩、驱动器温度和电机温度
        iq_measured = odrv0.axis0.motor.current_control.Iq_measured
        pos_estimate = odrv0.axis0.encoder.pos_estimate
        vel_estimate = odrv0.axis0.encoder.vel_estimate  # 采集速度
        torque_estimate = odrv0.axis0.motor.current_control.Iq_measured * odrv0.axis0.motor.config.torque_constant  # 计算力矩
        driver_temp = getattr(odrv0.axis0, 'fet_thermistor', None)
        driver_temp = driver_temp.temperature if driver_temp else float('nan')  # 如果属性不存在，设置为 NaN
        motor_temp = getattr(odrv0.axis0, 'motor_thermistor', None)
        if motor_temp:  # 检查 motor_thermistor 是否存在
            motor_temp = motor_temp.temperature
        else:
            motor_temp = float('nan')  # 如果不存在，设置为 NaN
        data.append([elapsed_time, pos_estimate, vel_estimate, torque_estimate, driver_temp, motor_temp])
    return data

def save_data_to_csv(data, file_path):
    """将采集的数据保存到 CSV 文件"""
    np.savetxt(
        file_path,  # 文件保存路径
        data,  # 要保存的数据
        delimiter=',',  # 数据分隔符为逗号
        header="Time (s),Pos_estimate,Vel_estimate (counts/s),Torque_estimate (Nm),Driver_temp (°C),Motor_temp (°C)"  # 更新表头
    )
    print(f"数据采集完成，已保存到 {file_path}")

# 主程序
if __name__ == "__main__":
    odrv0 = initialize_odrive()
    target_position = 80  # 设置目标位置为 8 圈
    data = collect_data(odrv0, target_position)
    save_data_to_csv(data, "C:\\Users\\Administrator\\Desktop\\odrvie_python_test - G60\\G60_demo\\captured_data.csv")