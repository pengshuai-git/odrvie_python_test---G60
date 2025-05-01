import numpy as np

def calculate_performance_metrics(time_list, feedback_list, setpoint_list, tol_5=0.05, tol_2=0.02):
    time_arr = np.array(time_list)
    feedback_arr = np.array(feedback_list)
    setpoint_arr = np.array(setpoint_list)
    # 自动检测阶跃段，取最大绝对值为稳态值
    unique_setpoints = np.unique(setpoint_arr)
    # 排除0，取最大绝对值
    nonzero_setpoints = unique_setpoints[np.abs(unique_setpoints) > 1e-6]
    if len(nonzero_setpoints) == 0:
        steady_value = 0
    else:
        steady_value = nonzero_setpoints[np.argmax(np.abs(nonzero_setpoints))]
    # 阶跃方向
    step_sign = np.sign(steady_value) if steady_value != 0 else 1
    # 检测阶跃起点
    setpoint_diff = np.diff(setpoint_arr)
    step_indices = np.where(np.abs(setpoint_diff) > 1e-6)[0]
    if len(step_indices) > 0:
        step_start_time = time_arr[step_indices[0]+1]  # 阶跃变化点的下一个采样点
    else:
        step_start_time = 0.0
    # 延迟时间 td（第一次达到50%稳态值，参考阶跃起点）
    td_idx = np.where(step_sign * feedback_arr >= 0.5 * np.abs(steady_value))[0]
    td = (time_arr[td_idx[0]] - step_start_time) if len(td_idx) > 0 else None
    # 上升时间 tr（10%->90%，参考阶跃起点）
    tr_10_idx = np.where(step_sign * feedback_arr >= 0.1 * np.abs(steady_value))[0]
    tr_90_idx = np.where(step_sign * feedback_arr >= 0.9 * np.abs(steady_value))[0]
    tr = (time_arr[tr_90_idx[0]] - time_arr[tr_10_idx[0]]) if (len(tr_10_idx) > 0 and len(tr_90_idx) > 0) else None
    # 峰值时间 tp（参考阶跃起点）
    if steady_value != 0:
        if step_sign > 0:
            peak_idx = np.argmax(feedback_arr)
        else:
            peak_idx = np.argmin(feedback_arr)
        tp = time_arr[peak_idx] - step_start_time
        # 最大超调量 Mp
        Mp = (feedback_arr[peak_idx] - steady_value) / np.abs(steady_value) * 100
    else:
        tp = None
        Mp = None
    # 调整时间 ts（±5%和±2%）
    def settle_time(tol):
        if steady_value == 0:
            return None
        lower = steady_value * (1 - tol)
        upper = steady_value * (1 + tol)
        for i in range(len(feedback_arr)-1, -1, -1):
            if not (lower <= feedback_arr[i] <= upper):
                return time_arr[i+1] if i+1 < len(time_arr) else None
        return time_arr[0]
    ts_5 = settle_time(tol_5)
    ts_2 = settle_time(tol_2)
    # 振荡次数 N（在ts_5内过稳态值的次数）
    if ts_5 is not None:
        idx_ts = np.where(time_arr <= ts_5)[0]
        feedback_in_ts = feedback_arr[idx_ts]
        cross = np.where(np.diff(np.sign(feedback_in_ts - steady_value)))[0]
        N = len(cross)
    else:
        N = None
    # 稳态误差：阶跃起点+2s到+5s区间的平均误差
    # 检测阶跃起点
    setpoint_diff = np.diff(setpoint_arr)
    step_indices = np.where(np.abs(setpoint_diff) > 1e-6)[0]
    if len(step_indices) > 0:
        step_start_time = time_arr[step_indices[0]+1]  # 阶跃变化点的下一个采样点
        idx_steady = np.where((time_arr >= step_start_time + 2.0) & (time_arr <= step_start_time + 5.0))[0]
        if len(idx_steady) > 0:
            steady_error = np.mean(setpoint_arr[idx_steady] - feedback_arr[idx_steady])
        else:
            steady_error = None
    else:
        steady_error = None
    return {
        'td': td,
        'tr': tr,
        'tp': tp,
        'Mp': Mp,
        'ts_5': ts_5,
        'ts_2': ts_2,
        'N': N,
        'error': steady_error
    }

# 测试代码
if __name__ == '__main__': 
    time_list = [0, 1, 2, 3, 4, 5, 6, 7]
    feedback_list = [0, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5]
    setpoint_list = [0, 1, 2, 3, 4, 5, 6, 7]
    metrics = calculate_performance_metrics(time_list, feedback_list, setpoint_list)
    print(metrics)