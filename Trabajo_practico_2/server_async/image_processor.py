import asyncio
from PIL import Image
import io
from aiohttp import web
# from server_async.server_async import send_to_scale_server

async def image_to_greyscale(reader, writer):

    data = await reader.read(1000000)
    image = Image.open(io.BytesIO(data)).convert("L")
    
    output = io.BytesIO()
    image.save(output, format='JPEG')
    output.seek(0)
    
    scaled_image_data = await send_to_scale_server(output.read())
    
    writer.write(scaled_image_data)
    await writer.drain()
    writer.close()

async def send_to_scale_server(image_data):
    reader, writer = await asyncio.open_connection('localhost', 9999)
    writer.write(image_data)
    await writer.drain()
    
    scaled_image_data = await reader.read(1000000)
    writer.close()
    await writer.wait_closed()
    return scaled_image_data

def scale_image(data, scale=0.5):
    image = Image.open(io.BytesIO(data))
    width, height = image.size
    scaled_image = image.resize((int(width * scale), int(height * scale)))
    output = io.BytesIO()
    scaled_image.save(output, format='JPEG')
    output.seek(0)
    return output.read()
