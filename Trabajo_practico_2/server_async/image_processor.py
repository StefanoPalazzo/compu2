
from PIL import Image
import io
from aiohttp import web

async def image_to_greyscale(request):

    data = await request.post()
    image_file = data['file'] 
    # Leer los datos de la imagen
    image_bytes = image_file.file.read()

    # Abrir la imagen con PIL (Image) para procesarla
    image = Image.open(io.BytesIO(image_bytes))

    # Convertir la imagen a escala de grises
    image = image.convert("L")

    # Guardar la imagen procesada en memoria
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    # Enviar la imagen procesada al cliente
    return web.Response(body=img_byte_arr.read(), content_type='image/png')