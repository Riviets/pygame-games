import pygame

pygame.init()
from random import randint, uniform

# uniform(a, b) - випадкове дробове число від a до b включно


# ---------------- Базовий клас ----------------
class Sprite:
    def __init__(self, x, y, w, h, img):
        self.img = pygame.image.load(img)
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self, surface):
        surface.blit(self.img, (self.rect.x, self.rect.y))


class Ball(Sprite):
    def __init__(self, x, y):
        super().__init__(x, y, 32, 32, "bird.png")
        self.fire = False
        self.vx = 0  # швидкість по X
        self.vy = 0  # швидкість по Y
        self.gravity = 1  # сила тяжіння
        self.count_fire = 30
        self.count = 0

    def draw(self, surface):
        if self.fire:
            surface.blit(self.img, (self.rect.x, self.rect.y))

    def move(self):
        if self.fire:
            self.rect.x += self.vx
            self.rect.y += self.vy
            self.vy += self.gravity  # прискорення вниз

            # Якщо вилетіла за межі екрана — вимикаємо
            if self.rect.x > 500 or self.rect.y > 500:
                self.fire = False

    def collide(self, sprites):
        for sprite in sprites[:]:
            if self.rect.colliderect(sprite.rect):
                sprites.remove(sprite)
                self.fire = False
                return True
        return False

    def update(self, walls, pigs):
        self.move()
        if self.collide(walls):
            self.count += 10
        if self.collide(pigs):
            self.count += 50


class Catapult(Sprite):
    def __init__(self, x, y):
        super().__init__(x, y, 150, 150, "k0.jpeg")
        self.fire = 0
        self.frames = []
        for i in range(10):
            self.frames.append(pygame.image.load(f"k{i}.jpeg"))

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.rect.y > 250:
            self.rect.y -= 5
        if keys[pygame.K_DOWN] and self.rect.y < 380:
            self.rect.y += 5

        if keys[pygame.K_SPACE] and self.fire == 0:
            self.fire = 1

    def update(self, ball):
        self.move()
        self.fire_ball(ball)

    def fire_ball(self, ball):
        if self.fire > 0:
            self.fire += 1
            if self.fire % 5 == 0:
                self.img = self.frames[self.fire // 5]
            if self.fire >= 45:
                self.fire = 0
                self.img = self.frames[0]
            if self.fire // 5 == 8 and not ball.fire:
                ball.fire = True
                ball.count_fire -= 1
                ball.rect.x = self.rect.x + 100
                ball.rect.y = self.rect.y + 50
                ball.vx = 12 + uniform(-2, 2)
                ball.vy = -10 + uniform(-2, 2)
                ball.gravity = 0.8


class Label:
    def __init__(self, x, y, text, font_size=30, color=(0, 0, 0)):
        self.font = pygame.font.SysFont("Arial", font_size)
        self.text = text
        self.color = color
        self.x = x
        self.y = y
        self.start = 0
        self.end = 0
        self.txts = [""]

    def draw(self, surface):
        img = self.font.render(self.text, True, self.color)
        surface.blit(img, (self.x, self.y))

    def update(self, text, surface):
        self.text = text
        self.draw(surface)


# ---------------- Карта ----------------
# 0 - empty space
# 1 - empty square
# 2 - square with pig
# size 64x64

pigs = []
walls = []


def create_map():
    start_x, start_y = 300, 260
    rows = 5
    cols = 4

    for r in range(rows):
        for c in range(cols):
            x = start_x + c * 40
            y = start_y + r * 40

            if r == rows - 1:
                walls.append(Sprite(x, y, 40, 40, "wall.png"))
            else:
                num = randint(0, 3)
                if num == 1:
                    walls.append(Sprite(x, y, 40, 40, "wall.png"))
                elif num == 2:
                    pigs.append(Sprite(x + 4, y + 4, 32, 32, "pig.png"))
                elif num == 3:
                    walls.append(Sprite(x, y, 40, 40, "wall.png"))
                    pigs.append(Sprite(x + 4, y + 4, 32, 32, "pig.png"))

    if not pigs:
        pigs.append(Sprite(start_x + 4, start_y + 4, 32, 32, "pig.png"))


# ---------------- Ініціалізація ----------------
screen = pygame.display.set_mode((500, 500))
fon = pygame.image.load("fon.png")
clock = pygame.time.Clock()
running = True

create_map()

catapult = Catapult(00, 380)
ball = Ball(0, 0)

score = Label(10, 10, "Score: 0", 30, (21, 143, 148))
fire = Label(350, 10, "Fire: 30", 30, (214, 121, 18))

# ---------------- Основний цикл ----------------
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(fon, (0, 0))

    score.update(f"Score: {ball.count}", screen)
    fire.update(f"Fire: {ball.count_fire}", screen)

    for wall in walls:
        wall.draw(screen)
    for pig in pigs:
        pig.draw(screen)
    catapult.draw(screen)
    catapult.update(ball)
    ball.update(walls, pigs)
    ball.draw(screen)

    pygame.display.flip()
    clock.tick(40)

pygame.quit()
