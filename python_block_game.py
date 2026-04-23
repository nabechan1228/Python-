import pygame
import sys
import time

# 初期化
pygame.init()
clock = pygame.time.Clock()
fps = 60

# 画面サイズ
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('ブロック崩し')

# 色の設定
black= (0, 0, 0)
white = (255,255,255)
blue = (0,0,255)
green = (0,255,0)

# フォントの設定
font = pygame.font.Font(None, 36)

# パドルの設定
paddle_width = 100
paddle_height = 10
paddle_speed = 10
paddle = pygame.Rect(screen_width // 2 - paddle_width // 2, screen_height -30, paddle_width, paddle_height)

# ボールの設定
ball_radius = 10
ball_speed_x = 5
ball_speed_y = 5
ball = pygame.Rect(screen_width // 2, screen_height// 2, ball_radius * 2, ball_radius * 2)

# ブロックの設定
block_width = 60
block_height = 20
block_rows = 5
block_cols = 11
blocks = []
for row in range(block_rows):
    for col in range(block_cols):
        block_x = col * (block_width + 10) + 20
        block_y = row * (block_height + 10) + 35
        block = pygame.Rect(block_x, block_y, block_width, block_height)
        blocks.append(block)  # 扱いやすくするために1次元リストに変更

running = True
game_over = False
game_clear = False
waiting = True # スタート前の待機状態

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_over or game_clear:
                    # ゲームのリセット
                    game_over = False
                    game_clear = False
                    waiting = True
                    blocks = []
                    for row in range(block_rows):
                        for col in range(block_cols):
                            block_x = col * (block_width + 10) + 20
                            block_y = row * (block_height + 10) + 35
                            blocks.append(pygame.Rect(block_x, block_y, block_width, block_height))
                    paddle.x = screen_width // 2 - paddle_width // 2
                    ball_speed_x = 5
                    ball_speed_y = 5
                elif waiting:
                    waiting = False

    if not game_over and not game_clear:
        # パドルの移動
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle.left > 0:
            paddle.x -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle.right < screen_width:
            paddle.x += paddle_speed

        if waiting:
            # 待機中はボールをパドルの上に固定
            ball.centerx = paddle.centerx
            ball.bottom = paddle.top
        else:
            # ボールの移動
            ball.x += ball_speed_x
            ball.y += ball_speed_y

            # 壁との衝突
            if ball.left <= 0 or ball.right >= screen_width:
                ball_speed_x *= -1
            if ball.top <= 0:
                ball_speed_y *= -1
            if ball.bottom >= screen_height:
                game_over = True

            # パドルとの衝突
            if ball.colliderect(paddle):
                # 衝突位置に応じて反射角を変える
                relative_intersect_x = (ball.centerx - paddle.centerx) / (paddle_width / 2)
                ball_speed_x = relative_intersect_x * 8 # 中心から離れるほど横に速くなる
                
                # 縦方向を反転
                ball_speed_y *= -1.05 # 5%加速
                ball_speed_x *= 1.05 # 横も加速
                
                # めり込み防止
                ball.bottom = paddle.top 

            # ブロックとの衝突
            for block in blocks[:]:
                if ball.colliderect(block):
                    ball_speed_y *= -1
                    blocks.remove(block)
                    if not blocks:
                        game_clear = True
                    break

    # 画面の描画
    screen.fill(black)
    pygame.draw.rect(screen, white, paddle)
    pygame.draw.circle(screen, white, ball.center, ball_radius)
    for block in blocks:
        pygame.draw.rect(screen, green, block)

    # メッセージ表示
    if waiting and not game_over and not game_clear:
        message = font.render("Press SPACE to Start", True, white)
        screen.blit(message, (screen_width // 2 - 120, screen_height // 2 + 50))
        
    if game_over:
        message = font.render("GAME OVER", True, blue)
        screen.blit(message, (screen_width // 2 - 80, screen_height // 2))
        retry_msg = font.render("Press SPACE to Retry", True, white)
        screen.blit(retry_msg, (screen_width // 2 - 110, screen_height // 2 + 50))
        
    if game_clear:
        message = font.render("CLEAR!", True, blue)
        screen.blit(message, (screen_width // 2 - 50, screen_height // 2))
        retry_msg = font.render("Press SPACE to Play Again", True, white)
        screen.blit(retry_msg, (screen_width // 2 - 150, screen_height // 2 + 50))

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
sys.exit()
        
        
        
    







