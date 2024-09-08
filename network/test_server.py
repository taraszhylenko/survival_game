import argparse
import datetime
import os
import re
import socket
import threading

from manager import NetworkManager


def main(ip, port, buff_size, tag):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(5)
    print(f'[*] Listening on {ip}:{port}')

    lock = threading.Lock()
    connections = dict()

    while True:
        sock, address = server.accept()
        print(f'[*] Accepted connection from {address[0]}: {address[1]}')
        threading.Thread(target=handle_connection, args=(sock, buff_size, lock, connections, tag)).start()

def handle_connection(sock, buff_size, lock, connections, tag):
    try:
        today_str = datetime.datetime.today().strftime("%Y%m%d")
        nm = NetworkManager(sock, buff_size)
        game_tag = nm.recv()
        assert bool(re.compile(f'{today_str}.*{tag}').match(game_tag)), \
            f"{game_tag} doesn't match expectation {today_str}.*{tag}"
        if game_tag in connections:
            print(f'[*] creating game with two players')
            sock_old = connections.pop(game_tag)
            handle_game(sock_old, sock, buff_size, lock)
        else:
            print(f'[*] adding first player with tag {game_tag}')
            connections[game_tag] = sock
    except Exception as e:
        print(e)


def handle_game(sock0, sock1, buff_size, lock):
    nm0 = NetworkManager(sock0, buff_size)
    nm1 = NetworkManager(sock1, buff_size)
    nm0.send("Connected as player 0")
    nm1.send("Connected as player 1")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip',        type=str, required=True)
    parser.add_argument('--port',      type=int, required=True)
    parser.add_argument('--buff_size', type=int, required=True)
    parser.add_argument('--tag',       type=str, required=True)

    args = parser.parse_args()

    main(args.ip, args.port, args.buff_size, args.tag)
