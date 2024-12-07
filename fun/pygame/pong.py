import sys
import pygame
import numpy as np

pygame.init()

# screen
width = 1920
height = 1280
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("PONG")

# ball
ball_vel = pygame.Vector2(0.4*np.random.rand() + 0.2, 0.4*np.random.rand() + 0.2)
ball_pos = pygame.Vector2(width/2, height/2)
ball_r = 10

# paddle
paddle_height = 10*ball_r
paddle_width = ball_r
paddle_speed = 0.4

# human
human_vel = 0
human_pos = pygame.Vector2(width/30, height/2 - paddle_height/2)
human_rect = pygame.rect.Rect(human_pos.x, human_pos.y, paddle_width, paddle_height)
human_score = 0

# computer
computer_vel = 0
computer_pos = pygame.Vector2(width - human_pos.x, height/2 - paddle_height/2)
computer_rect = pygame.rect.Rect(computer_pos.x, computer_pos.y, paddle_width, paddle_height)
computer_score = 0

# midline
midline = pygame.rect.Rect(width/2, 0, ball_r/2, height)

# clock
dt = 0
FPS = 144
clock = pygame.time.Clock()

# main loop
running = True
while running:
    # handle exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False

    # screen
    screen.fill("black")

    # midline
    pygame.draw.rect(screen, "white", midline)

    # score
    font = pygame.font.SysFont("dejavusans", 100, bold=True)
    text = font.render(str(human_score), True, "white", "black")
    text_rect = text.get_rect()
    text_rect.center = (width/2 - 60, 60)
    screen.blit(text, text_rect)
    text = font.render(str(computer_score), True, "white", "black")
    text_rect = text.get_rect()
    text_rect.center = (width/2 + 60, 60)
    screen.blit(text, text_rect)

    # handle ball
    ball = pygame.draw.circle(screen, "white", ball_pos, ball_r)
    if ball.left < 0:
        computer_score += 1 
        if computer_score == 10: break
        ball_pos = pygame.Vector2(width/2, height/2)
        ball_vel = pygame.Vector2(0.4*np.random.rand() + 0.2, 0.4*np.random.rand() + 0.2)
        continue
    if ball.right > width:
        human_score += 1
        if human_score == 10: break
        ball_pos = pygame.Vector2(width/2, height/2)
        ball_vel = pygame.Vector2(0.4*np.random.rand() + 0.2, 0.4*np.random.rand() + 0.2)
        continue
    if human_rect.colliderect(ball) or computer_rect.colliderect(ball):
        ball_vel.x = -ball_vel.x
    if ball.top < 0 or ball.bottom > height:
        ball_vel.y = -ball_vel.y
    ball_pos += ball_vel*dt
    
    # handle human
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        if human_rect.top > 0:
            human_rect = human_rect.move(0, -paddle_speed*dt)
    if keys[pygame.K_DOWN]:
        if human_rect.bottom < height:
            human_rect = human_rect.move(0, paddle_speed*dt)
    pygame.draw.rect(screen, "white", human_rect)

    # handle computer
    if ball_pos.y < computer_rect.center[1]:
        if computer_rect.top > 0:
            computer_rect = computer_rect.move(0, -paddle_speed*dt)
    if ball_pos.y > computer_rect.center[1]:
        if computer_rect.bottom < height:
            computer_rect = computer_rect.move(0, paddle_speed*dt)
    pygame.draw.rect(screen, "white", computer_rect)

    # flip display
    pygame.display.flip()

    # compute dt
    dt = clock.tick(FPS)

# GAME OVER screen
running = True
while running:
    # handle exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False
    screen.fill("black")
    font = pygame.font.SysFont("dejavusans", 300, bold=True)
    text = font.render("GAME OVER", True, "white", "black")
    text_rect = text.get_rect()
    text_rect.center = (width/2, height/2)
    screen.blit(text, text_rect)
    pygame.display.flip()