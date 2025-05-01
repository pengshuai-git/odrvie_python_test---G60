import odrive
import time

# 连接ODrive
drv = odrive.find_any()
time.sleep(1)

# 进入电流环模式前，先将q轴电流设定为0
axis = drv.axis0

axis.controller.config.control_mode = 1  # CURRENT_CONTROL
#axis.requested_state = 8  # CLOSED_LOOP_CONTROL
# 设定q轴电流为0（使用input_torque，适配新版ODrive）
axis.controller.input_torque = 0.4
time.sleep(0.5)

print('t(s), iq_measured, iq_setpoint, id_measured, id_setpoint')
start_time = time.time()
while True:
    t = time.time() - start_time
    iq_measured = drv.axis0.motor.current_control.Iq_measured
    iq_setpoint = drv.axis0.motor.current_control.Iq_setpoint
    id_measured = drv.axis0.motor.current_control.Id_measured
    id_setpoint = drv.axis0.motor.current_control.Id_setpoint
    print(f'{t:.0f}, {iq_measured:+.3f}, {iq_setpoint:+.3f}, {id_measured:+.3f}, {id_setpoint:+.3f}')
    time.sleep(1)
