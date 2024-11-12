import http.server
import socketserver
from PIL import Image
from io import BytesIO
from multiprocessing import Process
from server_async.image_processor import scale_image
import cgi
import logging
import io



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
