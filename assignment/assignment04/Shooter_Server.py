# server.py
import json
import socket
from threading import Thread

#from assignment.assignment04.Shooter_Client import game_state


class Server:
    def __init__(self):
        self.port = 5000  # 1
        self.host = "127.0.0.1" # CHANGE TO 0.0.0.0 OR OTHERS IF YOU NEED
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.players_data = {}  # 2

    def start(self):  # 3
        self.get_socket_ready()
        self.handle_connection()

    def get_socket_ready(self):  # 4
        self.sock.bind((self.host, self.port))
        self.sock.listen()
        print("服务器已准备接收客户端连接")

    def handle_connection(self):  # 5
        while True:
            conn, addr = self.sock.accept()
            print(f"接收到来自{addr}的连接")
            conn.send(str(id(conn)).encode("utf-8"))
            Thread(target=self.handle_message, args=(conn,)).start()

    def handle_message(self, conn):  # 6
        while True:
            try:
                data = conn.recv(2048)
                print(data)
                if not data:
                    print("未接收到数据，关闭连接")
                    self.players_data.pop(str(id(conn)))
                    conn.close()
                    break
                else:
                    data = json.loads(data.decode("utf-8"))
                    self.update_one_player_data(data)
                    conn.sendall(json.dumps(self.get_other_players_data(data["id"])).encode("utf-8"))
            except Exception as e:
                print(repr(e))
                break

    def update_one_player_data(self, data):
        key = data["id"]
        pos = data["pos"]
        color = data["color"]
        bullet_state = data["bullet_state"]
        game_states = data["game_state"]
        enemy_bullet_poi_y=data["enemy_bullet_poi_y"]
        self.players_data[key] = {"pos": pos, "color": color, "bullet_state": bullet_state, "game_state": game_states,"enemy_bullet_poi_y":enemy_bullet_poi_y}

    def get_other_players_data(self, current_player_id):
        data = {}
        for key, value in self.players_data.items():
            if key != current_player_id:
                data[key] = value
        return data


if __name__ == '__main__':
    server = Server()
    server.start()

