import pygame
import sys
import time

# 初期化
pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('ボールバウンズ')

# 色の定義
black = (0, 0, 0)
white = (255, 255, 255)

# ボールの設定
ball_radius = 10
ball_speed_x = 5
ball_speed_y = 5
ball = pygame.Rect(screen_width // 2, screen_height // 2, ball_radius * 2, ball_radius * 2)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
    # ボールの移動
    ball.x += ball_speed_x
    ball.y += ball_speed_y
    # 壁との衝突判定
    if ball.left <= 0 or ball.right >= screen_width:
        ball_speed_x = -ball_speed_x
    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y = -ball_speed_y
    # 画面の描画
    screen.fill(black)
    pygame.draw.ellipse(screen, white, ball)
    pygame.display.flip()
    time.sleep(0.01)
    
    
    