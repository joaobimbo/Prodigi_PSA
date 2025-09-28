import matplotlib.pyplot as plt

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
        self.devs['motor.right'].setVelocity(0)
        self.devs['motor.left'].setVelocity(0)


    def set_motors(self, l, r):
        self.devs['motor.right'].setVelocity(r)
        self.devs['motor.left'].setVelocity(l)
        self.step_controller(1)

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
        

    def init_realtime_plot(self, labels, max_points=None):
        """
        Inicializa o grafico em tempo real.
        
        labels: lista de nomes das variaveis (ex: ['Erro','PID'])
        max_points: numero maximo de pontos a mostrar (None = todos)
        """
        plt.ion()  # modo interativo
        self.fig, self.ax = plt.subplots()
        self.ax.set_xlabel("Amostras")
        self.ax.set_ylabel("Valores")
        self.ax.set_title("Gráfico em tempo real")

        # Dicionario que guarda os dados e as linhas
        self.plot_data = {
            lbl: {"x": [], "y": [], "line": None} for lbl in labels
        }
        colors = ['r-', 'g-', 'b-', 'm-', 'y-', 'c-', 'k-']
        
        for lbl, color in zip(labels, colors):
            line, = self.ax.plot([], [], color, label=lbl)
            self.plot_data[lbl]["line"] = line
        
        self.ax.legend()
        self.max_points = max_points
        self.counter = 0  # numero de amostras
        plt.show()

    def update_realtime_plot(self, values):
        """
        Atualiza o grafico em tempo real.
        
        values: dicionario {label: valor} com os dados atuais
        """
        self.counter += 1

        for lbl, val in values.items():
            self.plot_data[lbl]["x"].append(self.counter)
            self.plot_data[lbl]["y"].append(val)

            # manter apenas os ultimos max_points se definido
            if self.max_points is not None and len(self.plot_data[lbl]["x"]) > self.max_points:
                self.plot_data[lbl]["x"] = self.plot_data[lbl]["x"][-self.max_points:]
                self.plot_data[lbl]["y"] = self.plot_data[lbl]["y"][-self.max_points:]

            # atualizar a linha do grafico
            self.plot_data[lbl]["line"].set_xdata(self.plot_data[lbl]["x"])
            self.plot_data[lbl]["line"].set_ydata(self.plot_data[lbl]["y"])

        self.ax.relim()
        self.ax.autoscale_view()
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

