#################################################
# 15-112 Term Project
# mainGame.py
#
# Your name:Yuhang Liang
# Your andrew id:yuhangl
#################################################

import pygame as pg
import sys
from os import path
import random
import math
import time
from network import Network
import pygame.locals as pl
from textInput import TextInput

#################################################
# Helper functions
#################################################

# load images in 'image' folder
def loadImages(fileName):
    gameFolder = path.dirname(__file__)
    imageFolder = path.join(gameFolder, 'image')
    return pg.image.load(path.join(imageFolder, fileName))

# load and resize a list of images in 'image' folder
def loadGroupImages(fileList, newSize=(0, 0)):    
    gameFolder = path.dirname(__file__)
    imageFolder = path.join(gameFolder, 'image')
    initImages = []
    for i in range(len(fileList)):
        newImage = pg.image.load(path.join(imageFolder, \
                                            fileList[len(fileList)-i-1]))
        if newSize != (0, 0):
            newImage = pg.transform.scale(newImage, newSize)
        initImages.append(newImage)
    for i in fileList:
        newImage = pg.image.load(path.join(imageFolder, i))
        if newSize != (0, 0):
            newImage = pg.transform.scale(newImage, newSize)
        initImages.append(newImage)
    newImage = pg.image.load(path.join(imageFolder, fileList[-1]))
    if newSize != (0, 0):
            newImage = pg.transform.scale(newImage, newSize)
    initImages.append(newImage)
    return initImages

# load music in 'music' folder
def loadMusic(fileName):
    gameFolder = path.dirname(__file__)
    musicFolder = path.join(gameFolder, 'music')
    return pg.mixer.Sound(path.join(musicFolder, fileName))

# load score in 'score' folder
def loadScores(numOfPlayers):
    gameFolder = path.dirname(__file__)
    scoreFolder = path.join(gameFolder, "score")
    score = []
    if numOfPlayers == 1:
        scoreFile = path.join(scoreFolder, 'allScoreOnePlayer.txt')
    elif numOfPlayers == 2:
        scoreFile = path.join(scoreFolder, 'allScoreTwoPlayers.txt')
    with open(scoreFile, 'r') as f:
        for line in f.readlines():
            subScore = []
            list = line.split(":")
            for i in range(len(list)):
                if i == 0:
                    subScore.append(int(list[i]))
                else:
                    subScore.append(list[i][:-1])
            score.append(subScore)
    return sorted(score, reverse=True)

# recommend suitable level for users according to their previous highest score
def getLevel(name):
    score = loadScores(1)
    highestScore = -1
    for player in score:
        if player[1] == name or player[1] == name+"\n":
            if int(player[0]) > highestScore:
                highestScore = int(player[0])
    level1, level2, level3, level4, level5 = 100, 200, 400, 700, 1000
    if highestScore == -1: return 3
    elif highestScore < level1: return 1
    elif highestScore < level2: return 2
    elif highestScore < level3: return 3
    elif highestScore < level4: return 4
    elif highestScore < level5: return 5
    return 6

#################################################
# Main Game
#################################################

# define player1
class Player1(pg.sprite.Sprite):
    def __init__(self, mode, playerX, playerY):
        pg.sprite.Sprite.__init__(self)
        # initialize parameters
        self.speed = 5
        self.health = 13
        self.numOfBullets = 5
        self.numOfRockets = 3
        self.isShield = False
        self.isJump = False
        self.jumpCount = 10
        self.jumpTimes = 3
        self.isTrueShield = False
        self.trueShieldTimes = 3
        # load images and initialize location
        # image was downloaded from:
        # http://www.java1234.com/a/kaiyuan/sucai/2016/0907/6667.html
        image = loadImages('player1.png')
        self.newSize = (60, 60)
        self.image = pg.transform.scale(image, self.newSize)
        self.rect = self.image.get_rect()
        self.rect.centerx = playerX
        self.rect.centery = playerY


# define player2
class Player2(Player1):
    def __init__(self, mode, playerX, playerY):
        super().__init__(mode, playerX, playerY)
        # load images and initialize the size of image
        # image was downloaded from:
        # http://www.java1234.com/a/kaiyuan/sucai/2016/0907/6667.html
        image = loadImages('player2.png')
        self.newSize = (60, 60)
        self.image = pg.transform.scale(image, self.newSize)


# define shield
class Shield(pg.sprite.Sprite):
    def __init__(self, player1):
        pg.sprite.Sprite.__init__(self)
        # load images and initialize location
        # image was downloaded from:
        # http://www.java1234.com/a/kaiyuan/sucai/2016/0907/6667.html
        image = loadImages('shield.png')
        self.newSize = (75, 75)
        self.image = pg.transform.scale(image, self.newSize)
        self.rect = self.image.get_rect()
        self.rect.centerx = player1.rect.centerx
        self.rect.centery = player1.rect.centery
        self.player1 = player1
    
    def update(self):
        if self.player1.isShield or self.player1.isTrueShield:
            self.rect.centerx = self.player1.rect.centerx
            self.rect.centery = self.player1.rect.centery
        else:
            self.kill()


# define player1's bullets
class Player1Bullet(pg.sprite.Sprite):
    def __init__(self, player1, width, height):
        pg.sprite.Sprite.__init__(self)
        # load images and initialize location
        # image was downloaded from:
        # http://www.java1234.com/a/kaiyuan/sucai/2016/0907/6667.html
        image = loadImages('player1Bullet.png')
        self.newSize = (30, 30)
        self.image = pg.transform.scale(image, self.newSize)
        self.rect = self.image.get_rect()
        self.rect.centerx = player1.rect.centerx
        self.rect.bottom = player1.rect.top
        # initialize parameters
        self.margin = 15
        self.width = width
        self.height = height
        self.speed = 20
    
    def update(self):
        self.rect.top -= self.speed
        if self.rect.bottom < 0:
            game.player1.numOfBullets += 1
            self.kill()


# define player2's bullets
class Player2Bullet(pg.sprite.Sprite):
    def __init__(self, player2, width, height):
        pg.sprite.Sprite.__init__(self)
        # load images and initialize location
        # image was downloaded from:
        # http://www.java1234.com/a/kaiyuan/sucai/2016/0907/6667.html
        image = loadImages('player2Bullet.png')
        self.newSize = (30, 30)
        self.image = pg.transform.scale(image, self.newSize)
        self.rect = self.image.get_rect()
        self.rect.centerx = player2.rect.centerx
        self.rect.bottom = player2.rect.top
        # initialize parameters
        self.margin = 15
        self.width = width
        self.height = height
        self.speed = 20
    
    def update(self):
        self.rect.top -= self.speed
        if self.rect.bottom < 0:
            game.player2.numOfBullets += 1
            self.kill()


# define player1's rockets
class Player1Rocket(pg.sprite.Sprite):
    def __init__(self, width, height):
        pg.sprite.Sprite.__init__(self)
        self.speed = 30
        margin = 100
        # load images and initialize location
        # image was downloaded from:
        # http://www.java1234.com/a/kaiyuan/sucai/2016/0907/6667.html
        image = loadImages('rocket.gif')
        changeX = 50
        changeY = 1500
        self.newSize = (100, 100)
        self.image = pg.transform.scale(image, self.newSize)
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randrange(0, width)
        self.rect.top = random.randrange(height+changeX, height+changeY)
    
    def update(self):
        self.rect.top -= self.speed
        if self.rect.bottom < 0:
            self.kill()


# define player2's rockets
class Player2Rocket(pg.sprite.Sprite):
    def __init__(self, width, height):
        pg.sprite.Sprite.__init__(self)
        self.speed = 30
        margin = 100
        # load images and initialize location
        # image was downloaded from:
        # http://www.java1234.com/a/kaiyuan/sucai/2016/0907/6667.html
        image = loadImages('rocket2.gif')
        changeX = 50
        changeY = 1500
        self.newSize = (18, 30)
        self.image = pg.transform.scale(image, self.newSize)
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randrange(0, width)
        self.rect.top = random.randrange(height+changeX, height+changeY)
    
    def update(self):
        self.rect.top -= self.speed
        if self.rect.bottom < 0:
            self.kill()


# define enemies' bullets
class EnemyBullet(pg.sprite.Sprite):
    def __init__(self, player1, enemy, width, height):
        pg.sprite.Sprite.__init__(self)
        # initialize parameters
        self.width = width
        self.height = height
        self.speed = 5
        self.margin = 10
        # load images and initialize location
        # image was downloaded from:
        # http://www.java1234.com/a/kaiyuan/sucai/2016/0907/6667.html
        image = loadImages('enemyBullet.png')
        self.newSize = (10, 10)
        self.image = pg.transform.scale(image, self.newSize)
        self.rect = self.image.get_rect()
        self.rect.centerx = enemy.rect.centerx
        self.rect.top = enemy.rect.bottom
        # initialize direction
        horizontal = player1.rect.centerx-enemy.rect.centerx
        vertical = player1.rect.centery-enemy.rect.centery
        hypotenuse = (horizontal**2 + vertical**2) ** 0.5
        self.speedX = horizontal / hypotenuse * self.speed
        self.speedY = vertical / hypotenuse * self.speed
    
    def update(self):
        # do move
        self.rect.centerx += self.speedX
        self.rect.centery += self.speedY
        if self.rect.top > self.height + self.margin or \
           self.rect.left < -self.margin or \
           self.rect.right > self.width + self.margin or self.rect.bottom < 0:
            self.kill()


# define boss's bullets
class BossEnemyBullet(EnemyBullet):
    def __init__(self, player1, bossEnemy, width, height, x, y, \
                                        directionX, directionY):
        super().__init__(player1, bossEnemy, width, height)
        self.rect.centerx = x
        self.rect.centery = y
        self.speedX = self.speed * directionX
        self.speedY = self.speed * directionY


# define character's boxes
class CharacterBox(pg.sprite.Sprite):
    def __init__(self, image, x, y, size):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(image, size)
        self.rect = self.image.get_rect()
        self.rect.right = x
        self.rect.top = y


# define meteorolites
class Meteorolite(pg.sprite.Sprite):
    def __init__(self, width, height, meteorImages):
        pg.sprite.Sprite.__init__(self)
        self.width = width
        self.height = height
        # initialize parameters
        self.health = 1
        self.speed = 5
        self.range = 3
        self.points = 1
        self.speedX = random.randrange(-self.range, self.range)
        self.speedY = random.randrange(1, self.speed)
        self.rotSpeed = random.randrange(-self.speed, self.speed)
        # load images
        self.index = random.randrange(0, 4)
        self.image = meteorImages[self.index]
        self.orgImage = self.image
        self.rect = self.image.get_rect()
        self.margin = 50
        self.rect.centerx = random.randrange(-self.margin, width+self.margin)
        self.rect.centery = -self.margin
        self.rotation = 0
        # record the last rotating time
        self.lastTime = pg.time.get_ticks()
    
    def rotate(self):
        presentTime = pg.time.get_ticks()
        timeDifference = presentTime - self.lastTime
        resonableDifference = 200
        circle = 360
        if timeDifference > resonableDifference:
            self.lastTime = presentTime
            self.rotation = (self.rotation + self.rotSpeed) % circle
            newImage = pg.transform.rotate(self.orgImage, self.rotation)
            center = self.rect.center
            self.image = newImage
            self.rect = self.image.get_rect()
            self.rect.center = center

    def update(self):
        self.rotate()
        self.rect.centerx += self.speedX
        self.rect.centery += self.speedY
        if self.rect.top > self.height + self.margin or \
           self.rect.left < -self.margin or \
           self.rect.right > self.width + self.margin or self.health <= 0:
            self.rect.centerx = \
                        random.randrange(-self.margin, self.width+self.margin)
            self.rect.centery = -self.margin
            self.speedX = random.randrange(-self.range, self.range)
            self.speedY = random.randrange(1, self.speed)


class Dead(pg.sprite.Sprite):
    def __init__(self, image, center):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = center


# define normal enemy
class NormalEnemy(Meteorolite):
    def __init__(self, width, height, meteorImages, player1):
        super().__init__(width, height, meteorImages)
        # initialize parameters
        self.speed = random.randrange(5, 10)
        self.angle = math.radians(random.randrange(30, 60))
        self.startX = random.randint(0, width)
        self.startY = random.randint(-100, -self.margin)
        self.acceleration = -3.5
        self.sign = random.choice([-1, 1])
        self.startTime = pg.time.get_ticks()
        # load images and initialize location
        index = random.randrange(0,4)
        self.index = index
        self.image = meteorImages[index]
        # initialize health value
        if index == 2: self.health = 2
        elif index == 3: self.health = 3
        else: self.health = 1
        self.points = self.health
        # record the last rotating time
        self.lastTime = pg.time.get_ticks()
        self.player1 = player1

    def rotate(self):
        pass

    def update(self):
        presentTime = pg.time.get_ticks()
        timeDifference = 150.0
        timeChange = (presentTime - self.startTime) / timeDifference
        if timeChange > 0:
            self.speedX = self.sign * self.speed * math.cos(self.angle)
            self.speedY = -(self.speed * math.sin(self.angle) - \
                                            (self.acceleration * timeChange))
            newX = 2 * self.speedX * timeChange * math.cos(self.angle)
            halpAccelerationSquared = (self.acceleration * \
                                                (timeChange * timeChange))
            newY = (self.speedY * timeChange * math.sin(self.angle)) - \
                                                    halpAccelerationSquared
            newY = - abs(newY)/4
            self.rect.center = ((self.startX + int(newX), \
                                                self.startY - int(newY)))
        # if enemy move outside, redefine its location
        if self.rect.top > self.height + self.margin or \
           self.rect.left < -self.margin or \
           self.rect.right > self.width + self.margin or self.health <= 0:
            start = 5
            end = 10
            self.speed = random.randrange(start, end)
            start = 30
            end = 60
            self.angle = math.radians(random.randrange(start, end))
            self.startX = random.randint(0, self.width)
            start = 100
            self.startY = random.randint(-start, -self.margin)
            self.acceleration = -3.5
            self.sign = random.choice([-1, 1])
            self.startTime = pg.time.get_ticks()
        # launch bullets at regular intervals
        presentTime = pg.time.get_ticks()
        timeDifference = presentTime - self.lastTime
        resonableDifference = 5000
        if timeDifference > resonableDifference:
            self.lastTime = presentTime
            newBullet = EnemyBullet(self.player1, self, self.width, self.height)
            game.enemyBulletGroup.add(newBullet)
            game.allGroup.add(newBullet)


# define boss enemy
class BossEnemy(Meteorolite):
    def __init__(self, width, height, player1):
        pg.sprite.Sprite.__init__(self)
        # initialize parameters
        self.player1 = player1
        self.width = width
        self.height = height
        self.health = 150
        if numOfPlayers == 2:
            self.health = 250
        self.lastTime = pg.time.get_ticks()
        # initialize parameters
        self.speed = 1
        self.speedX = 0
        self.speedY = 1
        # load images and initialize location
        # image was downloaded from:
        # http://www.java1234.com/a/kaiyuan/sucai/2016/0907/6667.html
        image = loadImages('boss1.png')
        self.newSize = (600, 600)
        self.orgImage = pg.transform.scale(image, self.newSize)
        self.image = pg.transform.scale(image, self.newSize)
        self.rect = self.image.get_rect()
        self.rect.centerx = 0
        self.rect.bottom = 100
        self.points = 200
    
    def rotate(self):
        pass

    def update(self):
        if self.health <= 0:
            game.points += 200
            game.points2 += 200
            self.kill()
        # do move
        self.rotate()
        self.rect.centery += self.speedY
        margin0 = 100
        if self.rect.bottom > self.height//2: self.speedY = -1
        if self.rect.bottom < margin0: self.speedY = 1
        # launch bullets at regular intervals
        presentTime = pg.time.get_ticks()
        timeDifference = presentTime - self.lastTime
        resonableDifference = 10000
        rangeEnd = 9
        rotateDevide = 18
        minus = 100
        if timeDifference > resonableDifference:
            self.lastTime = presentTime
            numList = [math.pi/rotateDevide*i for i in range(1, rangeEnd)]
            for i in numList:
                r = self.newSize[0]//2 - minus
                directionX = math.cos(i)
                directionY = math.sin(i)
                x = self.rect.centerx + r * directionX
                y = self.rect.centery + r * directionY
                newBullet = BossEnemyBullet(self.player1, self, self.width, \
                                    self.height, x, y, directionX, directionY)
                game.enemyBulletGroup.add(newBullet)
                game.allGroup.add(newBullet)


# define pictures in the start of the game
class InitImage(pg.sprite.Sprite):
    def __init__(self, width, height, image):
        pg.sprite.Sprite.__init__(self)
        self.rect = image.get_rect()
        self.rect.centerx = width
        self.rect.centery = height
        self.image = image
        self.count = 0


# define the custom mouse
class Mouse(pg.sprite.Sprite):
    def __init__(self, width, height, image):
        pg.sprite.Sprite.__init__(self)
        self.rect = image.get_rect()
        self.rect.centerx = width
        self.rect.centery = height
        self.image = image

    def update(self):
        pos = pg.mouse.get_pos()
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]


# define the explosion effect
class Explosion(pg.sprite.Sprite):
    def __init__(self, images, center):
        pg.sprite.Sprite.__init__(self)
        self.images = images
        self.image = images[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.index = 0
        self.lastUpdate = pg.time.get_ticks()
        self.updateTimeInterval = 80
    
    def update(self):
        presentTime = pg.time.get_ticks()
        if presentTime - self.lastUpdate > self.updateTimeInterval:
            self.lastUpdate = presentTime
            self.index += 1
            if self.index == len(self.images):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.images[self.index]
                self.rect = self.image.get_rect()
                self.rect.center = center


# define the start of the game
class IntroGameMode:
    def __init__(mode, width, height):
        # initialize pygame and create game window
        pg.init()
        pg.mixer.init()
        pg.mouse.set_visible(0)
        mode.width = width
        mode.height = height
        mode.screen = pg.display.set_mode([width, height])
        pg.display.set_caption('Interstellar')
        mode.clock = pg.time.Clock()
        mode.FPS = 25
        mode.isGameRunning = True
        mode.lastUpadate = pg.time.get_ticks()
        mode.index = 0
        mode.isInit1Running = True
        mode.isInit2Running = False
        mode.isInit3Running = False
        mode.isInit4Running = False
        # initialize music
        # music was downloaded from:
        # https://mp3.pm/song/84656858/Two_Steps_From_Hell_Battlecry_-_Star_Sky/
        mode.BMG = loadMusic('Two Steps From Hell - Star Sky.wav')
        mode.BMG.play()
        # initialize sprite groups
        mode.allGroup = pg.sprite.Group()
        mode.initGroup = pg.sprite.Group()
        mode.mouseGroup = pg.sprite.Group()
        # initialize background
        mode.background = loadImages('blackBackground.png')
        mode.backgroundRect = mode.background.get_rect()
        mode.backgroundRect.x = 0
        mode.backgroundRect.y = 0
        newBackgroundSize = (1000, 1000)
        mode.background = pg.transform.scale(mode.background, newBackgroundSize)
        # initialize animation
        mode.init1List = ['init1.gif', 'init2.gif', 'init3.gif', 'init4.gif',
                      'init5.gif', 'init6.gif', 'init7.gif', 'init8.gif',
                      'init9.gif', 'init10.gif', 'init11.gif']
        # image was downloaded from:
        # https://ru-bykov.livejournal.com/3941071.html
        mode.init2List = ['2init1.png', '2init2.png', '2init3.png', \
                    '2init4.png', '2init5.png', '2init6.png', '2init7.png',\
                    '2init8.png', '2init9.png', '2init10.png', '2init11.png']
        mode.init3List = ['3init1.png', '3init2.png', '3init3.png', \
                    '3init4.png', '3init5.png', '3init6.png', '3init7.png',\
                    '3init8.png', '3init9.png', '3init10.png', '3init11.png']
        # image was downloaded from:
        # https://www.kinokopilka.pro/movies/23191-igra-endera?page=2
        mode.init4List = ['4init1.png', '4init2.png', '4init3.png', \
                    '4init4.png', '4init5.png', '4init6.png', '4init7.png',\
                    '4init8.png', '4init9.png', '4init10.png', '4init11.png']
        mode.initImages = loadGroupImages(mode.init1List)

        mode.newInit = InitImage(width//2, height//2, \
                                        mode.initImages[mode.index])
        mode.allGroup.add(mode.newInit)
        mode.initGroup.add(mode.newInit)
        mode.player1Name = None
        mode.player2Name = None

    def redrawAll(mode):
        for event in pg.event.get(): 
            if event.type == pg.QUIT: 
                self.isGameRunning = False
        mode.clock.tick(mode.FPS)
        mode.screen.blit(mode.background, mode.backgroundRect)
        presentTime = pg.time.get_ticks()
        time = 150
        if presentTime - mode.lastUpadate > time:
            mode.lastUpadate = presentTime
            mode.newInit.kill()
            mode.index += 1
            mode.newInit = InitImage(mode.width//2, mode.height//2, \
                                            mode.initImages[mode.index])
            mode.allGroup.add(mode.newInit)
            mode.initGroup.add(mode.newInit)
            if mode.index >= len(mode.initImages)-1:
                mode.index = 0
                if mode.isInit1Running:
                    mode.isInit1Running = False
                    mode.isInit2Running = True
                    size = (960, 600)
                    mode.initImages = loadGroupImages(mode.init2List, size)
                elif mode.isInit2Running:
                    mode.isInit2Running = False
                    mode.isInit3Running = True
                    mode.initImages = loadGroupImages(mode.init3List)
                elif mode.isInit3Running:
                    mode.isInit3Running = False
                    mode.isInit4Running = True
                    size = (800, 600)
                    mode.initImages = loadGroupImages(mode.init4List, size)
                elif mode.isInit4Running:
                    mode.isGameRunning = False
        # update and draw sprite group
        mode.allGroup.update()
        mode.allGroup.draw(mode.screen)  
        pg.display.flip()


# define the splash game mode
class SplashGameMode:
    def __init__(mode, width, height):
        # initialize pygame and create game window
        pg.init()
        pg.mouse.set_visible(0)
        mode.width = width
        mode.height = height
        mode.screen = pg.display.set_mode([width, height])
        pg.display.set_caption('Interstellar')
        mode.clock = pg.time.Clock()
        mode.FPS = 25
        mode.isGameRunning = True
        mode.isTrueGameRunning = False
        mode.recommendedLevel = None
        # initialize sprite groups
        mode.allGroup = pg.sprite.Group()
        mode.initGroup = pg.sprite.Group()
        mode.mouseGroup = pg.sprite.Group()
        # initialize background
        # image was downloaded from:
        # http://pictures.4ever.eu/cartoons/digital-art/space-collision-226972
        mode.background = loadImages('splashBackground.png')
        mode.backgroundRect = mode.background.get_rect()
        mode.backgroundRect.x = 0
        mode.backgroundRect.y = 0
        newBackgroundSize = (1060, 600)
        mode.background = pg.transform.scale(mode.background, newBackgroundSize)
        # initialize buttons
        # image was downloaded from:
        # https://pngio.com/images/png-32423.html
        mode.buttonImages = loadImages('button.png')
        newButtonSize = (210, 80)
        mode.buttonWidth = newButtonSize[0]
        mode.buttonHeight = newButtonSize[1]
        mode.buttonImages = pg.transform.scale(mode.buttonImages, newButtonSize)
        diff = 100
        mode.level = InitImage(width//2, height//2-diff, mode.buttonImages)
        mode.onePlayer = InitImage(width//2, height//2, mode.buttonImages)
        mode.twoPlayer = InitImage(width//2, height//2+diff, mode.buttonImages)
        mode.help = InitImage(width//2, height//2+diff*2, mode.buttonImages)
        # image was downloaded from:
        # http://www.aigei.com/view/72299.html?order=name&page=
        mode.titleImages = loadImages('title.png')
        newTitleSize = (400, 60)
        location = 100
        mode.titleImages = pg.transform.scale(mode.titleImages, newTitleSize)
        mode.titleImages = InitImage(width//2, location, mode.titleImages)
        mode.allGroup.add(mode.level)
        mode.initGroup.add(mode.level)
        mode.allGroup.add(mode.onePlayer)
        mode.initGroup.add(mode.onePlayer)
        mode.allGroup.add(mode.twoPlayer)
        mode.initGroup.add(mode.twoPlayer)
        mode.allGroup.add(mode.help)
        mode.initGroup.add(mode.help)
        mode.allGroup.add(mode.titleImages)
        mode.initGroup.add(mode.titleImages)
        # image was downloaded from:
        # https://www.pngfind.com/mpng/iThwTJm_blue-plus-icon-add-new-button-
        # png-transparent/
        mode.changeImages = loadImages('plus.png')
        changeSize = (40, 40)
        mode.changeWidth = changeSize[0]
        mode.changeHeight = changeSize[1]
        mode.changeImages = pg.transform.scale(mode.changeImages, changeSize)
        diff = 130
        location = 170
        mode.plus = InitImage(width//2+diff, location, mode.changeImages)
        # image was downloaded from:
        # http://www.downloadclipart.net/browse/10794/minus-button-clipart
        mode.changeImages = loadImages('minus.png')
        mode.changeImages = pg.transform.scale(mode.changeImages, changeSize)
        location = 220
        mode.minus = InitImage(width//2+diff, location, mode.changeImages)
        mode.allGroup.add(mode.plus)
        mode.initGroup.add(mode.plus)
        mode.allGroup.add(mode.minus)
        mode.initGroup.add(mode.minus)
        # initialize mouse sprite
        # image was downloaded from:
        # https://www.trzcacak.rs/so/cool-cursor/
        mouse = loadImages('mouse.png')
        newSize = (15, 25)
        mouse = pg.transform.scale(mouse, newSize)
        mode.mouse = Mouse(width//2, height//2, mouse)
        mode.allGroup.add(mode.mouse)
        mode.mouseGroup.add(mode.mouse)
        mode.lastPressed = pg.time.get_ticks()

    def mousePressed(mode):
        global numOfPlayers
        pos = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()
        if mode.onePlayer.rect.centerx-mode.buttonWidth//2 < pos[0] < \
            mode.onePlayer.rect.centerx+mode.buttonWidth//2 and \
            mode.onePlayer.rect.centery-mode.buttonHeight//2 < pos[1] < \
            mode.onePlayer.rect.centery+mode.buttonHeight//2:
            if click[0] == 1:
                mode.isGameRunning = False
                mode.isTrueGameRunning = True
                initGame.BMG.stop()
                numOfPlayers = 1
                isGameRunning = True
        elif mode.twoPlayer.rect.centerx-mode.buttonWidth//2 < pos[0] < \
            mode.twoPlayer.rect.centerx+mode.buttonWidth//2 and \
            mode.twoPlayer.rect.centery-mode.buttonHeight//2 < pos[1] < \
            mode.twoPlayer.rect.centery+mode.buttonHeight//2:
            if click[0] == 1:
                mode.isGameRunning = False
                mode.isTrueGameRunning = True
                initGame.BMG.stop()
                numOfPlayers = 2
                isGameRunning = True
        elif mode.help.rect.centerx-mode.buttonWidth//2 < pos[0] < \
            mode.help.rect.centerx+mode.buttonWidth//2 and \
            mode.help.rect.centery-mode.buttonHeight//2 < pos[1] < \
            mode.help.rect.centery+mode.buttonHeight//2:
            if click[0] == 1:
                mode.isGameRunning = False
                helpMode.isGameRunning = True
        elif mode.level.rect.centerx-mode.buttonWidth//2 < pos[0] < \
            mode.level.rect.centerx+mode.buttonWidth//2 and \
            mode.level.rect.centery-mode.buttonHeight//2 < pos[1] < \
            mode.level.rect.centery+mode.buttonHeight//2:
            if click[0] == 1 and mode.recommendedLevel == None:
                textInput = TextInputMode(mode.width, mode.height)
                while textInput.isGameRunning == True:
                    textInput.redrawAll()
                name = textInput.textInput.input_string
                mode.recommendedLevel = getLevel(name)
        elif mode.plus.rect.centerx-mode.changeWidth//2 < pos[0] < \
            mode.plus.rect.centerx+mode.changeWidth//2 and \
            mode.plus.rect.centery-mode.changeHeight//2 < pos[1] < \
            mode.plus.rect.centery+mode.changeHeight//2:
            if click[0] == 1 and mode.recommendedLevel != None:
                presentPressed = pg.time.get_ticks()
                diff = 200
                if presentPressed - mode.lastPressed > diff:
                    mode.lastPressed = presentPressed
                    maxLevel = 6
                    if mode.recommendedLevel < maxLevel: 
                        mode.recommendedLevel += 1
        elif mode.minus.rect.centerx-mode.changeWidth//2 < pos[0] < \
            mode.minus.rect.centerx+mode.changeWidth//2 and \
            mode.minus.rect.centery-mode.changeHeight//2 < pos[1] < \
            mode.minus.rect.centery+mode.changeHeight//2:
            if click[0] == 1 and mode.recommendedLevel != None:
                presentPressed = pg.time.get_ticks()
                diff = 200
                if presentPressed - mode.lastPressed > diff:
                    mode.lastPressed = presentPressed
                    if mode.recommendedLevel > 1: 
                        mode.recommendedLevel -= 1

    def redrawAll(mode):
        for event in pg.event.get(): 
            if event.type == pg.QUIT: 
                self.isGameRunning = False
        mode.clock.tick(mode.FPS)
        mode.screen.blit(mode.background, mode.backgroundRect)
        mode.mousePressed()
        # update and draw sprite group
        mode.allGroup.update()
        mode.allGroup.draw(mode.screen)  
        # draw texts on the buttons
        fontName = pg.font.match_font('arial')
        fontSize = 33
        font = pg.font.Font(fontName, fontSize)
        # read the players' input
        if mode.recommendedLevel == None:
            text = "Enter name"
        else:
            text = f"Level: {mode.recommendedLevel}"
        white = (255, 255, 255)
        diff = 100
        textSurface = font.render(text, True, white)
        textRect = textSurface.get_rect()
        textRect.center = (mode.width//2, mode.height//2-diff)
        mode.screen.blit(textSurface, textRect)
        # draw the text on the screen
        textSurface = font.render('1 Player', True, white)
        textRect = textSurface.get_rect()
        textRect.center = (mode.width//2, mode.height//2)
        mode.screen.blit(textSurface, textRect)
        textSurface = font.render('2 Players', True, white)
        textRect = textSurface.get_rect()
        textRect.center = (mode.width//2, mode.height//2+diff)
        mode.screen.blit(textSurface, textRect)
        textSurface = font.render('Help', True, white)
        textRect = textSurface.get_rect()
        textRect.center = (mode.width//2, mode.height//2+diff*2)
        mode.screen.blit(textSurface, textRect)
        # draw texts on the title
        fontSize = 40
        font = pg.font.Font(fontName, fontSize)
        textSurface = font.render('Interstellar', True, white)
        textRect = textSurface.get_rect()
        location = 100
        textRect.center = (mode.width//2, location)
        mode.screen.blit(textSurface, textRect)        

        pg.display.flip()


class TextInputMode:
    def __init__(mode, width, height):
        pg.init()
        mode.width = width
        mode.height = height
        mode.screen = pg.display.set_mode([width, height])
        pg.display.set_caption('Enter your name ---> Press Enter to record')
        mode.clock = pg.time.Clock()
        mode.FPS = 25
        mode.isGameRunning = True
        mode.textInput = TextInput()
        # initialize background
        # image was downloaded from:
        # https://www.wired.com/2017/06/tim-peake-iss-photos/
        mode.background = loadImages('backgroundOfTextInput.png')
        mode.backgroundRect = mode.background.get_rect()
        mode.backgroundRect.x = 0
        mode.backgroundRect.y = 0
        newBackgroundSize = (901, 600)
        mode.background = pg.transform.scale(mode.background, newBackgroundSize)
    
    def keyPressed(mode):
        keys = pg.key.get_pressed()
        if keys[pg.K_RETURN]:
            mode.isGameRunning = False 

    def redrawAll(mode):
        mode.screen.blit(mode.background, mode.backgroundRect)
        events = pg.event.get()
        for event in events: 
            if event.type == pg.QUIT: 
                mode.isGameRunning = False
        mode.clock.tick(mode.FPS)
        mode.textInput.update(events) 
        mode.keyPressed()
        locationOfText = (10, 10)
        mode.screen.blit(mode.textInput.get_surface(), locationOfText)

        pg.display.flip()

# define the help mode
class HelpMode:
    def __init__(mode, width, height):
        # initialize pygame and create game window
        pg.init()
        pg.mouse.set_visible(0)
        mode.width = width
        mode.height = height
        mode.screen = pg.display.set_mode([width, height])
        pg.display.set_caption('Interstellar')
        mode.clock = pg.time.Clock()
        mode.FPS = 25
        mode.isGameRunning = False
        # initialize sprite groups
        mode.allGroup = pg.sprite.Group()
        mode.initGroup = pg.sprite.Group()
        mode.mouseGroup = pg.sprite.Group()
        # initialize background
        # background was downloaded from:
        # https://www.origo.hu/tudomany/20150619-galaxis-csillag-univerzum-
        # vilagur-felfedezes.html
        mode.background = loadImages('help.png')
        mode.backgroundRect = mode.background.get_rect()
        mode.backgroundRect.x = 0
        mode.backgroundRect.y = 0
        newBackgroundSize = (600, 600)
        mode.background = pg.transform.scale(mode.background, newBackgroundSize)
        # initialize button
        # image was downloaded from:
        # http://www.aigei.com/s?q=quit+button
        mode.buttonImages = loadImages('exit.png')
        newButtonSize = (140, 32)
        mode.buttonWidth = newButtonSize[0]
        mode.buttonHeight = newButtonSize[1]
        mode.buttonImages = pg.transform.scale(mode.buttonImages, newButtonSize)
        diff0 = 80
        diff1 = 30
        mode.button = InitImage(width-diff0, height-diff1, mode.buttonImages)
        mode.allGroup.add(mode.button)
        mode.mouseGroup.add(mode.button)
        # initialize mouse sprite
        # image was downloaded from:
        # https://www.trzcacak.rs/so/cool-cursor/
        mouse = loadImages('mouse.png')
        newSize = (15, 25)
        mouse = pg.transform.scale(mouse, newSize)
        mode.mouse = Mouse(width//2, height//2, mouse)
        mode.allGroup.add(mode.mouse)
        mode.mouseGroup.add(mode.mouse)
    
    def mousePressed(mode):
        pos = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()
        if mode.button.rect.centerx-mode.buttonWidth//2 < pos[0] < \
            mode.button.rect.centerx+mode.buttonWidth//2 and \
            mode.button.rect.centery-mode.buttonHeight//2 < pos[1] < \
            mode.button.rect.centery+mode.buttonHeight//2:
            if click[0] == 1:
                mode.isGameRunning = False
                splashGame.isGameRunning = True
    
    def redrawAll(mode):
        for event in pg.event.get(): 
            if event.type == pg.QUIT: 
                self.isGameRunning = False
        mode.clock.tick(mode.FPS)
        mode.screen.blit(mode.background, mode.backgroundRect)
        mode.mousePressed()
        mode.allGroup.update()
        mode.allGroup.draw(mode.screen)  

        pg.display.flip()
        

# define the ranking mode
class RankingMode(HelpMode):
    def __init__(mode, width, height):
        # initialize pygame and create game window
        super().__init__(width, height)
        mode.isGameRunning = False
        # initialize background
        # image was downloaded from:
        # https://phys.org/news/2019-07-einstein-relativity-theory.html
        mode.background = loadImages('rankingBackground.png')
        mode.backgroundRect = mode.background.get_rect()
        mode.backgroundRect.x = 0
        mode.backgroundRect.y = 0
        newBackgroundSize = (1104, 600)
        mode.background = pg.transform.scale(mode.background, newBackgroundSize)

    def mousePressed(mode):
        pos = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()
        if mode.button.rect.centerx-mode.buttonWidth//2 < pos[0] < \
            mode.button.rect.centerx+mode.buttonWidth//2 and \
            mode.button.rect.centery-mode.buttonHeight//2 < pos[1] < \
            mode.button.rect.centery+mode.buttonHeight//2:
            if click[0] == 1:
                mode.isGameRunning = False
                gameEndMode.isGameRunning = True

    def redrawAll(mode):
        for event in pg.event.get(): 
            if event.type == pg.QUIT: 
                self.isGameRunning = False
        mode.clock.tick(mode.FPS)
        mode.screen.blit(mode.background, mode.backgroundRect)
        mode.mousePressed()
        # initialize the ranking text
        fontName = pg.font.match_font('arial')
        fontSize = 33
        font = pg.font.Font(fontName, fontSize)
        score = loadScores(numOfPlayers)
        length = len(score)
        maxLength = 10
        white = (255, 255, 255)
        if length > maxLength: length = maxLength
        basicHeight = 170
        plusHeight = 40
        for i in range(length):
            textSurface = font.render(\
             f'NO.{i} ---> {score[i][1]}: {score[i][0]}', True, white)
            textRect = textSurface.get_rect()
            textRect.center = (mode.width//2, basicHeight+plusHeight*i)
            mode.screen.blit(textSurface, textRect)
        # draw texts on the title
        fontSize = 40
        font = pg.font.Font(fontName, fontSize)
        if numOfPlayers == 1:
            textSurface = font.render('One Player Mode Ranking', True, white)
        else:
            textSurface = font.render('Two Players Mode Ranking', True, white)
        textRect = textSurface.get_rect()
        location = 100
        textRect.center = (mode.width//2, location)
        mode.screen.blit(textSurface, textRect)

        mode.allGroup.update()
        mode.allGroup.draw(mode.screen)  

        pg.display.flip()


# define the end of the game
class GameEndMode(SplashGameMode):
    def __init__(mode, width, height):
        super().__init__(width, height)
        # initialize background
        # image was downloaded from:
        # https://wallpaperscraft.com/download/battlefleet_gothic_armada_
        # warhammer_40k_black_legion_110453/1280x800
        mode.background = loadImages('gameOver.png')
        mode.backgroundRect = mode.background.get_rect()
        mode.backgroundRect.x = 0
        mode.backgroundRect.y = 0
        mode.isGameRunning = False
        newBackgroundSize = (1060, 600)
        mode.level.kill()
        mode.minus.kill()
        mode.plus.kill()
        mode.background = pg.transform.scale(mode.background, newBackgroundSize)
        mode.clickTimes = 0

    def mousePressed(mode):
        pos = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()
        if mode.onePlayer.rect.centerx-mode.buttonWidth//2 < pos[0] < \
            mode.onePlayer.rect.centerx+mode.buttonWidth//2 and \
            mode.onePlayer.rect.centery-mode.buttonHeight//2 < pos[1] < \
            mode.onePlayer.rect.centery+mode.buttonHeight//2:
            if click[0] == 1:
                mode.isGameRunning = False
                game.BMG.stop()
                initGame.BMG.play()
        elif mode.twoPlayer.rect.centerx-mode.buttonWidth//2 < pos[0] < \
            mode.twoPlayer.rect.centerx+mode.buttonWidth//2 and \
            mode.twoPlayer.rect.centery-mode.buttonHeight//2 < pos[1] < \
            mode.twoPlayer.rect.centery+mode.buttonHeight//2:
            if click[0] == 1:
                mode.clickTimes += 1
                gameFolder = path.dirname(__file__)
                scoreFolder = path.join(gameFolder, "score")
                if mode.clickTimes == 1:
                    if numOfPlayers == 1:
                        scoreFile = path.join(scoreFolder, \
                                                    'allScoreOnePlayer.txt')
                        textInput = TextInputMode(mode.width, mode.height)
                        while textInput.isGameRunning == True:
                            textInput.redrawAll()
                        name = textInput.textInput.input_string
                        content = f"{game.points}:{name}\n"
                        with open(scoreFile, 'a') as f:
                            f.write(content)
                    else:
                        scoreFile = path.join(scoreFolder, \
                                                    'allScoreTwoPlayers.txt')
                        textInput = TextInputMode(mode.width, mode.height)
                        while textInput.isGameRunning == True:
                            textInput.redrawAll()
                        player1Name = textInput.textInput.input_string
                        textInput = TextInputMode(mode.width, mode.height)
                        while textInput.isGameRunning == True:
                            textInput.redrawAll()
                        player2Name = textInput.textInput.input_string
                        content0 = f"{game.points}:{player1Name}\n"
                        content1 = f"{game.points2}:{player2Name}\n"
                        with open(scoreFile, 'a') as f:
                            f.write(content0)
                            f.write(content1)
        elif mode.help.rect.centerx-mode.buttonWidth//2 < pos[0] < \
            mode.help.rect.centerx+mode.buttonWidth//2 and \
            mode.help.rect.centery-mode.buttonHeight//2 < pos[1] < \
            mode.help.rect.centery+mode.buttonHeight//2:
            if click[0] == 1:
                mode.isGameRunning = False
                rankingMode.isGameRunning = True

    def redrawAll(mode):
        for event in pg.event.get(): 
            if event.type == pg.QUIT: 
                self.isGameRunning = False
        mode.clock.tick(mode.FPS)
        mode.screen.blit(mode.background, mode.backgroundRect)
        mode.mousePressed()
        # update and draw sprite group
        mode.allGroup.update()
        mode.allGroup.draw(mode.screen)  
        # draw texts on the buttons
        fontName = pg.font.match_font('arial')
        font = pg.font.Font(fontName, 33)
        textSurface = font.render('Go Back', True, (255, 255, 255))
        textRect = textSurface.get_rect()
        textRect.center = (mode.width//2, mode.height//2)
        mode.screen.blit(textSurface, textRect)
        textSurface = font.render('Record score', True, (255, 255, 255))
        textRect = textSurface.get_rect()
        textRect.center = (mode.width//2, mode.height//2+100)
        mode.screen.blit(textSurface, textRect)
        textSurface = font.render('Ranking', True, (255, 255, 255))
        textRect = textSurface.get_rect()
        textRect.center = (mode.width//2, mode.height//2+200)
        mode.screen.blit(textSurface, textRect)
        # draw texts on the title
        font = pg.font.Font(fontName, 40)
        if numOfPlayers == 1:
            textSurface = font.render(f'Player 1: {game.points}', \
                                                    True, (255, 255, 255))
        else:
            textSurface = font.render(\
                f'Player 1: {game.points}  Player 2: {game.points2}', \
                True, (255, 255, 255))
        textRect = textSurface.get_rect()
        textRect.center = (mode.width//2, 100)
        mode.screen.blit(textSurface, textRect)

        pg.display.flip()


# define main game class
class GameMode:
    def __init__(mode, width, height, numOfPlayers):
        # initialize pygame and create game window
        pg.init()
        pg.mixer.init()
        mode.width = width
        mode.height = height
        mode.screen = pg.display.set_mode([width, height])
        pg.display.set_caption('Interstellar')
        mode.clock = pg.time.Clock()
        mode.isGameRunning = splashGame.isTrueGameRunning
        mode.gameOver = False
        mode.FPS = 25
        margin = 20
        mode.mount = 0
        mode.points = 0
        mode.points2 = 0
        mode.numOfPlayers = numOfPlayers
        if mode.numOfPlayers > 1:
            mode.network = Network()
            # waiting for another player
            mode.waitingImages = loadImages('waiting.png')
            mode.waitingImagesRect = mode.waitingImages.get_rect()
            mode.waitingImagesRect.centerx = mode.width//2
            mode.waitingImagesRect.centery = mode.height//2
            isWaiting = [0, 0, 0, 0]
            while isWaiting == [0, 0, 0, 0]:
                order = [0, 0, 0, 0]
                isWaiting = mode.network.send(order)
                print("iswaiting")
            mode.orderFromServer = isWaiting
        # initialize music
        # music was downloaded from:
        # https://audiograb.com/ETBdO7FxCd
        mode.BMG = loadMusic('background.wav')
        mode.BMG.play()
        # initialize sprite groups
        mode.allGroup = pg.sprite.Group()
        mode.playerGroup = pg.sprite.Group()
        mode.player1Group = pg.sprite.Group()
        mode.player2Group = pg.sprite.Group()
        mode.enemyGroup = pg.sprite.Group()
        mode.bossEnemyGroup = pg.sprite.Group()
        mode.meteorGroup = pg.sprite.Group()
        mode.enemyBulletGroup = pg.sprite.Group()
        mode.player1BulletGroup = pg.sprite.Group()
        mode.player1RocketGroup = pg.sprite.Group()
        mode.player2BulletGroup = pg.sprite.Group()
        mode.player2RocketGroup = pg.sprite.Group()
        mode.playerBulletGroup = pg.sprite.Group()
        mode.playerRocketGroup = pg.sprite.Group()
        mode.shieldGroup = pg.sprite.Group()
        mode.characterBoxGroup = pg.sprite.Group()
        mode.shieldLogGroup = pg.sprite.Group()
        mode.rocketLogGroup = pg.sprite.Group()
        mode.jumpLogGroup = pg.sprite.Group()
        mode.shieldLog2Group = pg.sprite.Group()
        mode.rocketLog2Group = pg.sprite.Group()
        mode.jumpLog2Group = pg.sprite.Group()
        mode.explosionGroup = pg.sprite.Group()
        mode.deadGroup = pg.sprite.Group()
        minusHeight = 200
        mode.player1 = Player1(mode, width//2-minusHeight, height-margin)
        # initialize boss enemy sprite
        mode.boss1 = BossEnemy(width, height, mode.player1)
        mode.bossEnemyGroup.add(mode.boss1)
        mode.allGroup.add(mode.boss1)
        # initialize player sprite
        mode.playerGroup.add(mode.player1)
        mode.player1Group.add(mode.player1)
        mode.allGroup.add(mode.player1)
        plusHeight = 200
        if numOfPlayers == 2:
            mode.player2 = Player2(mode, width//2+plusHeight, height-margin)
            mode.playerGroup.add(mode.player2)   
            mode.player2Group.add(mode.player2)
            mode.allGroup.add(mode.player2)
        # initialize meteor sprite
        gameFolder = path.dirname(__file__)
        imageFolder = path.join(gameFolder, 'image')
        mode.meteorImages = []
        # image was downloaded from:
        # http://www.java1234.com/a/kaiyuan/sucai/2016/0907/6667.html
        meteorList = ['meteor1.png', 'meteor2.png', \
                      'meteor3.png', 'meteor4.png']
        for m in meteorList:
            newImage = pg.image.load(path.join(imageFolder, m))
            mode.meteorImages.append(newImage)
        # image was downloaded from:
        # https://www.youtube.com/watch?v=AdG_ITCFHDI&list=PLsk-HSGFjnaH5yghzu7
        # PcOzm9NhsW0Urw&index=13
        mode.explosionImages = []
        explosionList = ['regularExplosion00.png', 'regularExplosion01.png',\
                        'regularExplosion02.png', 'regularExplosion03.png', \
                        'regularExplosion04.png', 'regularExplosion05.png',\
                        'regularExplosion06.png', 'regularExplosion07.png',\
                        'regularExplosion08.png']
        for e in explosionList:
            newImage = pg.image.load(path.join(imageFolder, e))
            newImageSize = (60, 60)
            newImage = pg.transform.scale(newImage, newImageSize)
            mode.explosionImages.append(newImage)
        # image was downloaded from: http://616pic.com/sucai/18mid5rnd.html
        newImage = loadImages("dead.png")
        newImageSize = (30, 30)
        newImage = pg.transform.scale(newImage, newImageSize)
        mode.deadImage = newImage
        if splashGame.recommendedLevel != None:
            numOfMeteor = splashGame.recommendedLevel * 5
        else: 
            numOfMeteor = 15
        if numOfPlayers == 2:
            if splashGame.recommendedLevel != None:
                times = 8
                numOfMeteor = splashGame.recommendedLevel * times
            else: 
                numOfMeteor = 25
        for _ in range(numOfMeteor):
            newMeteor = Meteorolite(width, height, mode.meteorImages)
            mode.allGroup.add(newMeteor)
            mode.meteorGroup.add(newMeteor)
        # initialize enemy sprite
        mode.enemyImages = []
        # image was downloaded from:
        # http://www.java1234.com/a/kaiyuan/sucai/2016/0907/6667.html
        enemyList = ['enemy1.png', 'enemy2.png', 'enemy3.png', 'enemy4.png']
        for e in enemyList:
            newImage = pg.image.load(path.join(imageFolder, e))
            newImageSize = (60, 60)
            newImage = pg.transform.scale(newImage, newImageSize)
            mode.enemyImages.append(newImage)
        if splashGame.recommendedLevel != None:
            times = 6
            numOfEnemy = splashGame.recommendedLevel * times
        else:
            numOfEnemy = 20
        if numOfPlayers == 2:
            if splashGame.recommendedLevel != None:
                times = 11
                numOfEnemy = splashGame.recommendedLevel * times
            else:   
                numOfEnemy = 30
        for _ in range(numOfEnemy):
            if mode.numOfPlayers > 1:
                player = [mode.player1, mode.player2]
                target = random.choice(player)
            else:
                target = mode.player1
            newEnemy = NormalEnemy(width, height, \
                                    mode.enemyImages, target)
            mode.allGroup.add(newEnemy)
            mode.enemyGroup.add(newEnemy)
        # load images
        gameFolder = path.dirname(__file__)
        imageFolder = path.join(gameFolder, 'image')
        # image was downloaded from:
        # https://opengameart.org/sites/default/files/Starbasesnow.png
        mode.background = pg.image.load(path.join(imageFolder, \
                                        'background.png')).convert()
        mode.backgroundRect = mode.background.get_rect()
        mode.backgroundRect.x = 0
        mode.backgroundRect.y = -1000
        newBackgroundSize = (1000, 2000)
        mode.background = pg.transform.scale(mode.background, newBackgroundSize)
        # initialize character box
        # image was downloaded from:
        # http://www.aigei.com/view/73255.html?order=name&page=5
        image0 = loadImages('characterBox.png')
        # image was downloaded from:
        # https://opengameart.org/sites/default/files/Starbasesnow.png
        image1 = loadImages('player1.png')
        mode.image2 = loadImages('green.png')
        # image was downloaded from:
        # http://www.sucai999.com/search/jinsedunpaihuizhang.html
        mode.image3 = loadImages('newShield.png')
        mode.image4 = loadImages('rocket.gif')
        # image was downloaded from:
        # http://www.kewynnpt.com/tag/exercise/
        mode.image5 = loadImages('jump.png')
        # image was downloaded from:
        # http://www.java1234.com/a/kaiyuan/sucai/2016/0907/6667.html
        image6 = loadImages('player2.png')
        mode.image7 = loadImages('rocket2.gif')
        location = (150, 59)
        minus = 3
        characterBox = CharacterBox(image0, mode.width-minus, 0, location)
        location = (30, 30)
        diff = 10
        character = CharacterBox(image1, mode.width-diff, diff, location)
        location = (130, 6)
        minus = 7
        diff = 48
        mode.liveRect = CharacterBox(mode.image2, mode.width-minus, \
                                                                diff, location)
        mode.characterBoxGroup.add(characterBox)
        mode.allGroup.add(characterBox)
        mode.characterBoxGroup.add(character)
        mode.allGroup.add(character)
        mode.characterBoxGroup.add(mode.liveRect)
        mode.allGroup.add(mode.liveRect)
        # draw the logos on the character box
        times = 13
        minus = 48
        numOfHeight = 5
        size = (10, 10)
        for i in range(mode.player1.trueShieldTimes):
            shield = CharacterBox(mode.image3, mode.width-minus-i*times, \
                                                            numOfHeight, size)
            mode.shieldLogGroup.add(shield)
            mode.allGroup.add(shield)
        minus = 38
        numOfHeight = 10
        size = (30, 30)
        for i in range(mode.player1.numOfRockets):
            rocket = CharacterBox(mode.image4, mode.width-minus-i*times, \
                                                            numOfHeight, size)
            mode.rocketLogGroup.add(rocket)
            mode.allGroup.add(rocket)
        minus = 45
        numOfHeight = 32
        size = (10, 10)
        for i in range(mode.player1.jumpTimes):
            jump = CharacterBox(mode.image5, mode.width-minus-i*times, \
                                                            numOfHeight, size)
            mode.jumpLogGroup.add(jump)
            mode.allGroup.add(jump)
        minus0 = 3
        minus1 = 10
        minus2 = 7
        numOfHeight0 = 60
        numOfHeight1 = 70
        numOfHeight2 = 130
        size0 = (150, 59)
        size1 = (30, 30)
        size2 = (130, 6)
        if mode.numOfPlayers == 2:
            characterBox2 = CharacterBox(image0, mode.width-minus0, \
                                                        numOfHeight0, size0)
            character2 = CharacterBox(image6, mode.width-minus1, \
                                                        numOfHeight1, size1)
            mode.liveRect1 = CharacterBox(mode.image2, mode.width-minus2, \
                                                        numOfHeight2, size2)
            mode.characterBoxGroup.add(characterBox2)
            mode.allGroup.add(characterBox2)
            mode.characterBoxGroup.add(character2)
            mode.allGroup.add(character2)
            mode.characterBoxGroup.add(mode.liveRect1)
            mode.allGroup.add(mode.liveRect1)
            times = 13
            minus0 = 48
            minus1 = 38
            minus2 = 45
            numOfHeight0 = 65
            numOfHeight1 = 70
            numOfHeight2 = 92
            size0 = (10, 10)
            size1 = (10, 6)
            for i in range(mode.player2.trueShieldTimes):
                shield = CharacterBox(mode.image3, mode.width-minus0-i*times, \
                                                            numOfHeight0, size0)
                mode.shieldLog2Group.add(shield)
                mode.allGroup.add(shield)
            for i in range(mode.player2.numOfRockets):
                rocket = CharacterBox(mode.image7, mode.width-minus1-i*times, \
                                                            numOfHeight1, size1)
                mode.rocketLog2Group.add(rocket)
                mode.allGroup.add(rocket)
            for i in range(mode.player2.jumpTimes):
                jump = CharacterBox(mode.image5, mode.width-minus2-i*times, \
                                                            numOfHeight2, size0)
                mode.jumpLog2Group.add(jump)
                mode.allGroup.add(jump)
        # define the time of last keyPressed
        mode.lastPressedSpace = pg.time.get_ticks()
        mode.lastPressedC = pg.time.get_ticks()
        mode.lastPressedS = pg.time.get_ticks()
        mode.lastPressedN = pg.time.get_ticks()
        mode.lastPressedJ = pg.time.get_ticks()
        mode.lastPressedK = pg.time.get_ticks()
        mode.lastPressedL = pg.time.get_ticks()
        mode.player1shieldTime = pg.time.get_ticks()
        mode.player1TrueShieldTime = pg.time.get_ticks()
        mode.player2shieldTime = pg.time.get_ticks()
        mode.player2TrueShieldTime = pg.time.get_ticks()

    def player1keyPressed(mode):
        # execute the player1's order
        order = [0, 0, 0, 0, 0, 0, 0, 0]
        for event in pg.event.get():
            if event.type == pg.QUIT:
                mode.isGameRunning = False
        keys = pg.key.get_pressed()
        if keys[pg.K_ESCAPE]:
            mode.isGameRunning = False
        if keys[pg.K_t]:
            help = HelpMode(mode.width, mode.height)
            help.isGameRunning = True
            while help.isGameRunning:
                help.redrawAll()
        if keys[pg.K_LEFT] and mode.player1.rect.centerx > 0:
            mode.player1.rect.centerx -= mode.player1.speed
            order[2] = 1
        if keys[pg.K_RIGHT] and mode.player1.rect.centerx < mode.width:
            mode.player1.rect.centerx += mode.player1.speed
            order[3] = 1
        if keys[pg.K_SPACE] and mode.player1.health > 0:
            presentPressedSpace = pg.time.get_ticks()
            timeInterval = 200
            if mode.player1.numOfBullets > 0 and \
                    presentPressedSpace-mode.lastPressedSpace > timeInterval:
                mode.player1.numOfBullets -= 1
                order[4] = 1
                mode.lastPressedSpace = presentPressedSpace
                newBullet = Player1Bullet(mode.player1, mode.width, mode.height)
                mode.allGroup.add(newBullet)
                mode.player1BulletGroup.add(newBullet)
                mode.playerBulletGroup.add(newBullet)
        if keys[pg.K_c] and mode.player1.health > 0:
            presentPressedC = pg.time.get_ticks()
            timeInterval = 500
            if mode.player1.numOfRockets > 0 and \
                    presentPressedC-mode.lastPressedC > timeInterval:
                order[7] = 1
                mode.lastPressedC = presentPressedC
                mode.player1.numOfRockets -= 1
                num = 40
                for _ in range(num):
                    newRocket = Player1Rocket(mode.width, mode.height)
                    mode.allGroup.add(newRocket)
                    mode.player1RocketGroup.add(newRocket)
                    mode.playerRocketGroup.add(newRocket)
        if keys[pg.K_z] and mode.player1.health > 0:
            presentPressedS = pg.time.get_ticks()
            timeInterval = 500
            if mode.player1.trueShieldTimes > 0 and \
                    presentPressedS-mode.lastPressedS > timeInterval:
                order[5] = 1
                mode.lastPressedS = presentPressedS
                mode.player1TrueShieldTime = pg.time.get_ticks()
                mode.player1.trueShieldTimes -= 1
                mode.player1.isTrueShield = True
                mode.shield = Shield(mode.player1)
                mode.allGroup.add(mode.shield)
                mode.shieldGroup.add(mode.shield)
        if not mode.player1.isJump:
            if keys[pg.K_UP]: order[0] = 1
            if keys[pg.K_UP] and mode.player1.rect.centery > 0:
                mode.player1.rect.centery -= mode.player1.speed
            if keys[pg.K_DOWN]: order[1] = 1
            if keys[pg.K_DOWN] and mode.player1.rect.centery < mode.height:
                mode.player1.rect.centery += mode.player1.speed
            if keys[pg.K_x]: order[6] = 1
            if keys[pg.K_x] and mode.player1.jumpTimes > 0 and \
                                                    mode.player1.health > 0:
                mode.player1.isShield = True
                mode.player1.isJump = True
                mode.player1.jumpTimes -= 1
                mode.shield = Shield(mode.player1)
                mode.allGroup.add(mode.shield)
                mode.shieldGroup.add(mode.shield)
                mode.player1shieldTime = pg.time.get_ticks()
        else:
            jumpMax = 10
            if mode.player1.jumpCount >= -jumpMax:
                neg = 1
                if mode.player1.jumpCount <= 0:
                    neg = -1
                square = 2
                root = 0.5
                mode.player1.rect.centery -= (mode.player1.jumpCount**square) \
                                                                * root * neg
                mode.player1.jumpCount -= 1
            else:
                mode.player1.isJump = False
                mode.player1.jumpCount = 10
                mode.player1shieldTime = pg.time.get_ticks()
        presentShield = pg.time.get_ticks()
        time = 2000
        if presentShield - mode.player1shieldTime > time and \
                        mode.player1.isShield == True:
            mode.player1shieldTime = presentShield
            mode.player1.isShield = False
        presentTrueShieldTime = pg.time.get_ticks()
        time0 = 6000
        if presentTrueShieldTime - mode.player1TrueShieldTime > time0 and \
            mode.player1.isTrueShield == True:
            mode.player1.isTrueShield = False
        # hand information from the server and transfer data to server
        if mode.numOfPlayers == 2:
            enemy = []
            meteor = []
            bullet = []
            player1 = [mode.player1.rect.centerx, mode.player1.rect.centery, \
                        mode.player1.numOfRockets, mode.player1.jumpTimes, 
                        mode.player1.trueShieldTimes]
            player2 = [mode.player2.rect.centerx, mode.player2.rect.centery, \
                        mode.player2.numOfRockets, mode.player2.jumpTimes, 
                        mode.player2.trueShieldTimes]
            player1Bullet = []
            player2Bullet = []
            player1Rocket = []
            player2Rocket = []
            shield = []
            boss = []
            explosions = []
            for i in mode.enemyGroup:
                subEnemy = [i.rect.centerx, i.rect.centery, i.index]
                enemy.append(subEnemy)
            for i in mode.meteorGroup:
                sMeteor = [i.rect.centerx, i.rect.centery, i.index, i.rotation]
                meteor.append(sMeteor)
            for i in mode.enemyBulletGroup:
                subBullet = [i.rect.centerx, i.rect.centery]
                bullet.append(subBullet)
            for i in mode.player1BulletGroup:
                subBullet = [i.rect.centerx, i.rect.centery]
                player1Bullet.append(subBullet)
            for i in mode.player2BulletGroup:
                subBullet = [i.rect.centerx, i.rect.centery]
                player2Bullet.append(subBullet)
            for i in mode.player1RocketGroup:
                subBullet = [i.rect.centerx, i.rect.centery]
                player1Rocket.append(subBullet)
            for i in mode.player2RocketGroup:
                subBullet = [i.rect.centerx, i.rect.centery]
                player2Rocket.append(subBullet)
            for i in mode.shieldGroup:
                subShield = [i.rect.centerx, i.rect.centery]
                shield.append(subShield)
            for i in mode.bossEnemyGroup:
                boss = [i.rect.centerx, i.rect.centery]
                boss.append(boss)
            for i in mode.explosionGroup:
                explosion = i.rect.center
                explosions.append(explosion)
            transferData = [order, enemy, meteor, bullet, player1, player2, \
                player1Bullet, player2Bullet, player1Rocket, player2Rocket, \
                shield, boss, explosions, mode.player1.health, \
                mode.player2.health, mode.points, mode.points2]
            dataFromServe = mode.network.send(transferData)
            if dataFromServe == None:
                dataFromServe = [[0, 0, 0, 0, 0, 0, 0, 0], [], [], [], 0]
            dataFromServe = dataFromServe[0]
            if dataFromServe[2] and mode.player2.rect.centerx > 0:
                mode.player2.rect.centerx -= mode.player2.speed
            if dataFromServe[3] and mode.player2.rect.centerx < mode.width:
                mode.player2.rect.centerx += mode.player2.speed
            if dataFromServe[4] and mode.player2.health > 0:
                if mode.player2.numOfBullets > 0:
                    mode.player2.numOfBullets -= 1
                    newBullet = Player2Bullet(mode.player2, mode.width, \
                                                                    mode.height)
                    mode.allGroup.add(newBullet)
                    mode.player2BulletGroup.add(newBullet)
                    mode.playerBulletGroup.add(newBullet)
            if dataFromServe[7] and mode.player2.health > 0:
                if mode.player2.numOfRockets > 0:
                    mode.player2.numOfRockets -= 1
                    num = 40
                    for _ in range(num):
                        newRocket = Player2Rocket(mode.width, mode.height)
                        mode.allGroup.add(newRocket)
                        mode.player2RocketGroup.add(newRocket)
                        mode.playerRocketGroup.add(newRocket)
            if dataFromServe[5] and mode.player2.health > 0:
                if mode.player2.trueShieldTimes > 0:
                    mode.player2TrueShieldTime = pg.time.get_ticks()
                    mode.player2.trueShieldTimes -= 1
                    mode.player2.isTrueShield = True
                    mode.shield = Shield(mode.player2)
                    mode.allGroup.add(mode.shield)
                    mode.shieldGroup.add(mode.shield)
            if not mode.player2.isJump:
                if dataFromServe[0] and mode.player2.rect.centery > 0:
                    mode.player2.rect.centery -= mode.player2.speed
                if dataFromServe[1] and mode.player2.rect.centery < mode.height:
                    mode.player2.rect.centery += mode.player2.speed
                if dataFromServe[6] and mode.player2.jumpTimes > 0 and \
                                    mode.player2.health > 0:
                    mode.player2.isShield = True
                    mode.player2.isJump = True
                    mode.player2.jumpTimes -= 1
                    mode.shield = Shield(mode.player2)
                    mode.allGroup.add(mode.shield)
                    mode.shieldGroup.add(mode.shield)
                    mode.player2shieldTime = pg.time.get_ticks()
            else:
                if mode.player2.jumpCount >= -10:
                    neg = 1
                    if mode.player2.jumpCount <= 0:
                        neg = -1
                    s = 2
                    root = 0.5
                    mode.player2.rect.centery -= (mode.player2.jumpCount**s) \
                                                                    * root * neg
                    mode.player2.jumpCount -= 1
                else:
                    mode.player2.isJump = False
                    mode.player2.jumpCount = 10
                    mode.player2shieldTime = pg.time.get_ticks()
            presentShield = pg.time.get_ticks()
            timeInterval = 2000
            if presentShield - mode.player2shieldTime > timeInterval and \
                            mode.player2.isShield == True:
                mode.player2shieldTime = presentShield
                mode.player2.isShield = False
            presentTrueShieldTime = pg.time.get_ticks()
            time = 6000
            if presentTrueShieldTime - mode.player2TrueShieldTime > time and \
                mode.player2.isTrueShield == True:
                mode.player2.isTrueShield = False
    
    def player2keyPressed(mode):
        order = [0, 0, 0, 0, 0, 0, 0, 0]
        for event in pg.event.get():
            if event.type == pg.QUIT:
                mode.isGameRunning = False
        keys = pg.key.get_pressed()
        if keys[pg.K_ESCAPE]:
            mode.isGameRunning = False
        if keys[pg.K_a] and mode.player2.rect.centerx > 0: order[2] = 1
        if keys[pg.K_d] and mode.player2.rect.centerx < mode.width: order[3] = 1
        if keys[pg.K_n]:
            presentPressedN = pg.time.get_ticks()
            timeInterval = 200
            if mode.player2.numOfBullets > 0 and \
                    presentPressedN-mode.lastPressedN > timeInterval:
                order[4] = 1
                mode.lastPressedN = presentPressedN
        if keys[pg.K_l]:
            presentPressedL = pg.time.get_ticks()
            timeInterval = 500
            if mode.player2.numOfRockets > 0 and \
                    presentPressedL-mode.lastPressedL > timeInterval:
                order[7] = 1
                mode.lastPressedL = presentPressedL
        if keys[pg.K_j]:
            presentPressedJ = pg.time.get_ticks()
            timeInterval = 500
            if mode.player2.trueShieldTimes > 0 and \
                    presentPressedJ-mode.lastPressedJ > timeInterval:
                order[5] = 1
                mode.lastPressedJ = presentPressedJ
        if not mode.player2.isJump:
            if keys[pg.K_w]: order[0] = 1
            if keys[pg.K_s]: order[1] = 1
            if keys[pg.K_k]: order[6] = 1
        # hand information from the server
        if mode.numOfPlayers == 2:
            transferData = [order, [], [], []]
            dataFromServe = mode.network.send(transferData)
            for i in mode.enemyGroup:
                i.kill()
            for i in mode.meteorGroup:
                i.kill()
            for i in mode.enemyBulletGroup:
                i.kill()
            for i in mode.player1BulletGroup:
                i.kill()
            for i in mode.player2BulletGroup:
                i.kill()
            for i in mode.player1RocketGroup:
                i.kill()
            for i in mode.player2RocketGroup:
                i.kill()
            for i in mode.player1Group:
                i.kill()
            for i in mode.player2Group:
                i.kill()
            for i in mode.shieldGroup:
                i.kill()
            for i in mode.bossEnemyGroup:
                i.kill()
            for i in dataFromServe[1]:
                mode.newEnemy = NormalEnemy(mode.width, mode.height, \
                                    mode.enemyImages, mode.player1)
                mode.newEnemy.rect.centerx = i[0]
                mode.newEnemy.rect.centery = i[1]
                mode.newEnemy.image = mode.enemyImages[i[2]]
                mode.enemyGroup.add(mode.newEnemy)
            for i in dataFromServe[2]:
                newMeteor = Meteorolite(mode.width, mode.height, \
                                                        mode.meteorImages)
                newMeteor.rect.centerx = i[0]
                newMeteor.rect.centery = i[1]
                newImage = pg.transform.rotate(mode.meteorImages[i[2]], i[3])
                center = newMeteor.rect.center
                newMeteor.image = newImage
                newMeteor.rect = newMeteor.image.get_rect()
                newMeteor.rect.center = center
                mode.meteorGroup.add(newMeteor)
            for i in dataFromServe[3]:
                newBullet = EnemyBullet(mode.player1, mode.newEnemy, \
                                                    mode.width, mode.height)
                newBullet.rect.centerx = i[0]
                newBullet.rect.centery = i[1]
                mode.enemyBulletGroup.add(newBullet)
            for i in dataFromServe[6]:
                newBullet = Player1Bullet(mode.player1, mode.width, mode.height)
                newBullet.rect.centerx = i[0]
                newBullet.rect.centery = i[1]
                mode.player1BulletGroup.add(newBullet)
            for i in dataFromServe[7]:
                newBullet = Player2Bullet(mode.player1, mode.width, mode.height)
                newBullet.rect.centerx = i[0]
                newBullet.rect.centery = i[1]
                mode.player2BulletGroup.add(newBullet)
            for i in dataFromServe[8]:
                newRocket = Player1Rocket(mode.width, mode.height)
                newRocket.rect.centerx = i[0]
                newRocket.rect.centery = i[1]
                mode.player1RocketGroup.add(newRocket)
            for i in dataFromServe[9]:
                newRocket = Player2Rocket(mode.width, mode.height)
                newRocket.rect.centerx = i[0]
                newRocket.rect.centery = i[1]
                mode.player2RocketGroup.add(newRocket)
            for i in dataFromServe[10]:
                newShield = Shield(mode.player1)
                newShield.rect.centerx = i[0]
                newShield.rect.centery = i[1]
                mode.shieldGroup.add(newShield)
            explosionLocations = []
            for i in mode.explosionGroup:
                explosionLocations.append(i.rect.center)
            for i in dataFromServe[12]:
                if i not in explosionLocations:
                    newExplosion = Explosion(mode.explosionImages, i)
                    mode.explosionGroup.add(newExplosion)
            boss = BossEnemy(mode.width, mode.height, mode.player1)
            boss.rect.centerx = dataFromServe[11][0]
            boss.rect.centery = dataFromServe[11][1]
            mode.bossEnemyGroup.add(boss)
            mode.player1 = Player1(mode, dataFromServe[4][0], \
                                                        dataFromServe[4][1])
            mode.player2 = Player2(mode, dataFromServe[5][0], \
                                                        dataFromServe[5][1])
            mode.player1Group.add(mode.player1)
            mode.player2Group.add(mode.player2)
            mode.points = dataFromServe[-3]
            mode.points2 = dataFromServe[-2]
            mode.player1.numOfRockets = dataFromServe[4][2]
            mode.player1.jumpTimes = dataFromServe[4][3]
            mode.player1.trueShieldTimes = dataFromServe[4][4]
            mode.player2.numOfRockets = dataFromServe[5][2]
            mode.player2.jumpTimes = dataFromServe[5][3]
            mode.player2.trueShieldTimes = dataFromServe[5][4]
            mode.player1.health = dataFromServe[-5]
            mode.player2.health = dataFromServe[-4]
            dataFromServe = dataFromServe[0]
            if mode.player1.health <= 0:
                for i in mode.player1Group:
                    i.kill()
            if mode.player2.health <= 0:
                for i in mode.player2Group:
                    i.kill()

    def redrawAll(mode):
        mode.clock.tick(mode.FPS)
        mode.screen.blit(mode.background, mode.backgroundRect)
        if mode.numOfPlayers > 1:
            if mode.player1.health <= 0: mode.player1.kill()
            if mode.player2.health <= 0: mode.player2.kill()
            if mode.player1.health <= 0 and mode.player2.health <= 0:
                mode.isGameRunning = False
                gameEndMode.isGameRunning = True
        mode.backgroundRect.y += 1  
        mode.mount += 1
        countMax = 1000
        if mode.mount == countMax:
            mode.backgroundRect.y -= mode.mount
            mode.mount = 0
        mode.liveRect.kill()
        if mode.player1.health <= 0:
            mode.player1.health = 0
        minus = 7
        h0 = 48
        times = 10
        h1 = 6
        mode.liveRect = CharacterBox(mode.image2, mode.width-minus, h0, \
                                            (times*mode.player1.health, h1))
        mode.characterBoxGroup.add(mode.liveRect)
        mode.allGroup.add(mode.liveRect)
        # draw the player2's character box
        if mode.numOfPlayers > 1:
            mode.liveRect1.kill()
            if mode.player2.health <= 0:
                mode.player2.health = 0
            h0 = 108
            mode.liveRect1 = CharacterBox(mode.image2, mode.width-minus, h0, \
                                        (times*mode.player2.health, h1))
            mode.characterBoxGroup.add(mode.liveRect1)
            mode.allGroup.add(mode.liveRect1)
        # player1's bullet hits meteor
        isHits = pg.sprite.groupcollide(mode.meteorGroup, \
                    mode.player1BulletGroup, False, pg.sprite.collide_circle)
        for isHit in isHits:
            isHit.health -= 1
            mode.player1.numOfBullets += 1
            if isHit.health <= 0:
                mode.points += isHit.points
                center = isHit.rect.center
                explosion = Explosion(mode.explosionImages, center)
                mode.explosionGroup.add(explosion)
                mode.allGroup.add(explosion)
                isHit.kill()
                newMeteor = Meteorolite(game.width, game.height, \
                                                        mode.meteorImages)
                mode.allGroup.add(newMeteor)
                mode.meteorGroup.add(newMeteor)
        
        if mode.numOfPlayers == 1 or (mode.numOfPlayers == 2 and \
                    mode.orderFromServer[-1] == 0):
            # player2's bullet hits meteor
            isHits = pg.sprite.groupcollide(mode.meteorGroup, \
                        mode.player2BulletGroup, False, \
                                                    pg.sprite.collide_circle)
            for isHit in isHits:
                isHit.health -= 1
                mode.player2.numOfBullets += 1
                if isHit.health <= 0:
                    mode.points2 += isHit.points
                    center = isHit.rect.center
                    explosion = Explosion(mode.explosionImages, center)
                    mode.explosionGroup.add(explosion)
                    mode.allGroup.add(explosion)
                    isHit.kill()
                    newMeteor = Meteorolite(game.width, game.height, \
                                                            mode.meteorImages)
                    mode.allGroup.add(newMeteor)
                    mode.meteorGroup.add(newMeteor)
            # players' bullet hits boss
            isHits = pg.sprite.groupcollide(mode.playerBulletGroup, \
                        mode.bossEnemyGroup, False, False)
            for isHit in isHits:
                ratio0 = 0.75
                if pg.sprite.collide_circle_ratio(ratio0)(mode.boss1, isHit):
                    mode.boss1.health -= 1
                    center = isHit.rect.center
                    explosion = Explosion(mode.explosionImages, center)
                    mode.explosionGroup.add(explosion)
                    mode.allGroup.add(explosion)
                    isHit.kill()
                    mode.player1.numOfBullets += 1
                    if mode.numOfPlayers == 2:
                        mode.player2.numOfBullets += 1
            # players' rocket hits boss
            isHits = pg.sprite.groupcollide(mode.playerRocketGroup, \
                        mode.bossEnemyGroup, False, False)
            for isHit in isHits:
                ratio0 = 0.75
                if pg.sprite.collide_circle_ratio(ratio0)(mode.boss1, isHit):
                    center = isHit.rect.center
                    explosion = Explosion(mode.explosionImages, center)
                    mode.explosionGroup.add(explosion)
                    mode.allGroup.add(explosion)
                    mode.boss1.health -= 1
                    isHit.kill()
            # player1's rocket hits meteor
            isHits = pg.sprite.groupcollide(mode.meteorGroup, \
                        mode.player1RocketGroup, False, \
                                                    pg.sprite.collide_circle)
            for isHit in isHits:
                isHit.health -= 1
                if isHit.health <= 0:
                    mode.points += isHit.points
                    center = isHit.rect.center
                    explosion = Explosion(mode.explosionImages, center)
                    mode.explosionGroup.add(explosion)
                    mode.allGroup.add(explosion)
                    isHit.kill()
                    newMeteor = Meteorolite(game.width, game.height, \
                                                            mode.meteorImages)
                    mode.allGroup.add(newMeteor)
                    mode.meteorGroup.add(newMeteor)
            # player2's rocket hits meteor
            isHits = pg.sprite.groupcollide(mode.meteorGroup, \
                        mode.player2RocketGroup, False, \
                                                    pg.sprite.collide_circle)
            for isHit in isHits:
                isHit.health -= 1
                if isHit.health <= 0:
                    mode.points2 += isHit.points
                    center = isHit.rect.center
                    explosion = Explosion(mode.explosionImages, center)
                    mode.explosionGroup.add(explosion)
                    mode.allGroup.add(explosion)
                    isHit.kill()
                    newMeteor = Meteorolite(game.width, game.height, \
                                                            mode.meteorImages)
                    mode.allGroup.add(newMeteor)
                    mode.meteorGroup.add(newMeteor)
            # player1's bullet hits normal enemy
            isHits = pg.sprite.groupcollide(mode.enemyGroup, \
                        mode.player1BulletGroup, False, \
                                                    pg.sprite.collide_circle)
            for isHit in isHits:
                isHit.health -= 1
                mode.player1.numOfBullets += 1
                if isHit.health <= 0:
                    mode.points += isHit.points
                    center = isHit.rect.center
                    explosion = Explosion(mode.explosionImages, center)
                    mode.explosionGroup.add(explosion)
                    mode.allGroup.add(explosion)
                    isHit.kill()
                    newEnemy = NormalEnemy(mode.width, mode.height, \
                                                mode.enemyImages, mode.player1)
                    mode.allGroup.add(newEnemy)
                    mode.enemyGroup.add(newEnemy)
            # player2's bullet hits normal enemy
            isHits = pg.sprite.groupcollide(mode.enemyGroup, \
                        mode.player2BulletGroup, False, \
                                                    pg.sprite.collide_circle)
            for isHit in isHits:
                isHit.health -= 1
                mode.player2.numOfBullets += 1
                if isHit.health <= 0:
                    mode.points2 += isHit.points
                    center = isHit.rect.center
                    explosion = Explosion(mode.explosionImages, center)
                    mode.explosionGroup.add(explosion)
                    mode.allGroup.add(explosion)
                    isHit.kill()
                    newEnemy = NormalEnemy(mode.width, mode.height, \
                                                mode.enemyImages, mode.player2)
                    mode.allGroup.add(newEnemy)
                    mode.enemyGroup.add(newEnemy)
            # player1's rocket hits normal enemy
            isHits = pg.sprite.groupcollide(mode.enemyGroup, \
                        mode.player1RocketGroup, False, \
                                                    pg.sprite.collide_circle)
            for isHit in isHits:
                isHit.health -= 1
                if isHit.health <= 0:
                    mode.points += isHit.points
                    center = isHit.rect.center
                    explosion = Explosion(mode.explosionImages, center)
                    mode.explosionGroup.add(explosion)
                    mode.allGroup.add(explosion)
                    isHit.kill()
                    newEnemy = NormalEnemy(mode.width, mode.height, \
                                                mode.enemyImages, mode.player1)
                    mode.allGroup.add(newEnemy)
                    mode.enemyGroup.add(newEnemy)
            # player2's rocket hits normal enemy
            isHits = pg.sprite.groupcollide(mode.enemyGroup, \
                        mode.player2RocketGroup, False, \
                                                    pg.sprite.collide_circle)
            for isHit in isHits:
                isHit.health -= 1
                if isHit.health <= 0:
                    mode.points2 += isHit.points
                    center = isHit.rect.center
                    explosion = Explosion(mode.explosionImages, center)
                    mode.explosionGroup.add(explosion)
                    mode.allGroup.add(explosion)
                    isHit.kill()
                    newEnemy = NormalEnemy(mode.width, mode.height, \
                                                mode.enemyImages, mode.player1)
                    mode.allGroup.add(newEnemy)
                    mode.enemyGroup.add(newEnemy)
            # enemy's bullet hits the player1
            isHits = pg.sprite.groupcollide(mode.enemyBulletGroup, \
                        mode.player1Group, False, False)
            for isHit in isHits:
                if mode.player1.isShield == True or \
                    mode.player1.isTrueShield == True: ratio = 0.8
                else: ratio = 0.75
                if pg.sprite.collide_circle_ratio(ratio)(mode.player1, isHit):
                    isHit.kill()
                    if mode.player1.isShield == False and \
                        mode.player1.isTrueShield == False:
                        mode.player1.health -= 1
            # enemy's bullet hits the player2
            isHits = pg.sprite.groupcollide(mode.enemyBulletGroup, \
                        mode.player2Group, False, False)
            for isHit in isHits:
                if mode.player2.isShield == True or \
                    mode.player2.isTrueShield == True: ratio = 0.8
                else: ratio = 0.75
                if pg.sprite.collide_circle_ratio(ratio)(mode.player2, isHit):
                    isHit.kill()
                    if mode.player2.isShield == False and \
                        mode.player2.isTrueShield == False:
                        mode.player2.health -= 1
            # normal enemy hits the player1
            isHits = pg.sprite.groupcollide(mode.enemyGroup, \
                        mode.player1Group, False, False)
            for isHit in isHits:
                if mode.player1.isShield == True or \
                    mode.player1.isTrueShield == True: ratio = 0.8
                else: ratio = 0.7
                if pg.sprite.collide_circle_ratio(ratio)(mode.player1, isHit):
                    isHit.health -= 1
                    if isHit.health <= 0:
                        mode.points += isHit.points
                        center = isHit.rect.center
                        explosion = Explosion(mode.explosionImages, center)
                        mode.explosionGroup.add(explosion)
                        mode.allGroup.add(explosion)
                        isHit.kill()
                        newEnemy = NormalEnemy(mode.width, mode.height, \
                                                mode.enemyImages, mode.player1)
                        mode.allGroup.add(newEnemy)
                        mode.enemyGroup.add(newEnemy)
                        if mode.player1.isShield == False and \
                            mode.player1.isTrueShield == False:
                            mode.player1.health -= 1
            # normal enemy hits the player2
            isHits = pg.sprite.groupcollide(mode.enemyGroup, \
                        mode.player2Group, False, False)
            for isHit in isHits:
                if mode.player2.isShield == True or \
                    mode.player2.isTrueShield == True:
                    ratio = 0.8
                else:
                    ratio = 0.7
                if pg.sprite.collide_circle_ratio(ratio)(mode.player2, isHit):
                    isHit.health -= 1
                    if isHit.health <= 0:
                        mode.points2 += isHit.points
                        center = isHit.rect.center
                        explosion = Explosion(mode.explosionImages, center)
                        mode.explosionGroup.add(explosion)
                        mode.allGroup.add(explosion)
                        isHit.kill()
                        newEnemy = NormalEnemy(mode.width, mode.height, \
                                                mode.enemyImages, mode.player2)
                        mode.allGroup.add(newEnemy)
                        mode.enemyGroup.add(newEnemy)
                        if mode.player2.isShield == False and \
                            mode.player2.isTrueShield == False:
                            mode.player2.health -= 1
            # meteor hits the player1
            isHits = pg.sprite.groupcollide(mode.meteorGroup, \
                        mode.player1Group, False, False)
            for isHit in isHits:
                if mode.player1.isShield == True or \
                    mode.player1.isTrueShield == True:
                    ratio = 0.8
                else:
                    ratio = 0.7
                if pg.sprite.collide_circle_ratio(ratio)(mode.player1, isHit):
                    isHit.health -= 1
                    if isHit.health <= 0:
                        mode.points += isHit.points
                        center = isHit.rect.center
                        explosion = Explosion(mode.explosionImages, center)
                        mode.explosionGroup.add(explosion)
                        mode.allGroup.add(explosion)
                        isHit.kill()
                        if mode.player1.isShield == False and \
                            mode.player1.isTrueShield == False:
                            mode.player1.health -= 1
                        newMeteor = Meteorolite(game.width, game.height, \
                                                            mode.meteorImages)
                        mode.allGroup.add(newMeteor)
                        mode.meteorGroup.add(newMeteor)
            # meteor hits the player2
            isHits = pg.sprite.groupcollide(mode.meteorGroup, \
                        mode.player2Group, False, False)
            for isHit in isHits:
                if mode.player2.isShield == True or \
                    mode.player2.isTrueShield == True: ratio = 0.8
                else: ratio = 0.7
                if pg.sprite.collide_circle_ratio(ratio)(mode.player2, isHit):
                    isHit.health -= 1
                    if isHit.health <= 0:
                        mode.points2 += isHit.points
                        center = isHit.rect.center
                        explosion = Explosion(mode.explosionImages, center)
                        mode.explosionGroup.add(explosion)
                        mode.allGroup.add(explosion)
                        isHit.kill()
                        if mode.player2.isShield == False and \
                            mode.player2.isTrueShield == False:
                            mode.player2.health -= 1
                        newMeteor = Meteorolite(game.width, game.height, \
                                                            mode.meteorImages)
                        mode.allGroup.add(newMeteor)
                        mode.meteorGroup.add(newMeteor)
        # handle information from players
        if mode.numOfPlayers == 1:
            mode.player1keyPressed()
            mode.allGroup.update()
            mode.allGroup.draw(mode.screen)  
        if mode.numOfPlayers == 2:
            if mode.orderFromServer[-1] == 0:
                mode.player1keyPressed()
                mode.allGroup.update()
                mode.allGroup.draw(mode.screen)  
            elif mode.orderFromServer[-1] == 1:
                mode.player2keyPressed()
                mode.explosionGroup.update()
                mode.playerBulletGroup.update()
                mode.playerRocketGroup.update()
                mode.characterBoxGroup.update()
                mode.shieldLogGroup.update()
                mode.rocketLogGroup.update()
                mode.jumpLogGroup.update()
                mode.shieldLog2Group.update()
                mode.rocketLog2Group.update()
                mode.jumpLog2Group.update()
                mode.bossEnemyGroup.draw(mode.screen)
                mode.allGroup.draw(mode.screen)  
                mode.enemyGroup.draw(mode.screen)  
                mode.meteorGroup.draw(mode.screen)  
                mode.enemyBulletGroup.draw(mode.screen)  
                mode.player1Group.draw(mode.screen)  
                mode.player2Group.draw(mode.screen)  
                mode.shieldGroup.draw(mode.screen)
                mode.explosionGroup.draw(mode.screen)
                mode.player1BulletGroup.draw(mode.screen)  
                mode.player1RocketGroup.draw(mode.screen)  
                mode.player2BulletGroup.draw(mode.screen)  
                mode.player2RocketGroup.draw(mode.screen)  
        # update character box of player1
        for shield in mode.shieldLogGroup:
            shield.kill()
        m = 48
        times = 13
        h = 5
        size = (10, 10)
        for i in range(mode.player1.trueShieldTimes):
            shield = CharacterBox(mode.image3, mode.width-m-i*times, h, size)
            mode.shieldLogGroup.add(shield)
            mode.allGroup.add(shield)
        for rocket in mode.rocketLogGroup:
            rocket.kill()
        m = 38
        h = 10
        size = (30, 30)
        for i in range(mode.player1.numOfRockets):
            rocket = CharacterBox(mode.image4, mode.width-m-i*times, h, size)
            mode.rocketLogGroup.add(rocket)
            mode.allGroup.add(rocket)
        for jump in mode.jumpLogGroup:
            jump.kill()
        m = 45
        h = 32
        size = (10, 10)
        for i in range(mode.player1.jumpTimes):
            jump = CharacterBox(mode.image5, mode.width-m-i*times, h, size)
            mode.jumpLogGroup.add(jump)
            mode.allGroup.add(jump)
        # update character box of player2
        if mode.numOfPlayers == 2:
            for shield in mode.shieldLog2Group:
                shield.kill()
            m = 48
            h = 65
            time = 13
            for i in range(mode.player2.trueShieldTimes):
                shield = CharacterBox(mode.image3, mode.width-m-i*time, h, size)
                mode.shieldLog2Group.add(shield)
                mode.allGroup.add(shield)
            for rocket in mode.rocketLog2Group:
                rocket.kill()
            m = 45
            h = 81
            size = (10, 6)
            for i in range(mode.player2.numOfRockets):
                rocket = CharacterBox(mode.image7, mode.width-m-i*time, h, size)
                mode.rocketLog2Group.add(rocket)
                mode.allGroup.add(rocket)
            for jump in mode.jumpLog2Group:
                jump.kill()
            h = 92
            size = (10, 10)
            for i in range(mode.player2.jumpTimes):
                jump = CharacterBox(mode.image5, mode.width-m-i*time, h, size)
                mode.jumpLog2Group.add(jump)
                mode.allGroup.add(jump)
        # draw text on the screen
        fontName = pg.font.match_font('arial')
        fontSize = 15
        font = pg.font.Font(fontName, fontSize)
        white = (255, 255, 255)
        textSurface = font.render('Score:', True, white)
        textRect = textSurface.get_rect()
        minus = 102
        h = 10
        textRect.midtop = (mode.width-minus, h)
        mode.screen.blit(textSurface, textRect)
        if mode.numOfPlayers > 1:
            textSurface = font.render('Score:', True, white)
            textRect = textSurface.get_rect()
            h = 70
            textRect.midtop = (mode.width-minus, h)
            mode.screen.blit(textSurface, textRect)
        fontSize = 30
        font = pg.font.Font(fontName, fontSize)
        textSurface = font.render(f'{mode.points}', True, white)
        textRect = textSurface.get_rect()
        h = 25
        textRect.midtop = (mode.width-minus, h)
        mode.screen.blit(textSurface, textRect)
        if mode.numOfPlayers > 1:
            textSurface = font.render(f'{mode.points2}', True, white)
            textRect = textSurface.get_rect()
            h = 85
            textRect.midtop = (mode.width-minus, h)
            mode.screen.blit(textSurface, textRect)
            for i in mode.deadGroup:
                i.kill()
            if mode.player1.health <= 0: 
                center = mode.player1.rect.center
                dead = Dead(mode.deadImage, center)
                mode.deadGroup.add(dead)
                mode.allGroup.add(dead)
                mode.player1.kill()
            if mode.player2.health <= 0: 
                center = mode.player2.rect.center
                dead = Dead(mode.deadImage, center)
                mode.deadGroup.add(dead)
                mode.allGroup.add(dead)
                mode.player2.kill()
            if mode.player1.health <= 0 and mode.player2.health <= 0:
                mode.isGameRunning = False
                gameEndMode.isGameRunning = True
        else:
            if mode.player1.health <= 0:
                center = mode.player1.rect.center
                explosion = Explosion(mode.explosionImages, center)
                mode.explosionGroup.add(explosion)
                mode.allGroup.add(explosion)
                mode.isGameRunning = False
                gameEndMode.isGameRunning = True
        pg.display.flip()

WIDTH = 600
HEIGHT = 600
initGame = IntroGameMode(WIDTH, HEIGHT)
isWholeGameRunning = True
numOfPlayers = 1
isGameRunning = False
while isWholeGameRunning:
    while initGame.isGameRunning:
        initGame.redrawAll()
    splashGame = SplashGameMode(WIDTH, HEIGHT)
    rankingMode = RankingMode(WIDTH, HEIGHT)
    gameEndMode = GameEndMode(WIDTH, HEIGHT)
    helpMode = HelpMode(WIDTH, HEIGHT)
    while splashGame.isGameRunning:
        splashGame.redrawAll()
    game = GameMode(WIDTH, HEIGHT, numOfPlayers)
    while game.isGameRunning:
        game.redrawAll()
    game.BMG.stop()
    while helpMode.isGameRunning:
        helpMode.redrawAll()
    while gameEndMode.isGameRunning:
        gameEndMode.redrawAll()
    while rankingMode.isGameRunning:
        rankingMode.redrawAll()
pg.quit()