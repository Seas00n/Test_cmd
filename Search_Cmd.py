import numpy as np


def unpack_cmd(cmd):
    cmd_value = str.split(cmd, " ")

    pos = np.bitwise_or(np.left_shift(int(cmd_value[0], 16), 8),
                        int(cmd_value[1], 16)).astype(np.int16)
    pos = float(pos * 0.1)

    vel = np.bitwise_or(np.left_shift(int(cmd_value[2], 16), 8),
                        int(cmd_value[3], 16)).astype(np.int16)
    vel = float(vel * 10.0)
    vel_erpm = vel
    vel = vel / 21.0 / 64.0  # ERPM to RPM
    vel = vel * np.pi / 30.0  # RPM to rad/s

    cur = np.bitwise_or(np.left_shift(int(cmd_value[4], 16), 8),
                        int(cmd_value[5], 16)).astype(np.int16)
    cur = float(cur * 0.01)

    temperature = np.array(int(cmd_value[6], 16)).astype(np.int16)
    error = np.array(int(cmd_value[7], 16)).astype(np.int16)
    info = "Pos:{},Vel:{},I:{},T:{}\n" \
           "Vel:{} rad/s, {} deg/s, {} erpm".format(pos, vel, cur, temperature,
                                                    vel, vel * 180.0 / np.pi, vel_erpm)
    if error == 0:
        return info
    elif error == 1:
        return "Over Temperature    " + info
    elif error == 2:
        return "Over Current    " + info
    elif error == 3:
        return "Over Voltage    " + info
    elif error == 4:
        return "Low Voltage     " + info
    elif error == 5:
        return "Encoder Error   " + info
    elif error == 6:
        return "Hardware Broken     " + info


def str_hex_to_int16(str):
    return np.array(int(str, 16)).astype(np.int16)
