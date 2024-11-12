import http.server
import socketserver
from PIL import Image
from io import BytesIO
from multiprocessing import Process
import cgi
import logging
import io


def scale_image(data, scale_factor=0.5):
    image = Image.open(io.BytesIO(data))
    width, height = image.size
    scaled_image = image.resize((int(width * scale_factor), int(height * scale_factor)))
    output = io.BytesIO()
    scaled_image.save(output, format='JPEG')
    output.seek(0)
    return output.read()

class ScaleRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1000000)
        scaled_image_data = scale_image(data)
        self.request.sendall(scaled_image_data)


def start_scale_server_process(host, port):
    process = Process(target=start_server, args=(host, port))
    process.start()
    

def start_server(host, port):

    with socketserver.TCPServer((host, port), ScaleRequestHandler) as server:
        print(f'serving Scale Server at {host}:{port}')
        server.serve_forever()

if __name__ == '__main__':
    start_server('localhost', 9898)
