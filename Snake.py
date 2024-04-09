import pygame
from pygame.locals import *
from sys import exit
from random import randint

pygame.init()

# Configuração do volume da música de fundo e carregamento da música
pygame.mixer.music.set_volume(0.4)
background_music = pygame.mixer.music.load('BoxCat Games - Mission.mp3')
pygame.mixer.music.play(-1)

# Som de colisão
collision_sound = pygame.mixer.Sound('smw_blargg.wav')

largura = 640
altura = 480

# Posição inicial da cobra
snake_x_pos = int(largura / 2)
snake_y_pos = int(altura / 2)

speed = 10
x_control = speed
y_control = 0

# Posição inicial da maçã
fruit_x = randint(40, 600)
fruit_y = randint(50, 430)

score = 0
fonte = pygame.font.SysFont('arial', 40, bold=True, italic=True)

# Configuração da tela do jogo
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Jogo')
clock = pygame.time.Clock()
snake_list = []
comprimento_inicial = 5


# Função para aumentar o comprimento da cobra
def snake_size(snake_list):
    for XeY in snake_list:
        pygame.draw.rect(tela, (0, 255, 0), (XeY[0], XeY[1], 20, 20))


# Loop principal do jogo
while True:
    clock.tick(30)
    tela.fill((255, 255, 255))

    mensagem = f'Pontuação: {score}'
    texto_formatado = fonte.render(mensagem, True, (0, 0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

        if event.type == KEYDOWN:
            if event.key == K_a:
                if x_control == speed:
                    pass
                else:
                    x_control = -speed
                    y_control = 0
            if event.key == K_d:
                if x_control == -speed:
                    pass
                else:
                    x_control = speed
                    y_control = 0
            if event.key == K_w:
                if y_control == speed:
                    pass
                else:
                    y_control = -speed
                    x_control = 0
            if event.key == K_s:
                if y_control == -speed:
                    pass
                else:
                    y_control = speed
                    x_control = 0

    snake_x_pos = snake_x_pos + x_control
    snake_y_pos = snake_y_pos + y_control

    snake = pygame.draw.rect(tela, (0, 255, 0),
                             (snake_x_pos, snake_y_pos, 20, 20))
    fruit = pygame.draw.rect(tela, (255, 0, 0), (fruit_x, fruit_y, 20, 20))

    # Verifica colisão entre a cobra e a maçã
    if snake.colliderect(fruit):
        fruit_x = randint(40, 600)
        fruit_y = randint(50, 430)
        score += 1
        collision_sound.play()
        comprimento_inicial += 1

    head = []
    head.append(snake_x_pos)
    head.append(snake_y_pos)

    snake_list.append(head)

    if len(snake_list) > comprimento_inicial:
        del snake_list[0]

    snake_size(snake_list)

    tela.blit(texto_formatado, (450, 40))

    pygame.display.update()
