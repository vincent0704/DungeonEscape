import random, sys, copy, os, pygame
from pygame.locals import *
#pygame的必要
pygame.init()
pygame.display.set_caption('Dungeon Escape')
pygame.mixer.music.load('backMusic.mp3')   # 加載音樂檔
pygame.mixer.music.play(0)            #撥放音樂檔
#顏色的編碼
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (147, 147, 147)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
RED = (255,0,0)
ONE = 0
TWO = 0
direction = 'NONE'

DISPLAYSURF = pygame.display.set_mode((1240, 760))

FPSCLOCK = pygame.time.Clock()

#X的正方向往右，Y的正方向往下
XMAPCORD = 0
YMAPCORD = 0
#判斷所在關卡
currentLevelIndex = 50
mapNeedsRedraw = True
def resetLevel():
    pygame.Surface.fill(DISPLAYSURF, BLACK)
def doNothing():
    redrawMap()
currentLevel = ['w']
#創造地圖
def createMapList():
    global currentLevel
    global tilesWidth
    global currentLevelIndex
    file = open('dungeonescapelevels.txt', 'r')
    mainList = []
    nextList = []
    #用來存各個地圖的寬度
    widthList = [14, 9, 15, 12, 9, 9, 7,
                 11, 9, 16, 13, 15, 13, 19, 13, 9, 18,
                 11, 27, 12, 10, 9, 15, 23, 8, 25, 9,
                 15, 15, 17, 14, 18, 18, 24, 21, 22, 26,
                 23, 24, 25, 26, 27, 27, 29, 26, 23, 24,
                 24, 19, 30, 24, 23, 30, 22, 23, 25, 27
]

    for i, line in enumerate(file):  # line is a string 
        # get rid of semicolons, new line characters, and blank spaces
        line = line.replace(";", "")
        line = line.replace("\n", "")
        line = line.replace(" ", "")

        # if next line contains a digit, dump current list as next
        #list element of the main list and start a new list but
        #don't add the line with the digit itself to the new list
        if (line.isdigit() == True):
            nextList = []
            mainList.append(nextList)
        else:
            nextList.extend(list(line))
    #依據currentLevelIndex判斷地圖的畫法
    for i in range(currentLevelIndex + 1):
        tilesWidth = widthList[i]
        currentLevel = mainList[currentLevelIndex]



#將.txt的地圖製作到畫面中
def redrawMap():
    global XMAPCORD
    global YMAPCORD
    global currentLevelIndex
    resetLevel()
    for i in range(0,len(currentLevel)):
#'w'為場外
        if playerPositionMap[i-1] == 'w':
            drawWall()
            XMAPCORD = XMAPCORD + 40
#'s'為路徑
        elif playerPositionMap[i-1] == 's':
            drawStone()
            XMAPCORD = XMAPCORD + 40
#'g'為目標
        elif playerPositionMap[i-1] == 'g':
            drawGoal()
            XMAPCORD = XMAPCORD + 40
#'p'為玩家
        elif playerPositionMap[i-1] == 'p':
            drawPlayer()
            XMAPCORD = XMAPCORD + 40
#'k'為石頭 (遊戲目的)
        elif playerPositionMap[i-1] == 'k':
            drawKey()
            XMAPCORD = XMAPCORD + 40
#'f'為已經有石頭的目標點
        elif playerPositionMap[i-1] == 'f':
            drawFinish()
            XMAPCORD = XMAPCORD + 40
#'G'為玩家在目標上
        elif playerPositionMap[i-1] == 'G':
            drawPlayerGoal()
            XMAPCORD = XMAPCORD + 40
        if i % tilesWidth == 0:
            YMAPCORD = YMAPCORD + 40
            XMAPCORD = 0
        elif i == len(playerPositionMap) - 1:
            XMAPCORD = 0
            YMAPCORD = 0
        mapNeedsRedraw = False

#遊戲的主要移動
def movePlayer():
    createMapList()
    global currentLevel
    global tilesWidth 				#地圖的寬度
    global playerPositionMap
    global drawmap
    global playerPosition
    global mapNeedsRedraw
    global currentLevelIndex
    global direction
    #僅改變玩家所在位置的map，使玩家按'r'時可以重玩此關
    playerPositionMap = currentLevel
    redrawMap()

    running = True
    drawmap = True
    FPS = 30
    fpsClock = pygame.time.Clock()
    while running:
        #判斷是否有G在
        #如果沒有G則代表玩家已經通過此關
        if 'g' not in playerPositionMap and 'G' not in playerPositionMap:
            currentLevelIndex = currentLevelIndex + 1
            createMapList()
            playerPositionMap = currentLevel
            redrawMap()
        #可直接關遊戲
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                sys.exit()
            #依照玩家按的按鍵移動角色
            if event.type == KEYDOWN:
                #回傳玩家在表格中的位置
                # 'G' and 'F' are simply the player on top of different tiles
                if 'p' in playerPositionMap:
                    playerPosition = playerPositionMap.index('p')
                elif 'G' in playerPositionMap:
                    playerPosition = playerPositionMap.index('G')
                if ((event.key == K_r) and (currentLevelIndex == 4)):
                    currentLevelIndex = currentLevelIndex + 1
                    createMapList()
                    playerPositionMap = currentLevel
                    redrawMap()
                #重玩此關
                elif (event.key == K_r):
                    createMapList()
                    playerPositionMap = currentLevel
                    redrawMap()
                elif ((event.key == K_n) and (currentLevelIndex > 6)):
                    currentLevelIndex = currentLevelIndex + 1
                    if currentLevelIndex > 56:
                        currentLevelIndex = 7
                    createMapList()
                    playerPositionMap = currentLevel
                    redrawMap()
                elif ((event.key == K_b) and (currentLevelIndex > 6)):
                    currentLevelIndex = currentLevelIndex - 1
                    if currentLevelIndex < 7:
                        currentLevelIndex = 56
                    createMapList()
                    playerPositionMap = currentLevel
                    redrawMap()
					
                #判斷玩家的移動方向
                if ((event.key == K_LEFT or event.key == K_a) and (playerPositionMap[playerPosition - 1] != 'w')):
                    ONE = 1
                    TWO = 2
                    direction = 'LEFT'
                elif ((event.key == K_DOWN or event.key == K_s) and (playerPositionMap[playerPosition + tilesWidth] != 'w')):
                        ONE = tilesWidth
                        TWO = (tilesWidth*2)
                        direction = 'DOWN'
                elif ((event.key == K_RIGHT or event.key == K_d) and (playerPositionMap[playerPosition + 1] != 'w')):
                        ONE = 1
                        TWO = 2
                        direction = 'RIGHT'
                elif ((event.key == K_UP or event.key == K_w) and (playerPositionMap[playerPosition - tilesWidth] != 'w')):
                        ONE = tilesWidth
                        TWO = (tilesWidth*2)
                        direction = 'UP'
                if direction == 'NONE':
                    doNothing()
                elif direction == 'DOWN' or direction == 'RIGHT':
                    if playerPositionMap[playerPosition + ONE] == 'w':
                        doNothing()
                    elif playerPositionMap[playerPosition + ONE] == 'k':
                        if playerPositionMap[playerPosition + TWO] == 'g':
                            playerPositionMap[playerPosition + TWO] = 'f'
                            playerPositionMap[playerPosition + ONE] = 'p'
                            playerPositionMap[playerPosition] = 's'
                        elif playerPositionMap[playerPosition + TWO] == 'w' or playerPositionMap[playerPosition + TWO] == 'k' or playerPositionMap[playerPosition + TWO] == 'f':
                            doNothing()
                        elif playerPositionMap[playerPosition] == 'G':
                            playerPositionMap[playerPosition + TWO] = 'k'
                            playerPositionMap[playerPosition + ONE] = 'p'
                            playerPositionMap[playerPosition] = 'g'
                        else:
                            playerPositionMap[playerPosition + TWO] = 'k'
                            playerPositionMap[playerPosition + ONE] = 'p'
                            playerPositionMap[playerPosition] = 's'
                    elif playerPositionMap[playerPosition] == 'G':
                        if playerPositionMap[playerPosition + ONE] == 'g':
                            playerPositionMap[playerPosition + ONE] = 'G'
                            playerPositionMap[playerPosition] = 'g'
                        elif playerPositionMap[playerPosition + ONE] == 'f':
                            if playerPositionMap[playerPosition + TWO] == 'w' or playerPositionMap[playerPosition + TWO] == 'f' or playerPositionMap[playerPosition + TWO] == 'k':
                                doNothing()
                            elif playerPositionMap[playerPosition + TWO] == 'g':
                                playerPositionMap[playerPosition + TWO] = 'f'
                                playerPositionMap[playerPosition + ONE] = 'G'
                                playerPositionMap[playerPosition] = 'g'
                            else:
                                playerPositionMap[playerPosition + TWO] = 'k'
                                playerPositionMap[playerPosition + ONE] = 'G'
                                playerPositionMap[playerPosition] = 'g'
                        else:
                            playerPositionMap[playerPosition + ONE] = 'p'
                            playerPositionMap[playerPosition] = 'g'
                    elif playerPositionMap[playerPosition + ONE] == 'g':
                        playerPositionMap[playerPosition + ONE] = 'G'
                        playerPositionMap[playerPosition] = 's'
                    elif playerPositionMap[playerPosition + ONE] == 'f':
                        if playerPositionMap[playerPosition + TWO] == 'w' or playerPositionMap[playerPosition + TWO] == 'f' or playerPositionMap[playerPosition + TWO] == 'k':
                            doNothing()
                        elif playerPositionMap[playerPosition + TWO] == 'g':
                            playerPositionMap[playerPosition + TWO] = 'f'
                            playerPositionMap[playerPosition + ONE] = 'G'
                            playerPositionMap[playerPosition] = 's'
                        else:
                            playerPositionMap[playerPosition + TWO] = 'k'
                            playerPositionMap[playerPosition + ONE] = 'G'
                            playerPositionMap[playerPosition] = 's'
                    else:
                        playerPositionMap[playerPosition + ONE] = 'p'
                        playerPositionMap[playerPosition] = 's'
                    mapNeedsRedraw = True
                elif direction == 'UP' or direction == 'LEFT':
                    if playerPositionMap[playerPosition - ONE] == 'w':
                        doNothing()
                    elif playerPositionMap[playerPosition - ONE] == 'k':
                        if playerPositionMap[playerPosition - TWO] == 'g':
                            playerPositionMap[playerPosition - TWO] = 'f'
                            playerPositionMap[playerPosition - ONE] = 'p'
                            playerPositionMap[playerPosition] = 's'
                        elif playerPositionMap[playerPosition - TWO] == 'w' or playerPositionMap[playerPosition - TWO] == 'k' or playerPositionMap[playerPosition - TWO] == 'f':
                            doNothing()
                        elif playerPositionMap[playerPosition] == 'G':
                            playerPositionMap[playerPosition - TWO] = 'k'
                            playerPositionMap[playerPosition - ONE] = 'p'
                            playerPositionMap[playerPosition] = 'g'
                        else:
                            playerPositionMap[playerPosition - TWO] = 'k'
                            playerPositionMap[playerPosition - ONE] = 'p'
                            playerPositionMap[playerPosition] = 's'
                    elif playerPositionMap[playerPosition] == 'G':
                        if playerPositionMap[playerPosition - ONE] == 'g':
                            playerPositionMap[playerPosition - ONE] = 'G'
                            playerPositionMap[playerPosition] = 'g'
                        elif playerPositionMap[playerPosition - ONE] == 'f':
                            if playerPositionMap[playerPosition - TWO] == 'w' or playerPositionMap[playerPosition - TWO] == 'f' or playerPositionMap[playerPosition - TWO] == 'k':
                                doNothing()
                            elif playerPositionMap[playerPosition - TWO] == 'g':
                                playerPositionMap[playerPosition - TWO] = 'f'
                                playerPositionMap[playerPosition - ONE] = 'G'
                                playerPositionMap[playerPosition] = 'g'
                            else:
                                playerPositionMap[playerPosition - TWO] = 'k'
                                playerPositionMap[playerPosition - ONE] = 'G'
                                playerPositionMap[playerPosition] = 'g'
                        else:
                            playerPositionMap[playerPosition - ONE] = 'p'
                            playerPositionMap[playerPosition] = 'g'
                    elif playerPositionMap[playerPosition - ONE] == 'g':
                        playerPositionMap[playerPosition - ONE] = 'G'
                        playerPositionMap[playerPosition] = 's'
                    elif playerPositionMap[playerPosition - ONE] == 'f':
                        if playerPositionMap[playerPosition - TWO] == 'w' or playerPositionMap[playerPosition - TWO] == 'f' or playerPositionMap[playerPosition - TWO] == 'k':
                            doNothing()
                        elif playerPositionMap[playerPosition - TWO] == 'g':
                            playerPositionMap[playerPosition - TWO] = 'f'
                            playerPositionMap[playerPosition - ONE] = 'G'
                            playerPositionMap[playerPosition] = 's'
                        else:
                            playerPositionMap[playerPosition - TWO] = 'k'
                            playerPositionMap[playerPosition - ONE] = 'G'
                            playerPositionMap[playerPosition] = 's'
                    else:
                        playerPositionMap[playerPosition - ONE] = 'p'
                        playerPositionMap[playerPosition] = 's'
                    mapNeedsRedraw = True
                #重新refresh產生的畫面
                if mapNeedsRedraw:
                    direction = 'NONE'
                    if 'p' in playerPositionMap:
                        playerPosition = playerPositionMap.index('p')
                    elif 'G' in playerPositionMap:
                        playerPosition = playerPositionMap.index('G')
                    redrawMap()
        #依時間刷新遊戲畫面畫面
        pygame.display.update()
        fpsClock.tick(FPS)
    
#設置牆
def drawWall():
    pygame.draw.rect(DISPLAYSURF, WHITE, (XMAPCORD, YMAPCORD, 40, 40), 0)
#設置路徑
def drawStone():
    pygame.draw.rect(DISPLAYSURF, GRAY, (XMAPCORD, YMAPCORD, 40, 40), 0)
#設置石頭放置的目標
def drawGoal():
    pygame.draw.rect(DISPLAYSURF, ORANGE, (XMAPCORD, YMAPCORD, 40, 40), 0)
#設置玩家所在位置
def drawPlayer():
    pygame.draw.rect(DISPLAYSURF, GRAY, (XMAPCORD, YMAPCORD, 40, 40), 0)
    pygame.draw.rect(DISPLAYSURF, BLACK, (XMAPCORD + 10, YMAPCORD + 10, 20, 20), 0)
#設置石頭(遊戲目的)
def drawKey():
    pygame.draw.rect(DISPLAYSURF, YELLOW, (XMAPCORD, YMAPCORD, 40, 40), 0)
#設置已有石頭的目標
def drawFinish():
    pygame.draw.rect(DISPLAYSURF, RED, (XMAPCORD, YMAPCORD, 40, 40), 0)
#設置玩家站在目標上
def drawPlayerGoal():
    pygame.draw.rect(DISPLAYSURF, ORANGE, (XMAPCORD, YMAPCORD, 40, 40), 0)
    pygame.draw.rect(DISPLAYSURF, BLACK, (XMAPCORD + 10, YMAPCORD + 10, 20, 20), 0)

def drawReset():
    pygame.draw.rect(DISPLAYSURF, BLACK, (XMAPCORD, YMAPCORD, 40, 40), 0)

#執行遊戲
movePlayer()
