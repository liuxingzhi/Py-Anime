import pygame
import random

SCREEN_HEIGHT = 900
SCREEN_WIDTH = 1500
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("18年")

# TODO add background for screen


if __name__ == "__main__":
    clock = pygame.time.Clock()
    done = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        # TODO show background
        # screen.blit(bg, (0, 0))

        # TODO show texts

        # update the contents of the entire display
        pygame.display.flip()
        clock.tick(40)
