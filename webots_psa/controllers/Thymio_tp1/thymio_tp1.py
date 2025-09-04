from controller import Robot, Motor
from ThymioPSA import *

thymio = Robot()
r=ThymioPSA(thymio)

# Funcoes auxiliares
def turn_right(r):
    #print('right')
    r.set_motors(5.0,0.0)

def turn_left(r):
    #print('left')
    r.set_motors(0.0,5.0)

def go_forward(r):
    #print('fwd')
    r.set_motors(5.0,5.0)

def go_back(r):
    #print('back')
    r.set_motors(-3.0,-3.0)

def get_line_sensor(r):
    return [r.get_sensor('prox.ground.0'),r.get_sensor('prox.ground.1')]

while r.running():
    d=get_line_sensor(r)
    #print(d)
    # Codigo segue-linha aqui