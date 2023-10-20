import pygame
class Button():

    # инициализация переменных у кнопки
    def __init__(self, x, y, image, s_image, scale):
        height = image.get_height()
        width = image.get_width()
        s_height = s_image.get_height()
        s_width =s_image.get_width()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.s_image = pygame.transform.scale(s_image, (int(s_width * scale), int(s_height * scale)))
        self.s_rect = self.s_image.get_rect()
        self.rect.center = (x, y)
        self.s_rect.center = (x, y)
        self.clicked = False

    # функция отрисовки кнопки и возвращения значения True если на кнопку нажали
    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

        if self.rect.collidepoint(pos):
            surface.blit(self.s_image, (self.s_rect.x, self.s_rect.y))
        else:
            surface.blit(self.image, (self.rect.x, self.rect.y))
        return action
