import pygame, sys, random, time
from pygame.locals import *

def terminate(): # end game
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey(): # nhấn phím để tiếp tục, trừ khi nhấn phím Escape hoặc X
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return

def drawText(text, font, surface, x, y): # vẽ và định vị văn bản 
    textobj = font.render(text, 1, WHITE)
    textrect = textobj.get_rect()
    textrect.centerx = x
    textrect.centery = y
    surface.blit(textobj, textrect)

def rectCollideSide(a, b): # cho hai hình chữ nhật (a) và (b)
                           # xác định cạnh của (b) hình chữ nhật đó (a) chạm vào khi (a) & (b) chồng lên nhau hoặc va chạm
    if abs(a.right-b.left) < abs(a.left-b.right): 
        if abs(a.bottom-b.top) < abs(a.top-b.bottom): 
            if abs(a.right-b.left) > abs(a.bottom-b.top):
                return 'TOP'
            else:
                return 'LEFT'
        else:
            if abs(a.right-b.left) > abs(a.top-b.bottom):
                return 'BOTTOM'
            else:
                return 'LEFT'
    else:
        if abs(a.bottom-b.top) < abs(a.top-b.bottom):
            if abs(a.left-b.right) > abs(a.bottom-b.top):
                return 'TOP'
            else:
                return 'RIGHT'
        else:
            if abs(a.left-b.right) > abs(a.top-b.bottom):
                return 'BOTTOM'
            else:
                return 'RIGHT'

def ballTrajectory(x1, y1, y2, ballDir, windowWidth): # cho tọa độ bắt đầu x1 y1, tọa độ kết thúc y2, hướng bóng và chiều rộng cửa sổ
                                                      # về tọa độ kết thúc x2 khi máy dùng thanh trượt
                                                      # giả định rằng quả bóng chỉ nảy lên khi ra khỏi tường tối đa và quả bóng di chuyển cùng một khoảng cách theo hướng x và y

    dy = abs(y2-y1)
    dx = dy

    if ballDir == UPRIGHT or ballDir == DOWNRIGHT:
        dx_wall = windowWidth - x1
    else:
        dx_wall = x1

    if dx < dx_wall:
        if ballDir == UPRIGHT or ballDir == DOWNRIGHT:
            return x1 + dx
        else:
            return x1 - dx
    else:
        x_offset = dx - dx_wall
        if ballDir == UPRIGHT or ballDir == DOWNRIGHT:
            return windowWidth - x_offset
        else:
            return x_offset

def randomReturn(vDir): # given vertical direction, returns random horizontal direction for ball

    if vDir == 'UP':
        if random.randint(0,1) == 0:
            ball['dir'] = UPRIGHT
        else:
            ball['dir'] = UPLEFT
    if vDir == 'DOWN':
        if random.randint(0,1) == 0:
            ball['dir'] = DOWNRIGHT
        else:
            ball['dir'] = DOWNLEFT

def resetPaddles(): # resets paddles to center

    pTop = {'rect':pygame.Rect(PADDLETOP_LEFT, PADDLETOP_TOP, PADDLEWIDTH, PADDLEHEIGHT), 'color':GREEN}
    pBot = {'rect':pygame.Rect(PADDLEBOTTOM_LEFT, PADDLEBOTTOM_TOP, PADDLEWIDTH, PADDLEHEIGHT), 'color':GREEN}
    return pTop, pBot

# set up pygame
pygame.mixer.pre_init(44100, -16, 1, 512) # needed to remove sound delays
pygame.init()
mainClock = pygame.time.Clock()

# set up window
WINDOWWIDTH = 750
WINDOWHEIGHT = 600
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Pong')

# set up color
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# set up font
font = pygame.font.SysFont('Courier New', 24)

# set up sound
pongSound = pygame.mixer.Sound('pongsound.wav')
winSound = pygame.mixer.Sound('gamewin.wav')
loseSound = pygame.mixer.Sound('gamelose.flac')

# set up direction variables 
DOWNLEFT = 1 
DOWNRIGHT = 3
UPLEFT = 7
UPRIGHT = 9

# set up movement variables
moveLeft = moveRight = moveDown = moveUp = False

# set up serve direction variables
serveLeft = serveRight = False

# set up paddle and ball sizes
PADDLEWIDTH = 50
PADDLEHEIGHT = 10
BALLWIDTH = 10

# set up paddle + ball move speed (pixels moved per iteration)
PADDLESPEED = 4
BALLSPEED = 4

# set up bottom paddle, controlled by player
PADDLEBOTTOM_LEFT = WINDOWWIDTH/2 - PADDLEWIDTH/2 
PADDLEBOTTOM_TOP = 9*WINDOWHEIGHT/10 - PADDLEHEIGHT

# set up top paddle, controlled by computer
PADDLETOP_LEFT = WINDOWWIDTH/2- PADDLEWIDTH/2 
PADDLETOP_TOP = WINDOWHEIGHT/10 

# show start screen
drawText('PONG!', font, windowSurface, (WINDOWWIDTH/2), (WINDOWHEIGHT/2)-25)
drawText('Nhan bat ki de bat dau.', font, windowSurface, (WINDOWWIDTH/2), (WINDOWHEIGHT/2)+25)
pygame.display.update()
waitForPlayerToPressKey()
    
# run loop
while True:

    # set (or reset) scores
    playerScore = 0
    computerScore = 0

    # set up or reset paddles 
    paddleTop, paddleBottom = resetPaddles()

    # blank out screen
    windowSurface.fill(BLACK)

    # select paddle
    drawText('1 = Thanh Trên', font, windowSurface, (WINDOWWIDTH/2), (WINDOWHEIGHT/2)-25)
    drawText('2 = Thanh Dưới', font, windowSurface, (WINDOWWIDTH/2), (WINDOWHEIGHT/2)+25)
    pygame.draw.rect(windowSurface, paddleBottom['color'], paddleBottom['rect'])
    pygame.draw.rect(windowSurface, paddleTop['color'], paddleTop['rect'])
    pygame.display.update()
    while True:
        pressedKeys = pygame.key.get_pressed() # giant array of 1s and 0s with each specific space assigned towards key state
        if pressedKeys[49] == 1: # 1 is pressed
            playerIsTopPaddle = True
            break
        if pressedKeys[50] == 1: # 2 is pressed
            playerIsTopPaddle = False
            break
        else:
            waitForPlayerToPressKey() # if any other key is pressed, does not enter infinite while loop

    # set up ball
    ball = {'rect':pygame.Rect(WINDOWWIDTH/2-BALLWIDTH/2, WINDOWHEIGHT/2-BALLWIDTH/2, BALLWIDTH, BALLWIDTH), 'color':WHITE, 'dir':DOWNLEFT}
    if playerIsTopPaddle:
        ball['rect'].midtop = paddleTop['rect'].midbottom
        randomReturn('DOWN')
    else:
        ball['rect'].midbottom = paddleBottom['rect'].midtop
        randomReturn('UP')

    # blank out screen
    windowSurface.fill(BLACK)
    
    # show which paddle goes first screen
    drawText('Bạn giao bóng.', font, windowSurface, (WINDOWWIDTH/2), (WINDOWHEIGHT/2)-25)
    drawText('bấm bất kì để giao bóng.', font, windowSurface, (WINDOWWIDTH/2), (WINDOWHEIGHT/2)+25)
    pygame.draw.rect(windowSurface, paddleBottom['color'], paddleBottom['rect'])
    pygame.draw.rect(windowSurface, paddleTop['color'], paddleTop['rect'])
    pygame.display.update()
    waitForPlayerToPressKey()

    # run gameplay loop
    while True:

        # serve ball boolean
        serveBall = False

        # draw black background onto surface
        windowSurface.fill(BLACK)
 
        # check for events
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN: # a key is pressed
                if event.key == K_LEFT:
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT:
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP:
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN:
                    moveUp = False
                    moveDown = True
                if event.key == ord('a'):
                    serveLeft = False
                    serveRight = True
                if event.key == ord('d'):
                    serveRight = False
                    serveLeft = True
            if event.type == KEYUP: # a key is released
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == K_LEFT:
                    moveLeft = False
                if event.key == K_RIGHT:
                    moveRight = False
                if event.key == K_UP:
                    moveUp = False
                if event.key == K_DOWN:
                    moveDown = False
                if event.key == ord('a'):
                    serveLeft = False
                if event.key == ord('d'):
                    serveRight = False
        
        # move ball data structure
        if ball['dir'] == DOWNLEFT: 
            ball['rect'].left -= BALLSPEED 
            ball['rect'].top += BALLSPEED 
        if ball['dir'] == DOWNRIGHT:
            ball['rect'].left += BALLSPEED
            ball['rect'].top += BALLSPEED
        if ball['dir'] == UPLEFT:
            ball['rect'].left -= BALLSPEED
            ball['rect'].top -= BALLSPEED
        if ball['dir'] == UPRIGHT:
            ball['rect'].left += BALLSPEED
            ball['rect'].top -= BALLSPEED

        # ball bounces off left side
        if ball['rect'].left < 0:
            if ball['dir'] == DOWNLEFT:
                ball['dir'] = DOWNRIGHT
            if ball['dir'] == UPLEFT: 
                ball['dir'] = UPRIGHT

        # ball bounces off right side
        if ball['rect'].right > WINDOWWIDTH:
            if ball['dir'] == DOWNRIGHT:
                ball['dir'] = DOWNLEFT
            if ball['dir'] == UPRIGHT: 
                ball['dir'] = UPLEFT

        # ball hits bottom - top paddle gets point, reset 
        if ball['rect'].bottom > WINDOWHEIGHT:
            if playerIsTopPaddle:
                playerScore += 1
            else:
                computerScore += 1
            serveBall = True
            paddleTop, paddleBottom = resetPaddles()
            ball['rect'].midtop = paddleTop['rect'].midbottom
            pygame.draw.rect(windowSurface, ball['color'], ball['rect'])
            if not playerIsTopPaddle: 
                randomReturn('DOWN')

        # ball hits top - bottom paddle gets point, reset 
        if ball['rect'].top < 0:
            if not playerIsTopPaddle:
                playerScore += 1
            else:
                computerScore += 1
            serveBall = True
            paddleTop, paddleBottom = resetPaddles()
            ball['rect'].midbottom = paddleBottom['rect'].midtop
            pygame.draw.rect(windowSurface, ball['color'], ball['rect'])
            if playerIsTopPaddle:
                randomReturn('UP')
                    
        # player + computer movement if player is top paddle
        if playerIsTopPaddle:

            # player is top
            if moveLeft and paddleTop['rect'].left > 0:
                paddleTop['rect'].left -= PADDLESPEED
            if moveRight and paddleTop['rect'].right < WINDOWWIDTH:
                paddleTop['rect'].right += PADDLESPEED

            # computer is bottom
            if ball['dir'] == DOWNRIGHT or ball['dir'] == DOWNLEFT:
                returnPosition = ballTrajectory(ball['rect'].centerx, ball['rect'].centery, paddleBottom['rect'].bottom, ball['dir'], WINDOWWIDTH)
                if returnPosition < paddleBottom['rect'].centerx and paddleBottom['rect'].left > 0:
                    paddleBottom['rect'].centerx -= PADDLESPEED
                if returnPosition > paddleBottom['rect'].centerx and paddleBottom['rect'].right < WINDOWWIDTH:
                    paddleBottom['rect'].centerx += PADDLESPEED

        # player + computer movement if player is bottom paddle
        else:

            # player is bottom
            if moveLeft and paddleBottom['rect'].left > 0:
                paddleBottom['rect'].left -= PADDLESPEED
            if moveRight and paddleBottom['rect'].right < WINDOWWIDTH:
                paddleBottom['rect'].right += PADDLESPEED

            # computer is top
            if ball['dir'] == UPRIGHT or ball['dir'] == UPLEFT:
                returnPosition = ballTrajectory(ball['rect'].centerx, ball['rect'].centery, paddleTop['rect'].bottom, ball['dir'], WINDOWWIDTH)
                if returnPosition < paddleTop['rect'].centerx and paddleTop['rect'].left > 0:
                    paddleTop['rect'].centerx -= PADDLESPEED
                if returnPosition > paddleTop['rect'].centerx and paddleTop['rect'].right < WINDOWWIDTH:
                    paddleTop['rect'].centerx += PADDLESPEED
        
        # code that applies to both paddles
        for paddle in [paddleTop, paddleBottom]: 

            # ball collides with paddle
            if ball['rect'].colliderect(paddle['rect']):

                # play pong sound
                pongSound.play()
                
                # collision + redirection of ball if player is top paddle
                if playerIsTopPaddle:
                    
                    # player is top paddle, ball collides with bottom - redirect based on player movement
                    if rectCollideSide(ball['rect'], paddle['rect']) == 'BOTTOM': 
                        if ball['dir'] == UPLEFT:
                            if moveRight == True: 
                                ball['dir'] = DOWNRIGHT
                            else: 
                                ball['dir'] = DOWNLEFT
                        if ball['dir'] == UPRIGHT:
                            if moveLeft == True: 
                                ball['dir'] = DOWNLEFT
                            else: 
                                ball['dir'] = DOWNRIGHT

                    # computer is bottom paddle, ball collides with top - randomize return
                    if rectCollideSide(ball['rect'], paddle['rect']) == 'TOP':
                        if ball['dir'] == DOWNLEFT or ball['dir'] == DOWNRIGHT:
                            randomReturn('UP')
                            
                # collision + redirection of ball if player is bottom paddle
                else:

                    # player is bottom paddle, ball collides with top - redirect based on player movement
                    if rectCollideSide(ball['rect'], paddle['rect']) == 'TOP':
                        if ball['dir'] == DOWNLEFT:
                            if moveRight == True: 
                                ball['dir'] = UPRIGHT
                            else: 
                                ball['dir'] = UPLEFT
                        if ball['dir'] == DOWNRIGHT:
                            if moveLeft == True: 
                                ball['dir'] = UPLEFT
                            else: 
                                ball['dir'] = UPRIGHT

                    # computer is top paddle, ball collides with bottom - randomize return
                    if rectCollideSide(ball['rect'], paddle['rect']) == 'BOTTOM':
                        if ball['dir'] == UPLEFT or ball['dir'] == UPRIGHT:
                            randomReturn('DOWN')
                        
                # bounce if ball hits left of paddle
                if rectCollideSide(ball['rect'], paddle['rect']) == 'LEFT':
                    if ball['dir'] == DOWNRIGHT:
                        ball['dir'] = DOWNLEFT
                    if ball['dir'] == UPRIGHT:
                        ball['dir'] = UPLEFT

                # bounce if ball hits right of paddle
                if rectCollideSide(ball['rect'], paddle['rect']) == 'RIGHT':
                    if ball['dir'] == DOWNLEFT:
                        ball['dir'] = DOWNRIGHT
                    if ball['dir'] == UPLEFT:
                        ball['dir'] = UPRIGHT
                        
            # draw paddle onto surface
            pygame.draw.rect(windowSurface, paddle['color'], paddle['rect'])

        # draw ball onto surface
        pygame.draw.rect(windowSurface, ball['color'], ball['rect'])

        # break if score for one paddle is 5
        if playerScore == 5 or computerScore == 5:
            break

        # draw scores
        drawText('%s - %s' %(playerScore, computerScore), font, windowSurface, WINDOWWIDTH/2, WINDOWHEIGHT/2)

        # pause if point is scored and serve is done
        if serveBall:
            pygame.time.delay(2000)

        # draw window onto screen
        pygame.display.update()
        mainClock.tick(100)

    # check who won game
    if playerScore == 5:
        endSound = winSound
        endMessage = 'Thắng!'
    else:
        endSound = loseSound
        endMessage = 'Thua!'

    # game over
    endSound.play()
    drawText('GAME OVER. YOU %s' %(endMessage), font, windowSurface, (WINDOWWIDTH/2), (WINDOWHEIGHT/2)-50)
    drawText('%s - %s' %(playerScore, computerScore), font, windowSurface, (WINDOWWIDTH/2), (WINDOWHEIGHT/2))
    drawText('Nhấn phím bất kì để bắt đầu lại.', font, windowSurface, (WINDOWWIDTH/2), (WINDOWHEIGHT/2)+50)
    pygame.display.update()
    waitForPlayerToPressKey()
    endSound.stop()