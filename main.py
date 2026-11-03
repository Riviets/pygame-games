import pygame

pygame.init()
from random import randint


# ---------------- Базовий клас ----------------
class Sprite:
    def __init__(self, x, y, img):
        self.img = pygame.image.load(img)
        self.rect = pygame.Rect(x, y, 24, 24)

    def draw(self, surface):
        surface.blit(self.img, (self.rect.x, self.rect.y))


# ---------------- Лічильники ----------------
class Label(Sprite):
    """Лічильник із зображенням і числом для відображення часу або здоров'я"""

    def __init__(self, x, y, img, count, dx, dy):
        super().__init__(x, y, img)
        self.font = pygame.font.Font(None, 28)
        self.count = count
        self.dx = dx
        self.dy = dy

    def draw(self, surface):
        super().draw(surface)
        text = self.font.render(str(int(self.count)), True, (255, 0, 0))
        surface.blit(text, (self.rect.x + self.dx, self.rect.y + self.dy))


# ---------------- Труби ----------------
class Wall:
    def __init__(self):
        self.rects = []
        self.img = pygame.image.load("wall.png")

        x = 500
        for _ in range(3):  # три пари труб
            self.add_pipe_pair(x)
            x += 200

    def add_pipe_pair(self, x):
        """Створює пару труб із випадковим проміжком"""
        y = randint(-70, 0)
        top = pygame.Rect(x, y, 30, 250)
        bottom = pygame.Rect(x, y + 320, 30, 250)
        self.rects.extend([top, bottom])

    def randomize_pipe(self, i):
        """Оновлює одну пару труб (за індексом верхньої або нижньої)"""
        x = randint(600, 800)
        y = randint(-70, 0)
        if i % 2 == 0:  # верхня труба
            self.rects[i].x, self.rects[i].y = x, y
            self.rects[i + 1].x, self.rects[i + 1].y = x, y + 320
        else:  # нижня труба
            self.rects[i - 1].x, self.rects[i - 1].y = x, y
            self.rects[i].x, self.rects[i].y = x, y + 320

    def draw(self, surface):
        for rect in self.rects:
            surface.blit(self.img, (rect.x - 60, rect.y))
            # pygame.draw.rect(surface, (255, 0, 0), rect, 2)  # для дебага

    def update(self):
        for i, rect in enumerate(self.rects):
            rect.x -= 2
            if rect.x < -80:  # якщо вилетіла труба → робимо нову пару
                self.randomize_pipe(i)


# ---------------- Пташка ----------------
class Bird(Sprite):
    def __init__(self, x, y):
        """Пташка, що літає між трубами"""
        super().__init__(x, y, "b1.png")
        self.gravity = 0
        self.anim = 0

    def animate(self):
        self.anim += 0.1
        if self.anim >= 6:
            self.anim = 0
            self.img = pygame.image.load("b2.png")
        elif self.anim >= 3:
            self.img = pygame.image.load("b1.png")

    def update(self):
        """Оновлення стану пташки: гравітація, анімація, стрибок"""
        self.animate()
        self.gravity += 0.2
        self.rect.y += self.gravity
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.jump()

    def jump(self):
        self.gravity = -2.5

    def collide(self, wall):
        for i, rect in enumerate(wall.rects):
            if self.rect.colliderect(rect):
                # скидаємо пташку назад
                self.rect.x, self.rect.y = 50, 250
                self.gravity = 0
                # переносимо пару труб
                wall.randomize_pipe(i)
                return True
        return False


# ---------------- Ініціалізація ----------------
screen = pygame.display.set_mode((500, 500))
fon = pygame.image.load("fon.png")
clock = pygame.time.Clock()
running = True
font_large = pygame.font.Font(None, 64)

"""Ініціалізація пташки, труб, лічильників здоров'я і часу"""
wall = Wall()
bird = Bird(30, 125)

health_label = Label(10, 10, "b1.png", count=3, dx=30, dy=2)
time_label = Label(400, 10, "b1.png", count=30, dx=30, dy=2)

game_over = False

# ---------------- Основний цикл ----------------
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(fon, (0, 0))
    if not game_over:
        wall.update()
        bird.update()

        time_label.count -= 1 / 40

        if bird.collide(wall) or bird.rect.y > 500 or bird.rect.y < 0:
            health_label.count -= 1

        if health_label.count <= 0 or time_label.count <= 0:
            game_over = True

    wall.draw(screen)
    bird.draw(screen)
    health_label.draw(screen)
    time_label.draw(screen)

    if game_over:
        over_text = font_large.render("GAME OVER", True, (255, 0, 0))
        text_rect = over_text.get_rect(center=(250, 250))
        screen.blit(over_text, text_rect)

    pygame.display.flip()
    clock.tick(40)

pygame.quit()

