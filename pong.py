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

def drawText(text, font, surface, x, y): # vẽ và định vị 
    textobj = font.render(text, 1, WHITE)
    textrect = textobj.get_rect()
    textrect.centerx = x
    textrect.centery = y
    surface.blit(textobj, textrect)

def rectCollideSide(a, b): # cho hai hình chữ nhật (a) và (b)
                           # xác định điểm (b) của hình chữ nhật đó (a) chạm vào khi (a) & (b) chồng lên nhau hoặc va chạm
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
                                                      # giả định rằng quả bóng chỉ nảy lên khi ra khỏi tường và quả bóng di chuyển cùng một khoảng cách theo hướng x và y

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

def randomReturn(vDir): # hướng dọc cho trước, trả về hướng ngang ngẫu nhiên cho quả bóng

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

def resetPaddles(): # đặt lại paddles về giữa

    pTop = {'rect':pygame.Rect(PADDLETOP_LEFT, PADDLETOP_TOP, PADDLEWIDTH, PADDLEHEIGHT), 'color':GREEN}
    pBot = {'rect':pygame.Rect(PADDLEBOTTOM_LEFT, PADDLEBOTTOM_TOP, PADDLEWIDTH, PADDLEHEIGHT), 'color':GREEN}
    return pTop, pBot

# set up pygame
pygame.mixer.pre_init(44100, -16, 1, 512) # loại bỏ độ trễ âm thanh
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

#  thiết lập các biến hướng
DOWNLEFT = 1 
DOWNRIGHT = 3
UPLEFT = 7
UPRIGHT = 9

# biến di chuyển
moveLeft = moveRight = moveDown = moveUp = False

# set up biến giao bóng
serveLeft = serveRight = False

# set up chiều rộng thanh trượt và bóng
PADDLEWIDTH = 50
PADDLEHEIGHT = 10
BALLWIDTH = 10

# set up tốc độ thanh trượt và bóng
PADDLESPEED = 4
BALLSPEED = 4

# set up thanh trượt dưới ( người )
PADDLEBOTTOM_LEFT = WINDOWWIDTH/2 - PADDLEWIDTH/2 
PADDLEBOTTOM_TOP = 9*WINDOWHEIGHT/10 - PADDLEHEIGHT

# set up thanh trượt trên ( máy)
PADDLETOP_LEFT = WINDOWWIDTH/2- PADDLEWIDTH/2 
PADDLETOP_TOP = WINDOWHEIGHT/10 

# màn hình khởi động
drawText('PONG!', font, windowSurface, (WINDOWWIDTH/2), (WINDOWHEIGHT/2)-25)
drawText('Nhan bat ki de bat dau.', font, windowSurface, (WINDOWWIDTH/2), (WINDOWHEIGHT/2)+25)
pygame.display.update()
waitForPlayerToPressKey()
    
# chạy vòng lập chính
while True:

    # reset điểm số về 0
    playerScore = 0
    computerScore = 0

    # set up và reset paddles
    paddleTop, paddleBottom = resetPaddles()

    # màn hình trống
    windowSurface.fill(BLACK)

    # select paddle
    drawText('1 = Thanh Trên', font, windowSurface, (WINDOWWIDTH/2), (WINDOWHEIGHT/2)-25)
    drawText('2 = Thanh Dưới', font, windowSurface, (WINDOWWIDTH/2), (WINDOWHEIGHT/2)+25)
    pygame.draw.rect(windowSurface, paddleBottom['color'], paddleBottom['rect'])
    pygame.draw.rect(windowSurface, paddleTop['color'], paddleTop['rect'])
    pygame.display.update()
    while True:
        pressedKeys = pygame.key.get_pressed() # "Cấu trúc mảng lớn gồm các số 1 và 0 với mỗi không gian cụ thể được gán cho trạng thái khóa tương ứng"
        if pressedKeys[49] == 1: # 1 được chọn
            playerIsTopPaddle = True
            break
        if pressedKeys[50] == 1: # 2 được chọn 
            playerIsTopPaddle = False
            break
        else:
            waitForPlayerToPressKey() # ngăn chặn việc vào vòng lập vô hạn

    # setup bóng (*)4
    ball = {'rect':pygame.Rect(WINDOWWIDTH/2-BALLWIDTH/2, WINDOWHEIGHT/2-BALLWIDTH/2, BALLWIDTH, BALLWIDTH), 'color':WHITE, 'dir':DOWNLEFT}
    if playerIsTopPaddle:
        ball['rect'].midtop = paddleTop['rect'].midbottom
        randomReturn('DOWN')
    else:
        ball['rect'].midbottom = paddleBottom['rect'].midtop
        randomReturn('UP')

    # màn hình trống
    windowSurface.fill(BLACK)
    
    # hiện thị thanh chọn để giao bóng (*)5
    drawText('Bạn giao bóng.', font, windowSurface, (WINDOWWIDTH/2), (WINDOWHEIGHT/2)-25)
    drawText('bấm bất kì để giao bóng.', font, windowSurface, (WINDOWWIDTH/2), (WINDOWHEIGHT/2)+25)
    pygame.draw.rect(windowSurface, paddleBottom['color'], paddleBottom['rect'])
    pygame.draw.rect(windowSurface, paddleTop['color'], paddleTop['rect'])
    pygame.display.update()
    waitForPlayerToPressKey()

    # run gameplay loop (vòng lặp trò chơi. *6)
    while True:

        # đưa biến giao bóng về false để giao bóng
        serveBall = False

        # vẽ nền đen
        windowSurface.fill(BLACK)
 
        # kiểm tra sự kiện
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN: # một phím được nhấn
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
            if event.type == KEYUP: # một phím được thả ( a = 97)(d=100)
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
        
        # cách mà bóng di chuyển
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

        # bóng bật sang trái
        if ball['rect'].left < 0:
            if ball['dir'] == DOWNLEFT:
                ball['dir'] = DOWNRIGHT
            if ball['dir'] == UPLEFT: 
                ball['dir'] = UPRIGHT

        # bóng bật sang phải
        if ball['rect'].right > WINDOWWIDTH:
            if ball['dir'] == DOWNRIGHT:
                ball['dir'] = DOWNLEFT
            if ball['dir'] == UPRIGHT: 
                ball['dir'] = UPLEFT

        # bóng chạm dưới - top paddle được điểm, reset(8)
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

        # bóng chạm trên - bottom paddle được điểm, reset
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
                    
        # người + máy di chuyển nếu người chơi là thanh trượt trên(9)
        if playerIsTopPaddle:

            # người chơi ở trên
            if moveLeft and paddleTop['rect'].left > 0:
                paddleTop['rect'].left -= PADDLESPEED
            if moveRight and paddleTop['rect'].right < WINDOWWIDTH:
                paddleTop['rect'].right += PADDLESPEED

            # máy ở dưới
            if ball['dir'] == DOWNRIGHT or ball['dir'] == DOWNLEFT:
                returnPosition = ballTrajectory(ball['rect'].centerx, ball['rect'].centery, paddleBottom['rect'].bottom, ball['dir'], WINDOWWIDTH)
                if returnPosition < paddleBottom['rect'].centerx and paddleBottom['rect'].left > 0:
                    paddleBottom['rect'].centerx -= PADDLESPEED
                if returnPosition > paddleBottom['rect'].centerx and paddleBottom['rect'].right < WINDOWWIDTH:
                    paddleBottom['rect'].centerx += PADDLESPEED

        # người + máy di chuyển nếu người chơi là thanh trượt dưới
        else:

            # người chơi ở dưới
            if moveLeft and paddleBottom['rect'].left > 0:
                paddleBottom['rect'].left -= PADDLESPEED
            if moveRight and paddleBottom['rect'].right < WINDOWWIDTH:
                paddleBottom['rect'].right += PADDLESPEED

            # máy ở trên
            if ball['dir'] == UPRIGHT or ball['dir'] == UPLEFT:
                returnPosition = ballTrajectory(ball['rect'].centerx, ball['rect'].centery, paddleTop['rect'].bottom, ball['dir'], WINDOWWIDTH)
                if returnPosition < paddleTop['rect'].centerx and paddleTop['rect'].left > 0:
                    paddleTop['rect'].centerx -= PADDLESPEED
                if returnPosition > paddleTop['rect'].centerx and paddleTop['rect'].right < WINDOWWIDTH:
                    paddleTop['rect'].centerx += PADDLESPEED
        
        # kiểm tra va chạm giữa thanh trượt và bóng ( cho cả hai thanh trượt 10*)
        for paddle in [paddleTop, paddleBottom]: 

            # va chạm giữa thanh trượt và bóng
            if ball['rect'].colliderect(paddle['rect']):

                # phát âm thanh va chạm
                pongSound.play()
                
                # va chạm + đổi hướng bóng nếu người chơi là thanh trượt trên
                if playerIsTopPaddle:
                    
                    # Người chơi ở trên, bóng va chạm với phía dưới - chuyển hướng dựa trên chuyển động của người chơi
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

                    # máy ở dưới - bóng va chạm với phía trên - trả về ngẫu nhiên
                    if rectCollideSide(ball['rect'], paddle['rect']) == 'TOP':
                        if ball['dir'] == DOWNLEFT or ball['dir'] == DOWNRIGHT:
                            randomReturn('UP')
                            
                # va chạm + đổi hướng bóng nếu người chơi là thanh trượt dưới
                else:

                    # người chơi ở dưới, bóng va chạm với phía trên - chuyển hướng dựa trên chuyển động của người chơi
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

                    # máy ở trên - bóng va chạm với phía dưới - trả về ngẫu nhiên
                    if rectCollideSide(ball['rect'], paddle['rect']) == 'BOTTOM':
                        if ball['dir'] == UPLEFT or ball['dir'] == UPRIGHT:
                            randomReturn('DOWN')
                        
                # nảy lên nếu bóng chạm vào phía trái của thanh trượt(11*)
                if rectCollideSide(ball['rect'], paddle['rect']) == 'LEFT':
                    if ball['dir'] == DOWNRIGHT:
                        ball['dir'] = DOWNLEFT
                    if ball['dir'] == UPRIGHT:
                        ball['dir'] = UPLEFT

                # nảy lên nếu bóng chạm vào phía phải của thanh trượt
                if rectCollideSide(ball['rect'], paddle['rect']) == 'RIGHT':
                    if ball['dir'] == DOWNLEFT:
                        ball['dir'] = DOWNRIGHT
                    if ball['dir'] == UPLEFT:
                        ball['dir'] = UPRIGHT
                        
            # vẽ thanh trượt
            pygame.draw.rect(windowSurface, paddle['color'], paddle['rect'])

        # vẽ bóng
        pygame.draw.rect(windowSurface, ball['color'], ball['rect'])

        # dừng nếu người chơi hoặc máy đạt 5 điểm
        if playerScore == 5 or computerScore == 5:
            break

        # vẽ điểm số
        drawText('%s - %s' %(playerScore, computerScore), font, windowSurface, WINDOWWIDTH/2, WINDOWHEIGHT/2)

        # dừng nếu bóng được giao
        if serveBall:
            pygame.time.delay(2000)

        # vẽ màn hình
        pygame.display.update()
        mainClock.tick(100)

    # kiểm tra điểm số cuối cùng
    if playerScore == 5:
        endSound = winSound
        endMessage = 'Thắng!'
    else:
        endSound = loseSound
        endMessage = 'Thua!'

    # hiển thị màn hình kết thúc
    endSound.play()
    drawText('hết game. Bạn %s' %(endMessage), font, windowSurface, (WINDOWWIDTH/2), (WINDOWHEIGHT/2)-50)
    drawText('%s - %s' %(playerScore, computerScore), font, windowSurface, (WINDOWWIDTH/2), (WINDOWHEIGHT/2))
    drawText('Nhấn phím bất kì để bắt đầu lại.', font, windowSurface, (WINDOWWIDTH/2), (WINDOWHEIGHT/2)+50)
    pygame.display.update()
    waitForPlayerToPressKey()
    endSound.stop()