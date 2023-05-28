import pygame, sys, random
from pygame.locals import *

WinWidth = 640
WinHeight = 480
BWidth = 4
BHeight = 4
TileSize = 80
FPS = 30

Black = (0, 0, 0)
White = (255, 255, 255)
KBlue = (65, 105, 225)
DT = (3, 54, 73)
AGN = (0, 250, 154)

BGColor = DT
TileColor = AGN
TextColor = White
BorderColor = KBlue
FontSize = 20

ButtonColor = White
ButtonTextColor = Black
MSGColor = White

XMargin = int((WinWidth - (TileSize * BWidth + (BWidth - 1))) / 2)
YMargin = int((WinHeight - (TileSize * BHeight + (BHeight - 1))) / 2)

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

def main():
    global FPSClock, DisplaySurf, BasicFont, Reset_Surf, Reset_Rect, New_Surf, New_Rect 

    pygame.init()
    FPSClock = pygame.time.Clock()
    DisplaySurf = pygame.display.set_mode((WinWidth, WinHeight))
    pygame.display.set_caption('Pyatnashki')
    BasicFont = pygame.font.Font('freesansbold.ttf', FontSize)

    Reset_Surf, Reset_Rect = makeText('Перезапустить', TextColor, TileColor, WinWidth - 120, WinHeight - 90)
    New_Surf, New_Rect = makeText('Новая игра', TextColor, TileColor, WinWidth - 120, WinHeight - 60)

    mainBoard, solutionSeq = generateNewPuzzle(80)
    SolvedBoard = getStartingBoard()
    allMoves = []

    while True:
        slideTo = None
        msg = ''
        if mainBoard == SolvedBoard:
            msg = 'Решено!'
        drawBoard(mainBoard, msg)

        checkForQuit()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                spotx, spoty = getSpotClicked(mainBoard, event.pos[0], event.pos[1])

                if (spotx, spoty) == (None, None):
                    if Reset_Rect.collidepoint(event.pos):
                        resetAnimation(mainBoard, allMoves)
                        allMoves = []
                    elif New_Rect.collidepoint(event.pos):
                        mainBoard, solutionSeq = generateNewPuzzle(80)
                        allMoves = []
                else:
                    blankx, blanky = getBlankPosition(mainBoard)
                    if spotx == blankx + 1 and spoty == blanky:
                        slideTo = LEFT
                    elif spotx == blankx - 1 and spoty == blanky:
                        slideTo = RIGHT
                    elif spotx == blankx and spoty == blanky + 1:
                        slideTo = UP
                    elif spotx == blankx and spoty == blanky - 1:
                        slideTo = DOWN

            elif event.type == KEYUP:
                if event.key in (K_LEFT, K_a) and isValidMove(mainBoard, LEFT):
                    slideTo = LEFT
                elif event.key in (K_RIGHT, K_d) and isValidMove(mainBoard, RIGHT):
                    slideTo = RIGHT
                elif event.key in (K_UP, K_w) and isValidMove(mainBoard, UP):
                    slideTo = UP
                elif event.key in (K_DOWN, K_s) and isValidMove(mainBoard, DOWN):
                    slideTo = DOWN
        
        if slideTo:
            slideAnimation(mainBoard, slideTo, 'Нажми на клетку или нажимай стрелочки чтобы передвинуть.', 8)
            makeMove(mainBoard, slideTo)
            allMoves.append(slideTo)
        pygame.display.update()
        FPSClock.tick(FPS)

def terminate():
    pygame.quit()
    sys.exit()

def checkForQuit():
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event)

def getStartingBoard():
    counter = 1
    board = []
    for x in range(BWidth):
        column = []
        for y in range(BHeight):
            column.append(counter)
            counter += BWidth
        board.append(column)
        counter -= BWidth * (BHeight - 1) + BWidth - 1

    board[BWidth-1] [BHeight-1] = None
    return board

def getBlankPosition(board):
    for x in range(BWidth):
        for y in range(BHeight):
            if board[x][y] == None:
                return (x, y)

def makeMove(board, move):
    blankx, blanky = getBlankPosition(board)
    if move == UP:
        board[blankx][blanky], board[blankx][blanky + 1] = board[blankx][blanky + 1], board[blankx][blanky]
    elif move == DOWN:
        board[blankx][blanky], board[blankx][blanky - 1] = board[blankx][blanky - 1], board[blankx][blanky]
    elif move == LEFT:
        board[blankx][blanky], board[blankx + 1][blanky] = board[blankx + 1][blanky], board[blankx][blanky]
    elif move == RIGHT:
        board[blankx][blanky], board[blankx - 1][blanky] = board[blankx - 1][blanky], board[blankx][blanky]

def isValidMove(board, move):
    blankx, blanky = getBlankPosition(board)
    return (move == UP and blanky != len(board[0]) - 1) or \
            (move == DOWN and blanky != 0) or \
            (move == LEFT and blankx != len(board) - 1) or \
            (move == RIGHT and blankx != 0)

def getRandomMove(board, lastMove=None):
    validMoves = [UP, DOWN, LEFT, RIGHT]
    if lastMove == UP or not isValidMove(board, DOWN):
        validMoves.remove(DOWN)
    if lastMove == DOWN or not isValidMove(board, UP):
        validMoves.remove(UP)
    if lastMove == LEFT or not isValidMove(board, RIGHT):
        validMoves.remove(RIGHT)
    if lastMove == RIGHT or not isValidMove(board, LEFT):
        validMoves.remove(LEFT)

    return random.choice(validMoves)

def getLeftTopOfTile(tilex, tiley):
    left = XMargin + (tilex * TileSize) + (tilex - 1)
    top = YMargin + (tiley * TileSize) + (tiley - 1)
    return (left, top)

def getSpotClicked(board, x, y):
    for tilex in range(len(board)):
        for tiley in range(len(board[0])):
            left, top = getLeftTopOfTile(tilex, tiley)
            tileRect = pygame.Rect(left, top, TileSize, TileSize)
            if tileRect.collidepoint(x, y):
                return (tilex, tiley)
    return (None, None)

def drawTile(tilex, tiley, number, adjX=0, adjY=0):
    left, top = getLeftTopOfTile(tilex, tiley)
    pygame.draw.rect(DisplaySurf, TileColor, (left + adjX, top + adjY, TileSize, TileSize))
    textSurf = BasicFont.render(str(number), True, TextColor)
    textRect = textSurf.get_rect()
    textRect.center = left + int(TileSize / 2) + adjX, top + int(TileSize / 2) + adjY
    DisplaySurf.blit(textSurf, textRect)

def makeText(text, color, bgcolor, top, left):
    textSurf = BasicFont.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return(textSurf, textRect)

def drawBoard(board, message):
    DisplaySurf.fill(BGColor)
    if message:
        textSurf, textRect = makeText(message, MSGColor, BGColor, 5, 5)
        DisplaySurf.blit(textSurf, textRect)

    for tilex in range(len(board)):
        for tiley in range(len(board[0])):
            if board[tilex][tiley]:
                drawTile(tilex, tiley, board[tilex][tiley])

    left, top = getLeftTopOfTile(0, 0)
    width = BWidth * TileSize
    height = BHeight * TileSize
    pygame.draw.rect(DisplaySurf, BorderColor, (left - 5, top - 5, width + 11, height + 11), 4)

    DisplaySurf.blit(Reset_Surf, Reset_Rect)
    DisplaySurf.blit(New_Surf, New_Rect)

def slideAnimation(board, direction, message, animationSpeed):
    blankx, blanky = getBlankPosition(board)
    if direction == UP:
        moveX = blankx
        moveY = blanky + 1
    elif direction == DOWN:
        moveX = blankx
        moveY = blanky - 1
    elif direction == LEFT:
        moveX = blankx + 1
        moveY = blanky 
    elif direction == RIGHT:
        moveX = blankx - 1
        moveY = blanky

    drawBoard(board, message)
    baseSurf = DisplaySurf.copy()
    moveLeft, moveTop = getLeftTopOfTile(moveX, moveY)
    pygame.draw.rect(baseSurf, BGColor, (moveLeft, moveTop, TileSize, TileSize))

    for i in range (0, TileSize, animationSpeed):
        checkForQuit()
        DisplaySurf.blit(baseSurf, (0, 0))
        if direction == UP:
            drawTile(moveX, moveY, board[moveX][moveY], 0, -i)
        if direction == DOWN:
            drawTile(moveX, moveY, board[moveX][moveY], 0, i)
        if direction == LEFT:
            drawTile(moveX, moveY, board[moveX][moveY], -i, 0)
        if direction == RIGHT:
            drawTile(moveX, moveY, board[moveX][moveY], i, 0)

        pygame.display.update()
        FPSClock.tick(FPS)

def generateNewPuzzle(numSlides):
    sequence = []
    board = getStartingBoard()
    drawBoard(board, '')
    pygame.display.update()
    pygame.time.wait(500)
    lastMove = None
    for i in range (numSlides):
        move = getRandomMove(board, lastMove)
        slideAnimation(board, move, 'Генерируем новый пазл...', int(TileSize / 3))
        makeMove(board, move)
        sequence.append(move)
        lastMove = move
    return(board, sequence)
def resetAnimation(board, allMoves):
    revallMoves = allMoves[:]
    revallMoves.reverse()

    for move in revallMoves:
        if move == UP:
            oppositeMove = DOWN
        elif move == DOWN:
            oppositeMove = UP
        elif move == RIGHT:
            oppositeMove = LEFT
        elif move == LEFT:
            oppositeMove = RIGHT
        slideAnimation(board, oppositeMove, '', int(TileSize / 2))
        makeMove(board, oppositeMove)

if __name__ == '__main__':
    main()
