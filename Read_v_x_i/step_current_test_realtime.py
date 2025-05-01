import odrive
import time
import matplotlib.pyplot as plt
from collections import deque
import threading
import matplotlib.gridspec as gridspec
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文
matplotlib.rcParams['axes.unicode_minus'] = False    # 正常显示负号

# 连接ODrive
drv = odrive.find_any()
time.sleep(1)

axis = drv.axis0
axis.controller.config.control_mode = 1  # CURRENT_CONTROL
axis.requested_state = 8  # CLOSED_LOOP_CONTROL
time.sleep(0.5)

# 阶跃信号参数
current_low = -0.6 # 1A
current_high = -1  # 1.5A
period = 200/1000  # 1000ms #设置1s #由于硬件采样限制，实际周期会更长
on_time = period * 0.5  # 50%占空比

t_data = deque(maxlen=2000) #队列长度
iq_measured_data = deque(maxlen=2000)
iq_setpoint_data = deque(maxlen=2000)
id_measured_data = deque(maxlen=2000)
id_setpoint_data = deque(maxlen=2000)
iq_error_data = deque(maxlen=2000)
id_error_data = deque(maxlen=2000)

# 采集线程
stop_flag = threading.Event()
def data_acquire():
    start_time = time.time()
    while not stop_flag.is_set():
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
        iq_error = iq_measured - iq_setpoint
        id_error = id_measured - id_setpoint
        t_data.append(t)
        iq_measured_data.append(iq_measured)
        iq_setpoint_data.append(iq_setpoint)
        id_measured_data.append(id_measured)
        id_setpoint_data.append(id_setpoint)
        iq_error_data.append(iq_error)
        id_error_data.append(id_error)
        print(f'{t:.2f}, {iq_measured:+.3f}, {iq_setpoint:+.3f}, {id_measured:+.3f}, {id_setpoint:+.3f}, iq_error={iq_error:+.3f}, id_error={id_error:+.3f}')
        time.sleep(0.001)

data_thread = threading.Thread(target=data_acquire, daemon=True)
data_thread.start()

# 主线程绘图
plt.ion()
fig = plt.figure(figsize=(14, 10))
gs = gridspec.GridSpec(3, 2, height_ratios=[1, 1, 1])
# 上面两个并排
ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
# 中间横跨两列
ax3 = fig.add_subplot(gs[1, :])
# 最下横跨两列
ax4 = fig.add_subplot(gs[2, :])
# iq/id全局
l1, = ax1.plot([], [], label='iq_measured')
l2, = ax1.plot([], [], label='iq_setpoint')
l3, = ax1.plot([], [], label='id_measured')
l4, = ax1.plot([], [], label='id_setpoint')
ax1.legend(loc='upper right', ncol=2)
ax1.set_ylabel('Current (A)')
ax1.set_title('iq/id 全局')
# iq/id局部放大
l1z, = ax2.plot([], [], label='iq_measured')
l2z, = ax2.plot([], [], label='iq_setpoint')
l3z, = ax2.plot([], [], label='id_measured')
l4z, = ax2.plot([], [], label='id_setpoint')
ax2.legend(loc='upper right', ncol=2)
ax2.set_ylabel('Current (A)')
ax2.set_title('iq/id 局部放大(3周期)')
# iq误差
l5, = ax3.plot([], [], label='iq_error')
ax3.legend(loc='upper right')
ax3.set_ylabel('iq_error (A)')
ax3.set_xlabel('t (s)')
ax3.set_title('iq_measured - iq_setpoint')
# id误差
l6, = ax4.plot([], [], label='id_error')
ax4.legend(loc='upper right')
ax4.set_ylabel('id_error (A)')
ax4.set_xlabel('t (s)')
ax4.set_title('id_measured - id_setpoint')

try:
    while True:
        min_len = min(len(t_data), len(iq_measured_data), len(iq_setpoint_data), len(id_measured_data), len(id_setpoint_data), len(iq_error_data), len(id_error_data))
        if min_len > 0:
            t_arr = list(t_data)[-min_len:]
            iqm_arr = list(iq_measured_data)[-min_len:]
            iqs_arr = list(iq_setpoint_data)[-min_len:]
            idm_arr = list(id_measured_data)[-min_len:]
            ids_arr = list(id_setpoint_data)[-min_len:]
            iqe_arr = list(iq_error_data)[-min_len:]
            ide_arr = list(id_error_data)[-min_len:]
            # 全局
            l1.set_data(t_arr, iqm_arr)
            l2.set_data(t_arr, iqs_arr)
            l3.set_data(t_arr, idm_arr)
            l4.set_data(t_arr, ids_arr)
            ax1.relim(); ax1.autoscale_view()
            # 局部放大（3周期）
            tmax = t_arr[-1]
            tmin = max(0, tmax - 3*period)
            idx = [i for i, tt in enumerate(t_arr) if tt >= tmin]
            t_zoom = [t_arr[i] for i in idx]
            iqm_zoom = [iqm_arr[i] for i in idx]
            iqs_zoom = [iqs_arr[i] for i in idx]
            idm_zoom = [idm_arr[i] for i in idx]
            ids_zoom = [ids_arr[i] for i in idx]
            l1z.set_data(t_zoom, iqm_zoom)
            l2z.set_data(t_zoom, iqs_zoom)
            l3z.set_data(t_zoom, idm_zoom)
            l4z.set_data(t_zoom, ids_zoom)
            ax2.set_xlim(tmin, tmax)
            ax2.relim(); ax2.autoscale_view()
            # iq误差
            l5.set_data(t_arr, iqe_arr)
            ax3.relim(); ax3.autoscale_view()
            # id误差
            l6.set_data(t_arr, ide_arr)
            ax4.relim(); ax4.autoscale_view()
        plt.pause(0.02)
except KeyboardInterrupt:
    print('测试结束，关闭窗口...')
    stop_flag.set()
    data_thread.join()
    plt.ioff(); plt.show()
except Exception as e:
    print(f'主线程异常: {e}')
    stop_flag.set()
    data_thread.join()
    plt.ioff(); plt.show()
