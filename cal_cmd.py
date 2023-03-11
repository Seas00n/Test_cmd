import numpy as np
pos_max = 12.5
pos_min = -12.5
vel_max = 8.00
vel_min = -8.00
T_max = 144
T_min = -144
Kp_max = 500
Kp_min = 0
Kd_max = 5
Kd_min = 0



def float_to_int(v, v_max, v_min,bits):
    span = v_max - v_min
    v_ = max(min(v,v_max),v_min)
    return (int)((v_-v_min)*((float)((1<<bits)/span)))

def pack_cmd(pos,vel,torque,kp,kd):
    pos = float_to_int(pos,pos_max,pos_min,16)
    vel = float_to_int(vel,vel_max,vel_min,12)
    kp = float_to_int(kp,Kp_max,Kp_min,12)
    kd = float_to_int(kd,Kd_max,Kd_min,12)
    torque = float_to_int(torque,T_max,T_min,12)
    TxData = []
    TxData.append(np.right_shift(pos,8))
    TxData.append(np.bitwise_and(pos,0xff))
    TxData.append(np.right_shift(vel,4))
    TxData.append(np.bitwise_or(
        np.left_shift(np.bitwise_and(vel,0xf),4),
        np.right_shift(kp,8)
    ))
    TxData.append(np.bitwise_and(kp,0xff))
    TxData.append(np.right_shift(kd,4))
    TxData.append(np.bitwise_or(
        np.left_shift(np.bitwise_and(kd,0xf),4),
        np.right_shift(torque,8)
    ))
    TxData.append(np.bitwise_and(torque,0xff))
    return TxData


if __name__=='__main__':
    Position = 0.00
    Velocity = 0.00
    Torque = 0.00
    Kp = 0.00
    Kd = 0.0
    TxData = pack_cmd(Position,Velocity,Torque,Kp,Kd)
    print('---------------\n\n')
    print('{:02X} {:02X} {:02X} {:02X} {:02X} {:02X} {:02X} {:02X}'.format(
        TxData[0],TxData[1],TxData[2],TxData[3],TxData[4],TxData[5],TxData[6],TxData[7]))
    print('\n\n --------------')