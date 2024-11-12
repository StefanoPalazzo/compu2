from server_async.server_async import start_async_server
import asyncio
import argparse

parser = argparse.ArgumentParser(description='TP2 - Image filtering and scaling')

parser.add_argument('-i','--ip', required=True, help="The server's IP address")
parser.add_argument('-p', '--port', required=True, type=int, help="The filtering server's port")



args = parser.parse_args()



if __name__ == "__main__":
    asyncio.run(start_async_server(args.ip, args.port))