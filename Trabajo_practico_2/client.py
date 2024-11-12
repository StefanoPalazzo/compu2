
import asyncio
import argparse
import os

parser = argparse.ArgumentParser(description='Client to send images to the server')

parser.add_argument('-r','--route', required=True, help="The route of the image to process")
parser.add_argument('-o', '--output', required=True, help="The route of the output of the program")



args = parser.parse_args()

async def send_image(image_path):
    reader, writer = await asyncio.open_connection('localhost', 9898)
    
    with open(image_path, 'rb') as f:
        writer.write(f.read())
    
    await writer.drain()
    processed_data = await reader.read(10000)

    output_dir = os.path.dirname(args.output)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    
    with open(args.output, 'wb') as f:
        f.write(processed_data)
    
    writer.close()
    await writer.wait_closed()

# Ejecuta el cliente con la imagen de ejemplo
asyncio.run(send_image(args.route))