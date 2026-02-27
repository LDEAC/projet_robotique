from controller import Robot


# PARAMETRES

MAX_SPEED = 9.0
TH_DETECT = 500

STATE_GO = 0
STATE_STOP = 1


# FONCTIONS

def read_sensors(distanceSensors):
    vals = []
    for i in range(7):
        vals.append(distanceSensors[i].getValue())
    return vals

def max_front_value(vals):
    m = vals[0]
    for i in range(1, 5):
        if vals[i] > m:
            m = vals[i]
    return m

def obstacle_detected(vals):
    return max_front_value(vals) > TH_DETECT

def behavior_go():
    vL = 0.6 * MAX_SPEED
    vR = 0.6 * MAX_SPEED
    return vL, vR

def behavior_stop():
    vL = 0.0
    vR = 0.0
    return vL, vR

def set_motors(motor_left, motor_right, vL, vR):
    motor_left.setVelocity(vL)
    motor_right.setVelocity(vR)


# PROGRAMME PRINCIPAL

robot = Robot()
timestep = int(robot.getBasicTimeStep())

# Moteurs
motor_left = robot.getDevice('motor.left')
motor_right = robot.getDevice('motor.right')
motor_left.setPosition(float('inf'))
motor_right.setPosition(float('inf'))
motor_left.setVelocity(0.0)
motor_right.setVelocity(0.0)

# Capteurs
distanceSensors = []
for i in range(7):
    ds = robot.getDevice('prox.horizontal.' + str(i))
    ds.enable(timestep)
    distanceSensors.append(ds)

state = STATE_GO

while robot.step(timestep) != -1:

    vals = read_sensors(distanceSensors)
    seen = obstacle_detected(vals)

    #2 états
    if seen:
        state = STATE_STOP
    else:
        state = STATE_GO

    # Action
    if state == STATE_GO:
        vL, vR = behavior_go()
    else:
        vL, vR = behavior_stop()

    set_motors(motor_left, motor_right, vL, vR)