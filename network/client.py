import argparse
import datetime
import os
import re
import select
import socket
import threading
import time

from network.manager import NetworkManager
from engine.render import Render


class GameClient:
    def __init__(self, ip, port, buff_size, tag):
        sock = socket.socket()
        sock.connect((str(ip), int(port)))
        nm = NetworkManager(sock, buff_size)
        nm.send(tag)
        player_id = nm.recv()
        print(f'Entered as player {player_id}. Include it in all your commands')
        while True:
            command = input("enter command:")
            nm.send(command)
            status, render = nm.recv()
            Render(render).print()
            print(f'command status: {status}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip',        type=str, required=True)
    parser.add_argument('--port',      type=int, required=True)
    parser.add_argument('--buff_size', type=int, required=True)
    parser.add_argument('--tag',       type=str, required=True)

    args = parser.parse_args()

    GameClient(args.ip, args.port, args.buff_size, args.tag)
