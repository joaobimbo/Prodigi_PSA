from controller import Robot
import math

robot = Robot()
timestep = int(robot.getBasicTimeStep())

motor = robot.getDevice("wall_motor")
motor.setVelocity(1.0)  # speed of rotation

# swing limits
left_limit = -math.radians(30)
right_limit = math.radians(30)

# start state
target = right_limit
motor.setPosition(target)

# every few seconds, flip the target
counter = 0
switch_interval = int(2000 / timestep)  # ~2 seconds

while robot.step(timestep) != -1:
    counter += 1
    if counter > switch_interval:
        target = left_limit if target == right_limit else right_limit
        motor.setPosition(target)
        counter = 0
