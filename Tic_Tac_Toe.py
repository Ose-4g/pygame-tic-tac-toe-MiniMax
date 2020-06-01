import pygame
import os
import sys
from pygame.locals import *
import time
import random

pygame.init()  #initializes pygame
surface=pygame.display.set_mode((500,500))  #creates the window
fpsClock=pygame.time.Clock() # Game clock


class Game:
    '''
    Holds game variables
    '''
#game variables
    def __init__(self):
        self.board=[[None]*3 for i in range(3)]#the 3 by 3 board
        self.isdraw=False #checks if all slots of the board are filled
        self.isWin=False #checks if a game is won
        self.winner=None#Whoever wis=ns the game
        self.player='X' #sets the current player
        
    def change_player(self):
        '''
        changes the current player
        '''
        if self.player=='O':
            self.player='X'
        else:
            self.player='O'

#initialize the game object
game=Game()
 



def check_win(game):
    #checks if the game is won and sets the variable
    game.isWin= False
    #checking rows:
    board=game.board
    for i in range(3):
        if board[i][0]==board[i][1]==board[i][2]!=None:
            game.isWin= True
            game.winner=board[i][0]

    #checking columns
    for i in range(3):
        if board[0][i]==board[1][i]==board[2][i]!=None:
            game.isWin= True
            game.winner=board[0][i]

    #checking diagonals
    if board[0][0]==board[1][1]==board[2][2]!=None:
        game.isWin= True
        game.winner=board[1][1]
    if board[0][2]==board[1][1]==board[2][0]!=None:
        game.isWin= True
        game.winner=board[1][1]


def check_draw(game):
    #check if there is any empty space. If there is then there is still a move to be made
    game.isdraw = True
    board=game.board
    for i in range(3):
        for j in range(3):
            if board[i][j]==None:
                game.isdraw= False
    

def draw_board(surface,game):
    '''
    Draws an x or o in the correct position on the board
    '''
    board=game.board
    #loads images from memory
    x=pygame.image.load('my_x.PNG')
    o=pygame.image.load('my_o.PNG')
    
    #scales the images to size
    X=pygame.transform.scale(x,(80,80))
    O=pygame.transform.scale(o,(80,80))
    
    #blits the right images to the screen
    for i in range(3):
        for j in range(3):
            x=100*(j+1)+10
            y=100*(i+1)+10
            if board[i][j]=='O':
                pos=O.get_rect()
                pos.left=x
                pos.top=y
                surface.blit(O,pos)
            elif board[i][j]=='X':
                pos=X.get_rect()
                pos.left=x
                pos.top=y
                surface.blit(X,pos)
    pygame.display.update()

def game_over(surface):
    '''
    shows game over on the screen an asks if they want to play again
    '''
    text='GAME OVER'
    text2='PRESS SPACE FOR REMATCH'
    
    font=pygame.font.Font(None,30)
    text=font.render(text,10,(255,255,255))
    back=text.get_rect(centerx=surface.get_width()/2,centery=surface.get_height()/2)
    
    
    pygame.draw.rect(surface,(0,0,0),(100,200,300,100))#draws rectangle on the surface
    surface.blit(text,back)
    pygame.display.update()
    time.sleep(0.5)

    #second stage
    surface.fill((0,0,0))
    text2=font.render(text2,10,(255,255,255))
    back=text2.get_rect(centerx=surface.get_width()/2,centery=surface.get_height()/2)
    surface.blit(text2,back)
    pygame.display.update()
    
def starting_animation(surface):
    '''
    starting game animation
    just for fun
    '''
    #imports picture as pygame object
    game_start=pygame.image.load('game_start_screen.PNG')

    #scale the picture to the screen size
    start=pygame.transform.scale(game_start,(500,300))

    #fill surface with colour white
    surface.fill((255,255,255))
    #blit image on the backgground
    surface.blit(start,(0,100))
    pygame.display.update()#update the display
    time.sleep(1.5)
    pygame.display.update()

def initialize_board(surface):
    '''
    draws the game board screen
    '''
    #show game window
    pygame.display.set_caption('My Tic-Tac-Toe Game')

    surface.fill((255,255,255))
    pygame.display.update()

    #draw horizontal lines
    pygame.draw.line(surface,(0,0,0),(90,200),(410,200),3)
    pygame.draw.line(surface,(0,0,0),(90,300),(410,300),3)

    #draw vertical lines
    pygame.draw.line(surface,(0,0,0),(200,90),(200,410),3)
    pygame.draw.line(surface,(0,0,0),(300,90),(300,410),3)
    pygame.display.update()

def draw_status(surface,game):
    '''
    checks for a winner or draw if not it shows current player
    '''
    check_win(game)
    check_draw(game)
    surface.fill((0,0,0),(0,500-80,500,80))
    curr_player=game.player
    
    #if there is a winner
    if game.isWin:
        game.change_player()
        curr_player=game.player
        message='{} WON'.format(curr_player)
        
    #if it is draw
    elif game.isdraw:
        message='ITS A DRAW'
        
    #base case
    else:
        message='{}\'s turn'.format(curr_player)
    
    #display message to screen    
    font=pygame.font.Font(None,45)
    info=font.render(message,10,(255,255,255))
    pos=info.get_rect(centerx=surface.get_width()/2,top=surface.get_height()-50)
    surface.blit(info,pos)
    pygame.display.update()
    if game.isWin or game.isdraw:
        time.sleep(1)
        pygame.display.update()

def get_mouse_input(surface,game):
    '''
    gets input from mouse
    '''
    x,y=pygame.mouse.get_pos()#mouse x and y postion in pixels
    board=game.board
    if 100<=x<=200:
        col=0
    elif 200<x<=300:
        col=1
    elif 300<x<=400:
        col=2
    else:
        col=3

    if 100<=y<=200:
        row=0
    elif 200<y<=300:
        row=1
    elif 300<y<=400:
        row=2
    else:
        row=3
    if 0<=row<=2 and 0<=col<=2:
        if board[row][col]==None:
            board[row][col]=game.player
            game.change_player()
            return True #if move was valid
    return False# if input was invalid and doesnt chaneg plYER

def reset(game):
    '''
    resets game variables for a new game
    '''
    game.isWin=False
    game.isdraw=False
    game.board=[[None]*3 for i in range(3)]
    game.isplayng=True
    initialize_board(surface)
    game.player='X'
    draw_status(surface,game)
            

def computer_play(game):
    '''
    if in user vs computer we use this.
    computer plays a random move
    '''
    board=game.board
    while True:
        row=random.randint(0,2)
        col=random.randint(0,2)
        if board[row][col]==None:
            board[row][col]=game.player
            game.change_player()
            break

def two_or_one(surface):
    #asks the user if he wants single player or multiplayer mode
    
    surface.fill((255,255,255))
    surface.fill((0,0,0),(0,0,surface.get_width(),surface.get_height()/2))
    text1='USER VS COMPUTER'
    text2='USER 1 VS USER 2'
    font=pygame.font.Font(None,65)
    text1=font.render(text1,10,(255,255,255))
    text2=font.render(text2,10,(0,0,0))
    text1_r=text1.get_rect(centerx=surface.get_width()/2,centery=surface.get_height()/4)
    text2_r=text2.get_rect(centerx=surface.get_width()/2,centery=3*surface.get_height()/4)
    surface.blit(text1,text1_r)
    surface.blit(text2,text2_r)

    font=pygame.font.Font(None,30)
    text='Press Arrow Up key'
    text=font.render(text,5,(255,255,255))
    backing=text.get_rect(centerx=surface.get_width()/2,centery=surface.get_width()/8)
    surface.blit(text,backing)
    
    text='Press Arrow Down key'
    text=font.render(text,5,(0,0,0))
    backing=text.get_rect(centerx=surface.get_width()/2,centery=7*surface.get_width()/8)
    surface.blit(text,backing)
    pygame.display.update()



def MiniMax(game,winner,depth=1):
    '''
    takes in board state
    knows whoever just played
    checks for opponents best move
    returns a score based on that
    '''
    check_win(game)
    check_draw(game)
    board=game.board
    
    if game.isWin:
        if game.winner==winner:
            return 10/depth
        else:
            return -10/depth
    elif game.isdraw:
        return 0
    else:
        if game.player=='X':
            next_player='O'
        else:
            next_player='X'

        n_game=Game()
        n_game.player=next_player
        for i in range(3):
            for j in range(3):
                n_game.board[i][j]=board[i][j]


        #game.player has already played.        
        if game.player==winner:
            #IF GAME.player is the player
            best_move=2000
            for i in range(3):
                for j in range(3):
                    if board[i][j]==None:
                        n_game.board[i][j]=next_player
                        move=MiniMax(n_game,winner,depth+1)
                        
                        n_game.board[i][j]=None
                        #opponents bast move is lowest score
                        best_move=min(move,best_move)
            return best_move

        else:#if game.player is the opponent
            best_move=-2000
            for i in range(3):
                for j in range(3):
                    if board[i][j]==None:
                        n_game.board[i][j]=next_player
                        move=MiniMax(n_game,winner,depth+1)
                        
                        n_game.board[i][j]=None
                        #your best move is highest score
                        best_move=max(move,best_move)
            return best_move


def computer_best_move(game):
    x,y=None,None
    board=game.board
    n_game=Game()
    n_game.player=game.player
    for i in range(3):
        for j in range(3):
            n_game.board[i][j]=board[i][j]
    best_move=-20
    for i in range(3):
        for j in range(3):
            if n_game.board[i][j]==None:
                n_game.board[i][j]=n_game.player
                
                a=MiniMax(n_game,n_game.player)

                
                n_game.board[i][j]=None
                    
                if a>best_move:
                    best_move=a
                    x,y=i,j

    board[x][y]=game.player
    game.change_player()
    '''
    for i in board:
        print(i)
    print()
    '''

starting_animation(surface)
two_or_one(surface)
vs_comp=True #single player or multiplayer
while True:
    for event in pygame.event.get():
        keys=pygame.key.get_pressed()
        
        #if key up is pressed down
        if keys[K_UP]:
            vs_comp=True
            initialize_board(surface)
            draw_status(surface,game)
       
        #if key down is pressed
        elif keys[K_DOWN]:
            vs_comp=False
            initialize_board(surface)
            draw_status(surface,game)
            
        #let the game begin
        if event.type==MOUSEBUTTONDOWN and not(game.isWin==True or game.isdraw==True):
            if vs_comp:
                
                
                a=get_mouse_input(surface,game)
                draw_board(surface,game)
                draw_status(surface,game)
                time.sleep(0.5)

                if a and not (game.isWin or game.isdraw):
                    computer_best_move(game)
                    draw_board(surface,game)
                    draw_status(surface,game)
                
            else:
                get_mouse_input(surface,game)
                draw_board(surface,game)
                draw_status(surface,game)
                
            if game.isWin==True or game.isdraw==True:
                game_over(surface)
                
        if keys[K_SPACE]:
            reset(game)
            
        if event.type==QUIT:
            surface.fill((0,0,0))
            message='LIVE LONG AND PROSPER'
            font=pygame.font.Font(None,45)
            text=font.render(message,10,(255,255,255))
            text_r=text.get_rect(centerx=surface.get_width()/2,centery=surface.get_height()/2)
            surface.blit(text,text_r)
            pygame.display.update()
            time.sleep(1)
            pygame.quit()
            sys.exit()         
        
    pygame.display.update()
    fpsClock.tick(30)
           





