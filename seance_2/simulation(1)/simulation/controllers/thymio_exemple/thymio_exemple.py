from controller import Robot


# PARAMETRES

MAX_MOTOR = 9.53
TH_DETECT = 1000
TH_VERY_CLOSE = 2000
NORM_MAX = 2000.0

FORWARD_STEPS = 15
forward_counter = 0

STATE_SEARCH = 0
STATE_FOLLOW = 1

# Cible de "mur à gauche" (
LEFT_TARGET = 0.35

# Gain de correction (
Kp = 0.9 * MAX_MOTOR

def limit_speed(v):
    if v > MAX_MOTOR:
        return MAX_MOTOR
    if v < -MAX_MOTOR:
        return -MAX_MOTOR
    return v

def read_sensors(distanceSensors):
    vals = []
    for i in range(7):
        vals.append(distanceSensors[i].getValue())
    return vals

def normalize(vals):
    s = []
    for i in range(7):
        x = vals[i] / NORM_MAX
        if x < 0.0:
            x = 0.0
        if x > 1.0:
            x = 1.0
        s.append(x)
    return s

def max_front_value(vals):
    m = vals[0]
    for i in range(1, 5):
        if vals[i] > m:
            m = vals[i]
    return m

def obstacle_detected(vals):
    return max_front_value(vals) > TH_DETECT

def behavior_search(forward_counter):
    # Avance un peu, puis tourne à gauche
    if forward_counter < FORWARD_STEPS:
        vL = 0.6 * MAX_MOTOR
        vR = 0.6 * MAX_MOTOR
        forward_counter += 1
    else:
        vL = 0.35 * MAX_MOTOR
        vR = 0.65 * MAX_MOTOR
    return vL, vR, forward_counter

def behavior_follow(vals, s):
    # Mesure "mur à gauche" avec capteurs 0 et 1
    left = s[0]
    if s[1] > left:
        left = s[1]

    front = s[2]
    max_front = max_front_value(vals)

    # Base avance
    base = 0.55 * MAX_MOTOR

    # Erreur : si left > target => trop collé => tourner à droite
    # turn > 0 => gauche ; turn < 0 => droite
    error = LEFT_TARGET - left
    turn = Kp * error

    # Sécurité si très proche en face : tourner à droite
    if (max_front > TH_VERY_CLOSE) or (front > 0.95):
        turn = -0.7 * MAX_MOTOR

    vL = base - turn
    vR = base + turn

    return vL, vR


# PROGRAMME PRINCIPAL

robot = Robot()
timestep = int(robot.getBasicTimeStep())

kb = robot.getKeyboard()
kb.enable(timestep)

motor_left = robot.getDevice('motor.left')
motor_right = robot.getDevice('motor.right')
motor_left.setPosition(float('inf'))
motor_right.setPosition(float('inf'))
motor_left.setVelocity(0.0)
motor_right.setVelocity(0.0)

distanceSensors = []
for i in range(7):
    ds = robot.getDevice('prox.horizontal.' + str(i))
    ds.enable(timestep)
    distanceSensors.append(ds)

state = STATE_SEARCH

while robot.step(timestep) != -1:

    vals = read_sensors(distanceSensors)
    s = normalize(vals)
    seen = obstacle_detected(vals)

    # Etats
    if state == STATE_SEARCH:
        if seen:
            state = STATE_FOLLOW
            forward_counter = 0
    elif state == STATE_FOLLOW:
        if not seen:
            state = STATE_SEARCH
            forward_counter = 0

   
    if state == STATE_SEARCH:
        vL, vR, forward_counter = behavior_search(forward_counter)
    else:
        vL, vR = behavior_follow(vals, s)

    # Limite moteur 
    vL = limit_speed(vL)
    vR = limit_speed(vR)

    motor_left.setVelocity(vL)
    motor_right.setVelocity(vR)
    print("----")
    # Clavier
    key = kb.getKey()
    if key == kb.LEFT:
        print("left")
        motor_left.setVelocity(0.0)
        motor_right.setVelocity(MAX_MOTOR)
    elif key == kb.RIGHT:
        print("reight")
        motor_left.setVelocity(MAX_MOTOR)
        motor_right.setVelocity(0.0)
    elif key==kb.UP:
        print("UP")
        motor_left.setVelocity(MAX_MOTOR)
        motor_right.setVelocity(MAX_MOTOR)
    elif key==kb.DOWN:
        print("DOWN")
        motor_left.setVelocity(-MAX_MOTOR)
        motor_right.setVelocity(-MAX_MOTOR)