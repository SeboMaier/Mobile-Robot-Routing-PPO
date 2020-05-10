import pygame
from loader import load_image


class RoRange(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('range.png', False)
        self.image_orig = self.image
        self.rect = self.image.get_rect()
        self.screen = pygame.display.get_surface()
        self.area = self.screen.get_rect()
        self.CENTER_X = int(pygame.display.Info().current_w / 2)
        self.CENTER_Y = int(pygame.display.Info().current_h / 2)
        self.x = self.CENTER_X
        self.y = self.CENTER_Y

        self.rect.topleft = (self.x - 100, self.y - 100)
        self.mask = pygame.mask.from_surface(self.image)


    def reset(self):
        self.x = self.CENTER_X
        self.y = self.CENTER_Y
        self.mask = pygame.mask.from_surface(self.image)


    def update(self, delta_x, delta_y):
        self.x = self.x + delta_x
        self.y = self.y + delta_y



