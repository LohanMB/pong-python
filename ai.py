def move_ai(paddle, ball, difficulty):
    if difficulty == "Fácil":
        speed = 5
    elif difficulty == "Médio":
        speed = 6
    elif difficulty == "Difícil":
        speed = 7
    else:
        speed = 4  # padrão

    if paddle.centery < ball.centery:
        paddle.y += speed
    elif paddle.centery > ball.centery:
        paddle.y -= speed