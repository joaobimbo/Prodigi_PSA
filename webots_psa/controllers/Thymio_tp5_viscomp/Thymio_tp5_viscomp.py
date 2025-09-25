from controller import Robot, Motor, Camera, Display
from ThymioPSA import *
import numpy as np
from ImgProc import *

# Criar instancia do robo
thymio = Robot()
robot = ThymioPSA(thymio)

# Funcoes auxiliares
def processar_imagem(image, w, h):
    """
    Aplica mascara de cor e calcula o centro do alvo.
    Retorna: imagem processada, coordenadas
    """
    img_array = np.frombuffer(image, dtype=np.uint8).reshape((h, w, 4))
    img = mask_image(RGBA2HSV(img_array), [25, 40], [20, 255], [20, 255]) # amarelo
    #img = mask_image(RGBA2HSV(img_array), [60, 80], [50, 255], [10, 255]) #verde
    img, x, y = centroid(img)
    return img, x, y

def get_image():
    """
    Captura imagem da camara e devolve coordenadas do alvo.
    """
    cam = robot.devs["front_camera"]
    image = cam.getImage()
    w, h = cam.getWidth(), cam.getHeight()
    disp = robot.devs["display"]

    img, cX, cY = processar_imagem(image, w, h)

    # Mostrar imagem no display do Thymio
    ir = disp.imageNew(img.tobytes(), Display.RGB, w, h)
    disp.imagePaste(ir, 0, 0, False)
    disp.imageDelete(ir)

    return cX, cY, w, h


# Ciclo principal
while robot.running():

    # Obter coordenadas do alvo
    cX, cY, largura, altura = get_image()

    # Centro ideal da imagem
    centro_imagem = largura // 2

    # Calcular erro (quanto o alvo esta afastado do centro)
    erro = centro_imagem - cX

    # -------------------------
    # IMPLEMENTAR CONTROLADOR AQUI

    # -------------------------
    print(f"Alvo em X={cX}, Erro={erro}")
