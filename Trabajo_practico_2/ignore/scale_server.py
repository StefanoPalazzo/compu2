import http.server
import socketserver
from PIL import Image
from io import BytesIO
from multiprocessing import Process
import cgi


class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):

    def do_POST(self):

        try:
            # Leer el contenido del body
            content_length = int(self.headers['Content-Length'])
            image_data = self.rfile.read(content_length)

            # Convertir los datos de imagen a un objeto Image
            image = Image.open(BytesIO(image_data))

            # Calcular las nuevas dimensiones (mitad del tamaño)
            new_width = image.width // 2
            new_height = image.height // 2

            # Redimensionar la imagen manteniendo el modo escala de grises
            resized_image = image.resize(
                (new_width, new_height),
                Image.Resampling.LANCZOS
            )

            # Preparar la respuesta
            output_buffer = BytesIO()
            resized_image.save(output_buffer, format="JPEG", quality=95)
            output_buffer.seek(0)

            # Enviar la respuesta
            self.send_response(200)
            self.set_headers()
            self.wfile.write(output_buffer.getvalue())

        except Exception as e:
            self.send_response(500)
            self.set_headers("text/plain")
            self.wfile.write(f"Error al procesar la imagen: {e}".encode())


    # def _set_headers(self, content_type="image/jpeg"):
    #     self.send_header("Access-Control-Allow-Origin", "*")
    #     self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
    #     self.send_header("Access-Control-Allow-Headers", "Content-Type")
    #     self.send_header("Content-Type", content_type)

    
    # def do_POST(self):
    #     if self.path == '/upload':
    #         content_type, pdict = cgi.parse_header(self.headers['Content-Type'])
    #         if content_type == 'multipart/form-data':
    #             pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
    #             form_data = cgi.parse_multipart(self.rfile, pdict)
                
    #             # Obtenemos el archivo de imagen
    #             if 'file' in form_data:
    #                 image_data = form_data['file'][0]  # Primer archivo subido (solo uno en este caso)
    #                 image_file = BytesIO(image_data)

    #                 try:
    #                     # Leer la imagen usando Pillow
    #                     image = Image.open(image_file)

    #                     # Convertir la imagen a escala de grises
    #                     grayscale_image = image.convert("L")

    #                     # Guardar la imagen procesada en un buffer
    #                     output_buffer = BytesIO()
    #                     grayscale_image.save(output_buffer, format="JPEG")
    #                     output_buffer.seek(0)

    #                     # Enviar la imagen procesada como respuesta
    #                     self.send_response(200)
    #                     self._set_headers("image/jpeg")
    #                     self.end_headers()
    #                     self.wfile.write(output_buffer.read())

    #                 except Exception as e:
    #                     self.send_response(500)
    #                     self._set_headers("text/plain")
    #                     self.end_headers()
    #                     self.wfile.write(f"Error al procesar la imagen: {e}".encode())
    #             else:
    #                 self.send_response(400)
    #                 self._set_headers("text/plain")
    #                 self.end_headers()
    #                 self.wfile.write("No se encontró un archivo de imagen en la solicitud.".encode())

def start_scale_server_process(host, port):
    process = Process(target=start_server, args=(host, port))
    process.start()

def start_server(host, port):

    Handler = CustomHTTPRequestHandler
    
    with socketserver.TCPServer((host, port), Handler) as httpd:
        print(f'serving Scale Server at {host}:{port}')
        httpd.serve_forever()

if __name__ == '__main__':
    start_server('localhost', 9898)
