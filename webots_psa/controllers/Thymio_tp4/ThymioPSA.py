class ThymioPSA:
    def __init__(self, robot):
        self.robot = robot
        self.timestep = int(robot.getBasicTimeStep())
        self.devs = {}
        print(robot.getNumberOfDevices())
        for i in range(robot.getNumberOfDevices()):
            print(i, robot.getDeviceByIndex(i).name)
            self.devs[robot.getDeviceByIndex(i).name] = robot.getDeviceByIndex(i)
            try:
                robot.getDeviceByIndex(i).enable(self.timestep)
            except:
                pass

        self.devs['motor.right'].setPosition(float('inf'))
        self.devs['motor.left'].setPosition(float('inf'))

    def set_motors(self, l, r):
        self.devs['motor.right'].setVelocity(r)
        self.devs['motor.left'].setVelocity(l)

    def running(self):
        return self.robot.step(self.timestep) != -1

    def get_sensor(self, name):
        try:
            return self.devs[name].getValue()
        except:
            pass

    def step_controller(self, N=100):
        for _ in range(N):
            self.robot.step()

    def wait(self, seconds):
        steps = int(seconds * 1000 / self.timestep)
        for _ in range(steps):
            if self.robot.step(self.timestep) == -1:
                break

    def get_acc(self):
        return self.devs['acc'].getValues()

    def set_led_rgb(self, nome_led, r, g, b):
        color_int = (r << 16) | (g << 8) | b
        self.devs[f'leds.{nome_led}'].set(color_int)

    def set_led_prox(self, nome_led, valor):
        self.devs[f'leds.prox.{nome_led}'].set(int(valor))
