import os
import time
import threading
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import odrive
from odrive.enums import AXIS_STATE_CLOSED_LOOP_CONTROL
import matplotlib
import performance_metrics as pm
import csv
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文
matplotlib.rcParams['axes.unicode_minus'] = False    # 正常显示负号
# 切换到指定路径
os.chdir(r'F:\00_Odrive\odrvie_python_test - G60\Read_velocity')

# 采集数据的全局变量
vel_feedback = []
vel_setpoint = []
vel_error = []
time_list = []
collecting = True

# 采集线程

def collect_data(axis, setpoint_profile):
    global collecting
    t0 = time.time()
    idx = 0
    while collecting:
        now = time.time() - t0
        # 设定值随时间变化
        if idx < len(setpoint_profile) and now > setpoint_profile[idx][0]:
            axis.controller.input_vel = setpoint_profile[idx][1] / 60.0
            idx += 1
        feedback = axis.encoder.vel_estimate * 60.0 /7.75
        setpoint = axis.controller.input_vel * 60.0 /7.75
        error = feedback - setpoint
        time_list.append(now)
        vel_feedback.append(feedback)
        vel_setpoint.append(setpoint)
        vel_error.append(error)
        time.sleep(0.01)

if __name__ == '__main__':
    print('正在查找odrive...')
    odrv = odrive.find_any()
    print('已连接odrive')
    axis = odrv.axis0
    axis.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
    axis.controller.config.control_mode = 2  # 速度模式
    # 速度设定曲线：(时间点, 设定值)
    setpoint_profile = [
        (0, 0),      # 0s 速度0
        (1, 40*7.75),     # 1s 速度10RPM
        (7, 0)       # 6s 速度0RPM
    ]
    # 启动采集线程
    t_collect = threading.Thread(target=collect_data, args=(axis, setpoint_profile))
    t_collect.start()
    # 主线程绘图
    plt.ion()
    fig = plt.figure(figsize=(10, 4))
    gs = gridspec.GridSpec(1, 2, width_ratios=[2, 1])
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1])
    start_time = time.time()
    while time.time() - start_time < 7:
        ax1.clear()
        ax2.clear()
        ax1.plot(time_list, vel_feedback, label='反馈值')
        ax1.plot(time_list, vel_setpoint, label='设定值')
        ax1.set_title('速度反馈与设定')
        ax1.set_xlabel('时间(s)')
        ax1.set_ylabel('速度(RPM)')
        ax1.legend()
        ax2.plot(time_list, vel_error, label='误差', color='r')
        ax2.set_title('速度误差')
        ax2.set_xlabel('时间(s)')
        ax2.set_ylabel('误差(RPM)')
        plt.pause(0.005)
    collecting = False
    t_collect.join()
    plt.ioff()
    plt.show()
    print('采集与绘图结束')
    # 计算性能指标
    metrics = pm.calculate_performance_metrics(time_list, vel_feedback, vel_setpoint)
    # 增加safe_fmt函数，防止性能指标为None时报错，打印时更健壮。
    def safe_fmt(val, fmt, none_str='无'):
        return fmt.format(val) if val is not None else none_str

    print("动态与稳态性能指标：")
    print(f"延迟时间 td: {safe_fmt(metrics['td'], '{:.3f} s')}")
    print(f"上升时间 tr: {safe_fmt(metrics['tr'], '{:.3f} s')}")
    print(f"峰值时间 tp: {safe_fmt(metrics['tp'], '{:.3f} s')}")
    print(f"最大超调量 Mp: {safe_fmt(metrics['Mp'], '{:.2f} %')}")
    print(f"调整时间 ts(±5%): {safe_fmt(metrics['ts_5'], '{:.3f} s')}")
    print(f"调整时间 ts(±2%): {safe_fmt(metrics['ts_2'], '{:.3f} s')}")
    print(f"振荡次数 N: {metrics['N'] if metrics['N'] is not None else '无'}")
    print(f"稳态误差 error: {safe_fmt(metrics['error'], '{:.3f} RPM')}")
    # 保存图片和数据
    data_dir = os.path.join(os.getcwd(), 'data')
    os.makedirs(data_dir, exist_ok=True)
    # 保存图片
    fig.savefig(os.path.join(data_dir, 'velocity_plot.png'), dpi=300)
    # 保存数据到csv
    csv_path = os.path.join(data_dir, 'velocity_data.csv')
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['time', 'vel_feedback', 'vel_setpoint', 'vel_error'])
        for t, fb, sp, err in zip(time_list, vel_feedback, vel_setpoint, vel_error):
            writer.writerow([t, fb, sp, err])
    # 保存性能指标到txt
    txt_path = os.path.join(data_dir, 'step_performance.txt')
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(f"延迟时间 td: {safe_fmt(metrics['td'], '{:.3f} s')}\n")
        f.write(f"上升时间 tr: {safe_fmt(metrics['tr'], '{:.3f} s')}\n")
        f.write(f"峰值时间 tp: {safe_fmt(metrics['tp'], '{:.3f} s')}\n")
        f.write(f"最大超调量 Mp: {safe_fmt(metrics['Mp'], '{:.2f} %')}\n")
        f.write(f"调整时间 ts(±5%): {safe_fmt(metrics['ts_5'], '{:.3f} s')}\n")
        f.write(f"调整时间 ts(±2%): {safe_fmt(metrics['ts_2'], '{:.3f} s')}\n")
        f.write(f"振荡次数 N: {metrics['N'] if metrics['N'] is not None else '无'}\n")
        f.write(f"稳态误差 error: {safe_fmt(metrics['error'], '{:.3f} RPM')}\n")
    print(f'性能指标已保存到: {txt_path}')
    print(f'图片和数据已保存到: {data_dir}')

