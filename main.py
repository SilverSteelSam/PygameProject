import pygame, sys, os, random
#from pygame.locals import *

class Player(pygame.sprite.Sprite): # Класс игрока, описывающий функционал персонажа
    def __init__(self, x, y, num_of_shoots=None):
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
        self.level = 0
        
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
              
    def move(self, x, y):
        self.rect = self.rect.move(x, y)
        
    # def draw(self, screen):
    #     screen.blit(self.image, [self.rect.x, self.rect.y])
        
    def update(self, obstacles):
        spd = 7
        if self.moving_down:
            if not (pygame.sprite.spritecollideany(Dummy(pygame.Rect(self.rect.x, 
                                                                     self.rect.y + spd,
                                                                     self.rect.w,
                                                                     self.rect.h)),
                                                   obstacles)):
                self.rect.y += spd
        if self.moving_left:
            if not (pygame.sprite.spritecollideany(Dummy(pygame.Rect(self.rect.x - spd, 
                                                                     self.rect.y,
                                                                     self.rect.w,
                                                                     self.rect.h)),
                                                   obstacles)):
                self.rect.x -= spd
        if self.moving_up:
            if not (pygame.sprite.spritecollideany(Dummy(pygame.Rect(self.rect.x, 
                                                                     self.rect.y - spd,
                                                                     self.rect.w,
                                                                     self.rect.h)),
                                                   obstacles)):
                self.rect.y -= spd
        if self.moving_right:
            if not (pygame.sprite.spritecollideany(Dummy(pygame.Rect(self.rect.x + spd, 
                                                                     self.rect.y,
                                                                     self.rect.w,
                                                                     self.rect.h)),
                                                   obstacles)):
                self.rect.x += spd
            
    def shoot(self, pos, screen):
        pass
    
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
    pygame.sprite.Sprite().kill()

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
            
        # particles1.append([[500, 500], [random.randint(0, 20) / 10 - 1, -2], random.randint(4, 12)])
        # for particle in particles1:
        #     particle[0][0] += particle[1][0]
        #     particle[0][1] += particle[1][1]
        #     particle[2] -= 0.2
        #     # particle[1][1] += 0.1
        #     pygame.draw.circle(screen, (255, 255, 255), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
        #     if particle[2] <= 0:
        #         particles1.remove(particle)
        
        
    
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
    def __init__(self, pos1, width, height):
        super().__init__()
        self.rect = pygame.Rect(pos1[0], pos1[1], width, height)
        
    def draw(self, screen):
        pygame.draw.rect(screen, (97, 97, 97), self.rect)
        
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

def draw_text(text, font, color, surface, x, y): # Функция для отрисовки текста
    text_obj = font.render(text, 1, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

def main_menu(): # -----------------MAIN MENU FUNCTION------------------------
    pygame.init()
    pygame.display.set_caption('Untitled Firefighter Game')
    size = RESOLUTION
    pygame.display.set_icon(pygame.image.load('data/icon.png'))
    screen = pygame.display.set_mode(size)
    display = pygame.Surface((1920, 1080))
    # icon = pygame.Surface()
    
    pygame.mouse.set_visible(True)
    
    
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
                            pygame.mixer.Sound('data/sounds/Menu_btn.wav').play()
                        draw = button.n
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and\
                draw == 1:
                game(screen,
                     Maze(MazeWall((0, 0), 1800, 50),
                          MazeWall((1800, 0), 50, 1000),
                          MazeWall((0, 1000), 1850, 50),
                          MazeWall((0, 50), 50, 1000)),
                     Player(900, 900))
                
                pygame.mouse.set_visible(True)

                
        
        display.fill((61, 107, 214))
        menu.draw(display)
        all_buttons.draw(display)
        
        if draw: # Circle motion 
            if x[0] >= 475 and x[1]:
                x = x[0] - 0.1, 1
                if x[0] <= 475:
                    x = x[0], 0
            elif x[0] <= 480 and not x[1]:
                x = x[0] + 0.1, 0
                if x[0] >= 480:
                    x = x[0], 1
            pygame.draw.circle(display, (255, 255, 255),
                               (x[0], [445, 525, 605, 685][draw - 1] + 10),
                               7)
        screen.blit(pygame.transform.scale(display, RESOLUTION), (0, 0))
        pygame.display.update()

def options_menu(): # Функция, реализующая меню настроек
    pass

def pause_menu(): # Функция, реализующая меню паузы
    pass

def game(screen, maze, player, keys=False): # Функция, реализующая саму игру

    # player = Player(x, y)
    # maze = Maze(Mazewall sprites here)
    # keys - group of keys to detect collisions with them
    display = pygame.Surface((1920, 1080))
    
    running = True
    pygame.mouse.set_visible(False)
    
    # player_group = pygame.sprite.Group(player)
    bullets_group = Group_custom_draw()
    
    screen = pygame.display.set_mode(RESOLUTION)
    
    # wall1 = MazeWall((0, 0), 1800, 50)
    # wall2 = MazeWall((1800, 0), 50, 1000)
    # wall3 = MazeWall((0, 1000), 1850, 50)
    # wall4 = MazeWall((0, 50), 50, 1000)
    
    # Maze(MazeWall((0, 0), 1800, 50),
    #      MazeWall((1800, 0), 50, 1000),
    #      MazeWall((0, 1000), 1850, 50),
    #      MazeWall((0, 50), 50, 1000))
    
    # ,
    #                  pygame.sprite.Group(Key(300, 300, 'red'),
    #                                Key(300, 350, 'yellow'),
    #                                Key(300, 400, 'purple'))
     
    
    # all_keys = pygame.sprite.Group(Key(300, 300, 'red'),
    #                                Key(300, 350, 'yellow'),
    #                                Key(300, 400, 'purple'))
    if not player.level:
        print(type(screen))
    
    
    all_keys = keys    
    
    draw_crosshair = False, 0
    crosshair = pygame.image.load('data/crosshair.png')
    crosshair = pygame.transform.rotozoom(crosshair, 0, 2)
    
    print(crosshair.get_rect().center)
    
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or\
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False  
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
                pygame.mixer.Sound('data/sounds/Shoot.wav').play()
                bullets_group.add(Bullet(player.rect.center,
                                         (event.pos[0] * 1920 / RESOLUTION[0],
                                         event.pos[1] * 1080 / RESOLUTION[1])))
                #print(len(bullets_group))
                # player.shooting = True
                # x, y = event.pos

        display.fill((132, 175, 156))
        
        player.update(maze)
        player.draw(display)
        
        # particles.draw(screen)
        
        maze.draw(display)
        if all_keys:
            all_keys.draw(display)
        
        # print(maze1.sprites()[0])
        # sprite1 = maze1.sprites()[0]
        # for sprite in maze1:
        #     rect1 = sprite.rect
        # all_keys.draw(screen)
        
        bullets_group.update()
        bullets_group.draw(display)
        
        # particles.add(Particle(600, 600))
        # particles.update()
        # particles.draw(screen)
        
        
        # particles1.append([[500, 500], [random.randint(0, 30) / 10 - 1, -2], random.randint(4, 12)])
        # for particle in particles1:
        #     particle[0][0] += particle[1][0]
        #     particle[0][1] += -2
        #     particle[2] -= 0.2
        #     # particle[1][1] += 0.1
        #     pygame.draw.circle(screen, (255, 255, 255), [particle[0][0], particle[0][1]], particle[2])
        #     if particle[2] <= 0:
        #         particles1.remove(particle)
        
        if all_keys:
            for sprite in all_keys:
                if pygame.sprite.collide_rect(player, sprite):
                    player.keys.append(sprite.color)
                    all_keys.remove(sprite)
        
        for sprite in bullets_group:
            if pygame.sprite.spritecollideany(sprite, maze):
                pygame.mixer.Sound('data/sounds/Fire_extinguish.wav').play()
                bullets_group.remove(sprite)
                
        if draw_crosshair[0]:
            #print(draw_crosshair[1])
            display.blit(crosshair, (draw_crosshair[1][0],
                                    draw_crosshair[1][1]))
        screen.blit(pygame.transform.scale(display, RESOLUTION), (0, 0))
        
        pygame.display.update()
        clock.tick(60)

global RESOLUTION 
RESOLUTION = (1920, 1080)
main_menu()
