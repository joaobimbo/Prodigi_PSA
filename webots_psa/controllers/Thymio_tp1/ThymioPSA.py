class ThymioPSA:
  def __init__(self,robot):
    self.robot=robot
    self.timestep = int(robot.getBasicTimeStep())

    self.devs={}
    print(robot.getNumberOfDevices())
    for i in range(robot.getNumberOfDevices()):
        print(i,robot.getDeviceByIndex(i).name)
        self.devs[robot.getDeviceByIndex(i).name]=robot.getDeviceByIndex(i)
        try:
            robot.getDeviceByIndex(i).enable(self.timestep)
        except Exception as e:
            pass
            #print(e)
            
    #set velocity control mode
    self.devs['motor.right'].setPosition(float('inf'))
    self.devs['motor.left'].setPosition(float('inf'))


  def set_motors(self,l,r):
    self.devs['motor.right'].setVelocity(r)
    self.devs['motor.left'].setVelocity(l)

  def running(self):
      return self.robot.step(self.timestep) != -1
      
  def get_sensor(self,name):
      try:
          return self.devs[name].getValue()
      except:
          pass
          
  def step_controller(self,N=100):
      for _ in range(N):
          self.robot.step()

