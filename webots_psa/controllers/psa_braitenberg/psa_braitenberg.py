from controller import Robot, Motor

robot=Robot()
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
devs['left_motor'].setPosition(float('inf'))
devs['right_motor'].setPosition(float('inf'))

devs['right_motor'].setVelocity(0.0)
devs['left_motor'].setVelocity(0.0)

def set_lvel(v):
    devs['left_motor'].setVelocity(v)

def set_rvel(v):
    devs['right_motor'].setVelocity(v)
    
def get_lsens():
    return devs['ls_left'].getValue()
    
def get_rsens():
    return devs['ls_right'].getValue()

while robot.step(timestep) != -1:
    ls = get_lsens() #obter o valor do sensor esquerdo
    rs = get_rsens() #obter o valor do sensor direito
    #print(ls,rs)
    set_lvel(rs)
    set_rvel(ls)
    

    
    
    
