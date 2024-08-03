import cv2 as cv
import sys
import os

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

    lista_bloques = []

    # Agregamo cada parte de la imagen a la lista de bloques
    for i in range(0,altura, int(altura/nro_partes)):
        for j in range(0,ancho, int(ancho/nro_partes)):
            lista_bloques.append(img[i:i+altura_bloque, j:j+ancho_bloque]) 
        
    for tigre in lista_bloques:
        cv.imshow("Image", tigre)
        k = cv.waitKey(0)

    



def mostrar_imagen():
    cv.imshow("Image", img)
    k = cv.waitKey(0)

def main():
    os.system('clear')
    nro_partes = int(input("Ingrese el numero de partes en que desea dividir la imagen: "))
    cargar_imagen(nro_partes)
    # mostrar_imagen()

if __name__ == "__main__":
    main()

