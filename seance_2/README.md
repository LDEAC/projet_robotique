# Convoi de robots – Simulation Webots

## 1. Organisation du projet

Le dossier de la simulation contient les éléments suivants :

- `Indecis_controller/`  
  Contrôleur du robot **indécis**.

- `Timide_controller/`  
  Contrôleur du robot **timide**.

- `thymio_exemple/`  
  Contrôleur du robot **anxieux** (robot leader du convoi).


Un fichier vidéo est également fourni.  
Il montre les différents comportements des robots ainsi que le fonctionnement des convoi en simulation.
# Projet Robotique – Séance 2

# 2. Présentation générale

Le projet comporte trois contrôleurs correspondant à trois robots distincts :

- Robot anxieux (leader du convoi)
- Robot timide
- Robot indécis

Chaque robot est piloté par :
- Deux moteurs différentiels (`motor.left`, `motor.right`)
- Sept capteurs de proximité (`prox.horizontal.0` à `prox.horizontal.6`)

---

## Organisation des convois

Deux configurations ont été étudiées :

- Convoi 1 : Anxieux – Indécis – Indécis  
- Convoi 2 : Anxieux – Timide – Timide  

La configuration retenue comme fonctionnelle est :

Anxieux –Indécis-Indécis

Dans toutes les configurations, le robot anxieux joue le rôle de leader.  
Il fixe la trajectoire suivie par les robots placés derrière lui.

---

# 3. Robot anxieux (Leader)

## Rôle dans le convoi

Le robot anxieux est placé en tête du convoi et détermine la trajectoire globale.

Un contrôle manuel via les flèches du clavier a été implémenté dans son contrôleur afin de pouvoir modifier dynamiquement sa direction pendant la simulation. Toute modification de sa trajectoire influence immédiatement le reste du convoi.

## Principe général

Le robot anxieux repose sur une machine à deux états :

- `STATE_SEARCH` : recherche d’un mur ou obstacle (tourne en continu à gauche)
- `STATE_FOLLOW` : suivi du mur à gauche

Si un obstacle est détecté à l’avant, le robot passe en mode FOLLOW.  
Si l’obstacle disparaît, il repasse en mode SEARCH.

## Logique des vitesses
Le calcul des vitesses repose sur une logique inspirée du modèle de Braitenberg :  
En mode FOLLOW, les vitesses sont déterminées à partir de moyennes pondérées des capteurs latéraux et frontaux.

La logique reste réactive :  
- si le mur est trop proche, la vitesse d’un côté diminue pour corriger la trajectoire,  
- si le mur s’éloigne, le robot se rapproche.



---

# 4. Robot timide

## Principe général

Le robot timide utilise une machine à deux états :

- `STATE_GO` : avance en ligne droite
- `STATE_STOP` : arrêt immédiat
 
Si un obstacle est détecté au-delà d’un seuil, le robot s’arrête immédiatement.  
Dès que l’obstacle disparaît, il repart tout droit.

## Logique des vitesses
La vitesse reste calculée selon une logique inspirée de Braitenberg :  
plus l’obstacle frontal est proche, plus la vitesse diminue.


---

# 5. Robot indécis

## Principe général

Le robot indécis adopte un comportement réactif inspiré du modèle de Braitenberg.

Dans cette logique  les capteurs sont directement couplés aux moteurs :  
plus un obstacle est proche d’un côté, plus la roue correspondante ralentit.

## Logique des vitesses

Les vitesses des roues sont calculées à partir de combinaisons pondérées des capteurs latéraux.

Cette structure provoque automatiquement :
- un ralentissement en présence d’obstacles,
- une correction de trajectoire lorsque la perception est asymétrique.



---

# 5. Conclusion

Deux configurations ont été testées :

- Anxieux – Indécis – Indécis  
- Anxieux – Timide – Timide  

La configuration fonctionnelle retenue est :

Anxieux – Indécis-Indécis

