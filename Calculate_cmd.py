import numpy as np

def erpm_to_rad(vel):
    vel = vel / 21.0 / 64.0  # ERPM to RPM
    vel = vel * np.pi / 30.0  # RPM to rad/s
    return vel


def rad_to_erpm(vel):
    vel = vel * 30.0 / np.pi
    vel = vel * 21.0 * 64.0
    return vel

pos_max = 90
vel_max = erpm_to_rad(80000)
current_max = 20.0
Kp_max = 500.0
Kd_max = 5.0
torque_max = 144.0
accel_max = 30000

CAN_SET_DUTY = 0
CAN_SET_CURRENT = 1
CAN_SET_CURRENT_BRAKE = 2
CAN_SET_VELOCITY = 3
CAN_SET_POSITION = 4
CAN_SET_ORIGIN = 5
CAN_SET_POS_SPD = 6
CAN_MIT = 9


def calculate_ID(device_id, mode_id):
    if mode_id != CAN_MIT:
        can_id = np.bitwise_or(np.array(device_id).astype('uint8'),
                               np.left_shift(np.array(mode_id).astype('int32'), 8))
        return "ExtID:{:04X}    ".format(can_id)
    elif mode_id == CAN_MIT:
        can_id = np.array(0).astype('uint16') + np.array(device_id).astype('uint8')
        return "StdID:{:04X}    ".format(can_id)


def calculate_origin_cmd():
    return "00"


def calculate_current_cmd(I):
    cmd_value = []
    I = limit_value(I, current_max, -current_max)
    buffer_append_int32(cmd_value, np.array(1000.0 * I).astype('int32'))
    cmd = ""
    for i in range(len(cmd_value)):
        cmd = cmd + "{:02X} ".format(cmd_value[i])
    return cmd


def calculate_position_cmd(P):
    cmd_value = []
    P = limit_value(P, pos_max, -pos_max)
    buffer_append_int32(cmd_value, np.array(10000.0 * P).astype('int32'))
    cmd = ""
    for i in range(len(cmd_value)):
        cmd = cmd + "{:02X} ".format(cmd_value[i])
    return cmd


def calculate_velocity_cmd(V):
    cmd_value = []
    V = limit_value(V, vel_max, -vel_max)
    V = V * 30.0 / np.pi  # rad/s to rpm
    V = V * 21.0 * 64.0  # rpm to erpm
    buffer_append_int32(cmd_value, np.array(V).astype('int32'))
    cmd = ""
    for i in range(len(cmd_value)):
        cmd = cmd + "{:02X} ".format(cmd_value[i])
    return cmd


def calculate_p_and_s_cmd(P, V, A):
    cmd_value = []
    P = limit_value(P, pos_max, -pos_max)
    V = limit_value(V, vel_max, -vel_max)
    V = V * 30.0 / np.pi
    V = V * 21.0 * 64.0
    A = limit_value(A, accel_max, -accel_max)
    buffer_append_int32(cmd_value, np.array(P * 10000.0).astype('int32'))
    buffer_append_int16(cmd_value, np.array(V / 10.0).astype('int16'))
    buffer_append_int16(cmd_value, np.array(A / 10.0).astype('int16'))
    cmd = ""
    for i in range(len(cmd_value)):
        cmd = cmd + "{:02X} ".format(cmd_value[i])
    return cmd


def calculate_mit_cmd(P, V, T, Kp, Kb):
    pos = float_to_int(P, pos_max, -pos_max, 16)
    vel = float_to_int(V, vel_max, -vel_max, 12)
    kp = float_to_int(Kp, Kp_max, 0, 12)
    kd = float_to_int(Kb, Kd_max, 0, 12)
    torque = float_to_int(T, torque_max, -torque_max, 12)
    TxData = []
    TxData.append(np.right_shift(pos, 8))
    TxData.append(np.bitwise_and(pos, 0xff))
    TxData.append(np.right_shift(vel, 4))
    TxData.append(np.bitwise_or(
        np.left_shift(np.bitwise_and(vel, 0xf), 4),
        np.right_shift(kp, 8)
    ))
    TxData.append(np.bitwise_and(kp, 0xff))
    TxData.append(np.right_shift(kd, 4))
    TxData.append(np.bitwise_or(
        np.left_shift(np.bitwise_and(kd, 0xf), 4),
        np.right_shift(torque, 8)
    ))
    TxData.append(np.bitwise_and(torque, 0xff))
    cmd = ""
    for i in range(len(TxData)):
        cmd = cmd + "{:02X} ".format(TxData[i])
    return cmd


def buffer_append_int32(buffer, number):
    num = number.astype('int32')
    buffer.append(np.bitwise_and(np.right_shift(num, 24), 0xff))
    buffer.append(np.bitwise_and(np.right_shift(num, 16), 0xff))
    buffer.append(np.bitwise_and(np.right_shift(num, 8), 0xff))
    buffer.append(np.bitwise_and(num, 0xff))
    return buffer


def buffer_append_int16(buffer, number):
    num = number.astype('int16')
    buffer.append(np.bitwise_and(np.right_shift(num, 8), 0xff))
    buffer.append(np.bitwise_and(num, 0xff))


def float_to_int(v, v_max, v_min, bits):
    span = v_max - v_min
    v_ = max(min(v, v_max), v_min)
    return (int)((v_ - v_min) * ((float)((1 << bits) / span)))


def limit_value(v, v_max, v_min):
    v = max(v_min, min(v, v_max))
    return v


