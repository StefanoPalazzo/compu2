# Trabajo Práctico N°2 - Procesamiento de imágenes

## Descripción
Este trabajo práctico consiste en el desarrollo de un servidor asíncrono que recibe imágenes y les aplica un filtro, luego esta es enviada mediante sockets a otro servidor con multiprocesamiento. El servidor recibe la imagen, la reduce a la mitad de su tamaño y la guarda en una carpeta.

### **Objetivos**

- Manejo de archivos (apertura, escritura y cierre).
- Creación y gestión de tareas asíncronas y procesos.
- Uso de mecanismos de **Inter Process Communication** utilizando sockets.
- Uso de mecanismos de sincronización basados en **asyncio** y **multiprocessing**.
- Implementación de sockets tanto asíncronos como en procesos separados para comunicaciones en red.

## Instalación
Descargar el archivo y ejecutar el siguiente script para instalar las dependencias necesarias:
```bash 
$ pip install -r requirements.txt
```
## Instrucciones de Uso

### Correr Servidor
Para ejecutar el programa, se debe correr el siguiente comando:
```bash
$ python main.py -i [ip] -p [puerto]
```
o puede ejecutar el siguiente comando para obtener ayuda:
```bash
$ python main.py -h
```
Ejemplo:
```bash
$ python main.py -i 192.168.1.5 -p 8081
```

### Enviar imagen con cliente
Para enviar una imagen al servidor, se debe correr el siguiente comando:
```bash
$ python client.py -r [ruta_imagen] -o [ruta_output]
```
ejemplo:
```bash
$ python client.py -r ./images/imagen.jpg ./resultados/imagenprocesada.jpg
```
Esto enviará la imagen al servidor y se guardará en la carpeta `resultados/` con el nombre `imagenprocesada.jpg`.