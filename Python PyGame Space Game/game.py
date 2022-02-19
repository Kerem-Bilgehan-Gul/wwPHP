# wwPHP.com Space Game 19-02-2022
# Kerem Bilgehan Gül
# Adding Required Libraries.
import pygame;
import random;

programIcon = pygame.image.load('wwphp.png');
pygame.display.set_icon(programIcon);
pygame.display.set_caption('wwPHP Space Game');
# Game screen WIDTH and HEIGHT.(800x600)
SCREEN_WIDTH  = 800;
SCREEN_HEIGHT = 600;

# Import pygame.locals parameters to use supported features.
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    QUIT,
);

# Define the Player object.
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__();
        # Set player object image.
        self.surf = pygame.image.load("Player-Plane.png").convert_alpha();
        self.surf.set_colorkey((255, 255, 255), RLEACCEL);
        self.rect = self.surf.get_rect();

    # Key Presses Event.
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5); # if gamer press UP key on keyboard.
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5); # if gamer press DOWN key on keyboard.
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0); # if gamer press LEFT key on keyboard.
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0); # if gamer press RIGHT key on keyboard.

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0;
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH;
        if self.rect.top <= 0:
            self.rect.top = 0;
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT;

# Define the enemy object.
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__();
        self.surf = pygame.image.load("Enemy.png").convert_alpha();
        self.surf.set_colorkey((255, 255, 255), RLEACCEL);
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        );
        self.speed = random.randint(5, 20);

    # Move enemy.
    def update(self):
        self.rect.move_ip(-self.speed, 0);
        if self.rect.right < 0:
            self.kill();

# Define the Bullet object.
class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super(Bullet, self).__init__();
        self.surf = pygame.image.load("Player-Laser-Bullet.png").convert_alpha();
        self.surf.set_colorkey((255, 255, 255), RLEACCEL);
        self.rect = self.surf.get_rect(
		center=(
                player.rect.left+30,
                player.rect.top+12,
            )
		);

    # Move bullet.
    def update(self):
        self.rect.move_ip(25, 0);
        if self.rect.left > SCREEN_WIDTH:
            self.kill();


# Initialize pygame
pygame.init();
# Create game screen and set background image.
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT));
background_image = pygame.image.load("background.png").convert();

# Create player.
player = Player();

# Setup the clock for a decent framerate
clock = pygame.time.Clock()

# Create custom enemy.
# Clock object call ADDENEMY event.
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)

# Create groups to hold enemy and bullets sprites, and each sprite.
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
# Create group to hold all sprites.(render)
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Player score.
PlayerScore = 0;
# Score text font and size.
myfont = pygame.font.SysFont("Helvatica", 30)
# Score text put on screen.
label = myfont.render("Score : " + str(PlayerScore), 1, (0,100,0))

running = True
# Mail loop.
while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE: # if gamer press ESC on keyboard end the game.
                running = False
            if event.key == K_SPACE: # if gamer press SPACE on keyboard create new bullet object.
                new_bullet = Bullet()
                bullets.add(new_bullet)
                all_sprites.add(new_bullet)

        elif event.type == QUIT:
            running = False

        elif event.type == ADDENEMY: # ADDENEMY event called by the clock.(LINE 110)
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    # Update the position enemies and bullets.
    enemies.update()
    bullets.update();

    # Background image. Fill screen.
    screen.blit(background_image, [0, 0])
    # Draw all sprites on screen.
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    # if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        running = False
    # if any bullets have colliaded with the enemy
    EnemyShot = pygame.sprite.groupcollide(bullets, enemies, True, True);
    if EnemyShot:
        PlayerScore = PlayerScore+1;
        label = myfont.render("Score : " + str(PlayerScore), 1, (0,100,0))
    screen.blit(label, (700, 10));
    pygame.display.flip()
    clock.tick(30); # Framerate.