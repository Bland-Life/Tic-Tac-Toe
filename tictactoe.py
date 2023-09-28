# Example file showing a basic pygame "game loop"
import pygame
from scenes import *

# pygame setup
pygame.init()
window_title = pygame.display.set_caption("Tic Tac Toe")
clock = pygame.time.Clock()
running = True

# The pygame screen is created in the SceneManager class
manager = SceneManager()

while running:

    if manager.current_scene == None:
        manager.start_scene(TitleScene)
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for (button, action) in manager.get_scene().interactables:
                if button.collidepoint(mouse_pos):
                    action()
                    break

    pygame.display.flip()
    clock.tick(60)

pygame.quit()