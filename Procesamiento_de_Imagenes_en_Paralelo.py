import cv2 as cv
import sys
import os
import scipy as sp
from scipy.ndimage import uniform_filter, maximum_filter, gaussian_filter, minimum_filter
import random
import numpy as np
import multiprocessing
from time import perf_counter
import signal
import sys

ruta_imagen = "tigre.jpg"

def cargar_imagen(nro_partes):
    global img, altura, ancho, tamano_total, shared_array, lista_bloques
    img = cv.imread(ruta_imagen)
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
    global lista_bloques
    # Calculamos el tamaño de cada bloque
    altura_bloque = int(altura/nro_partes)
    ancho_bloque = int(ancho/nro_partes)

    
    lista_bloques = []

    # Agregamo cada parte de la imagen a la lista de bloques
    for i in range(0,altura, int(altura/nro_partes)):
        for j in range(0,ancho, int(ancho/nro_partes)):
            lista_bloques.append(img[i:i+altura_bloque, j:j+ancho_bloque]) 


def aplicar_filtro_a_bloque_sin_paralelismo(lista_bloques, filtro_elegido):
    global lista
    lista = []
    for bloque in lista_bloques:
        try:
            filtro = filtro_elegido
            bloque_filtrado = filtro(bloque)
            lista.append(bloque_filtrado)
        except Exception as e:
            print(f"Error al aplicar filtro: {e}")

def aplicar_filtro_a_bloque(bloque, filtro_elegido, result_array, index, lock):
    try:
        filtro = filtro_elegido
        bloque_filtrado = filtro(bloque)

        # Obtiene el Lock para sincronizar y escribe en el array compartido
        with lock:
            result_array[index * bloque_filtrado.size:(index + 1) * bloque_filtrado.size] = bloque_filtrado.flatten()
    except Exception as e:
        print(f"Error al aplicar filtro: {e}")


def aplicar_filtros(filtro_elegido):
    global lista_final, procesos
    lista_final = []
    procesos = []

    bloque_shape = lista_bloques[0].shape
    result_array = multiprocessing.Array('d', len(lista_bloques) * bloque_shape[0] * bloque_shape[1] * 3)
    lock = multiprocessing.Lock()

    for index, bloque in enumerate(lista_bloques):
        proceso = multiprocessing.Process(target=aplicar_filtro_a_bloque, args=(bloque, filtro_elegido, result_array, index, lock))
        procesos.append(proceso)
    
    for proceso in procesos:
        proceso.start()
    
    for proceso in procesos:
        proceso.join()
    
    for index in range(len(lista_bloques)):
        bloque = np.array(result_array[index * bloque_shape[0] * bloque_shape[1] * 3:(index + 1) * bloque_shape[0] * bloque_shape[1] * 3])
        lista_final.append(bloque.reshape(bloque_shape))


def unir_bloques(lista_final, nro_partes):
    altura_bloque, ancho_bloque = lista_final[0].shape[:2]
    imagen_final = np.zeros((altura_bloque * nro_partes, ancho_bloque * nro_partes, 3), dtype=np.uint8)
    
    for idx, bloque in enumerate(lista_final):
        i = idx // nro_partes
        j = idx % nro_partes
        imagen_final[i * altura_bloque: (i + 1) * altura_bloque, j * ancho_bloque: (j + 1) * ancho_bloque] = bloque

    return imagen_final

def mostrar_imagen(imagen_final):
    os.system('clear')
    print ('Presione "q" para cerrar la ventana de la imagen')
    cv.imshow("Image", imagen_final)
    while True:
        if cv.getWindowProperty("Image", cv.WND_PROP_VISIBLE) < 1:
            break
        if cv.waitKey(100) & 0xFF == ord('q'):
            break
    cv.destroyAllWindows()

def signal_handler(sig, frame):
    print('Interrupción recibida, terminando procesos...')
    if 'procesos' in globals():
        for proceso in procesos:
            if proceso.is_alive():
                proceso.terminate()
    sys.exit(0)
        

def filtro_gaussiano_blur(img):
    b, g, r = cv.split(img)
    # Tratar por separado los canales
    b = sp.ndimage.gaussian_filter(b, sigma=2)
    g = sp.ndimage.gaussian_filter(g, sigma=2)
    r = sp.ndimage.gaussian_filter(r, sigma=2)
    # Unir los canales
    result = cv.merge([b, g, r])
    return result

def filtro_gaussiano_ByN(img):
    img = sp.ndimage.gaussian_filter(img, sigma=5)
    return img

def sin_filtro(img):
    return img

def filtro_invertir(img):
    return cv.bitwise_not(img)


def filtro_rojizo(img):
    return minimum_filter(img, size=2)

def filtro_aumento_contraste(img):
    lab = cv.cvtColor(img, cv.COLOR_BGR2LAB)
    l, a, b = cv.split(lab)
    clahe = cv.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    l = clahe.apply(l)
    lab = cv.merge((l, a, b))
    return cv.cvtColor(lab, cv.COLOR_LAB2BGR)

def filtro_sepia(img):
    img_sepia = np.array(img, dtype=np.float64)  # Convertir a float para evitar overflow
    img_sepia = cv.transform(img_sepia, np.matrix([[0.393, 0.769, 0.189],
                                                   [0.349, 0.686, 0.168],
                                                   [0.272, 0.534, 0.131]]))
    img_sepia[np.where(img_sepia > 255)] = 255  # Limitar los valores a 255
    return np.array(img_sepia, dtype=np.uint8)  # Convertir de nuevo a uint8


def obtener_filtros():
    return [filtro_gaussiano_blur, filtro_gaussiano_ByN, filtro_sepia,filtro_invertir,filtro_rojizo, filtro_aumento_contraste, sin_filtro]
    
def menu_opciones():
    print ("1. Filtro Gaussiano")
    print ("2. Filtro Gaussiano ByN")
    print ("3. Filtro Sepia")
    print ("4. Invertir colores")
    print ("5. Filtro Rojizo")
    print ("6. Aumento de contraste")
    print ("7. Sin filtro")

    eleccion = int(input("Ingrese el numero del filtro que desea aplicar: "))
    return eleccion

def guardar_imagen(imagen_final):
    guardar = input("Desea guardar la imagen? (s/n): ").lower()
    while guardar != "s" and guardar != "n":
        print('Opción inválida, por favor ingrese "s" o "n"')
        guardar = input("Desea guardar la imagen? (s/n): ").lower()
    
    if guardar == "s":
        cv.imwrite("imagen_final.jpg", imagen_final)
        print("Imagen guardada con éxito.")
    else:
        print("Imagen no guardada.")



def main():
    os.system('clear')
    nro_partes = int(input("Ingrese el numero de partes en que desea dividir la imagen: "))
    cargar_imagen(nro_partes)
    eleccion = menu_opciones()
    filtro_elegido = obtener_filtros()[eleccion - 1]
    signal.signal(signal.SIGINT, signal_handler)
    aplicar_filtros(filtro_elegido)
    imagen_final = unir_bloques(lista_final, nro_partes)
    mostrar_imagen(imagen_final)
    guardar_imagen(imagen_final)

    
    

    
    


if __name__ == "__main__":
    main()

