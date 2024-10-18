from idlelib.configdialog import font_sample_text
from operator import truediv
from random import randrange

import pygame
import threading
import time

from sympy import false
from sympy.codegen import Print

# Initialize game interface
pygame.init()
screen=pygame.display.set_mode((800,600))
pygame.display.set_caption('JumpJump')
icon=pygame.image.load('CutePlayer.png') #Find player image which cute as me tho
pygame.display.set_icon(icon)
BGImage=pygame.image.load('BackGround.png') #Find background image
PlayerImage=pygame.image.load('CutePlayer.png')
PlayerImage=pygame.transform.scale(PlayerImage,(100,100))


# Game start
IniHigh=400 # Initial height
MaxHigh=180 # Maximum height
CurrentHigh=400 # Variable for player height adjustment
JumpInput=0 # Jumping speed
JumpState='Ground' # Player states
IniPoi=900
CurrentPoi=IniPoi
EnemySpeed=0.2
EnemyNum=0
timer=0
font = pygame.font.SysFont('Arial', 32)

# Define player states
def PlayerStates():
    global CurrentHigh,JumpState,JumpInput
    # 3 States control player's position
    if JumpState == 'Ground':  # Keep player in the ground
        CurrentHigh = IniHigh
        JumpInput = 0
    elif JumpState == 'Jumping':  # Increase height
        JumpInput = -0.3
        CurrentHigh += JumpInput
        if CurrentHigh < MaxHigh:  # Reach the maximum height
            JumpState = 'Falling'
    elif JumpState == 'Falling':  # Decrease height
        JumpInput = 0.3
        CurrentHigh += JumpInput
        if CurrentHigh >= IniHigh:  # Falling down to the ground
            JumpState = 'Ground'
    elif JumpState == 'Losing':
        pygame.display.set_caption('You Lose! Press R to reset')

class Enemy():
    global EnemySpeed, IniPoi, CurrentPoi
    def __init__(EnemyObj): # Enemy Object
            EnemyObj.img = pygame.image.load('EnemyPic.png')  # Find enemy image
            EnemyObj.img = pygame.transform.scale(EnemyObj.img, (100, 100))
            EnemyObj.CurrentPoi = IniPoi # Initialize enemy position
EnemyObjList=[]


def EnemyMove():
    global EnemySpeed, IniPoi, CurrentPoi,PlayerImage,JumpState
    for x in EnemyObjList:
        screen.blit(x.img, (x.CurrentPoi, IniHigh))  # Draw enemy image
        x.CurrentPoi -= EnemySpeed # Enemy moving
        if x.CurrentPoi < -10: # Delete enemy
            EnemyObjList.remove(x)
        if JumpState=='Losing': # Delete enemy
            EnemyObjList.remove(x)


def EnemyGenerate():# spawner
    EnemyObjList.append(Enemy())
    #print(len(EnemyObjList)) # spawner testing


def repeat_function(interval): # repeat spawner
    EnemyGenerate()
    threading.Timer(interval, repeat_function, [interval]).start()

RandomSec=randrange(3,6)
repeat_function(RandomSec)

def CollideDetect():
    global EnemySpeed, IniPoi, CurrentPoi, PlayerImage, JumpState
    for x in EnemyObjList:
        if x.CurrentPoi<10:
            if CurrentHigh>300:
                JumpState='Losing'

def SetText():
    if JumpState!='Losing':
        text = font.render('Press SPACE to jump', True, (0, 0, 0))  # Playing
    if JumpState == 'Losing':
        text = font.render('You Lose! REOPEN the game to reset', True, (0, 0, 0)) # Losed
    screen.blit(text, (0, 100))

# Start game
running=True
while running:
    screen.blit(BGImage,(0,0)) # Draw background image
    for event in pygame.event.get():

        if event.type == pygame.QUIT: # Click close window
            running=False # Quit game
        if JumpState=='Ground': # Space Input trigger jump action
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_SPACE:
                    JumpState='Jumping'
        if JumpState=='Losing':
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_r:
                    JumpState = 'Ground'
    SetText()
    PlayerStates() # States trigger actions
    EnemyMove()
    CollideDetect()
    screen.blit(PlayerImage, (0, CurrentHigh))# Draw player image
    pygame.display.update() # Show visual element