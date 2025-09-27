import cv2
import numpy as np

def RGBA2HSV(image):
    """
    Converte imagem RGBA (Webots) para HSV (OpenCV).
    """
    return cv2.cvtColor(image[:,:,:3], cv2.COLOR_BGR2HSV)

def mask_image(image, h, s, v):
    """
    Cria mascara binaria para cor dentro de intervalos HSV.
    """
    lower = np.array([h[0], s[0], v[0]])
    upper = np.array([h[1], s[1], v[1]])
    mask = cv2.inRange(image, lower, upper)   # binary mask
    result = cv2.bitwise_and(image, image, mask=mask)
    return cv2.cvtColor(result[:,:,:3], cv2.COLOR_HSV2RGB), mask


def centroid(img):
    """
    Calcula centro de massa do objeto segmentado (mascara).
    """
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray_image, 50, 255, 0)
    M = cv2.moments(thresh)
    cX, cY = 0, 0
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        cv2.circle(img, (cX, cY), 5, (255, 255, 255), -1)
    return img, cX, cY
