from controller import Robot, Motor, Display
import math
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

path='plot.png'
ps=[]

def plot(ps,t=100):
    plt.figure(figsize=(5.12, 2.56), dpi=100)
    plt.plot(ps)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(path, dpi=100)
    plt.close()

    # Load & paste into Display (upper-left origin)
    tex = devs['display'].imageLoad(path)
    devs['display'].imagePaste(tex, 0, 0, False)
    devs['display'].imageDelete(tex)

    

robot=Robot()
d=Display('POSITION_ERROR_GRAPH')
timestep = int(robot.getBasicTimeStep())

devs={}
print(robot.getNumberOfDevices())
for i in range(robot.getNumberOfDevices()):
    print(i,'->',robot.getDeviceByIndex(i).name)
    devs[robot.getDeviceByIndex(i).name]=robot.getDeviceByIndex(i)
    try:
        robot.getDeviceByIndex(i).enable(timestep)
    except Exception as e:
        pass        
#set velocity control mode
devs['shoulder_motor'].setPosition(float('inf'))
devs['shoulder_motor'].setVelocity(0.0)



def set_torque(v):
    devs['shoulder_motor'].setTorque(v)
    
def get_pos():
    return devs['shoulder_sensor'].getValue()

e_prev=0
i_e=0
print(devs.keys())
while robot.step(timestep) != -1:
    p = get_pos() #obter o valor do sensor esquerdo
    ps.append(p)
    #if len(ps)>100:
    #    ps.pop(0)
    plot(ps)
        
    e=1-p
    de=(e-e_prev)
    i_e=i_e+e
    set_torque(e*50.0+0*de*50+5*i_e*0)

    e_prev=e

   