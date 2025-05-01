import odrive
import time
import matplotlib.pyplot as plt
from collections import deque
import threading

# 连接ODrive
drv = odrive.find_any()
time.sleep(1)

axis = drv.axis0
axis.controller.config.control_mode = 1  # CURRENT_CONTROL
#axis.requested_state = 8  # CLOSED_LOOP_CONTROL
time.sleep(0.5)

# 阶跃信号参数
current_low = -0  # 1A
current_high =-0.6 # 1.5A
period = 1000  # 1000ms
on_time = period * 0.5  # 50%占空比

t_data = deque(maxlen=100)
iq_measured_data = deque(maxlen=100)
iq_setpoint_data = deque(maxlen=100)
id_measured_data = deque(maxlen=100)
id_setpoint_data = deque(maxlen=100)

# 实时绘图线程
def realtime_plot():
    plt.ion()
    fig, ax = plt.subplots()
    l1, = ax.plot([], [], label='iq_measured')
    l2, = ax.plot([], [], label='iq_setpoint')
    l3, = ax.plot([], [], label='id_measured')
    l4, = ax.plot([], [], label='id_setpoint')
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    ax.set_xlabel('t (s)')
    ax.set_ylabel('Current (A)')
    ax.set_title('Step Current Test Real-time')
    while True:
        if len(t_data) > 0:
            l1.set_data(t_data, iq_measured_data)
            l2.set_data(t_data, iq_setpoint_data)
            l3.set_data(t_data, id_measured_data)
            l4.set_data(t_data, id_setpoint_data)
            ax.relim()
            ax.autoscale_view()
            plt.pause(0.01)
        else:
            plt.pause(0.1)

plot_thread = threading.Thread(target=realtime_plot, daemon=False)
plot_thread.start()

print('t(s), iq_measured, iq_setpoint, id_measured, id_setpoint')
start_time = time.time()
try:
    while True:
        t = time.time() - start_time
        # 阶跃信号生成
        phase = (t % period)
        if phase < on_time:
            axis.controller.input_torque = current_high  # 1.5A
        else:
            axis.controller.input_torque = current_low   # 1A
        iq_measured = axis.motor.current_control.Iq_measured
        iq_setpoint = axis.motor.current_control.Iq_setpoint
        id_measured = axis.motor.current_control.Id_measured
        id_setpoint = axis.motor.current_control.Id_setpoint
        print(f'{t:.2f}, {iq_measured:+.3f}, {iq_setpoint:+.3f}, {id_measured:+.3f}, {id_setpoint:+.3f}')
        t_data.append(t)
        iq_measured_data.append(iq_measured)
        iq_setpoint_data.append(iq_setpoint)
        id_measured_data.append(id_measured)
        id_setpoint_data.append(id_setpoint)
        time.sleep(0.01)# 10ms采样
except KeyboardInterrupt:
    print('测试结束，等待关闭图像窗口...')
    plot_thread.join()
