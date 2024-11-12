import asyncio
from aiohttp import web
from PIL import Image
from .image_processor import image_to_greyscale
from io import BytesIO
import io
from scale_server.scale_server import start_scale_server_process




async def handle_image(reader, writer):
    await image_to_greyscale(reader, writer)


async def start_scale_server(ip):
    start_scale_server_process(ip, 9999)

async def start_async_server(ip, port):
    await start_scale_server(ip)
    server = await asyncio.start_server(handle_image, ip, port)
    print(f'Servidor de filtrado asincrónico iniciado en {ip}:{port}')
    async with server:
        await server.serve_forever()

