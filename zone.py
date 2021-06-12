import os
import pygame

class Surface:
    def __init__(self, 
        width, 
        height,
        ):

        self.size = (height, width)
        self.empty_surface = None

    def show_surface(self):
        self.empty_surface = pygame.Surface(self.size)
        return self.empty_surface

    def game_init(self):
        pygame.init()
        screen = pygame.display.set_mode(self.size)
        done = False
        screen.fill((255,255,255))

        while not done:
            for event in pygame.event.get():
                if(event.type == pygame.KEYDOWN):
                    if event.key == pygame.K_q:
                        done = True
                    elif event.key == pygame.K_a:
                        print('Move left')
                    elif event.key == pygame.K_w:
                        print('Move up')
                    elif event.key == pygame.K_d:
                        print('Move right')
                    elif event.key == pygame.K_s:
                        print('Move down')

            screen.blit(self.show_surface(), self.size)


if __name__ == "__main__":
    surface = Surface(
        width = 1000,
        height= 1000,
    )

    surface.game_init()