import pygame
import os
import sys

class Player(pygame.sprite.Sprite): # Класс игрока, описывающий функционал персонажа
    pass

class Button(pygame.sprite.Sprite):
    def __init__(self, image_path, number, x, y, group):
        super().__init__(group)
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.n = number
        
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

def draw_text(text, font, color, surface, x, y): # Функция для отрисовки текста
    text_obj = font.render(text, 1, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

def main_menu(): # Функция, реализующая главное меню
    pygame.init()
    size = 1480, 935
    screen = pygame.display.set_mode(size)
    
    all_buttons = pygame.sprite.Group()
    menu = pygame.sprite.Group()
    menu_sprite = pygame.sprite.Sprite()
    menu_sprite.image = load_image('menu/menu.png')
    menu_sprite.rect = menu_sprite.image.get_rect()    
    menu_sprite.rect.x = -2
    menu_sprite.rect.y = -2
    menu.add(menu_sprite)
    _ = Button('data/menu/begin_btn.png', 1, 510, 430, all_buttons)
    _ = Button('data/menu/options_btn.png', 2, 510, 510, all_buttons)
    _ = Button('data/menu/credits_btn.png', 3, 510, 590, all_buttons)
    _ = Button('data/menu/quit_btn.png', 4, 510, 670, all_buttons)
    running = True
    draw = 0
    x = 480, 1
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False       
            if event.type == pygame.MOUSEMOTION:
                for button in all_buttons:
                    if button.rect.collidepoint(event.pos):
                        draw = button.n
                        
        screen.fill((255, 255, 255))
        menu.draw(screen)
        all_buttons.draw(screen)
        if draw:
            if x[0] >= 475 and x[1]:
                x = x[0] - 0.1, 1
                if x[0] <= 475:
                    x = x[0], 0
            elif x[0] <= 480 and not x[1]:
                x = x[0] + 0.1, 0
                if x[0] >= 480:
                    x = x[0], 1
            pygame.draw.circle(screen, (255, 255, 255),
                               (x[0], [445, 525, 605, 685][draw - 1] + 10),
                               7)
            
        pygame.display.flip()
    pygame.quit()

def options_menu(): # Функция, реализующая меню настроек
    pass

def pause_menu(): # Функция, реализующая меню паузы
    pass

def game(): # Функция, реализующая саму игру
    pass

main_menu()
