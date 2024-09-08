import argparse
import os
import socket
import threading

from manager import NetworkManager

lock = threading.Lock()

def main(ip, port, buff_size):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(5)
    print(f'[*] Listening on {ip}:{port}')

    connections = []
    nms = []

    while len(connections) < 2:
        sock, address = server.accept()
        connections.append(sock)
        nms.append(NetworkManager(sock, buff_size))

    nms[0].send("From server: connection accepted as player 0")
    nms[1].send("From server: connection accepted as player 1")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('ip', type=str)
    parser.add_argument('port', type=int)
    parser.add_argument('buff_size', type=int)

    args = parser.parse_args()

    main(args.ip, args.port, args.buff_size)
