import odrive
import time
import matplotlib.pyplot as plt
from collections import deque
import threading

# 连接ODrive
drv = odrive.find_any()
time.sleep(1)

axis = drv.axis0
# 设定q轴电流为0（使用input_torque，适配新版ODrive）
axis.controller.input_torque = -1
axis.controller.config.control_mode = 1  # CURRENT_CONTROL
#axis.requested_state = 8  # CLOSED_LOOP_CONTROL
time.sleep(0.5)

# 实时绘图函数
def realtime_plot():
    plt.ion()
    fig, ax = plt.subplots()
    l1, = ax.plot([], [], label='iq_measured')
    l2, = ax.plot([], [], label='iq_setpoint')
    l3, = ax.plot([], [], label='id_measured')
    l4, = ax.plot([], [], label='id_setpoint')
    ax.legend()
    ax.set_xlabel('t (s)')
    ax.set_ylabel('Current (A)')
    ax.set_title('Current Loop Real-time')
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

# 启动绘图线程
t_data = deque(maxlen=100)
iq_measured_data = deque(maxlen=100)
iq_setpoint_data = deque(maxlen=100)
id_measured_data = deque(maxlen=100)
id_setpoint_data = deque(maxlen=100)
plot_thread = threading.Thread(target=realtime_plot, daemon=True)
plot_thread.start()

print('t(s), iq_measured, iq_setpoint, id_measured, id_setpoint')
start_time = time.time()
while True:
    t = time.time() - start_time
    iq_measured = drv.axis0.motor.current_control.Iq_measured
    iq_setpoint = drv.axis0.motor.current_control.Iq_setpoint
    id_measured = drv.axis0.motor.current_control.Id_measured
    id_setpoint = drv.axis0.motor.current_control.Id_setpoint
    print(f'{t:.0f}, {iq_measured:+.3f}, {iq_setpoint:+.3f}, {id_measured:+.3f}, {id_setpoint:+.3f}')
    t_data.append(t)
    iq_measured_data.append(iq_measured)
    iq_setpoint_data.append(iq_setpoint)
    id_measured_data.append(id_measured)
    id_setpoint_data.append(id_setpoint)
    time.sleep(0.1)