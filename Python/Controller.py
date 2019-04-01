import numpy as np
from math import cos, sin, pi, sqrt
from time import sleep

def calc_rw_angvec(av_target):
    print("calc_rw_angvec ::", av_target)

    izz = 40584.4155844
    # TODO
    x = 10
    y = 10
    z = 10

    rw1 = izz * (-0.5 * x * av_target[0] + 0.5774 * z * av_target[2])
    rw2 = izz * (-0.5 * x * av_target[0] - 0.5774 * y * av_target[1])
    rw3 = izz * (-0.5 * x * av_target[0] - 0.5774 * z * av_target[2])
    rw4 = izz * (-0.5 * x * av_target[0] + 0.5774 * y * av_target[1])

    rw_angvec = np.array([rw1, rw2, rw3, rw4])
    print(f"-> {rw_angvec}\n")
    return rw_angvec

def intert_to_body(a, r):
    print("intert_to_body ::", a, r)

    itb = np.array([
            cos(r[1]) * cos(r[2]) * a[0] + \
            cos(r[1]) * sin(r[2]) * a[1] - \
            sin(r[1]) * a[2],

            (sin(r[0]) * sin(r[1]) * cos(r[2]) - cos(r[0]) * sin(r[2])) * a[0] +\
            (sin(r[0]) * sin(r[1]) * sin(r[2]) + cos(r[0]) * cos(r[2])) * a[1] +\
            sin(r[0]) * cos(r[1]) * a[2],

            (cos(r[0]) * sin(r[1]) * cos(r[2]) + sin(r[0]) * sin(r[2])) * a[0] +\
            (cos(r[0]) * sin(r[1]) * sin(r[2]) - sin(r[0]) * cos(r[2])) * a[1] +\
            cos(r[0]) * cos(r[1]) * a[2]
            ])
    print(f"-> {itb}\n")
    return itb

def get_sat_Oinertial(rotation):
    print("get_sat_Oinertial ::", rotation)

    Oinertial = np.array([cos(rotation[1]) * cos(rotation[2]),
                         cos(rotation[1]) * sin(rotation[2]),
                         -sin(rotation[1])])
    print(f"-> {Oinertial}\n")
    return Oinertial

def vector_angle(a, b):
    print("vector_angle ::", a, b)

    mag_a = np.linalg.norm(a)
    mag_b = np.linalg.norm(b)
    dot = a @ b

    vec_ang = dot / mag_a / mag_b;
    print(f"-> {vec_ang}\n")
    return vec_ang

def do_slew(angle, spin_u):
    print("do_slew ::", angle, spin_u)

    cur_time = last_time = init_time = 0
    last_rww = rw_scw = np.array([0,0,0,0])
    last_satw = satw_IMU = satw = np.array([0,0,0])
    overshoot = False

    # TODO
    q = np.array([1,1,1])

    izz = 0.00002464
    kp = np.sqrt(spin_u[0] / q[0] * pi / angle / izz)
    wmax_sat = np.array([2 * izz * kp * angle / pi * q[i] for i in range(3)])

    while ((cur_time - init_time) < 2 * kp * angle):
        iteration = desired_wmag = 0

        desired_w = [0.5 * wmax_sat[i] *\
                (1 + sin(2 * pi * cur_time / (2 * kp * angle) - pi / 2))\
                for i in range(3)]

        desired_wmag += desired_wmag ** 2
        desired_wmag = sqrt(desired_wmag)

        if iteration == 0:
            init_time = cur_time
            iteration += 1

        rw_werr = [last_rww[i] - rw_scw[i] for i in range(4)]
        for werr in rw_werr:
            if werr > 157:
                print("Mechanical failure :: error > 1500rpm")
                exit(1)

        if desired_wmag > 0.008726:
            for i in range(3):
                satw_err[i] = desired_w[i] - 0.008726 * spin_u[i]
                desired_w[i] = 0.008727 * spin_u[i]
                satw_errmag += satw_err[i] ** 2

            satw_errmag = sqrt(satw_errmag)
            angle_err += 0.5 * (cur_time - last_time) * (satw_errmag - last_errmag)

            overshoot = True
            last_errmag = satw_errmag
        elif overshoot:
            continue

        desired_w = [desired_w[i] + last_satw[i] - satw_IMU[i] for i in range(3)]
        rw_w = calc_rw_angvec(desired_w)

        last_time = cur_time
        last_rww = rw_w
        last_satw = satw

        sleep(1)

    overshoot = False
    angle_err = 0

def bp(x):
    print(x)
    exit(1)

if __name__ == "__main__":
    cur_oerr_mag = 100

    # TODO
    light_p = [1,1,1]
    sat_p = [10,10,10]
    rotation = [1,1,1]

    while cur_oerr_mag > 0.01745:
        cur_oerr_mag = 0

        desired_o = np.array([light_p[i] - sat_p[i] for i in range(3)])
        current_o = get_sat_Oinertial(rotation)

        spin_vector = np.cross(current_o, desired_o)
        spin_vector_mag = np.linalg.norm(spin_vector)
        spin_u_inert = spin_vector / spin_vector_mag
        spin_u = intert_to_body(spin_u_inert, rotation)
        angle = vector_angle(current_o, desired_o)

        do_slew(angle, spin_u)

    cur_time = init_time = 0

    # TODO
    vector = np.array([0,0,0])

    while ((cur_time - init_time) < 10):
        current_o = np.array([1,0,0])
        spin_vector = np.cross(current_o, vector)
        spin_vector_mag = np.linalg.norm(spin_vector)
        spin_u = spin_vector / spin_vector_mag
        angle = vector_angle(current_o, vector)

        do_slew(angle, spin_u)
