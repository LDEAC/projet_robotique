from controller import Robot

robot = Robot()
timestep = int(robot.getBasicTimeStep())

# --- Moteurs ---
mL = robot.getDevice('motor.left')
mR = robot.getDevice('motor.right')
mL.setPosition(float('inf'))
mR.setPosition(float('inf'))
mL.setVelocity(0.0)
mR.setVelocity(0.0)

# clavier 
kb = robot.getKeyboard()
kb.enable(timestep)

#  Capteurs 
ds = []
for i in range(7):
    s = robot.getDevice('prox.horizontal.' + str(i))
    s.enable(timestep)
    ds.append(s)

# 
# PARAMETRES "ANXIEUX"
# 
MAX_SPEED = 6.5
SAT = 6

SEUIL_CAPTEURS = 3500.0

LEFT_MIN = 700.0
LEFT_MAX = 1400.0

K_ANX = 2.0

TH_DETECT = 1000.0
TH_VERY_CLOSE = 2000.0

STATE_SEARCH = 0
STATE_FOLLOW = 1
state = STATE_SEARCH


while robot.step(timestep) != -1:

    # 1) Lecture capteurs
    vals = [0.0] * 7
    for i in range(7):
        vals[i] = ds[i].getValue()

    max_front = max(vals[0], vals[1], vals[2], vals[3], vals[4])
    seen = max_front > TH_DETECT

    # 2) Machine à états
    if state == STATE_SEARCH:
        if seen:
            state = STATE_FOLLOW
    else:
        if not seen:
            state = STATE_SEARCH

    # 3) Calcul vitesses
    if state == STATE_SEARCH:
        speed_gauche = 0.45 * MAX_SPEED
        speed_droite = 0.75 * MAX_SPEED

    else:
        moy_gauche = (vals[0] + 5*vals[1] + 30*vals[2]) / 36.0
        moy_droite = (30*vals[2] + 5*vals[3] + vals[4]) / 36.0

        speed_gauche = MAX_SPEED - moy_gauche * (MAX_SPEED / SEUIL_CAPTEURS)
        speed_droite = MAX_SPEED - moy_droite * (MAX_SPEED / SEUIL_CAPTEURS)

        left = vals[0]
        if vals[1] > left:
            left = vals[1]

        if left < LEFT_MIN:
            panic = (LEFT_MIN - left) / LEFT_MIN
        elif left > LEFT_MAX:
            panic = -(left - LEFT_MAX) / LEFT_MAX
        else:
            panic = 0.0

        speed_gauche -= K_ANX * panic
        speed_droite += K_ANX * panic

        if max_front > TH_VERY_CLOSE:
            speed_gauche = 0.30 * MAX_SPEED
            speed_droite = -0.30 * MAX_SPEED

    # 4) Saturation
    if speed_gauche > SAT:
        speed_gauche = SAT
    elif speed_gauche < -SAT:
        speed_gauche = -SAT

    if speed_droite > SAT:
        speed_droite = SAT
    elif speed_droite < -SAT:
        speed_droite = -SAT

    # 5) Application vitesses
    mL.setVelocity(speed_gauche)
    mR.setVelocity(speed_droite)

    
    # CONTROLE CLAVIER 
    
    key = kb.getKey()

    if key == kb.LEFT:
        mL.setVelocity(0.0)
        mR.setVelocity(MAX_SPEED)

    elif key == kb.RIGHT:
        mL.setVelocity(MAX_SPEED)
        mR.setVelocity(0.0)

    elif key == kb.UP:
        mL.setVelocity(MAX_SPEED)
        mR.setVelocity(MAX_SPEED)

    elif key == kb.DOWN:
        mL.setVelocity(-MAX_SPEED)
        mR.setVelocity(-MAX_SPEED)