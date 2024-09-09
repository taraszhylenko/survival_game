import argparse
import datetime
import os
import random
import re
import select
import socket
import threading
import time

from network.manager import NetworkManager
from engine.game import Game
from engine.enum import TraitType as tt, ItemType as it

class GameServer:
    def __init__(self, ip, port, buff_size, tag, evolution_deck_file, area_deck_file):
        self.ip = ip
        self.port = port
        self.buff_size = buff_size
        self.tag = tag
        self.evolution_deck_file = evolution_deck_file
        self.area_deck_file = area_deck_file

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
                with self.lock:
                    sock_old = self.connections.pop(game_tag)
                self.handle_game(sock_old, sock)
            else:
                print(f'[*] adding first player to game {game_tag}')
                with self.lock:
                    self.connections[game_tag] = sock
        except Exception as e:
            print(e)

    def handle_game(self, sock0, sock1):
        game = Game(self.evolution_deck_file,
                    self.area_deck_file,
                    2)
        nm0 = NetworkManager(sock0, self.buff_size)
        nm1 = NetworkManager(sock1, self.buff_size)
        nm0.send(0)
        nm1.send(1)
        while True:
            time.sleep(0.1)
            sock0_ready = bool(select.select([sock0], [], [], 0.01)[0])
            sock1_ready = bool(select.select([sock1], [], [], 0.01)[0])
            if sock0_ready and sock1_ready:
                print(f'[*] {sock0_ready=}, {sock1_ready=}')
                nm0.recv()
                nm1.recv()
                nm0.send("repeat your turn", game.render().arr)
                nm1.send("repeat your turn", game.render().arr)
                print(f'[*] emptying queue as both requests arrived simultaneously')
            elif sock0_ready:
                print(f'[*] {sock0_ready=}, {sock1_ready=}')
                nm0.send(self.process_player_request(game, 0, sock0))
            elif sock1_ready:
                print(f'[*] {sock0_ready=}, {sock1_ready=}')
                nm1.send(self.process_player_request(game, 1, sock1))

    def process_player_request(self, game, player, sock):
        player_request = NetworkManager(sock, self.buff_size).recv()
        valid_requests = [f"^noop\({player}\)$",
                          f"^rules\({player}\)$",
                          f"^draw_card\({player}\)$",
                          f"^cast_animal\({player},\d+\)$",
                          f"(^cast_trait\({player},\d+,(tt.MAIN|tt.SHORT),\[\d+\]\)$|^cast_trait\({player},\d+,(tt.MAIN|tt.SHORT),\[\d+,\d+\]\)$)",
                          f"^discard_animal\({player},\d+\)$",
                          f"^discard_trait\({player},\d+\)$",
                          f"^discard_card\({player},\d+\)$",
                          f"^place_area\({player}\)$",
                          f"^remove_area\({player}\)$",
                          f"^take_item\({player},\d+,(it.RED|it.GREEN),\d+\)$",
                          f"^add_item\({player},\d+,(it.RED|it.GREEN|it.BLUE|it.FAT)\)$",
                          f"^remove_item\({player},\d+,(it.RED|it.GREEN|it.BLUE|it.FAT)\)$",
                          f"^roll_die\({player}\)$",
                          f"^run_extinction\({player}\)$"]
        if not any([bool(re.compile(el).match(player_request)) for el in valid_requests]):
            if player_request == "":
                return "ok", game.render(player).arr
            print(f'[*] got invalid request {player_request}')
            return ("invalid_format", game.render(player).arr)
        status = eval(f'game.{player_request}')
        print(f'[*] request {player_request} from {player}: {status}')
        return status, game.render(player).arr


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip',        type=str, required=True)
    parser.add_argument('--port',      type=int, required=True)
    parser.add_argument('--buff_size', type=int, required=True)
    parser.add_argument('--tag',       type=str, required=True)
    parser.add_argument('--evolution-deck-file', type=str, required=True)
    parser.add_argument('--area-deck-file',      type=str, required=True)

    args = parser.parse_args()

    GameServer(args.ip, args.port, args.buff_size, args.tag,
               args.evolution_deck_file, args.area_deck_file).run_server()
