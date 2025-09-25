from controller import Robot
from ThymioPSA import *

# Criar instância do robô
thymio = Robot()
robot = ThymioPSA(thymio)

robot.init_realtime_plot(["Erro", "SaidaPID"], max_points=100)  # mostra últimas 100 leituras

# Parâmetros PID (ajustar manualmente)
Kp = 0.02
Ki = 0.0
Kd = 0.001

# Configurações
val_alvo = 2500    # distância desejada à parede (valor do sensor)
erro_acumulado = 0
erro_anterior = 0

velocidade_base = 5.0  # velocidade média

while robot.running():
    # Leitura do sensor lateral direito
    val_leitura = robot.get_sensor('prox.horizontal.4')
    print(val_leitura)

    # Calcular erro
    erro = val_alvo - val_leitura

    # PID
    erro_acumulado += erro
    derivada = erro - erro_anterior
    saida = Kp*erro + Ki*erro_acumulado + Kd*derivada

    # Atualizar erro anterior
    erro_anterior = erro

    # Controlar motores
    v_esq = velocidade_base + saida
    v_dir = velocidade_base - saida
    robot.set_motors(v_esq, v_dir)
    
    # Atualizar gráfico
    robot.update_realtime_plot({"Erro": erro, "SaidaPID": saida})
    
    robot.wait(0.05)
