from pygame import *
from random import randint

# ✨(1) import the timing function so that the interpreter doesn’t need to look for this function in the pygame module time, give it a different name ourselves
from time import time as timer 

# Background music
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

# ✨(2) Load images --- ADD ASTEROID!
img_back = "galaxy.jpg" #game background
img_bullet = "bullet.png" #bullet
img_hero = "rocket.png" #hero
img_enemy = "ufo.png" #enemy
img_ast = "asteroid.png" #asteroid

# Create a window
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

# Fonts and captions
font.init()
# WINNING FONT
font1 = font.SysFont('Comic Sans MS', 80)
# SCORE FONT
font2 = font.SysFont('Comic Sans MS', 30)
# Captions
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0)) 
 
score = 0 #ships destroyed
lost = 0 #ships missed

max_lost = 10 #how many ships you can lose

goal = 20 #how many ships need to be shot down to win

# ✨(3) ADD LIVES
life = 3  #lives!
 
# GameSprite class - inheriting from class Sprite
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # Call for the class (Sprite) constructor:
        sprite.Sprite.__init__(self)
 
        # Every sprite must store the image property
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
 
        # Every sprite must have the rect property – the rectangle it is fitted in
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
   
    # Puts the character in the window
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
 
#main player class
class Player(GameSprite):
    # Function to control the sprite with arrow keys - only LEFT and RIGHT needed
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    
    # Function to "shoot" (use the player position to create a bullet there)
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
    
class Enemy(GameSprite):
    # Enemy movement
    def update(self):
        self.rect.y += self.speed
        global lost
        # Disappears upon reaching the screen edge
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

# Bullet sprite class  
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        # Disappears upon reaching the screen edge
        if self.rect.y < 0:
            self.kill()
  
#create sprites
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

#creating a group of enemy sprites
monsters = sprite.Group()
for i in range(1, 6):
   monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
   monsters.add(monster)

bullets = sprite.Group()
 
#------------------------------------#
# ✨(4) Asteroid sprites

asteroids = sprite.Group()

for i in range(1, 3):
   asteroid = Enemy(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
   asteroids.add(asteroid)
#------------------------------------# 

# The "game is over" variable 
# As soon as it becomes True, all sprites stop working in the main loop
finish = False

# Main game loop
# The game is reset by the window close button
run = True 

#------------------------------------#
#✨(5) Variables - reload, shots fired

# Reload time
rel_time = False 
 
# Count shots fired
num_fire = 0  
#------------------------------------#

#✨(6) Update the game loop

while run:
    # "Close" button press event ✅
    for e in event.get():
        if e.type == QUIT:
            run = False
       #event of pressing the spacebar - the sprite shoots ✅
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                # Check how many shots have been fired (151 - 158 : NEW!)
                # And whether reload is in progress
                # Replace the old firing!
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    ship.fire()
                     
                    if num_fire  >= 5 and rel_time == False : 
                        last_time = timer() #record time when this happened
                        rel_time = True #set the reload flag
              
    if not finish:
        # Don't forget your asteroids!
        # Update the background
        window.blit(background,(0,0))
    
        # Launch sprite movements
        ship.update()
        monsters.update()
        bullets.update()
        asteroids.update() 
    
        # Update them in a new location in each loop iteration
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)
 
        # Reload mechanism
        if rel_time == True:
            now_time = timer() 

            # Before 3 seconds are over, display reload message
            if now_time - last_time < 3: 
                reload = font2.render('Wait, reload...', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                # Reset time!
                num_fire = 0   
                rel_time = False 
 
        # Check for a collision between a bullet and monsters (both monster and bullet disappear upon a touch)

        collides = sprite.groupcollide(monsters, bullets, True, True)
        
        for c in collides:
            #this loop will repeat as many times as the number of monsters hit
            # Score +1
            score = score + 1 
            # Respawn
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            # Adding it to the monster group
            monsters.add(monster)

        #----------------------------#
        # UPDATE THIS SECTION!
        # Now with asteroids!
        #----------------------------#
        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)
            life = life - 1
    
        # NEW losing check!
        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))
 
       # Same winning check :)
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))
 
        # Captions

        text = font2.render("Score: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
    
        text_lose = font2.render("Missed: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        #-----------------------------#
        # NEW: LIVES TRACKER!
        #-----------------------------#
        # Set a different color depending on the number of lives
        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150, 0, 0)
    
        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (650, 10))
        #-----------------------------#
        display.update()
 
    #bonus: automatic restart of the game
    else:
        finish = False

        score = 0
        lost = 0

        # Add fire counter and lives
        num_fire = 0
        life = 3

        # Add asteroids
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()   
        
        time.delay(3000)

        for i in range(1, 6):
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        
        # Add asteroid re-spawn loop
        for i in range(1, 3):
            asteroid = Enemy(img_ast, randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
            asteroids.add(asteroid)   
    
    time.delay(50)
 
