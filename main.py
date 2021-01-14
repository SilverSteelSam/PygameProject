import pygame, sys, os, random
from itertools import cycle
#from pygame.locals import *

class Player(pygame.sprite.Sprite): # Класс игрока, описывающий функционал персонажа
    def __init__(self, x, y, num_of_shoots=None, level=0):
        super().__init__()
        self.image = pygame.image.load('data/player.png')
        self.image = pygame.transform.rotozoom(self.image, 0, 0.3)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.shooting = False
        self.keys = []
        self.num_of_shoots = num_of_shoots
        self.level = level
        
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        if self.num_of_shoots >= 0:
            draw_text(str(self.num_of_shoots),
                      (255, 255, 255), screen,
                      self.rect.x + 75, self.rect.y - 30)
        
              
    def move(self, x, y):
        self.rect.x = x
        self.rect.y = y
        
    def update(self, obstacles):
        spd = 7
        if self.moving_down:
            for sprite in pygame.sprite.spritecollide(Dummy(pygame.Rect(self.rect.x, 
                                                                     self.rect.y + spd,
                                                                     self.rect.w,
                                                                     self.rect.h)),
                                                      obstacles,
                                                      dokill=False):
                if sprite.color in self.keys:
                    pygame.mixer.Sound('data/sounds/dooropen.wav').play()
                    sprite.kill()
                
            if not (pygame.sprite.spritecollideany(Dummy(pygame.Rect(self.rect.x, 
                                                                     self.rect.y + spd,
                                                                     self.rect.w,
                                                                     self.rect.h)),
                                                   obstacles)):
                self.rect.y += spd

                
        if self.moving_left:
            for sprite in pygame.sprite.spritecollide(Dummy(pygame.Rect(self.rect.x - spd, 
                                                                     self.rect.y,
                                                                     self.rect.w,
                                                                     self.rect.h)),
                                                      obstacles,
                                                      dokill=False):
                if sprite.color in self.keys:
                    pygame.mixer.Sound('data/sounds/dooropen.wav').play()
                    sprite.kill()
                    
            if not (pygame.sprite.spritecollideany(Dummy(pygame.Rect(self.rect.x - spd, 
                                                                     self.rect.y,
                                                                     self.rect.w,
                                                                     self.rect.h)),
                                                   obstacles)):
                self.rect.x -= spd
        if self.moving_up:
            for sprite in pygame.sprite.spritecollide(Dummy(pygame.Rect(self.rect.x, 
                                                                     self.rect.y - spd,
                                                                     self.rect.w,
                                                                     self.rect.h)),
                                                      obstacles,
                                                      dokill=False):
                if sprite.color in self.keys:
                    pygame.mixer.Sound('data/sounds/dooropen.wav').play()
                    sprite.kill()
                    
            if not (pygame.sprite.spritecollideany(Dummy(pygame.Rect(self.rect.x, 
                                                                     self.rect.y - spd,
                                                                     self.rect.w,
                                                                     self.rect.h)),
                                                   obstacles)):
                self.rect.y -= spd
        if self.moving_right:
            for sprite in pygame.sprite.spritecollide(Dummy(pygame.Rect(self.rect.x + spd, 
                                                                     self.rect.y,
                                                                     self.rect.w,
                                                                     self.rect.h)),
                                                      obstacles,
                                                      dokill=False):
                if sprite.color in self.keys:
                    pygame.mixer.Sound('data/sounds/dooropen.wav').play()
                    sprite.kill()
                    
            if not (pygame.sprite.spritecollideany(Dummy(pygame.Rect(self.rect.x + spd, 
                                                                     self.rect.y,
                                                                     self.rect.w,
                                                                     self.rect.h)),
                                                   obstacles)):
                self.rect.x += spd
            
    def stop_moving(self):
        self.moving_down = False
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False

    
class Key(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.transform.rotozoom(pygame.image.load(f'data/{color}_key.png'),
                                               0,
                                               0.25)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.color = color


class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y,
                 r=0, 
                 x_vel=0,
                 y_vel=0):
        super().__init__()
        r, x_vel, y_vel = random.randint(6, 12), random.randint(0, 30) / 10 - 1, random.randint(0, 30) / 10 - 1
        self.rect = pygame.rect.Rect(x, y, 2 * r, 2 * r)
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.r = r
        
    def draw(self, screen):
        pygame.draw.circle(screen, (71, 201, 255), 
                           (self.rect.x, self.rect.y),
                           self.r)
        
    def update(self):
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel
        self.r -= 0.2
        if self.r <= 0:
            self.kill()

    
class Dummy(pygame.sprite.Sprite):
    def __init__(self, rect):
        super().__init__()
        self.rect = rect   
        

class Button(pygame.sprite.Sprite):
    def __init__(self, image_path, number, x, y, group):
        super().__init__(group)
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.n = number
        

class Group_custom_draw(pygame.sprite.Group):
    def draw(self, screen):
        for spr in self.sprites():
            spr.draw(screen)
        

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, cursor_pos):
        super().__init__()
        self.killed = pos == cursor_pos
        if not self.killed:
            self.rect = pygame.Rect(pos[0], pos[1], 20, 20) 
            self.pos = pygame.math.Vector2(pos)
            self.dir = pygame.math.Vector2(cursor_pos[0], cursor_pos[1]) - \
                        pygame.math.Vector2(pos[0], pos[1])
            pygame.math.Vector2.normalize_ip(self.dir)
            self.particles = Group_custom_draw()     
        
    def draw(self, screen):
        if self.alive():
            pygame.draw.circle(screen, (255, 255, 255), (self.pos.x, self.pos.y),
                               12)
            pygame.draw.circle(screen, (79, 201, 255), (self.pos.x, self.pos.y),
                               10)
            self.particles.draw(screen)
        
    def update(self):
        if self.killed:
            self.kill()
        if self.alive():
            self.pos += self.dir * 10
            self.rect = pygame.Rect(self.pos[0], self.pos[1], 20, 20)
            self.particles.add(Particle(self.rect.x, self.rect.y))
            self.particles.update()


class MazeWall(pygame.sprite.Sprite):
    def __init__(self, pos1, width, height, color=0, isfire=False):
        super().__init__()
        self.rect = pygame.Rect(pos1[0], pos1[1], width, height)
        self.color = color
        self.isfire = isfire
        
    def draw(self, screen):
        if self.isfire:
            pygame.draw.rect(screen, (100, 0, 0), self.rect)
        else:
            if not self.color:
                pygame.draw.rect(screen, (97, 97, 97), self.rect)
            elif self.color == 'purple':
                pygame.draw.rect(screen, (44, 0, 128), self.rect)
            elif self.color == 'yellow':
                pygame.draw.rect(screen, (255, 211, 0), self.rect)    
            elif self.color == 'red':
                pygame.draw.rect(screen, (141, 2, 31), self.rect)
    
    def move(self, x, y):
        self.rect.x += x
        self.rect.y += y
        

class Maze(pygame.sprite.Group):
    def __init__(self, *sprites):
        super().__init__(sprites) #ДОДЕЛАТЬ---------------
        # SPRITES WITH MAZE COLUMN
        #print(self.up_left)
        
    def draw(self, screen):
        for sprite in self.sprites():
            sprite.draw(screen)
            
    
    def move(self, x, y):
        for sprite in self.sprites():
            sprite.move(x, y)
        
        
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


def draw_text(text,
              color,
              surface,
              x, y,
              font=0,
              size=50): # Функция для отрисовки текста
    font = pygame.font.Font(None, size)
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)


def main_menu(): # -----------------MAIN MENU FUNCTION------------------------
    pygame.init()
    pygame.mixer.init()    
    pygame.font.init()
    pygame.display.set_caption('Untitled Firefighter Game')
    pygame.display.set_icon(pygame.image.load('data/icon.png'))
    screen = pygame.display.set_mode(RESOLUTION)
    display = pygame.Surface((1920, 1080))
    
    pygame.mouse.set_visible(True)
    
    clock = pygame.time.Clock()
    
    all_buttons = pygame.sprite.Group()
    menu = pygame.sprite.Group()
    menu_sprite = pygame.sprite.Sprite()
    menu_sprite.image = load_image('menu/menu.png')
    menu_sprite.rect = menu_sprite.image.get_rect()    
    menu_sprite.rect.x = -1
    menu_sprite.rect.y = -1
    menu.add(menu_sprite)
    _ = Button('data/menu/begin_btn.png', 1, 510, 430, all_buttons)
    _ = Button('data/menu/options_btn.png', 2, 510, 510, all_buttons)
    _ = Button('data/menu/credits_btn.png', 3, 510, 590, all_buttons)
    _ = Button('data/menu/quit_btn.png', 4, 510, 670, all_buttons)
    
    draw = 0
    x = 480, 1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or\
                (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and draw == 4) or\
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                for button in all_buttons:  
                    if button.rect.collidepoint((event.pos[0] * 1920 / RESOLUTION[0],
                                        event.pos[1] * 1080 / RESOLUTION[1])):
                        if draw != button.n:
                            
                            pygame.mixer.Sound('data/sounds/menu_btn.wav').play()
                        draw = button.n
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if draw == 1:
                    labyrinth_game(screen,
                         Maze(MazeWall((0, -1), 1920, 1),
                              MazeWall((1920, 0), 1, 1080),
                              MazeWall((0, 1080), 1920, 1),
                              MazeWall((0, -1), 1, 1080)),
                         Player(900, 900, num_of_shoots=-1))
                    
                    pygame.mouse.set_visible(True)
                elif draw == 2:
                    options_menu(screen)
        
        display.fill((61, 107, 214))
        menu.draw(display)
        all_buttons.draw(display)
        
        if draw: # Circle motion 
            if x[0] >= 475 and x[1]:
                x = x[0] - 0.2, 1
                if x[0] <= 475:
                    x = x[0], 0
            elif x[0] <= 480 and not x[1]:
                x = x[0] + 0.2, 0
                if x[0] >= 480:
                    x = x[0], 1
            pygame.draw.circle(display, (255, 255, 255),
                               (x[0], [445, 525, 605, 685][draw - 1] + 10),
                               7)
        screen.blit(pygame.transform.scale(display, RESOLUTION), (0, 0))
        pygame.display.update()
        clock.tick(FPS)

def options_menu(screen): # Функция, реализующая меню настроек
    global FPS, RESOLUTION, resolutions, fps_list
    display = pygame.Surface((1920, 1080))
    pygame.mouse.set_visible(True)
    
    clock = pygame.time.Clock()
    
    all_buttons = pygame.sprite.Group()
    menu = pygame.sprite.Group()
    menu_sprite = pygame.sprite.Sprite()
    menu_sprite.image = load_image('menu/settings_menu.png')
    menu_sprite.rect = menu_sprite.image.get_rect()    
    menu_sprite.rect.x = -1
    menu_sprite.rect.y = -1
    menu.add(menu_sprite)
    _ = Button('data/menu/resolution_btn.png', 1, 105, 240, all_buttons)
    _ = Button('data/menu/fps_btn.png', 2, 110, 350, all_buttons)
    _ = Button('data/menu/back_btn.png', 3, 110, 455, all_buttons)
    
    draw = 0
    x = 80, 1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or\
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                # pygame.mouse.set_visible(False)
                return True
            
            if event.type == pygame.MOUSEMOTION:
                for button in all_buttons:  
                    if button.rect.collidepoint((event.pos[0] * 1920 / RESOLUTION[0],
                                        event.pos[1] * 1080 / RESOLUTION[1])):
                        if draw != button.n:
                            
                            pygame.mixer.Sound('data/sounds/menu_btn.wav').play()
                        draw = button.n
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a or event.key == pygame.K_RIGHT:
                    pass
                
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if draw == 3:
                    return _
                    
                elif draw == 2:
                    FPS = next(fps_list)
                    
                elif draw == 1 and all_buttons.sprites()[0].rect.collidepoint((event.pos[0] * 1920 / RESOLUTION[0],
                                        event.pos[1] * 1080 / RESOLUTION[1])):
                    RESOLUTION = next(resolutions)
                    screen = pygame.display.set_mode(RESOLUTION)
 
        display.fill((61, 107, 214))
        menu.draw(display)
        all_buttons.draw(display)
        draw_text(str(RESOLUTION), 
                  (255, 255, 255),
                  display,
                  600, 250,
                  size=100)
        draw_text(str(FPS), 
                  (255, 255, 255),
                  display,
                  600, 360,
                  size=100)
        
        if draw: # Circle motion 
            if x[0] >= 80 and x[1]:
                x = x[0] - 0.2, 1
                if x[0] <= 80:
                    x = x[0], 0
            elif x[0] <= 85 and not x[1]:
                x = x[0] + 0.2, 0
                if x[0] >= 85:
                    x = x[0], 1
            pygame.draw.circle(display, (255, 255, 255),
                               (x[0], [230, 330, 430][draw - 1] + [45, 52, 60][draw - 1]),
                               7)
        screen.blit(pygame.transform.scale(display, RESOLUTION), (0, 0))
        pygame.display.update()
        clock.tick(FPS)
    

def pause_menu(screen): # Функция, реализующая меню паузы
    global FPS, RESOLUTION

    display = pygame.Surface((1920, 1080))
    pygame.mouse.set_visible(True)
    
    clock = pygame.time.Clock()
    
    all_buttons = pygame.sprite.Group()
    menu = pygame.sprite.Group()
    menu_sprite = pygame.sprite.Sprite()
    menu_sprite.image = load_image('menu/pause_menu.png')
    menu_sprite.rect = menu_sprite.image.get_rect()    
    menu_sprite.rect.x = -1
    menu_sprite.rect.y = -1
    menu.add(menu_sprite)
    _ = Button('data/menu/continue_btn.png', 1, 105, 240, all_buttons)
    _ = Button('data/menu/settings_btn.png', 2, 110, 350, all_buttons)
    _ = Button('data/menu/back_btn.png', 3, 110, 455, all_buttons)
    
    draw = 0
    x = 80, 1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or\
                (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and draw == 1) or\
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.mouse.set_visible(False)
                return True
            if event.type == pygame.MOUSEMOTION:
                for button in all_buttons:  
                    if button.rect.collidepoint((event.pos[0] * 1920 / RESOLUTION[0],
                                        event.pos[1] * 1080 / RESOLUTION[1])):
                        if draw != button.n:
                            
                            pygame.mixer.Sound('data/sounds/menu_btn.wav').play()
                        draw = button.n
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if draw == 3:
                    return False
                    
                    pygame.mouse.set_visible(True)
                    
                elif draw == 2:
                    options_menu(screen)

        display.fill((61, 107, 214))
        menu.draw(display)
        all_buttons.draw(display)
        
        if draw: # Circle motion 
            if x[0] >= 80 and x[1]:
                x = x[0] - 0.2, 1
                if x[0] <= 80:
                    x = x[0], 0
            elif x[0] <= 85 and not x[1]:
                x = x[0] + 0.2, 0
                if x[0] >= 85:
                    x = x[0], 1
            pygame.draw.circle(display, (255, 255, 255),
                               (x[0], [230, 330, 430][draw - 1] + [45, 52, 60][draw - 1]),
                               7)
        screen.blit(pygame.transform.scale(display, RESOLUTION), (0, 0))
        pygame.display.update()
        clock.tick(FPS)
        

def labyrinth_game(screen, maze, player, keys=False): # Функция, реализующая саму игру

    global FPS, RESOLUTION
    display = pygame.Surface((1920, 1080))
    
    back = True
    
    running = True
    pygame.mouse.set_visible(False)

    bullets_group = Group_custom_draw()
    
    screen = pygame.display.set_mode(RESOLUTION)
    
    if not player.level:
        portals = pygame.sprite.Group()
        surface = pygame.Surface((100, 100))
        surface.fill((132, 175, 156))
        pygame.draw.circle(surface, (255, 255, 255), (50, 50), 50)
        
        portal_tutorial = pygame.sprite.Sprite(portals)
        portal_tutorial.image = surface
        portal_tutorial.rect = surface.get_rect()
        portal_tutorial.rect.x = 240
        portal_tutorial.rect.y = 200
        
        portal_level1 = pygame.sprite.Sprite(portals)
        portal_level1.image = surface
        portal_level1.rect = surface.get_rect()
        portal_level1.rect.x = 880
        portal_level1.rect.y = 200
        
        portal_level2 = pygame.sprite.Sprite(portals)
        portal_level2.image = surface
        portal_level2.rect = surface.get_rect()
        portal_level2.rect.x = 1520
        portal_level2.rect.y = 200
        
    
    all_keys = keys    
    
    draw_crosshair = False, 0
    crosshair = pygame.image.load('data/crosshair.png')
    crosshair = pygame.transform.rotozoom(crosshair, 0, 2)
    
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                back = pause_menu(screen)
            
            elif event.type == pygame.KEYDOWN:   
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    player.moving_right = True
                    
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    player.moving_left = True
                
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    player.moving_up = True
                    
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    player.moving_down = True      
            elif event.type == pygame.KEYUP:               
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    player.moving_right = False
                    
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    player.moving_left = False
                    
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    player.moving_up = False
                    
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    player.moving_down = False
            elif event.type == pygame.MOUSEMOTION:
                draw_crosshair = True, ((event.pos[0] * 1920 / RESOLUTION[0] - 30,
                                        event.pos[1] * 1080 / RESOLUTION[1] - 30))
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if player.num_of_shoots != 0:
                    if player.num_of_shoots > 0:
                        player.num_of_shoots -= 1
                    sound = pygame.mixer.Sound('data/sounds/shoot.wav')
                    sound.set_volume(0.1)
                    sound.play()
                    bullets_group.add(Bullet(player.rect.center,
                                             (event.pos[0] * 1920 / RESOLUTION[0],
                                             event.pos[1] * 1080 / RESOLUTION[1])))
                

        if back:
            display.fill((132, 175, 156))
            
            maze.draw(display)
            
            player.update(maze)
            player.draw(display)
            
            if all_keys:
                all_keys.draw(display)
                
            if not player.level:
                portals.draw(display)
                if pygame.sprite.collide_rect(portal_tutorial, player):
                    x, y, num, lvl = 1705, 864, 3, 1
                    w, h = 200, 200
                    maze_tutorial = Maze(MazeWall((5, 10), 1910, 20),
                                         MazeWall((1895, 10), 20, 1060),
                                         MazeWall((5, 1055), 1910, 20),
                                         MazeWall((5, 10), 20, 1060))
                    labyrinth_game(screen,
                         maze_tutorial,
                         Player(x, y, num_of_shoots=num, level=lvl),
                         keys=pygame.sprite.Group())
                    player.move(900, 900)
                    player.stop_moving()
                    
                    
                elif pygame.sprite.collide_rect(portal_level1, player):
                    x, y, num, lvl = 0, 0, 8, 2
                    maze_level1 = Maze()
                    labyrinth_game(screen,
                         maze_level1,
                         Player(x, y, num_of_shoots=num, level=lvl),
                         keys=pygame.sprite.Group())
                    player.move(900, 900)
                    player.stop_moving()
                    
                elif pygame.sprite.collide_rect(portal_level2, player):
                    x, y, num, lvl = 0, 0, 21, 3
                    maze_level2 = Maze()
                    labyrinth_game(screen,
                         maze_level2,
                         Player(x, y, num_of_shoots=num, level=lvl),
                         keys=pygame.sprite.Group())
                    player.move(900, 900)
                    player.stop_moving()
            
            bullets_group.update()
            bullets_group.draw(display)
            if not player.level:
                draw_text('Tutorial level', (255, 255, 255), display, 180, 150)
                draw_text('First level', (255, 255, 255), display, 840, 150)
                draw_text('Second level', (255, 255, 255), display, 1460, 150)
    
            if all_keys:
                for sprite in all_keys:
                    if pygame.sprite.collide_rect(player, sprite):
                        player.keys.append(sprite.color)
                        all_keys.remove(sprite)
                        sound = pygame.mixer.Sound('data/sounds/pickup.wav')
                        sound.set_volume(0.07)
                        sound.play()
                        
            for sprite in bullets_group:
                if pygame.sprite.spritecollideany(sprite, maze):
                    sound = pygame.mixer.Sound('data/sounds/splash.wav')
                    sound.set_volume(0.05)
                    sound.play()
                    bullets_group.remove(sprite)
                    for wall in pygame.sprite.spritecollide(sprite, maze, dokill=False):
                        if wall.isfire:
                            sound = pygame.mixer.Sound('data/sounds/fire_extinguish.wav')
                            sound.set_volume(0.05)
                            sound.play()
                            wall.kill()
                    
            if draw_crosshair[0]:
                display.blit(crosshair, (draw_crosshair[1][0],
                                        draw_crosshair[1][1]))
            screen.blit(pygame.transform.scale(display, RESOLUTION), (0, 0))
            
            pygame.display.update()
            clock.tick(FPS)
        else:
            running = False

global RESOLUTION, FPS, resolutions, fps_list
# Resolutions: 16:9 (1024, 576); (1152, 648); (1280, 720);
#                   (1366, 768); (1600, 900); (1920, 1080)
RESOLUTION = (1920, 1080)
FPS = 60
resolutions = cycle([(1024, 576), (1152, 648), (1280, 720),
               (1366, 768), (1600, 900), (1920, 1080)][::-1])
fps_list = cycle([120, 15, 30, 60])
main_menu()
