from controller import Robot, Motor
from ThymioPSA import *
import matplotlib.pyplot as plt

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

# Preparar grafico em tempo real
plt.ion()
fig, ax = plt.subplots()
ax.set_title("Aceleracao (X,Y,Z)")
ax.set_xlabel("Amostras")
ax.set_ylabel("Leitura do sensor")

x_line, = ax.plot([], [], 'r-', label='X')
y_line, = ax.plot([], [], 'g-', label='Y')
z_line, = ax.plot([], [], 'b-', label='Z')
ax.legend()
plt.show()

acc_x = []
acc_y = []
acc_z = []

while robot.running():
    ax_, ay_, az_ = robot.get_acc()
    acc_x.append(ax_)
    acc_y.append(ay_)
    acc_z.append(az_)

    # manter apenas as 100 mais recentes
    if len(acc_x) > 100:
        acc_x.pop(0)
        acc_y.pop(0)
        acc_z.pop(0)

    x_line.set_xdata(range(len(acc_x)))
    x_line.set_ydata(acc_x)
    y_line.set_xdata(range(len(acc_y)))
    y_line.set_ydata(acc_y)
    z_line.set_xdata(range(len(acc_z)))
    z_line.set_ydata(acc_z)

    ax.relim()
    ax.autoscale_view()
    plt.pause(0.01)
    
    #---------- Exemplo de comportamento----------

    go_forward(robot)

    # Espera 0.1 segundos para limitar a taxa de execucao do ciclo,
    # evitando sobrecarga da simulacao devido aos graficos
    # (o ciclo pode ser muito exigente para o computador)    
    robot.wait(0.1)

 