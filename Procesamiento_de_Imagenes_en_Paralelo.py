import cv2 as cv
import sys
import os
import scipy as sp
from scipy.ndimage import median_filter, maximum_filter, sobel
import random
import numpy as np


def cargar_imagen(nro_partes):
    global img, altura, ancho
    img = cv.imread("tigre.jpg")
    if img is None:
        sys.exit("No se pudo encontrar la imagen.")

    # Definimos la altura y ancho de la imagen
    altura, ancho = img.shape[:2] 

    # Ajustamos la imagen para que sea divisible por el numero de partes
    altura = altura - (altura % nro_partes)
    ancho = ancho - (ancho % nro_partes)
    dividir_en_bloques(nro_partes)

def dividir_en_bloques(nro_partes):
    # Calculamos el tamaño de cada bloque
    altura_bloque = int(altura/nro_partes)
    ancho_bloque = int(ancho/nro_partes)

    global lista_bloques
    lista_bloques = []

    # Agregamo cada parte de la imagen a la lista de bloques
    for i in range(0,altura, int(altura/nro_partes)):
        for j in range(0,ancho, int(ancho/nro_partes)):
            lista_bloques.append(img[i:i+altura_bloque, j:j+ancho_bloque]) 

def aplicar_filtros():
    for i, bloque in enumerate(lista_bloques):
        filtros = obtener_filtros()
        filtro_aleatorio = random.choice(filtros)
        bloque = filtro_aleatorio(bloque)
        lista_bloques[i] = bloque 

def unir_bloques(nro_partes):
    # global img
    # img = cv.merge(lista_bloques)
    filas = []
    for i in range(nro_partes):
        fila = np.hstack(lista_bloques[i*nro_partes:(i+1)*nro_partes])
        filas.append(fila)
    imagen_final = np.vstack(filas)
    cv.imshow("Image", img)
    return imagen_final

def mostrar_imagen(imagen_final):
    cv.imshow("Image", imagen_final)
    while True:
        if cv.getWindowProperty("Image", cv.WND_PROP_VISIBLE) < 1:
            break
        if cv.waitKey(100) & 0xFF == ord('q'):
            break
    cv.destroyAllWindows()
        

def filtro_gaussiano_blur(img):
    b, g, r = cv.split(img)
    #Apply the Gaussian filter to each channel
    b = sp.ndimage.gaussian_filter(b, sigma=5)
    g = sp.ndimage.gaussian_filter(g, sigma=5)
    r = sp.ndimage.gaussian_filter(r, sigma=5)
    # Merge the channels back together
    result = cv.merge([b, g, r])
    return result

def filtro_gaussiano_ByN(img):
    img = sp.ndimage.gaussian_filter(img, sigma=5)
    return img

def filtro_maximum(img):
    b, g, r = cv.split(img)
    #Apply the Gaussian filter to each channel
    b = maximum_filter(b, size=10)
    g = maximum_filter(g, size=10)
    r = maximum_filter(r, size=10)
    # Merge the channels back together
    result = cv.merge([b, g, r])
    return result

def sin_filtro(img):
    return img

def filtro_sobel(img):
    img = sobel(img)
    return (img)

def obtener_filtros():
    return [filtro_sobel, filtro_gaussiano_blur, filtro_maximum, filtro_gaussiano_ByN,sin_filtro]


def main():
    os.system('clear')
    nro_partes = int(input("Ingrese el numero de partes en que desea dividir la imagen: "))
    cargar_imagen(nro_partes)
    aplicar_filtros()
    imagen_final = unir_bloques(nro_partes)
    mostrar_imagen(imagen_final)


if __name__ == "__main__":
    main()

