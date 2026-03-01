from controller import Robot

# =========================
# PARAMETRES
# =========================
MAX_SPEED = 6.0

# Plus grand => freine moins (v reste plus proche de MAX_SPEED)
SEUIL_CAPTEURS = 3500.0

# Seuil d'arrêt (sur la moyenne frontale pondérée)
TH_STOP = 1200.0

STATE_GO = 0
STATE_STOP = 1


# =========================
# FONCTIONS
# =========================
def read_sensors(distanceSensors):
    vals = []
    for i in range(7):
        vals.append(distanceSensors[i].getValue())
    return vals

def moy_front(vals):
    # moyenne pondérée frontale (0..4), poids fort au centre
    return (vals[0] + 5*vals[1] + 30*vals[2] + 5*vals[3] + vals[4]) / 42.0

def behavior_go(vals):
    mf = moy_front(vals)

    # vitesse proportionnelle (même logique que ton indécis)
    v = MAX_SPEED - mf * (MAX_SPEED / SEUIL_CAPTEURS)

    # bornes (évite vitesse négative / trop lente)
    if v < 0.25 * MAX_SPEED:
        v = 0.25 * MAX_SPEED
    if v > MAX_SPEED:
        v = MAX_SPEED

    return v, v

def behavior_stop():
    return 0.0, 0.0

def set_motors(motor_left, motor_right, vL, vR):
    motor_left.setVelocity(vL)
    motor_right.setVelocity(vR)


# =========================
# PROGRAMME PRINCIPAL
# =========================
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
    mf = moy_front(vals)

    # 2 états : GO / STOP (timide)
    if mf > TH_STOP:
        state = STATE_STOP
    else:
        state = STATE_GO

    # Action
    if state == STATE_GO:
        vL, vR = behavior_go(vals)
    else:
        vL, vR = behavior_stop()

    set_motors(motor_left, motor_right, vL, vR)