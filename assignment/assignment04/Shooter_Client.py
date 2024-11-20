import sys
import json
import pygame
import socket
import random
from random import randint

# Screen settings
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shooter Game")

# Colors
canvasGRAY = (215, 215, 215)
enemyBLUE = (50, 183, 240)
enemyFrozenBLUE = (116, 146, 157)
bossORANGE = (255, 97, 42)
bulletGREEN = (2, 255, 7)
healthYELLOW = (255, 255, 5)
textWHITE = (255, 255, 255)
playerBLUE = (2, 255, 255)

# Clock and font
clock = pygame.time.Clock()
#font = pygame.font.SysFont(None, 55)

# Player settings
#player_img = pygame.Surface((35, 35))
#player_img.fill(playerBLUE)
player_x = SCREEN_WIDTH // 2 - 25
player_y = SCREEN_HEIGHT - 70
player_speed = 7
player_lives = 3

# Bullet settings
bullet_img = pygame.Surface((10, 30))
bullet_img.fill(bulletGREEN)
bullet_speed = -20
bullet_state = 0
bullet_x = 0
bullet_y = player_y

# Enemy settings
Enemy_COUNT = 10
enemy_list = []
enemy_img = pygame.Surface((35, 35))
for i in range(Enemy_COUNT):
    Enemy_speed = random.choice([3, 4, 5])
    Enemy_x_location = random.randint(0, SCREEN_WIDTH - 50)
    Enemy_y_location = random.randint(50, 300)
    enemy_list.append([Enemy_x_location, Enemy_y_location, Enemy_speed, enemyBLUE])

# Boss settings
boss_img = pygame.Surface((50, 50))
boss_img.fill(bossORANGE)
boss_x = SCREEN_WIDTH - 100
boss_y = 50
boss_speed = -5
boss_active = True

# Game state
score = 0
time_remaining = 60
game_state = "playable"


class Player:
    def __init__(self, win, p_id, player_x, player_y, color,bullet):

        self.win = win  # 1
        self.id = p_id  # 2
        self.player_speed = 7  # 3
        self.player_x = SCREEN_WIDTH // 2 - 25
        self.player_y = SCREEN_HEIGHT - 70
        self.x = player_x
        self.y = player_y
        self.width = 35
        self.height = 35
        self.color = color
        self.bullet = bullet
        self.bullet_state = 0
        #player_lives = 3

    def move(self):  # 4
        global bullet_x
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.player_x > 0:
            self.player_x -= self.player_speed
        if keys[pygame.K_RIGHT] and self.player_x < SCREEN_WIDTH - 50:
            self.player_x += self.player_speed
        if keys[pygame.K_SPACE] and self.bullet_state == 0:
            bullet_x = self.player_x + 20
            self.bullet_state = 1

    def shoot(self): # 0: ready; 1: fired
        global bullet_x,bullet_y
        if self.bullet_state == 1:
            self.bullet=self.bullet_state
            bullet_y += bullet_speed
            if bullet_y < 0:
                self.bullet_state = 0
                self.bullet = self.bullet_state
                bullet_y = self.player_y
        else:
            bullet_x = self.player_x + 20
            bullet_y = self.player_y



    def draw(self):  # 5
        pygame.draw.rect(self.win, self.color, (self.player_x, self.player_y, self.width, self.height))
        if self.bullet_state == 1:
            SCREEN.blit(bullet_img, (bullet_x, bullet_y))
    def draw_other_player(self):
        pygame.draw.rect(self.win, bossORANGE, (self.player_x, 50 , self.width, self.height))
        if self.bullet_state == 1:
            enemy_bullet_y = self.player_y - bullet_y # 计算敌人子弹的 y 坐标
            SCREEN.blit(bullet_img, (bullet_x, enemy_bullet_y))


# client.py
class GameWindow:
    def __init__(self):
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.window = self.init_window()
        self.player = Player(win=self.window,           # 1
                             p_id=None,
                             player_x=randint(0, self.width - 50),
                             player_y=randint(0, self.height - 50),
                             color=playerBLUE,
                             bullet=0)

        self.port = 5000  # 1
        self.host = "127.0.0.1"
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.connect()  # 2
        self.other_players_dict = {}  # 3
    def connect(self):
        self.sock.connect((self.host, self.port))
        self.player.id = self.sock.recv(2048).decode("utf-8")

    def send_player_data(self):  # 4
        data = {
            "id": self.player.id,
            "pos": [self.player.player_x, self.player.player_y],
            "color": self.player.color,
            "bullet_state": self.player.bullet,
        }
        self.sock.send(json.dumps(data).encode("utf-8"))
        return self.sock.recv(2048).decode("utf-8")

    def update_window(self):  # 5
        self.window.fill(canvasGRAY)

        self.player.move()
        self.player.draw()
        self.player.shoot()

        other_players_data = json.loads(self.send_player_data())
        self.update_other_players_data(other_players_data)
        self.delete_offline_players(other_players_data)

        pygame.display.update()

    def update_other_players_data(self, data):  # 6
        print(f"Received data: {data}")
        for key, value in data.items():
            if not self.other_players_dict.get(key):
                self.add_one_player(key, value)
            else:
                pos = value["pos"]
                bullet = value.get("bullet_state", 0)  # 设置默认值
                self.other_players_dict[key].player_x = pos[0]
                self.other_players_dict[key].player_y = pos[1]
                self.other_players_dict[key].bullet_state = bullet
                self.other_players_dict[key].draw_other_player()

    def add_one_player(self, player_id, value):
        pos = value["pos"]
        color = value["color"]
        bullet = value.get("bullet_state", 0)  # 设置 bullet_state 的默认值为 0

        self.other_players_dict[player_id] = Player(self.window, player_id, pos[0], pos[1], color, bullet)

    def delete_offline_players(self, data):  # 8
        new_dict = {}
        for key in self.other_players_dict.keys():
            if data.get(key):
                new_dict[key] = self.other_players_dict[key]
        self.other_players_dict = new_dict

    def init_window(self):  # 1
        pygame.init()
        pygame.display.set_caption('Shooter Client')
        return pygame.display.set_mode((self.width, self.height))


    def start(self):  # 3
        clock = pygame.time.Clock()

        while True:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.update_window()


if __name__ == "__main__":
    game = GameWindow()
    game.start()


