import asyncio
from aiohttp import web
from PIL import Image
from .image_processor import image_to_greyscale
from io import BytesIO
import io
from scale_server.scale_server import start_scale_server_process


async def send_to_scale_server(image_data):
    reader, writer = await asyncio.open_connection('localhost', 9999)
    writer.write(image_data)
    await writer.drain()
    
    scaled_image_data = await reader.read(1000000)
    writer.close()
    await writer.wait_closed()
    return scaled_image_data

async def handle_image(reader, writer):
    data = await reader.read(1000000)
    image = Image.open(io.BytesIO(data)).convert("L")
    
    output = io.BytesIO()
    image.save(output, format='JPEG')
    output.seek(0)
    
    scaled_image_data = await send_to_scale_server(output.read())
    
    writer.write(scaled_image_data)
    await writer.drain()
    writer.close()


async def start_scale_server(ip):
    start_scale_server_process(ip, 9999)

async def start_async_server(ip, port):
    await start_scale_server(ip)
    server = await asyncio.start_server(handle_image, ip, port)
    print(f'Servidor de filtrado asincrónico iniciado en {ip}:{port}')
    async with server:
        await server.serve_forever()

