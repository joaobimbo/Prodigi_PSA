from controller import Robot, Motor, Camera, Display
from ThymioPSA import *
import numpy as np
from ImgProc import *

thymio = Robot()
r=ThymioPSA(thymio)

def processar_imagem(image,w,h):
    img_array = np.frombuffer(image, dtype=np.uint8).reshape((h, w, 4))
    #print(RGBA2HSV(img_array))
    img=mask_image(RGBA2HSV(img_array),[50,90],[50,255],[10,255]) #verde
    #img=mask_image(RGBA2HSV(img_array),[25,40],[20,255],[20,255]) #amarelo
    img,x,y=centroid(img)
    return img,x,y
    

def get_image():
    cam=r.devs["front_camera"]
    image = cam.getImage()
    w, h = cam.getWidth(), cam.getHeight()
    disp=r.devs["display"]
    img,cX,cY=processar_imagem(image,w,h)
    print(img.shape)
    ir = disp.imageNew(img.tobytes(), Display.RGB, w, h)
    #ir = disp.imageNew(image, Display.BGRA, w, h)
    disp.imagePaste(ir,0, 0, False)
    disp.imageDelete(ir)
    return cX,cY

def get_line_sensor(r):
    return [r.get_sensor('prox.ground.0'),r.get_sensor('prox.ground.1')]

while r.running():
    d=get_line_sensor(r)
    cX,cY=get_image()
    vl,vr=3+(cX-160)*0.3,3+(160-cX)*0.3
    r.set_motors(vl,vr)
    print(cX,cY)
    print(vl,vr)
    