import pygame
import time
from snake import Snake
from apple import Apple

SIZE = 40 
SCREEN_WIDTH = 1000 
SCREEN_HEIGHT = 800 

class Game:
    def __init__(self):
        pygame.init()  
        pygame.display.set_caption("Snake Game")  
        pygame.mixer.init()  
        self.background_music()  

        self.surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  
        self.snake = Snake(self.surface)  
        self.apple = Apple(self.surface)  

    def background_music(self):
        pygame.mixer.music.load('BoxCat Games - Tricks.mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1, 0) 

    def play_sound(self, sound_name):
        if sound_name == "crash":
            sound = pygame.mixer.Sound("smw_pipe.wav")
        elif sound_name == 'ding':
            sound = pygame.mixer.Sound("smw_1-up.wav")

        pygame.mixer.Sound.play(sound)

    def reset(self):
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)

    def is_collision(self, x1, y1, x2, y2):
        # Verifica se há colisão entre dois retângulos
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def render_background(self):
        bg = pygame.image.load("background.png").convert()  
        bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))  
        self.surface.blit(bg, (0, 0))  

    def play(self):
        self.render_background()  
        self.snake.walk()  
        self.apple.draw()  
        self.score()  
        pygame.display.flip()  

        # Verifica se a cobra comeu a maçã
        for i in range(self.snake.length):
            if self.is_collision(self.snake.x[i], self.snake.y[i], self.apple.x, self.apple.y):
                self.play_sound("ding") 
                self.snake.increase_length() 
                self.apple.move()

        # Verifica se a cobra colidiu com ela mesma
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound('crash')  
                raise Exception("Colidiu consigo mesma")  

        # Verifica se a cobra colidiu com as bordas da tela
        if not (0 <= self.snake.x[0] <= SCREEN_WIDTH and 0 <= self.snake.y[0] <= SCREEN_HEIGHT):
            self.play_sound('crash')  
            raise Exception("Colidiu com a borda")  

    def score(self):
        font = pygame.font.SysFont('arial', 30)  
        pontuacao = font.render(f"Pontuação: {self.snake.length}", True, (200, 200, 200))  
        self.surface.blit(pontuacao, (850, 10))  

    def game_over(self):
        self.render_background()  
        font = pygame.font.SysFont('arial', 30)  
        line1 = font.render(f"Game over! Sua pontuação foi de {self.snake.length}", True, (255, 255, 255))  
        self.surface.blit(line1, (200, 300))  
        line2 = font.render("Pressione Enter para jogar novamente ou para sair Pressione Escape.", True, (255, 255, 255))  
        self.surface.blit(line2, (200, 350))  
        pygame.mixer.music.pause()  
        pygame.display.flip()  
    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False  

                    if event.key == pygame.K_RETURN:
                        pygame.mixer.music.unpause()  
                        pause = False

                    if not pause:
                        if event.key == pygame.K_a: 
                            self.snake.move_left() 

                        if event.key == pygame.K_d: 
                            self.snake.move_right()  

                        if event.key == pygame.K_w:
                            self.snake.move_up()  

                        if event.key == pygame.K_s: 
                            self.snake.move_down()  

                elif event.type == pygame.QUIT:
                    running = False  

            try:
                if not pause:
                    self.play()  

            except Exception as e:
                self.game_over()  
                pause = True 
                self.reset()  

            time.sleep(.1) 
