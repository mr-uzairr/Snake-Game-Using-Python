import pygame
import sys
import os
import random 
import math

pygame.init()
pygame.display.set_caption("Snake Game")
pygame.font.init()
random.seed()


# we will declare global constant definitions

SPEED = 0.36
SNAKE_SIZE = 9
APPLE_SIZE = SNAKE_SIZE     # we will keep both food and size of snake same
SEPARATION = 10    # separation between two pixels
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800
FPS = 25
KEY = {"UP":1 , "DOWN":2 , "LEFT":3, "RIGHT":4}


# we will initialise screen
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.HWSURFACE)
# we have used hw surface which stands for hardware surface refers to using memory on the video card for storing
# draws as opposed to main memory

# Resources
score_font = pygame.font.Font(None,38)
score_numb_font = pygame.font.Font(None,28)
game_over_font = pygame.font.Font(None,46)
play_again_font = score_numb_font
score_msg = score_font.render("Score : ",1,pygame.Color("green"))
score_msg_size = score_font.size("Score")
background_color = pygame.Color(0,0,0)    # we will fill background color as black
black = pygame.Color(0,0,0)


# for clock at the left corner
gameClock = pygame.time.Clock()

def checkCollision(posA,As ,posB , Bs):    # As is the size of a and Bs is the size of b
    if(posA.x < posB.x+Bs and posA.x+As > posB.x and posA.y < posB.y+Bs and posA.y+As > posB.y):
        return True
    return False

# to check the boundaries  here we are not limiting boundaries like it can pass through screen and come from other side

def checkLimits(snake):
    if(snake.x > SCREEN_WIDTH):
        snake.x = SNAKE_SIZE
    if(snake.x < 0):    # this will be checked when some part of snake is on other side and some on opposite side
        snake.x = SCREEN_WIDTH - SNAKE_SIZE
    if(snake.y > SCREEN_HEIGHT):
        snake.y = SNAKE_SIZE
    if(snake.y < 0):   # this also same half half
        snake.y = SCREEN_HEIGHT - SNAKE_SIZE

# we will make class for food of the snake let's name it as apple

class Apple:
    def __init__(self, x ,y,state):
        self.x = x
        self.y = y
        self.state = state
        self.color = pygame.color.Color("orange")     # color of food

    def draw(self,screen):
        pygame.draw.rect(screen,self.color,(self.x,self.y,APPLE_SIZE,APPLE_SIZE),0)

class segment:
    # initially snake will move in up direction
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.direction = KEY["UP"]
        self.color = "white"

class snake:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.direction = KEY["UP"]
        self.stack =[]   # initially it will be empty
        self.stack.append(self)
        blackBox = segment(self.x , self.y + SEPARATION)
        blackBox.direction = KEY["UP"]
        blackBox.color = "NULL"
        self.stack.append(blackBox)

# we will define moves of the snake

    def move(self):
        last_element = len(self.stack)-1
        while(last_element != 0):
            self.stack[last_element].direction = self.stack[last_element-1].direction
            self.stack[last_element].x = self.stack[last_element-1].x 
            self.stack[last_element].y = self.stack[last_element-1].y 
            last_element-=1
        if(len(self.stack)<2):
            last_segment = self
        else:
            last_segment = self.stack.pop(last_element)
        last_segment.direction = self.stack[0].direction
        if(self.stack[0].direction ==KEY["UP"]):
            last_segment.y = self.stack[0].y - (SPEED * FPS)
        elif(self.stack[0].direction == KEY["DOWN"]):
            last_segment.y = self.stack[0].y + (SPEED * FPS) 
        elif(self.stack[0].direction ==KEY["LEFT"]):
            last_segment.x = self.stack[0].x - (SPEED * FPS)
        elif(self.stack[0].direction == KEY["RIGHT"]):
            last_segment.x = self.stack[0].x + (SPEED * FPS)
        self.stack.insert(0,last_segment)

    def getHead(self):    # head of the snake 
        return(self.stack[0])   # It will be always 0 index

    # now when snake its food it will grow so for that we will add that food to stack

    def grow(self):
        last_element = len(self.stack) -1
        self.stack[last_element].direction = self.stack[last_element].direction
        if(self.stack[last_element].direction == KEY["UP"]):
            newSegment = segment(self.stack[last_element].x, self.stack[last_element].y -SNAKE_SIZE)
            blackBox = segment(newSegment.x , newSegment.y-SEPARATION)
        
        elif(self.stack[last_element].direction == KEY["DOWN"]):
            newSegment = segment(self.stack[last_element].x, self.stack[last_element].y +SNAKE_SIZE)
            blackBox = segment(newSegment.x , newSegment.y+SEPARATION)

        elif(self.stack[last_element].direction == KEY["LEFT"]):
            newSegment = segment(self.stack[last_element].x - SNAKE_SIZE, self.stack[last_element].y)
            blackBox = segment(newSegment.x - SEPARATION , newSegment.y)
        
        elif(self.stack[last_element].direction == KEY["RIGHT"]):
            newSegment = segment(self.stack[last_element].x + SNAKE_SIZE, self.stack[last_element].y)
            blackBox = segment(newSegment.x + SEPARATION , newSegment.y)

        blackBox.color = "NULL"
        self.stack.append(newSegment)
        self.stack.append(blackBox)

    def iterateSegments(self,delta):
        pass

    def setDirection(self,direction):
        if(self.direction == KEY["RIGHT"] and direction == KEY["LEFT"] or self.direction == KEY["LEFT"] and 
                direction == KEY["RIGHT"]):
            pass
        elif(self.direction == KEY["UP"] and direction == KEY["DOWN"] or self.direction == KEY["UP"] and 
                direction == KEY["DOWN"]):
            pass
        else:
            self.direction = direction

    def get_rect(self):     # get the rectangle shape 
        rect = (self.x , self.y)
        return rect

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def setX(self,x):
        self.x = x
    
    def setY(self,y):
        self.y = y

    


