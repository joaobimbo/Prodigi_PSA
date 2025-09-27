from controller import Robot

robot = Robot()

# Enable the motor (if not already enabled in PROTO)
motor = robot.getDevice("wall_motor")
motor.setPosition(float('inf'))  # Continuous rotation
motor.setVelocity(3)           # Speed in rad/s

while robot.step(32) != -1:
    pass  # Keep the simulation running
