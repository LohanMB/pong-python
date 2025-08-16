import pygame
import sys
from config import *
from game import draw_game, handle_collision, update_score, reset_ball
from ai import move_ai

# Inicialização
pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong do Lohan")
CLOCK = pygame.time.Clock()

# Sons
click_sound = pygame.mixer.Sound("assets/sounds/click.wav")
hover_sound = pygame.mixer.Sound("assets/sounds/hover.wav")
pygame.mixer.music.load("assets/sounds/menu_theme.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)  # loop infinito

# Logo
logo = pygame.image.load("assets/logo.png")
logo = pygame.transform.scale(logo, (300, 100))


# Estados
MODE = "MENU"
DIFFICULTY = "Fácil"
POINT_LIMIT = 3
paused = False

# Objetos
ball = pygame.Rect(WIDTH//2 - 10, HEIGHT//2 - 10, 20, 20)
player1 = pygame.Rect(50, HEIGHT//2 - 60, 10, 120)
player2 = pygame.Rect(WIDTH - 60, HEIGHT//2 - 60, 10, 120)
ball_dx, ball_dy = BALL_SPEED, BALL_SPEED
score1, score2 = 0, 0

# Função para desenhar botões, botões com bordas arredondadas e efeito de escala.
hovered_button = None

def draw_gradient_background(surface, top_color, bottom_color):
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
        g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
        b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (WIDTH, y))

def draw_button(rect, text):
    global hovered_button
    mouse_pos = pygame.mouse.get_pos()
    hovered = rect.collidepoint(mouse_pos)
    if hovered and hovered_button != rect:
        hover_sound.play()
        hovered_button = rect

    base_color = (0, 80, 200)
    hover_color = (0, 120, 255)
    color = hover_color if hovered else base_color

    scale = 1.05 if hovered else 1.0
    scaled_rect = pygame.Rect(
        rect.x - (rect.width * (scale - 1)) // 2,
        rect.y - (rect.height * (scale - 1)) // 2,
        int(rect.width * scale),
        int(rect.height * scale)
    )

    pygame.draw.rect(WIN, color, scaled_rect, border_radius=12)
    pygame.draw.rect(WIN, WHITE, scaled_rect, 2, border_radius=12)

    label = FONT.render(text, True, WHITE)
    WIN.blit(label, (scaled_rect.x + (scaled_rect.width - label.get_width()) // 2,
                     scaled_rect.y + (scaled_rect.height - label.get_height()) // 2))


# Menu com botões interativos
def draw_menu_buttons():
    draw_gradient_background(WIN, (10, 10, 40), (30, 30, 100))
    WIN.blit(logo, (WIDTH//2 - 150, 30))

    buttons = {
        "1x1": pygame.Rect(WIDTH//2 - 100, 150, 200, 50),
        "1xIA": pygame.Rect(WIDTH//2 - 100, 220, 200, 50),
        "Dificuldade": pygame.Rect(WIDTH//2 - 100, 290, 200, 50),
        "Pontuação": pygame.Rect(WIDTH//2 - 100, 360, 200, 50),
    }

    draw_button(buttons["1x1"], "Jogador vs Jogador")
    draw_button(buttons["1xIA"], "Jogador vs IA")
    draw_button(buttons["Dificuldade"], f"Dificuldade: {DIFFICULTY}")
    draw_button(buttons["Pontuação"], f"Pontuação: {POINT_LIMIT}")

    pygame.display.flip()
    return buttons


# Menu de pausa
def draw_pause_menu():
    WIN.fill(BLACK)
    paused_text = FONT.render("Jogo Pausado", True, WHITE)
    option1 = FONT.render("R - Reiniciar", True, WHITE)
    option2 = FONT.render("M - Menu Inicial", True, WHITE)
    option3 = FONT.render("ESC - Voltar ao jogo", True, WHITE)
    WIN.blit(paused_text, (WIDTH//2 - paused_text.get_width()//2, 150))
    WIN.blit(option1, (WIDTH//2 - option1.get_width()//2, 220))
    WIN.blit(option2, (WIDTH//2 - option2.get_width()//2, 270))
    WIN.blit(option3, (WIDTH//2 - option3.get_width()//2, 320))
    pygame.display.flip()

def draw_pause_buttons():
    WIN.fill(BLACK)
    title = FONT.render("Jogo Pausado", True, WHITE)
    WIN.blit(title, (WIDTH//2 - title.get_width()//2, 100))

    buttons = {
        "Reiniciar": pygame.Rect(WIDTH//2 - 100, 180, 200, 50),
        "Menu": pygame.Rect(WIDTH//2 - 100, 250, 200, 50),
        "Voltar": pygame.Rect(WIDTH//2 - 100, 320, 200, 50)
    }

    draw_button(buttons["Reiniciar"], "Reiniciar")
    draw_button(buttons["Menu"], "Menu Inicial")
    draw_button(buttons["Voltar"], "Voltar ao Jogo")

    pygame.display.flip()
    return buttons

# Loop principal
while True:
    CLOCK.tick(FPS)

    if MODE == "MENU":
        buttons = draw_menu_buttons()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                click_sound.play()
                if buttons["1x1"].collidepoint(mouse_pos):
                    MODE = "1x1"
                elif buttons["1xIA"].collidepoint(mouse_pos):
                    MODE = "1xIA"
                elif buttons["Dificuldade"].collidepoint(mouse_pos):
                    if DIFFICULTY == "Fácil":
                        DIFFICULTY = "Médio"
                    elif DIFFICULTY == "Médio":
                        DIFFICULTY = "Difícil"
                    else:
                        DIFFICULTY = "Fácil"
                elif buttons["Pontuação"].collidepoint(mouse_pos):
                    idx = POINT_LIMITS.index(POINT_LIMIT)
                    POINT_LIMIT = POINT_LIMITS[(idx + 1) % len(POINT_LIMITS)]
                elif buttons["Iniciar"].collidepoint(mouse_pos):
                    score1, score2 = 0, 0
                    reset_ball(ball)
                    paused = False

    elif paused:
        pause_buttons = draw_pause_buttons()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if pause_buttons["Reiniciar"].collidepoint(mouse_pos):
                    score1, score2 = 0, 0
                    reset_ball(ball)
                    paused = False
                elif pause_buttons["Menu"].collidepoint(mouse_pos):
                    MODE = "MENU"
                    score1, score2 = 0, 0
                    reset_ball(ball)
                    paused = False
                elif pause_buttons["Voltar"].collidepoint(mouse_pos):
                    paused = False

    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and player1.top > 0:
            player1.y -= PADDLE_SPEED
        if keys[pygame.K_s] and player1.bottom < HEIGHT:
            player1.y += PADDLE_SPEED

        if MODE == "1x1":
            if keys[pygame.K_UP] and player2.top > 0:
                player2.y -= PADDLE_SPEED
            if keys[pygame.K_DOWN] and player2.bottom < HEIGHT:
                player2.y += PADDLE_SPEED
        elif MODE == "1xIA":
            move_ai(player2, ball, DIFFICULTY)

        ball.x += ball_dx
        ball.y += ball_dy
        ball_dx, ball_dy = handle_collision(ball, player1, player2, ball_dx, ball_dy)
        score1, score2 = update_score(ball, score1, score2)

        if score1 >= POINT_LIMIT or score2 >= POINT_LIMIT:
            MODE = "MENU"
            score1, score2 = 0, 0
            reset_ball(ball)

        draw_game(WIN, player1, player2, ball, score1, score2)