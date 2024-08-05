import cv2 as cv
import sys
import os
import scipy as sp
from scipy.ndimage import uniform_filter, maximum_filter, gaussian_filter
import random
import numpy as np
from multiprocessing import Pool
from time import perf_counter


def cargar_imagen(nro_partes):
    global img, altura, ancho
    img = cv.imread("otono4K.jpg")
    if img is None:
        sys.exit("No se pudo encontrar la imagen.")

    # Definimos la altura y ancho de la imagen
    altura, ancho = img.shape[:2] 

    # Si la imagen es muy grande la reducimos para visualizarla correctamente
    if altura > 3000 or ancho > 3000:
        img = cv.resize(img, (int(ancho/8), int(altura/8)))
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

def aplicar_filtros_global():
    for i, bloque in enumerate(lista_bloques):
        filtros = obtener_filtros()
        filtro_aleatorio = random.choice(filtros)
        bloque = filtro_aleatorio(bloque)
        # Comento la siguiente linea para no volver a aplicar filtros sobre la imagen filtrada anteriormente
        # Así se puede comparar el tiempo de ejecución con y sin paralelismo
        # lista_bloques[i] = bloque


def aplicar_filtro_a_bloque(bloque):
    filtros = obtener_filtros()
    filtro_aleatorio = random.choice(filtros)
    return filtro_aleatorio(bloque)

def aplicar_filtros():
    with Pool() as pool:
        global lista_bloques
        lista_bloques = pool.map(aplicar_filtro_a_bloque, lista_bloques)


def unir_bloques(nro_partes):
    # global img
    # img = cv.merge(lista_bloques)
    filas = []
    for i in range(nro_partes):
        fila = np.hstack(lista_bloques[i*nro_partes:(i+1)*nro_partes])
        filas.append(fila)
    imagen_final = np.vstack(filas)
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
    b = sp.ndimage.gaussian_filter(b, sigma=2)
    g = sp.ndimage.gaussian_filter(g, sigma=2)
    r = sp.ndimage.gaussian_filter(r, sigma=2)
    # Merge the channels back together
    result = cv.merge([b, g, r])
    return result

def filtro_gaussiano_ByN(img):
    img = sp.ndimage.gaussian_filter(img, sigma=1)
    return img

def filtro_maximum(img):
    b, g, r = cv.split(img)
    #Apply the Gaussian filter to each channel
    b = maximum_filter(b, size=2)
    g = maximum_filter(g, size=2)
    r = maximum_filter(r, size=2)
    # Merge the channels back together
    result = cv.merge([b, g, r])
    return result

def sin_filtro(img):
    return img

def filtro_uniform(img):
    img = uniform_filter(img, size=2)
    return (img)



def obtener_filtros():
    return [filtro_uniform, filtro_maximum, filtro_gaussiano_blur, filtro_gaussiano_ByN,sin_filtro]



def main():
    os.system('clear')
    nro_partes = int(input("Ingrese el numero de partes en que desea dividir la imagen: "))
    t1_start = perf_counter()
    cargar_imagen(nro_partes)
    t1_stop = perf_counter()
    aplicar_filtros()
    t2_stop = perf_counter()
    aplicar_filtros_global()
    t3_stop = perf_counter()
    imagen_final = unir_bloques(nro_partes)
    t4_stop = perf_counter()
    os.system('clear')
    print("Cargar imagen:", t1_stop - t1_start)
    print("Aplicar filtros:", t2_stop - t1_stop)
    print("Aplicar filtros sin paralelismo:", t3_stop - t2_stop)
    print("Unir bloques:", t4_stop - t3_stop)
    mostrar_imagen(imagen_final)
    
    


if __name__ == "__main__":
    main()

