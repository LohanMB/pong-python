import pygame

# Tela
WIDTH, HEIGHT = 800, 600
FPS = 90

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fonte
pygame.init()
FONT = pygame.font.SysFont("Arial", 20)

# Velocidades
BALL_SPEED = 7
PADDLE_SPEED = 9

# Pontuação
POINT_LIMITS = [3, 5, 7, 10]