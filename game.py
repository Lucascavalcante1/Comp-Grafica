import pygame
import time
from snake import Snake
from apple import Apple
import os

SIZE = 40
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Boribuider")
        pygame.mixer.init()

        self.surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)

    def play_music(self):
        pygame.mixer.music.load(os.path.join("assets", "music.mp3"))
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1, 0)

    def stop_music(self):
        pygame.mixer.music.stop()  

    def play_sound(self, sound_name):
    # Dicionário para mapear nomes de som a arquivos
        sound_files = {
            "crash": "grito.mp3",
            "ding": "birl.mp3"
        }

    # Verifica se o nome do som está no dicionário
        if sound_name in sound_files:
            sound_path = os.path.join("assets", sound_files[sound_name])
            sound = pygame.mixer.Sound(sound_path)
            sound.play()  # Toca o som
        else:
            print(f"Sound '{sound_name}' not found.")


    def reset(self):
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def render_background(self):
        bg = pygame.image.load(os.path.join("assets", "background.jpg")).convert()
        bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.surface.blit(bg, (0, 0))

    def play(self):
        if not pygame.mixer.music.get_busy():
            self.play_music()

        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.score()
        pygame.display.flip()

 
        for i in range(self.snake.length):
            if self.is_collision(self.snake.x[i], self.snake.y[i], self.apple.x, self.apple.y):
                self.play_sound("ding")
                self.snake.increase_length()
                self.apple.move()

      
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound('crash')
                raise Exception("Colidiu consigo mesma")

  
        if not (0 <= self.snake.x[0] <= SCREEN_WIDTH and 0 <= self.snake.y[0] <= SCREEN_HEIGHT):
            self.play_sound('crash')
            raise Exception("Colidiu com a borda")

    def score(self):
        font = pygame.font.SysFont('arial', 30)
        pontuacao = font.render(f"Pontuação: {self.snake.length}", True, (200, 200, 200))
        self.surface.blit(pontuacao, (850, 10))

    def game_over(self):
        self.stop_music()  
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game over! Sua pontuação foi de {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render("Pressione Enter para jogar novamente ou para sair Pressione Escape.", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        pygame.display.flip()

    def show_menu(self):
        self.surface.fill((0, 0, 0))  
    
        menu_image = pygame.image.load(os.path.join("assets", "menu.webp")).convert()
        menu_image = pygame.transform.scale(menu_image, (SCREEN_WIDTH, SCREEN_HEIGHT))  
        self.surface.blit(menu_image, (0, 0))

        font = pygame.font.SysFont('arial', 50)
        title = font.render("BORIBUILDER", True, (255, 255, 255))
        self.surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 3))

        font = pygame.font.SysFont('arial', 40)
        play_option = font.render("Pressione Enter para Jogar", True, (255, 255, 255))
        self.surface.blit(play_option, (SCREEN_WIDTH // 2 - play_option.get_width() // 2, SCREEN_HEIGHT // 2))

        pygame.display.flip()

    def run(self):
        running = True
        pause = False
        in_menu = True 

        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                    if event.key == pygame.K_RETURN:
                        if in_menu:  
                            in_menu = False 
                            pause = False
                        elif pause:  
                            pause = False

<<<<<<< HEAD
                    if not pause and not in_menu:
                        if event.key == pygame.K_a:
                            self.snake.move_left()

                        if event.key == pygame.K_d:
                            self.snake.move_right()

                        if event.key == pygame.K_w:
                            self.snake.move_up()

                        if event.key == pygame.K_s:
                            self.snake.move_down()
=======
                    if not pause:
                        if event.key == pygame.K_a: 
                            self.snake.move_left() 

                        if event.key == pygame.K_d: 
                            self.snake.move_right()  

                        if event.key == pygame.K_w:
                            self.snake.move_up()  

                        if event.key == pygame.K_s: 
                            self.snake.move_down()  
>>>>>>> 04c1341026fc8fdbe5de3951a4511f3853237425

                elif event.type == pygame.QUIT:
                    running = False

            if in_menu:
                self.show_menu()  
            else:
                try:
                    if not pause:
                        self.play()

                except Exception as e:
                    self.game_over()
                    pause = True
                    self.reset()

            time.sleep(.1)

if __name__ == "__main__":
    game = Game()
    game.run()
