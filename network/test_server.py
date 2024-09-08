import argparse
import datetime
import os
import re
import socket
import threading

from manager import NetworkManager

class GameServer:
    def __init__(self, ip, port, buff_size, tag):
        self.ip = ip
        self.port = port
        self.buff_size = buff_size
        self.tag = tag

    def run_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.ip, self.port))
        server.listen(5)
        print(f'[*] Listening on {self.ip}:{self.port}')

        self.lock = threading.Lock()
        self.connections = dict()

        while True:
            sock, address = server.accept()
            print(f'[*] Accepted connection from {address[0]}: {address[1]}')
            threading.Thread(target=self.handle_connection, args=(sock, )).start()

    def handle_connection(self, sock):
        try:
            today_str = datetime.datetime.today().strftime("%Y%m%d")
            nm = NetworkManager(sock, self.buff_size)
            game_tag = nm.recv()
            assert bool(re.compile(f'{today_str}.*{self.tag}').match(game_tag)), \
                f"{game_tag} doesn't match expectation {today_str}.*{self.tag}"
            if game_tag in self.connections:
                print(f'[*] creating game with two players')
                sock_old = self.connections.pop(game_tag)
                self.handle_game(sock_old, sock)
            else:
                print(f'[*] adding first player to game {game_tag}')
                self.connections[game_tag] = sock
        except Exception as e:
            print(e)

    def handle_game(self, sock0, sock1):
        nm0 = NetworkManager(sock0, self.buff_size)
        nm1 = NetworkManager(sock1, self.buff_size)
        nm0.send("Connected as player 0")
        nm1.send("Connected as player 1")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip',        type=str, required=True)
    parser.add_argument('--port',      type=int, required=True)
    parser.add_argument('--buff_size', type=int, required=True)
    parser.add_argument('--tag',       type=str, required=True)

    args = parser.parse_args()

    GameServer(args.ip, args.port, args.buff_size, args.tag).run_server()
