import sys
import json
import pygame
import socket
import random
from random import randint


pygame.init()
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
font = pygame.font.SysFont(None, 55)

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

enemyBulletMove=0
Game_Manager="playable"

def display_text(text, x, y):
    screen_text = font.render(text, True, bossORANGE)
    SCREEN.blit(screen_text, [x, y])

#Player object, contains data that will be sended to the server
class Player:
    def __init__(self, win, p_id, player_x, player_y, color, bullet,game_state):
        self.win = win #window
        self.id = p_id #client id
        self.player_speed = 7 # moving speed
        self.player_x = SCREEN_WIDTH // 2 - 25 # location of player
        self.player_y = SCREEN_HEIGHT - 70
        self.x = player_x
        self.y = player_y
        self.width = 35 # size of player
        self.height = 35
        self.color = color
        self.bullet = bullet # bullet states
        self.bullet_state = 0
        self.other_bullet_y = 50 #enemy bullet position
        self.other_bullet_state = "ready"
        self.bullet_img = pygame.Surface((10, 30)) #picture of bullet
        self.bullet_img.fill(bulletGREEN)
        self.other_bullet_img = pygame.Surface((10, 30)) #picture of enemy bullet
        self.other_bullet_img.fill(bossORANGE)
        self.game_state = game_state #0:playable; 1: lose
        self.other_game_state = 0 #0:playable; 1: win
        self.enemy_bullet_y=0 #enemy bullet position


    def move(self):
        global bullet_x
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.player_x > 0:
            self.player_x -= self.player_speed
        if keys[pygame.K_RIGHT] and self.player_x < SCREEN_WIDTH - 50: # moving
            self.player_x += self.player_speed
        if keys[pygame.K_SPACE] and self.bullet_state == 0: # shooting
            bullet_x = self.player_x + 20
            self.bullet_state = 1

    def shoot(self):
        global bullet_x, bullet_y
        if self.bullet_state == 1:
            self.bullet = self.bullet_state
            bullet_y += bullet_speed #bullet move
            if bullet_y < 0:
                self.bullet_state = 0
                self.bullet = self.bullet_state
                bullet_y = self.player_y
        else:
            bullet_x = self.player_x + 20
            bullet_y = self.player_y

    def other_shoot(self):
        global other_bullet_x,enemyBulletMove
        if self.bullet_state == 1:
            self.other_bullet_state = "fired" # states change enemy's bullet
        if self.other_bullet_y > 600:
            self.other_bullet_state = "ready"
        if self.other_bullet_state == "fired":
            self.other_bullet_y -= bullet_speed
        if self.other_bullet_state == "ready":
            other_bullet_x = self.player_x + 20
            self.other_bullet_y = 50
        enemyBulletMove=self.other_bullet_y

    def draw(self): # render player
        pygame.draw.rect(self.win, self.color, (self.player_x, self.player_y, self.width, self.height))
        if self.bullet_state == 1: # render bullet
            SCREEN.blit(self.bullet_img, (bullet_x, bullet_y))

    def draw_other_player(self):
        global other_bullet_x,enemyBulletMove
        pygame.draw.rect(self.win, bossORANGE, (self.player_x, 50, self.width, self.height)) # render enemy
        SCREEN.blit(self.other_bullet_img, (other_bullet_x, self.other_bullet_y)) # render enemy bullet

    def other_game_over(self):
        global Game_Manager
        if self.game_state==1: # unplayable
            #pygame.display.set_caption("you win")
            display_text("You Win!", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2)
            Game_Manager = "win"
    def game_over(self):
        #print(self.player_x,self.player_y,bullet_y)
        global other_bullet_x,enemyBulletMove,Game_Manager
        if self.game_state==0 and self.player_y < enemyBulletMove < self.player_y+35 and self.player_x < other_bullet_x < self.player_x + 35:
            self.game_state = 1
            self.other_game_state=self.game_state
        else: self.game_state = 0;self.other_game_state=self.game_state
        if self.game_state==1:
            #pygame.display.set_caption("you lose")
            display_text("You lose!" , SCREEN_WIDTH // 2 - 100,SCREEN_HEIGHT // 2)
            Game_Manager = "lose" # unplayable



# client.py
class GameWindow:
    def __init__(self):
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.window = self.init_window()
        self.player = Player(win=self.window,
                             p_id=None,
                             player_x=randint(0, self.width - 50),
                             player_y=randint(0, self.height - 50),
                             color=playerBLUE,
                             bullet=0,
                             game_state=0) # initial player

        self.port = 5000  # server inform
        self.host = "127.0.0.1"
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()  # 2
        self.other_players_dict = {}  # 3
    def connect(self):
        self.sock.connect((self.host, self.port))
        self.player.id = self.sock.recv(2048).decode("utf-8")

    def send_player_data(self):  # send players data
        data = {
            "id": self.player.id,
            "pos": [self.player.player_x, self.player.player_y],
            "color": self.player.color,
            "bullet_state": self.player.bullet,
            "game_state": self.player.game_state,
            "enemy_bullet_poi_y": self.player.other_bullet_y,
        }
        self.sock.send(json.dumps(data).encode("utf-8"))
        return self.sock.recv(2048).decode("utf-8")

    def update_window(self):  # players' function
        global Game_Manager,bullet_y
        if Game_Manager=="playable":
            self.window.fill(canvasGRAY)
            self.player.move()
            self.player.draw()
            self.player.shoot()
            # self.player.other_game_over()
            self.player.game_over()
            other_players_data = json.loads(self.send_player_data())
            self.update_other_players_data(other_players_data)
            self.delete_offline_players(other_players_data)

        if Game_Manager != "playable":  # reset game
            self.player_x = SCREEN_WIDTH // 2 - 25
            self.player_y = SCREEN_HEIGHT - 70
            self.x = player_x
            self.y = player_y
            self.bullet_state = 0
            self.other_bullet_y = 50
            self.other_bullet_state = "ready"
            self.game_state = 0  # 0:playable; 1: win
            self.other_game_state = 0
            self.enemy_bullet_y = 0
            bullet_y=player_y
            self.other_bullet_y = 50
            self.bullet_state
        pygame.display.update()

    def update_other_players_data(self, data):  # receive enemy's information from the server
        print(f"客户端接收到数据: {data}")
        for key, value in data.items():
            if not self.other_players_dict.get(key):
                self.add_one_player(key, value)
            else:
                pos = value["pos"]
                bullet = value.get("bullet_state", 0)  # 设置默认值
                other_game_state = value.get("game_state", 0)
                enemy_bullet_poi_y=value["enemy_bullet_poi_y"]

                self.other_players_dict[key].player_x = pos[0] # enemy position update
                self.other_players_dict[key].player_y = pos[1]
                self.other_players_dict[key].bullet_state = bullet # enemy bullet update
                self.other_players_dict[key].game_state = other_game_state # game state update
                self.other_players_dict[key].other_shoot() # enemy shoot state update
                self.other_players_dict[key].draw_other_player() # enemy render update
                self.other_players_dict[key].other_game_over() # game state update
                self.other_players_dict[key].enemy_bullet_poi_y = enemy_bullet_poi_y # load enemy y position
                self.player.enemy_bullet_y=self.other_players_dict[key].enemy_bullet_poi_y # load enemy's bullet position in this client
                #self.other_players_dict[key].game_over()

            if Game_Manager!="playable": # reset game
                self.other_players_dict[key].player_x = SCREEN_WIDTH // 2 - 25
                self.other_players_dict[key].player_y = 50
                self.other_players_dict[key].bullet_state = 0
                self.other_players_dict[key].game_state = 0

    def add_one_player(self, player_id, value): # add enemy and prepare to send date
        pos = value["pos"]
        color = value["color"]
        bullet = value.get("bullet_state", 0)  # 设置 bullet_state 的默认值为 0
        other_game_state = value.get("game_state", 0)

        self.other_players_dict[player_id] = Player(self.window, player_id, pos[0], pos[1], color, bullet,other_game_state)

    def delete_offline_players(self, data):
        new_dict = {}
        for key in self.other_players_dict.keys():
            if data.get(key):
                new_dict[key] = self.other_players_dict[key]
        self.other_players_dict = new_dict

    def init_window(self):  # 1

        pygame.display.set_caption('Shooter Client')
        return pygame.display.set_mode((self.width, self.height))


    def start(self):  # 3
        global Game_Manager
        clock = pygame.time.Clock()

        while True:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if Game_Manager != "playable":
                    pygame.time.delay(2000)
                    display_text(" ", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2)
                    Game_Manager = "playable"
            self.update_window() # all game function store here


if __name__ == "__main__":
    game = GameWindow()
    game.start()


