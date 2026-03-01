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

kb = robot.getKeyboard()
kb.enable(timestep)

# --- Capteurs ---
ds = []
for i in range(7):
    s = robot.getDevice('prox.horizontal.' + str(i))
    s.enable(timestep)
    ds.append(s)

MAX_SPEED = 9
D = 10# cm
SEUIL_CAPTEURS = max(500, min(4500, -397.62 * D + 4686.9))
SAT = 9.52

# --- Etats ---
ETAT_NORMAL = 0
ETAT_TOURNE = 1
ETAT_STOP = 2

etat = ETAT_NORMAL

while robot.step(timestep) != -1:

    # 1) Lecture capteurs 
    vals = [0.0] * 7
    for i in range(7):
        vals[i] = ds[i].getValue()

    # 2) Moyennes pondérées 
    moy_gauche = (vals[0] + 5*vals[1] + 30*vals[2]) / 36
    moy_droite = (30*vals[2] + 5*vals[3] + vals[4]) / 36

    # 3) Calcul vitesses proportionnelles
    speed_gauche = MAX_SPEED - moy_gauche * (MAX_SPEED / SEUIL_CAPTEURS)
    speed_droite = MAX_SPEED - moy_droite * (MAX_SPEED / SEUIL_CAPTEURS)

    # 4) Saturation
    if speed_gauche > SAT:
        speed_gauche = SAT
    elif speed_gauche < -SAT:
        speed_gauche = -SAT

    if speed_droite > SAT:
        speed_droite = SAT
    elif speed_droite < -SAT:
        speed_droite = -SAT

    # 5) état 
    if speed_gauche == 0 and speed_droite == 0:
        etat = ETAT_STOP
    elif speed_gauche <= 0 or speed_droite <= 0:
        etat = ETAT_TOURNE
    else:
        etat = ETAT_NORMAL

    # 6) Actions 
    if etat == ETAT_STOP:
        mL.setVelocity(0)
        mR.setVelocity(0)
    else:
        mL.setVelocity(speed_gauche)
        mR.setVelocity(speed_droite)
        
        