import pygame
import random

FRAMES = 30
SCREEN_WIDTH = 1200
BOTTOM_PANEL = 200
SCREEN_HEIGHT = 650 + BOTTOM_PANEL
run = True
font = pygame.font.SysFont('tempussansitc', 27, True, False)
red = (255,0,0)
green = (0,255,0)
black = (0,0,0)
white = (255,255,255)
grey = (192,192,192)

clock = pygame.time.Clock()
pygame.display.set_caption("Forest")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
background_img = pygame.transform.scale(pygame.image.load("images/terrain/background.png").convert_alpha(), (SCREEN_WIDTH,SCREEN_HEIGHT-BOTTOM_PANEL))
border = pygame.transform.scale(pygame.image.load("images/terrain/panel2.png").convert_alpha(), (SCREEN_WIDTH,BOTTOM_PANEL))
bottom = pygame.transform.scale(pygame.image.load("images/terrain/bottom.png").convert_alpha(), (SCREEN_WIDTH,BOTTOM_PANEL))
potion = pygame.image.load(f"images/terrain/potion.png").convert_alpha()
potionh = pygame.image.load(f"images/terrain/potion_hover.png").convert_alpha()
win = pygame.transform.scale(pygame.image.load("images/terrain/win.png").convert_alpha(), (SCREEN_WIDTH/2,BOTTOM_PANEL))
lose = pygame.transform.scale(pygame.image.load("images/terrain/lose.png").convert_alpha(), (SCREEN_WIDTH/2,BOTTOM_PANEL))

def GameOver(victory):
    '''
    Displays gameover panel, victory if victory = 1, defeat otherwise
    
    Parameters:
    - victory: whether the player has won or not

    Returns:
    - None
    '''
    if victory == 1:
         screen.blit(win,(300,200))
    elif victory == 0:
         screen.blit(lose,(300,200))
    
def AddAnim(name,frame_count,anim):
    '''
    Creates a list of animation frames for entities

    Parameters:
    - name: name of entity
    - frame_count: number of images used for the animation
    - anim: name of the animation 

    Returns:
    - list of animation frames for specific animation and entity type 
    '''
    temp = []
    for i in range(frame_count):
        img = pygame.image.load(f'images/entities/{name}/{anim}{i}.png').convert_alpha()
        img = pygame.transform.scale(img, (img.get_width()*4,300))
        temp.append(img)
    return temp

def draw_text(text,font,text_colour,x,y):
    '''
    Displays text on screen

    Parameters:
    - text: string to be displayed on screen
    - font: font style for the text
    - text_colour: colour of the text
    - x: x-coordinate for the starting position of the text
    - y: y-coordinate for the starting position of the text

    Returns:
    - None
    '''

    img = font.render(text,True,text_colour)
    screen.blit(img, (x,y))

def draw_bg():
    '''
    Displays background image on screen; fills in bottom panel with solid colour

    Parameters:
    - None

    Returns:
    - None
    '''
    screen.blit(background_img,(0,0))
    screen.blit(bottom,(0,SCREEN_HEIGHT - BOTTOM_PANEL))

def draw_Combat():
    '''
    Displays background image on screen; accounts for size of bottom panel

    Parameters:
    - None

    Returns:
    - None
    '''
    screen.blit(background_img,(0,0))

def draw_panel():
    '''
    Displays bottom panel on screen with names and health of fighters

    Parameters:
    - None

    Returns:
    - None
    '''
    screen.blit(border,(0,SCREEN_HEIGHT - BOTTOM_PANEL))
    draw_text(f'{player.name} HP: {player.hp}/{player.max_health}', font, grey, 100, SCREEN_HEIGHT - BOTTOM_PANEL + 30)
    for count,enemy in enumerate(enemy_list):
        draw_text(f'{enemy.name} {count} HP: {enemy.hp}/{enemy.max_health}', font, grey, 850, SCREEN_HEIGHT - BOTTOM_PANEL + 30+(count*25))

def enemy_alive():
    '''
    Checks if any enemies are still alive

    Parameters:
    - None

    Returns:
    - True if any enemies are still alive, false otherwise
    '''
    if len(enemy_list) == 0:
        return False
    
    for enemy in enemy_list:
        if enemy.alive:
            return True
    return False

def genEnemies():
    '''
    Generates list of enemies of size 1-3

    Parameters:
    - None

    Returns:
    - List of 1 to 3 enemies 

    '''
    temp = []
    enemy_num = random.randint(1,3)
    if enemy_num == 1:
        temp.append(Person(800,470,"skeleton",50*(random.randint(1,2)),5*(random.randint(1,2)),1))
    else:
        for enemy in range(enemy_num):
            temp.append(Person(700+200*enemy,470,"skeleton",50*(random.randint(1,2)),5*(random.randint(1,2)),1))
    return temp

class Person():
    def __init__(self,x,y,name,max_health,strength, potions):
        '''
        Initializes instance of Person

        Parameters:
        - name: name of the entity
        - max_health: maximum health value for entity
        - hp: current health of the entity, originally initialized to max health
        - start_potions: original amount of healing potions  
        - cur_potions: current number of healing potions
        - alive: if entity's current hp > 0
        - frame_index: current frame for animation
        - update_time: controls timing for switching animation frames
        - action: current action to be animated 
        - animation_list: list of lists containing animation frames (0:idle, 1: attack, 2: hurt, 3: dead)
        - longdead: if entity has just died or not; if entity has just died play the whole death animation otherwise stay on last frame
        - image: current image representing entity
        - rect: "hitbox" of entity
        - rect.center: center of "hitbox"
        - health_bar: instance of health bar to display current health of entity
        '''
        self.name = name
        self.max_health = max_health
        self.hp = max_health
        self.strength = strength
        self.start_potions = potions
        self.cur_potions = potions 
        self.alive = True
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.action = 0
        self.animation_list = []
        self.longdead = False

        #fills out animation_list depending on which entity is being initialized, will be replaced by different classes later
        if self.name == "player":
            self.animation_list.append(AddAnim("player",4,"idle"))
            self.animation_list.append(AddAnim("player",10,"attack"))
            self.animation_list.append(AddAnim("player",4,"hit"))
            self.animation_list.append(AddAnim("player",9,"dead"))
            self.animation_list.append(AddAnim("player",7,"block"))
        else:
            self.animation_list.append(AddAnim("skeleton",4,"idle"))
            self.animation_list.append(AddAnim("skeleton",8,"attack"))
            self.animation_list.append(AddAnim("skeleton",4,"hit"))
            self.animation_list.append(AddAnim("skeleton",4,"dead"))
            self.animation_list.append(AddAnim("skeleton",4,"block"))

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.health_bar = HealthBar(x,y, self.hp, self.max_health,self.name)

    def update(self):
        '''
        Updates entity to reflect current action/animation

        '''
        anim_cd = 100
        self.image = self.animation_list[self.action][self.frame_index]

        if pygame.time.get_ticks() - self.update_time > anim_cd:
            self.update_time = pygame.time.get_ticks()
            if self.frame_index >= len(self.animation_list[self.action])-1:
                if self.longdead:
                     return
                else:
                    self.idle()
            else:
                self.frame_index +=1

    def drawPerson(self):
        '''
        Displays entity on screen

        '''
        screen.blit(self.image,self.rect)

    def idle(self):
        '''
        Set entity current animation to idle

        '''        
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
    
    def hit(self):
        '''
        Set entity current animation to hit

        '''   
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def die(self):
        '''
        Set entity current animation to death

        '''   
        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def attack(self, target):
        '''
        Subtracts health from a target, update animation for both self (attack) and 
        target (hit if target hp - damage > 0, dead if target hp - damage <= 0)
        Adds damage numbers to group of damage text to be displayed

        Parameters:
        - target: target to be attacked

        Returns:
        - None
        '''   
        dmg = self.strength + random.randint(1, 5)
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

        if dmg > target.hp:
            target.hp = 0  
        else:
            target.hp -= dmg
        damage_text = damageText(target.rect.centerx, target.rect.y, str(dmg), red)
        damage_text_group.add(damage_text)

        target.hit()

        if target.hp <= 0:
            target.die()  
            target.alive = False  
    
    def heal(self):        
        '''
        Increase current hp by 50, add healing amount to damage text group, decrement current potions and return True if current potions > 0,
        otherwise return False

        '''   
        if self.cur_potions > 0 and self.hp < self.max_health:
            if self.hp + 50 > self.max_health:
                heal = self.max_health - self.hp
                self.hp = self.max_health
            else:
                heal = 50
                self.hp += 50

            self.cur_potions -= 1
            heal_text = damageText(self.rect.centerx, self.rect.y, str(heal), green)
            damage_text_group.add(heal_text)
            
            return True
        
        return False
    
class HealthBar():
    def __init__(self,x,y,hp,max_hp,name):
        '''
        Initializes instance of HealthBar

        Parameters:
        - x: x coordinate
        - y: y coordinate
        - hp: current health of entity
        - max_hp: maximum health of entity
        - name: name of entity
        - img: health bar image
        '''
        self.x = x -75
        self.y = y -170 
        self.hp = hp 
        self.max_hp = max_hp
        self.name = name
        template = pygame.image.load(f'images/entities/health_bar.png').convert_alpha()
        self.img = pygame.transform.scale(template, (template.get_width()*2,template.get_height()*2))
    
    def draw(self,hp):
        '''
        Displays health bar of entity on screen, with name above it

        Parameters:
        - hp: current hp of entity

        Returns:
        - None
        '''
        bar = pygame.image.load(f'images/entities/health.png').convert_alpha()
        bar = pygame.transform.scale(bar, ((bar.get_width()*2)*(hp/self.max_hp),bar.get_height()*2))
        screen.blit(bar, (self.x+39,self.y+16))
        screen.blit(self.img, (self.x, self.y))
        draw_text(f'{self.name}', font, white, self.x+39, self.y-20)

class damageText(pygame.sprite.Sprite):
    def __init__(self,x,y,damage,colour):
        '''
        Initializes instance of damageText

        Parameters:
        - x: x coordinate
        - y: y coordinate
        - damage: number to be displayed
        - colour: colour of number to be displayed
        '''
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage,True,colour)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y-50)
        self.counter = 0

    def update(self):
        '''
        Displays text using Sprite update method and removes sprite after counter > 30
        '''
        self.rect.y -= 1
        self.counter += 1
        if self.counter > 30:
             self.kill()
        
class Button():
    def __init__(self,surface,x,y,image,size_x,size_y,hover_image):
        '''
        Initializes instance of Button

        Parameters:
        - surface: surface for the button to be displayed on (screen)
        - x: x coordinate
        - y: y coordinate
        - image: image used to represent button
        - size_x: length of button
        - size_y: height of button
        - hover_image: image displayed when cursor is on button
        '''
        self.image = pygame.transform.scale(image,(size_x,size_y))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.surface = surface
        self.hover_image = pygame.transform.scale(hover_image,(size_x,size_y))

    def hovered(self,pos):
        '''
        Displays hover_image if cursor is on top of button

        Parameters:
        - pos: position of cursor

        Returns:
        - None
        '''
        if self.rect.collidepoint(pos):
            self.surface.blit(self.hover_image,(self.rect.x,self.rect.y))

    def isClicked(self,pos,click):
        '''
        Checks if button has been clicked

        Parameters:
        - pos: position of cursor
        - click: if mouse button is held down

        Returns:
        - True if cursor is on top of button and mouse button is held down, False otherwise
        '''
        self.hovered(pos)
        if self.rect.collidepoint(pos) and click:
            return True
        else:
            return False


    def draw(self):
        '''
        Displays button on screen
        '''
        self.surface.blit(self.image,(self.rect.x,self.rect.y))

     
     

player = Person(100,470,"player",100,20,2)
player_heal = Button(screen,100,SCREEN_HEIGHT - BOTTOM_PANEL + 80,potion,90,90,potionh)
enemy_list = genEnemies()
damage_text_group = pygame.sprite.Group()
