import numpy as np

pos_max = 12.5
pos_min = -12.5
vel_max = 8.00
vel_min = -8.00
I_max = 144
I_min = -144
Kp_max = 500
Kp_min = 0
Kd_max = 5
Kd_min = 0


def int_to_float(v, v_max, v_min, bits):
    span = v_max - v_min
    offset = v_min
    return (float)(v * span / ((float)((1 << bits) - 1)) + offset)


def unpack_cmd(RxData):
    id = int(RxData[0], 16)
    print('Motor ID:{}'.format(id))
    pos = np.bitwise_or(
        (np.left_shift(int(RxData[1], 16), 8)),
        int(RxData[2], 16)
    )
    pos = int_to_float(pos, pos_max, pos_min, 16)
    print('Position:{}'.format(pos))
    vel = np.bitwise_or(
        (np.left_shift(int(RxData[3], 16), 4)),
        (np.right_shift(int(RxData[4], 16), 4))
    )
    vel = int_to_float(vel, vel_max, vel_min, 12)
    print('Velocity:{}'.format(vel))
    current = np.bitwise_or(
        (np.left_shift(np.bitwise_and(int(RxData[4], 16), 0xf), 8)),
        (int(RxData[5], 16))
    )
    current = int_to_float(current, I_max, I_min, 12)
    print('Current:{}'.format(current))
    temperature = int(RxData[6], 16)
    temperature -= 40
    print('Temperature:{}'.format(temperature))
    status = int(RxData[7], 16)
    if status != 0:
        print('Error')
    else:
        print('Normal')


if __name__ == '__main__':
    RxData = '01 e3 04 7f f8 0d 00 00'.split()
    unpack_cmd(RxData)
