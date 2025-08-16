import pygame
from config import *

def reset_ball(ball):
    ball.center = (WIDTH // 2, HEIGHT // 2)

def handle_collision(ball, player1, player2, ball_dx, ball_dy):
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_dy *= -1
    if ball.colliderect(player1) or ball.colliderect(player2):
        ball_dx *= -1
    return ball_dx, ball_dy

def update_score(ball, score1, score2):
    if ball.left <= 0:
        score2 += 1
        reset_ball(ball)
    elif ball.right >= WIDTH:
        score1 += 1
        reset_ball(ball)
    return score1, score2

def draw_game(win, player1, player2, ball, score1, score2):
    win.fill(BLACK)
    pygame.draw.rect(win, WHITE, player1)
    pygame.draw.rect(win, WHITE, player2)
    pygame.draw.ellipse(win, WHITE, ball)
    pygame.draw.aaline(win, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))
    score_text = FONT.render(f"{score1} - {score2}", True, WHITE)
    win.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 20))
    pygame.display.flip()