import pygame
from random import randint, choice

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

FPS = 60
GRAVITY = 0.8
JUMP_POWER = -15
GROUND = 400

pygame.init()
screen = pygame.display.set_mode((500, 500))

class Player:
    def __init__(self, x, y):
        self.img_run = [
            pygame.image.load("DinoRun1.png"),
            pygame.image.load("DinoRun2.png")
        ]
        self.img_jump = pygame.image.load("DinoJump.png")
        self.image = self.img_run[0]
        self.rect = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())
        self.speed = 8
        self.dy = 0
        self.frame = 0

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.right < 500:
            self.rect.x += self.speed

        if keys[pygame.K_SPACE] and self.on_ground():
            self.dy = JUMP_POWER

        self.dy += GRAVITY
        self.rect.y += self.dy

        if self.rect.bottom >= GROUND:
            self.rect.bottom = GROUND
            self.dy = 0

        if not self.on_ground():
            self.image = self.img_jump
        else:
            self.frame = (self.frame + 0.2) % 2
            self.image = self.img_run[int(self.frame)]

    def on_ground(self):
        return self.rect.bottom >= GROUND

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

class Cloud:
    def __init__(self):
        self.image = pygame.image.load("Cloud.png")
        self.x = 500
        self.y = randint(50, 150)
        self.speed = 2

    def update(self):
        self.x -= self.speed
        if self.x < -self.image.get_width():
            self.x = 500
            self.y = randint(50, 150)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class Cactus:
    def __init__(self, x):
        self.images = [
            pygame.image.load("SmallCactus1.png"),
            pygame.image.load("SmallCactus2.png"),
            pygame.image.load("SmallCactus3.png")
        ]
        self.x = x
        self.speed = 5
        self.reset_cactus()

    def reset_cactus(self):
        self.image = choice(self.images)
        self.rect = pygame.Rect(self.x, GROUND - self.image.get_height(), self.image.get_width(), self.image.get_height())

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.x = 500 + randint(50, 200)
            self.reset_cactus()

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

class Track:
    def __init__(self):
        self.image = pygame.image.load("Track.png")
        self.x1 = 0
        self.x2 = self.image.get_width()
        self.speed = 5

    def update(self):
        self.x1 -= self.speed
        self.x2 -= self.speed

        if self.x1 <= -self.image.get_width():
            self.x1 = self.x2 + self.image.get_width()
        if self.x2 <= -self.image.get_width():
            self.x2 = self.x1 + self.image.get_width()

    def draw(self, screen):
        screen.blit(self.image, (self.x1, GROUND - 10))
        screen.blit(self.image, (self.x2, GROUND - 10))

clock = pygame.time.Clock()
running = True

dino = Player(200, GROUND - 80)
cloud = Cloud()
cactus = Cactus(500)
track = Track()

score = 0
font = pygame.font.Font(None, 36)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    dino.update()
    cloud.update()
    cactus.update()
    track.update()
    
    if dino.rect.colliderect(cactus.rect):
        running = False

    score += 1

    screen.fill(WHITE)

    cloud.draw(screen)
    track.draw(screen)
    cactus.draw(screen)
    dino.draw(screen)

    score_text = font.render(str(score // 5), True, BLACK)
    screen.blit(score_text, (430, 20))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

