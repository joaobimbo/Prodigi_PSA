from controller import Robot, Motor
from ThymioPSA import *

# Criar instancia do robo
thymio = Robot()
robot = ThymioPSA(thymio)

# Funcoes auxiliares
def turn_right(robot):
    robot.set_motors(5.0, 0.0)

def turn_left(robot):
    robot.set_motors(0.0, 5.0)

def go_forward(robot):
    robot.set_motors(5.0, 5.0)

def go_back(robot):
    robot.set_motors(-5.0, -5.0)

def stop(robot):
    robot.set_motors(0.0, 0.0)

# ----- Exemplo de sensores -----
# Sensores frontais de proximidade
prox_left   = 'prox.horizontal.0'
prox_center = 'prox.horizontal.2'
prox_right  = 'prox.horizontal.4'
# Sensores frontais: 0 a 4 (esq -> dir)
# Sensores traseiros: 5 (esq) e 6 (dir)

# Ciclo principal
while robot.running():
    # Ler sensores
    #val_left   = robot.get_sensor(prox_left)
    #val_center = robot.get_sensor(prox_center)
    #val_right  = robot.get_sensor(prox_right)
    #print(val_center)

    # ---------- Exemplo de comportamento ----------
    #go_forward(robot)


    sp=2000
    sens=robot.get_sensor('prox.horizontal.4')
    vr=3.0-(sp-sens)*0.001
    vl=3.0
    robot.set_motors(vl,vr)
    print(f'v: {vl},{vr} {sens}')
    robot.step_controller(1)