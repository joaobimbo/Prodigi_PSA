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
    img, mask=mask_image(RGBA2HSV(img_array),[50,80],[50,255],[10,255]) # verde
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

def get_ground():
    gl=robot.get_sensor('prox.ground.0')
    gr=robot.get_sensor('prox.ground.1')
    return gl,gr
    

def controlador_1():
    thresh=700
    gl,gr = get_ground()
    if gl<thresh or gr<thresh or robot.get_sensor('prox.horizontal.2')>3000:
        robot.set_motors(-3,-3)
        robot.wait(1.0)
        rm=np.random.choice([-3,3])
        robot.set_motors(rm,-rm)
        print(rm)
        robot.wait(1.2)
    else:
        robot.set_motors(5.0,5.0)
           
           
def controlador_2():
    print(f"Alvo em X={cX}, Percentagem da imagem={perc:.2f}%")
    vl,vr=4+(cX-centro_imagem)*0.3,4+(centro_imagem-cX)*0.3
    robot.set_motors(vl,vr)
    
def controlador_3():
    print(f"marcha atras")
    robot.set_motors(-2,-2)
    robot.wait(2.0)
    print(f"vira esquerda")
    robot.set_motors(-2,2)
    robot.wait(2.0)
    print(f"frente")
    robot.set_motors(2,2)
    robot.wait(4.0)
    robot.set_motors(2,-2)
    print(f"vira direita")
    robot.wait(2.0)    
    robot.set_motors(2,2)
    robot.wait(8.0)
    robot.set_motors(-2,2)
    robot.wait(1.0)
   
    
    
def controlador_4():
    sp=1000
    sens=robot.get_sensor('prox.horizontal.4')
   
    vr=2.01-(sp-sens)*0.001
    vl=2.01+(sp-sens)*0.001
    robot.set_motors(vl,vr)
    if robot.get_sensor('prox.horizontal.2') > 3000:
        robot.set_motors(-1,2)
        robot.wait(2.0)    

    print(f'v: {vl},{vr} {sens}')
    robot.step_controller(2)

        
def controlador_5():
    sp=1000
    sens=robot.get_sensor('prox.horizontal.0')
    vl=2.01-(sp-sens)*0.001
    vr=2.01+(sp-sens)*0.001
    if robot.get_sensor('prox.horizontal.2') > 3000:
        robot.set_motors(2,-1)
        robot.wait(2.0)    
    
    robot.set_motors(vl,vr)
    print(f'v: {vl},{vr} {sens}')
    robot.step_controller(2)
    
def controlador_6():
    gl,gr = get_ground()
    e=gl-gr
    robot.set_motors(1+0.01*e,1-0.01*e)
    
def controlador_7():
    print(f"vira direita")
    robot.set_motors(2,-1)
    robot.wait(1.7)
    print(f"frente")
    robot.set_motors(5.8,5.8)
    robot.wait(8.0)



    
robot.wait(1.0)
fase=1


# Ciclo principal
while robot.running():

    cX, cY, largura, altura, perc = get_image() # Obter coordenadas do alvo
    centro_imagem = largura // 2 # Centro ideal da imagem
    gl,gr = get_ground()
    print(f'G: {gl},{gr}')        

    if fase==1:
        controlador_1()
        print(f'perc verde: {perc}')

        if perc>8:
            fase=2
    
    elif fase==2:
        controlador_2()
        gl,gr = get_ground()
        if gl < 200 or gr < 200:
            fase=3
    elif fase==3:
        controlador_3()
        fase=4
        robot.set_motors(0,0)
       
    elif fase==4:
        print('c4')
        controlador_4()
        if gl > 500 and gl < 600 and gr >500 and gr < 600:
            fase = 5
    elif fase==5:
        print('c5')
        controlador_5()  
        if gl < 400 or gr < 400:
            fase=6
    elif fase == 6:
        controlador_6()  
        sens=robot.get_sensor('prox.horizontal.0')   
        print(f'S: {sens}')
        if cX<20:
            fase=7
    elif fase == 7:
        controlador_7()
        fase=10
    
    
                
    else:
        print(f'fase: {fase}')
        robot.set_motors(-15.0,15.0)
    #if gl < 100 or gr < 100:
    #    robot.set_motors(0,0)
