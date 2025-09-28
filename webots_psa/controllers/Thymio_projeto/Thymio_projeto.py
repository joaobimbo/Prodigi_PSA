from controller import Robot, Motor, Camera, Display
from ThymioPSA import *
from ImgProc import *
import numpy as np

# Criar instancia do robo
thymio = Robot()
robot = ThymioPSA(thymio)

# Funcoes auxiliares
def processar_imagem(image, w, h):
    """
    Aplica mascara de cor, calcula o centro do alvo e a % da imagem ocupada
    Retorna: imagem processada, coordenadas
    """
    img_array = np.frombuffer(image, dtype=np.uint8).reshape((h, w, 4))
    #img, mask = mask_image(RGBA2HSV(img_array), [25, 40], [20, 255], [20, 255]) # amarelo
    img, mask=mask_image(RGBA2HSV(img_array),[0,255],[50,255],[10,255]) #cor a filtrar
    # calcular percentagem de pixeis "ativos"
    area_mask = np.count_nonzero(mask)
    total_area = mask.size
    percentagem = (area_mask / total_area) * 100.0
    
    img, x, y = centroid(img)
    return img, x, y, percentagem

def get_image():
    """
    Captura imagem da camara
    """
    cam = robot.devs["front_camera"]
    image = cam.getImage()
    w, h = cam.getWidth(), cam.getHeight()
    disp = robot.devs["display"]

    img, cX, cY, perc = processar_imagem(image, w, h)

    # Mostrar imagem no display do Thymio
    ir = disp.imageNew(img.tobytes(), Display.RGB, w, h)
    disp.imagePaste(ir, 0, 0, False)
    disp.imageDelete(ir)

    return cX, cY, w, h, perc


# Ciclo principal
while robot.running():

    cX, cY, largura, altura, perc = get_image() # Obter coordenadas do alvo
    centro_imagem = largura // 2 # Centro ideal da imagem
    
    vl,vr=4+(cX-160)*0.3,4+(160-cX)*0.3
    robot.set_motors(vl,vr)

    
    print(f"Alvo em X={cX}, Percentagem da imagem={perc:.2f}%")
