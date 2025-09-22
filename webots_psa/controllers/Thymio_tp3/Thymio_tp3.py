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

# Ciclo principal
while robot.running():

    # ---------- Exemplo de comportamento ----------

    go_forward(robot)
