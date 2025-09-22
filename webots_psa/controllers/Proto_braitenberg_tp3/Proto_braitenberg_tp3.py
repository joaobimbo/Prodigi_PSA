from controller import Robot

# Inicializacao
robo = Robot()
passo = int(robo.getBasicTimeStep())
disp = {}

for i in range(robo.getNumberOfDevices()):
    d = robo.getDeviceByIndex(i)
    disp[d.getName()] = d
    try:
        d.enable(passo)
    except:
        pass

disp['left_motor'].setPosition(float('inf'))
disp['right_motor'].setPosition(float('inf'))

val_max = 8

# Funcoes auxiliares
def motor_esq(v):
    disp['left_motor'].setVelocity(v)

def motor_dir(v):
    disp['right_motor'].setVelocity(v)

def sen_luz_esq():
    val = disp['ls_left'].getValue()
    return min(val, val_max)  # limitar a 8

def sen_luz_dir():
    val = disp['ls_right'].getValue()
    return min(val, val_max)  # limitar a 8

# Ciclo principal
while robo.step(passo) != -1:
    e = sen_luz_esq()
    d = sen_luz_dir()
    #print(e)

    # === ESCOLHER UMA CONFIGURACAO ===
    # Configuracao direta e ganho positivo
    motor_esq(e)
    motor_dir(d)
    
    # Configuracao cruzada e ganho positivo
    # motor_esq(d)
    # motor_dir(e)
    
    # Configuracao direta e ganho negativo
    # motor_esq(val_max - e)
    # motor_dir(val_max - d)

    # Configuracao cruzada e ganho negativo
    # motor_esq(val_max - d)
    # motor_dir(val_max - e)
