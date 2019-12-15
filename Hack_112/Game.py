#################################################
# Hack 15112.py
#
# Your Group: Magic Q
# Teammates: Yuhang Liang, Jiangwen Wei, Zhen ji, Yuchen Lu
#################################################

import math, copy
# this file is downloaded from:
# https://www.cs.cmu.edu/~112/notes/notes-animations-part1.html
from cmu_112_graphics import *
from tkinter import *
import random

#################################################

# finished
class EndMode1(Mode):
    def appStarted(mode):
        # For image
        urlOfBackground = 'https://tinyurl.com/1111111d'
        mode.image0 = mode.loadImage(urlOfBackground)
        mode.image0 = mode.scaleImage(mode.image0, 1.55)
    
    def keyPressed(mode, event):
        if event.key == 'r':
            mode.app.setActiveMode(mode.app.initialMode)
    
    def redrawAll(mode, canvas):
        # draw the background
        canvas.create_image(mode.width//2, mode.height//2-40, \
                            image=ImageTk.PhotoImage(mode.image0))

class EndMode2(Mode):
    def appStarted(mode):
        # For image
        urlOfBackground = 'https://tinyurl.com/y2yfyndu'
        mode.image0 = mode.loadImage(urlOfBackground)
        mode.image0 = mode.scaleImage(mode.image0, 1.55)
    
    def keyPressed(mode, event):
        if event.key == 'r':
            mode.app.setActiveMode(mode.app.initialMode)
    
    def redrawAll(mode, canvas):
        # draw the background
        canvas.create_image(mode.width//2, mode.height//2-40, \
                            image=ImageTk.PhotoImage(mode.image0))

class Tank1(object):
    def __init__(self, app, imageOfTank, imageOfBullet):
        self.app = app
        # basic parameters
        self.num = 1
        self.numOfBullet = 5
        self.health = 5
        self.x = 100
        self.y = 50
        self.bullet = {}
        self.totalBullet = 5
        for i in range(self.totalBullet):
            self.bullet[i] = []
        self.direction = ('up', 'down', 'left', 'right')
        # image of Tank
        self.image0 = imageOfTank
        self.image1 = self.image0.rotate(180)
        self.image2 = self.image0.rotate(90)
        self.image3 = self.image2.rotate(180)
        # image of bullets
        self.imageBulletUp = imageOfBullet
        self.imageBulletDown = self.imageBulletUp.rotate(180)
        self.imageBulletLeft = self.imageBulletUp.rotate(90)
        self.imageBulletRight = self.imageBulletLeft.rotate(180)
        self.bulletImage = self.imageBulletDown
        # initial tank image
        self.image = self.image0
    
    def reDirect(self, num):
        # reset the image of tank1
        self.num = num
        if num == 0:
            self.image = self.image0
            self.bulletImage = self.imageBulletUp
        elif num == 1:
            self.image = self.image1
            self.bulletImage = self.imageBulletDown
        elif num == 2:
            self.image = self.image2
            self.bulletImage = self.imageBulletLeft
        elif num == 3:
            self.image = self.image3
            self.bulletImage = self.imageBulletRight

    def shoot(self): 
        # initial coordinate of the play's bullet
        if self.numOfBullet > 0:
            self.numOfBullet -= 1
            self.imageWidth, self.imageHeight = self.image.size
            if self.num == 0:
                zx = self.x 
                zy = self.y - self.imageHeight//2
            elif self.num == 1:
                zx = self.x
                zy = self.y + self.imageHeight//2
            elif self.num == 2:
                zx = self.x - self.imageWidth//2
                zy = self.y
            elif self.num == 3:
                zx = self.x + self.imageWidth//2
                zy = self.y
        for i in range(self.totalBullet):
            if self.bullet[i] == []:
                self.bullet[i] = [zx, zy, self.num]
                break
    
    def checkInBound(self):
        if self.x > self.app.width:
            self.x = self.app.width
        elif self.x < 0:
            self.x = 0
        if self.y > self.app.height:
            self.y = self.app.height
        elif self.y < 0:
            self.y = 0

    def isNotCounter(self):
        if self.app.player2.x-50 < self.x < self.app.player2.x+50 and \
            self.app.player2.y-50 < self.y < self.app.player2.y+50:
            return False
        return True

    def move(self, direction):
        self.x += direction[0]
        self.y += direction[1]
        self.checkInBound()
        if not self.isNotCounter():
            self.x -= direction[0]
            self.y -= direction[1]
    
    def bulletMove(self):
        # move player's bullet
        if self.numOfBullet < 5:
            for i in range(self.totalBullet):
                if self.bullet[i] != []:
                    if self.bullet[i][2] == 1:
                        self.bullet[i][1] += 10
                        if self.bullet[i][1] > self.app.height or \
                            self.bullet[i][1] < 0:
                            self.bullet[i] = []
                            self.numOfBullet += 1
                    elif self.bullet[i][2] == 0:
                        self.bullet[i][1] -= 10
                        if self.bullet[i][1] > self.app.height or \
                            self.bullet[i][1] < 0:
                            self.bullet[i] = []
                            self.numOfBullet += 1
                    elif self.bullet[i][2] == 3:
                        self.bullet[i][0] += 10
                        if self.bullet[i][0] > self.app.width or \
                            self.bullet[i][0] < 0:
                            self.bullet[i] = []
                            self.numOfBullet += 1
                    elif self.bullet[i][2] == 2:
                        self.bullet[i][0] -= 10
                        if self.bullet[i][0] > self.app.width or \
                            self.bullet[i][0] < 0:
                            self.bullet[i] = []
                            self.numOfBullet += 1

    def isBulletCounter(self):
        for bullet in self.bullet:
            if self.bullet[bullet] != []:
                if self.app.player2.x-20 < self.bullet[bullet][0] \
                    < self.app.player2.x+20 and \
                    self.app.player2.y-20 < self.bullet[bullet][1] \
                    < self.app.player2.y+20:
                    self.bullet[bullet] = []
                    self.numOfBullet += 1
                    self.app.player2.health -= 1
                for (x, y) in self.app.background.bricks:
                    if self.app.background.bricks[(x, y)] > 0:
                        if self.bullet[bullet] != []:
                            if y*20-10 <= self.bullet[bullet][0] <= y*20+10 and\
                                x*20-10 <= self.bullet[bullet][1] <= x*20+10:
                                self.bullet[bullet] = []
                                self.numOfBullet += 1
                                self.app.background.bricks[(x, y)] -= 1
                                break

    def drawBullet(self, canvas):
        # draw the player's bullets
        if self.numOfBullet < 5:
            for i in range(self.totalBullet):
                if self.bullet[i] != []:
                    canvas.create_image(self.bullet[i][0], self.bullet[i][1], \
                                    image=ImageTk.PhotoImage(self.bulletImage))
    
    def drawTank(self, canvas):
        canvas.create_image(self.x, self.y, \
                image=ImageTk.PhotoImage(self.image))

class Tank2(Tank1):
    def __init__(self, app, imageOfTank, imageOfBullet):
        super().__init__(app, imageOfTank, imageOfBullet)
        # basic parameters
        self.x = self.app.width//2+100
        self.y = self.app.height - 50
        self.num = 0
        # images of tank2
        self.image0 = self.image1.rotate(180)
        self.image2 = self.image0.rotate(90)
        self.image3 = self.image2.rotate(180)
        # image of bullets2
        self.imageBulletDown = self.imageBulletUp.rotate(180)
        self.imageBulletLeft = self.imageBulletUp.rotate(90)
        self.imageBulletRight = self.imageBulletLeft.rotate(180)
        # initial tank image
        self.image = self.image1

    def shoot(self): 
        # initial coordinate of the play's bullet
        if self.numOfBullet > 0:
            self.numOfBullet -= 1
            self.imageWidth, self.imageHeight = self.image.size
            if self.num == 0:
                zx = self.x 
                zy = self.y + self.imageHeight//2
            elif self.num == 1:
                zx = self.x
                zy = self.y - self.imageHeight//2
            elif self.num == 2:
                zx = self.x + self.imageWidth//2
                zy = self.y
            elif self.num == 3:
                zx = self.x - self.imageWidth//2
                zy = self.y
        for i in range(self.totalBullet):
            if self.bullet[i] == []:
                self.bullet[i] = [zx, zy, self.num]
                break

    def bulletMove2(self):
        # move player's bullet
        if self.numOfBullet < 5:
            for i in range(self.totalBullet):
                if self.bullet[i] != []:
                    if self.bullet[i][2] == 0:
                        self.bullet[i][1] += 10
                        if self.bullet[i][1] > self.app.height or \
                            self.bullet[i][1] < 0:
                            self.bullet[i] = []
                            self.numOfBullet += 1
                    elif self.bullet[i][2] == 1:
                        self.bullet[i][1] -= 10
                        if self.bullet[i][1] > self.app.height or \
                            self.bullet[i][1] < 0:
                            self.bullet[i] = []
                            self.numOfBullet += 1
                    elif self.bullet[i][2] == 2:
                        self.bullet[i][0] += 10
                        if self.bullet[i][0] > self.app.width or \
                            self.bullet[i][0] < 0:
                            self.bullet[i] = []
                            self.numOfBullet += 1
                    elif self.bullet[i][2] == 3:
                        self.bullet[i][0] -= 10
                        if self.bullet[i][0] > self.app.width or \
                            self.bullet[i][0] < 0:
                            self.bullet[i] = []
                            self.numOfBullet += 1

    def isNotCounter(self):
        if self.app.player1.x-50 < self.x < self.app.player1.x+50 and \
            self.app.player1.y-50 < self.y < self.app.player1.y+50:
            return False
        return True

    def isBulletCounter(self):
        for bullet in self.bullet:
            if self.bullet[bullet] != []:
                if self.app.player1.x-20 < self.bullet[bullet][0] \
                    < self.app.player1.x+20 and \
                    self.app.player1.y-20 < self.bullet[bullet][1] \
                    < self.app.player1.y+20:
                    self.bullet[bullet] = []
                    self.numOfBullet += 1
                    self.app.player1.health -= 1
                for (x, y) in self.app.background.bricks:
                    if self.bullet[bullet] != []:
                        if self.app.background.bricks[(x, y)] > 0:
                            if y*20-10 <= self.bullet[bullet][0] <= y*20+10 and \
                                x*20-10 <= self.bullet[bullet][1] <= x*20+10:
                                self.bullet[bullet] = []
                                self.numOfBullet += 1
                                self.app.background.bricks[(x, y)] -= 1
                                break

class Background(Mode):
    def __init__(self, app):
        self.app = app
        self.bricks = dict()
        self.grass = dict()
        self.rocks = dict()
        self.river = dict()
        self.setBricks()
        self.setGrass()
        self.setRocks()
        self.setRiver()
        url = 'https://raw.githubusercontent.com/Yuhang-Liang/15-112-'+\
                'Homework9/master/222.png'
        self.imageCamp1 = self.loadImage(url)
        self.imageCamp2 = self.scaleImage(self.imageCamp1,1/10)

    def setBricks(self):
        # 15112
        for i in range(3):
            self.bricks[(4,10+i)] = 1
        for i in range(12):
            self.bricks[(4+i,12)] = 1
        for i in range(4):
            self.bricks[(3,10+i)] = 1
        for i in range(13):
            self.bricks[(3+i,13)] = 1
        #draw 1
        for i in range(5):
            self.bricks[(3,16+i)] = 1
        for i in range(5):
            self.bricks[(4+i,16)] = 1
        for i in range(5):
            self.bricks[(9,16+i)] = 1
        for i in range(7):
            self.bricks[(9+i,19)] = 1
        for i in range(4):
            self.bricks[(15,16+i)] = 1
        for i in range(4):
            self.bricks[(4,17+i)] = 1
        for i in range(4):
            self.bricks[(5+i,17)] = 1
        for i in range(3):
            self.bricks[(8,18+i)] = 1
        for i in range(6):
            self.bricks[(10+i,20)] = 1
        for i in range(3):
            self.bricks[(14,16+i)] = 1
        #draw 5 
        for i in range(3):
            self.bricks[(4,23+i)] = 1
        for i in range(12):
            self.bricks[(4+i,25)] = 1
        for i in range(4):
            self.bricks[(3,23+i)] = 1
        for i in range(13):
            self.bricks[(3+i,26)] = 1
        #draw another 1
        for i in range(3):
            self.bricks[(4,29+i)] = 1
        for i in range(12):
            self.bricks[(4+i,31)] = 1
        for i in range(4):
            self.bricks[(3,29+i)] = 1
        for i in range(13):
            self.bricks[(3+i,32)] = 1
        #draw 2 
        for i in range(4):
            self.bricks[(4,35+i)] = 1
        for i in range(6):
            self.bricks[(4+i,38)] = 1
        for i in range(4):
            self.bricks[(9,35+i)] = 1
        for i in range(6):
            self.bricks[(10+i,35)] = 1
        for i in range(5):
            self.bricks[(15,35+i)] = 1
        for i in range(5):
            self.bricks[(3,35+i)] = 1
        for i in range(7):
            self.bricks[(3+i,39)] = 1
        for i in range(5):
            self.bricks[(10,35+i)] = 1
        for i in range(4):
            self.bricks[(11+i,36)] = 1
        for i in range(3):
            self.bricks[(14,37+i)] = 1
        #draw H
        for i in range(12):
            self.bricks[(22+i,7)] = 1
        for i in range(12):
            self.bricks[(22+i,8)] = 1
        for i in range(3):
            self.bricks[(26,9+i)] = 1
        for i in range(3):
            self.bricks[(27,9+i)] = 1
        for i in range(8):
            self.bricks[(26+i,12)] = 1
        for i in range(8):
            self.bricks[(26+i,13)] = 1
        #draw A
        for i in range(5):
            self.bricks[(22,19+i)] = 1
        for i in range(5):
            self.bricks[(23,19+i)] = 1
        for i in range(10):
            self.bricks[(24+i,17)] = 1
        for i in range(10):
            self.bricks[(24+i,18)] = 1
        for i in range(10):
            self.bricks[(24+i,22)] = 1
        for i in range(10):
            self.bricks[(24+i,23)] = 1
        for i in range(3):
            self.bricks[(27,19+i)] = 1
        for i in range(5):
            self.bricks[(22,29+i)] = 1
        for i in range(5):
            self.bricks[(23,29+i)] = 1
        for i in range(10):
            self.bricks[(24+i,27)] = 1  
        for i in range(10):
            self.bricks[(24+i,28)] = 1
        for i in range(5):
            self.bricks[(32,29+i)] = 1
        for i in range(5):
            self.bricks[(33,29+i)] = 1
        #draw K
        for i in range(12):
            self.bricks[(22+i,37)] = 1
        for i in range(12):
            self.bricks[(22+i,38)] = 1
        for i in range(3):
            self.bricks[(28,39+i)] = 1
        for i in range(3):
            self.bricks[(29,39+i)] = 1
        for i in range(6):
            self.bricks[(22+i,42)] = 1
        for i in range(6):
            self.bricks[(22+i,43)] = 1
        for i in range(4):
            self.bricks[(30+i,42)] = 1
        for i in range(4):
            self.bricks[(30+i,43)] = 1
        #draw camp1
        for i in range(5):
            self.bricks[(43,5-i)] = 1
        for i in range(3):
            self.bricks[(44+i,1)] = 1
        for i in range(3):
            self.bricks[(44+i,5)] = 1
        #draw camp2
        for i in range(3):
            self.bricks[(i,48)] = 1
        for i in range(5):
            self.bricks[(3,48-i)] = 1
        for i in range(3):
            self.bricks[(i,44)] = 1

    def setGrass(self):
        for i in range(11):
            for j in range(2):
                self.grass[(18,5+i*4+j)] = 1
                self.grass[(19,5+i*4+j)] = 1
        
    def setRiver(self):
        for i in range(11):
            for j in range(2):
                self.river[(18,3+i*4+j)] = 1
                self.river[(19,3+i*4+j)] = 1
    
    def setRocks(self):
        for i in range(3):
            self.rocks[(18,i)] = 3
            self.rocks[(19,i)] = 3
        for i in range(3):
            self.rocks[(18,49-i)] = 3
            self.rocks[(19,49-i)] = 3
        #camp1 
        for i in range(7):
            self.rocks[(42,6-i)] = 3
        for i in range(4):
            self.rocks[(43+i,0)] = 3
        for i in range(4):
            self.rocks[(43+i,6)] = 3
        #camp2
        for i in range(4):
            self.rocks[(i,49)] = 3
        for i in range(7):
            self.rocks[(4,49-i)] = 3
        for i in range(4):
            self.rocks[(i,43)] = 3
            
    # helper function to draw cells
    def drawCell(self,canvas,row,col,fill='black'):
        cellWidth=20
        cellHeight=20
        canvas.create_rectangle(col*cellWidth,row*cellHeight,
                                (col+1)*cellWidth,(row+1)*cellHeight,
                                fill=fill,width=2,outline='grey')

    def drawBoard(self,canvas):
        for i in range(50):
            for j in range(50):
                self.drawCell(canvas,i,j)  

    def drawBricks(self,canvas):
        for brick in self.bricks:
            (i,j) = brick
            if self.bricks[brick] == 1:
                self.drawCell(canvas,i,j,'brown')
        
    def drawRiver(self,canvas):
        for river in self.river:
            (i,j) = river
            self.drawCell(canvas,i,j,'blue')

    def drawRock(self,canvas):
        for rock in self.rocks:
            (i,j) = rock
            if self.rocks[rock] > 0:
                self.drawCell(canvas,i,j,'white')

    def drawGrass(self,canvas):
        for grass in self.grass:
            (i,j) = grass
            self.drawCell(canvas,i,j,'green')

    def drawCamp(self,canvas):
        canvas.create_image(70,910,image= ImageTk.PhotoImage(self.imageCamp2))
        canvas.create_image(930,30,image= ImageTk.PhotoImage(self.imageCamp2))

class GameMode(Mode):
    def appStarted(mode):
        # images of tank1
        urlOfTank1 = 'https://tinyurl.com/tank1up'
        mode.image0 = mode.app.loadImage(urlOfTank1)
        mode.image0 = mode.app.scaleImage(mode.image0, 0.5)
        urlOfBullet1 = 'https://tinyurl.com/bullet-png'
        mode.imageBullet1 = mode.loadImage(urlOfBullet1)
        mode.imageBullet1 = mode.scaleImage(mode.imageBullet1, 0.2)
        # images of tank2
        urlOfTank1 = 'https://tinyurl.com/yyxcwvmj'
        mode.image1 = mode.app.loadImage(urlOfTank1)
        mode.image1 = mode.app.scaleImage(mode.image1, 0.5)
        urlOfBullet2 = 'https://tinyurl.com/bullet2222'
        mode.imageBullet2 = mode.loadImage(urlOfBullet2)
        mode.imageBullet2 = mode.scaleImage(mode.imageBullet2, 0.2)

        mode.player1 = Tank1(mode, mode.image0, mode.imageBullet1)
        mode.player2 = Tank2(mode, mode.image1, mode.imageBullet2)
        mode.background = Background(mode)

    def timerFired(mode):
        mode.player1.bulletMove()
        mode.player2.bulletMove2()
        mode.player1.isBulletCounter()
        mode.player2.isBulletCounter()
        if (mode.player2.health) <= 0:
            mode.app.setActiveMode(mode.app.endMode1)
        if (mode.player1.health) <= 0:
            mode.app.setActiveMode(mode.app.endMode2)
        for bullet in mode.player2.bullet:
            if mode.player2.bullet[bullet] != []:
                print("in condition1")
                print(mode.player2.bullet[bullet])
                if 30 <= mode.player2.bullet[bullet][0] <= 110 and \
                    880 <= mode.player2.bullet[bullet][1] <= 940:
                    mode.app.setActiveMode(mode.app.endMode1)
                if 890 <= mode.player2.bullet[bullet][0] <= 970 and \
                    0 <= mode.player2.bullet[bullet][1] <= 60:
                    mode.app.setActiveMode(mode.app.endMode2)
        for bullet in mode.player1.bullet:
            if mode.player1.bullet[bullet] != []:
                print("in condition2")
                print(mode.player1.bullet[bullet])
                if 30 <= mode.player1.bullet[bullet][0] <= 110 and \
                    880 <= mode.player1.bullet[bullet][1] <= 940:
                    mode.app.setActiveMode(mode.app.endMode1)
                if 890 <= mode.player1.bullet[bullet][0] <= 970 and \
                    0 <= mode.player1.bullet[bullet][1] <= 60:
                    mode.app.setActiveMode(mode.app.endMode2)
    
    def keyPressed(mode, event):
        if event.key == 'Up':
            direction = (0, -5)
            mode.player1.reDirect(0)
            mode.player1.move(direction)
        if event.key == 'Down':
            direction = (0, 5)
            mode.player1.reDirect(1)
            mode.player1.move(direction)
        if event.key == 'Left':
            direction = (-5, 0)
            mode.player1.reDirect(2)
            mode.player1.move(direction)
        if event.key == 'Right':
            direction = (5, 0)
            mode.player1.reDirect(3)
            mode.player1.move(direction)
        if event.key == 'w':
            direction = (0, -5)
            mode.player2.reDirect(1)
            mode.player2.move(direction)
        if event.key == 's':
            direction = (0, 5)
            mode.player2.reDirect(0)
            mode.player2.move(direction)
        if event.key == 'a':
            direction = (-5, 0)
            mode.player2.reDirect(3)
            mode.player2.move(direction)
        if event.key == 'd':
            direction = (5, 0)
            mode.player2.reDirect(2)
            mode.player2.move(direction)
        if event.key == 'h':
            mode.app.setActiveMode(app.helpMode)
        if event.key == 'Space':
            mode.player2.shoot()
        if event.key == '.':
            mode.player1.shoot()
    
    def redrawAll(mode, canvas):
        canvas.create_rectangle(0, 0, mode.width, mode.height, fill='black')
        mode.background.drawCell(canvas, 50, 50 ,fill='black')
        mode.background.drawBricks(canvas)
        mode.background.drawRiver(canvas)
        mode.player1.drawTank(canvas)
        mode.player2.drawTank(canvas)
        mode.player1.drawBullet(canvas)
        mode.player2.drawBullet(canvas)
        mode.background.drawGrass(canvas)
        mode.background.drawCamp(canvas)

# waited
class HelpMode(Mode):
        def appStarted(mode):
            URL=('https://s3.amazonaws.com/gameartpartnersimagehost/wp-'
                  +'content/uploads/2018/03/Game_Background_188.png')
            background=mode.loadImage(URL)
            URL2=('https://raw.githubusercontent.com/Yuhang-Liang'+
                  '/15-112-Homework9/master/1111.png')
            backImage=mode.loadImage(URL2)

            mode.backButton=mode.scaleImage(backImage,0.4)
            mode.background=mode.scaleImage(background,1.5)
            mode.ovalWidth=1
            mode.color='black'

        def inBackButtonBound(mode,x,y):
            r=60
            cx,cy=70,70
            if ((x-cx)**2+(y-cy)**2)**0.5<=r:
                return True

        def mouseMoved(mode,event):
            #red circle appears, if cursor into bound
            if mode.inBackButtonBound(event.x,event.y):
                mode.color='brown'
                mode.ovalWidth=10
            else:
                mode.color='black'
                mode.ovalWidth=0

        def mousePressed(mode,event):
            #return to game mode, if button clicked
            if mode.inBackButtonBound(event.x,event.y):
                mode.app.setActiveMode(mode.app.gameMode)

        def redrawAll(mode, canvas):
            image1=mode.background
            image2=mode.backButton
            canvas.create_image(500, 500, image=ImageTk.PhotoImage(image1))
            canvas.create_image(70,70,image=ImageTk.PhotoImage(image2))     
            canvas.create_oval (10,10,130,130,outline=mode.color,
                                width=mode.ovalWidth)
            color = random.choice(['black', 'grey', 'brown', 'white'])
            font = 'Arial 28 bold'
            canvas.create_text(mode.width/2, 150, text=
                               'Get Some Tips!', font='Helvetica 25 italic',
                               fill='black')
            canvas.create_text(mode.width/2, 250, text=
                               "Goal: bomb your enemy's base camp", font=font,
                               fill=color)
            canvas.create_text(mode.width/2, 350, text=
                "Player 1 press ↑↓←→ to move, press '.' to shoot", font=font,
                fill=color)
            canvas.create_text(mode.width/2, 450, text=
                "Player 2 press 'w,s,a,d' to move, press Space to shoot", 
                              font=font,fill=color)
            canvas.create_text(mode.width/2, 550, text=
                'Shoot the block to get rid of it', font=font,fill=color)
            canvas.create_text(mode.width/2, 650, text=
                'When your enemy looses his/her life, you win!', font=font,
                 fill=color)
            canvas.create_text(mode.width/2, 750, text=
                "When you destroy your enemy's base camp, you win!", font=font,
                 fill=color)

# finished
class InitialMode(Mode):
    def appStarted(mode):
        # For image
        urlOfBackground = 'https://tinyurl.com/y6o3b3sa'
        mode.image0 = mode.loadImage(urlOfBackground)
        mode.image0 = mode.scaleImage(mode.image0, 1.25)
        urlOfTank = 'https://tinyurl.com/StartModeTank-png'
        mode.image1 = mode.loadImage(urlOfTank)
        mode.image1 = mode.scaleImage(mode.image1, 1)
        mode.image1 = mode.image1.rotate(90)
        # For location parameters
        mode.tankHeight = 525
        mode.tankWidth = 300
    
    def keyPressed(mode, event):
        if event.key == 'Up':
            mode.tankHeight -= 80
            if mode.tankHeight < 525:
                mode.tankHeight = 525
        if event.key == 'Down':
            mode.tankHeight += 80
            if mode.tankHeight > 605:
                mode.tankHeight = 605
        if event.key == 'Enter':
            if mode.tankHeight == 605:
                mode.app.setActiveMode(mode.app.helpMode)
            elif mode.tankHeight == 525:
                mode.app.setActiveMode(mode.app.gameMode)
    
    def redrawAll(mode, canvas):
        # draw the background
        canvas.create_image(mode.width//2, mode.height//2, \
                            image=ImageTk.PhotoImage(mode.image0))
        # draw the tank
        canvas.create_image(mode.tankWidth, mode.tankHeight, \
                            image=ImageTk.PhotoImage(mode.image1))

# finished
class BeforeGame(Mode):
    def appStarted(mode):
        urlOfBackground = 'https://tinyurl.com/startgame-png'
        mode.image = mode.loadImage(urlOfBackground)
        mode.image = mode.scaleImage(mode.image, 1)
        mode.passTime = 0
        timerDelay = 10
    
    def timerFired(mode):
        mode.passTime += 1
        if mode.passTime > 20:
            mode.app.setActiveMode(mode.app.initialMode)
    
    def redrawAll(mode, canvas):
        # draw the background
        canvas.create_image(mode.width//2, mode.height//2, \
                            image=ImageTk.PhotoImage(mode.image))

# Top level ModalApp
class Battle112(ModalApp):
    def appStarted(app):
        app.beforeGame = BeforeGame()
        app.initialMode = InitialMode()
        app.helpMode = HelpMode()
        app.gameMode = GameMode()
        app.endMode1 = EndMode1()
        app.endMode2 = EndMode2()

        app.setActiveMode(app.beforeGame)

def runCreativeSidescroller():
    app = Battle112(width=1000, height=1000)

runCreativeSidescroller()