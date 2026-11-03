import pygame

pygame.init()
from random import choice, randint, uniform


# ---------------- Базовий клас ----------------
class Sprite:
    """Базовий клас для всіх об'єктів гри"""

    def __init__(self, x, y, w, h, img):
        self.img = pygame.image.load(img)
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self, surface):
        surface.blit(self.img, (self.rect.x, self.rect.y))


class Mink(Sprite):
    """Клас нірки"""

    def __init__(self, x, y, w, h, img):
        super().__init__(x, y, w, h, img)
        self.free = True


class Bobr(Sprite):
    """Клас бобра"""

    def __init__(self, x, y, w, h, img):
        super().__init__(x, y, w, h, img)
        self.anim = 0
        self.count = 0
        self.mink = choice(minks)
        self.sp = randint(1, 3)
        self.random_mink()

    def random_mink(self):
        """Вибір випадкової нірки для появи бобра"""
        mink = choice(minks)
        while not mink.free:
            mink = choice(minks)
        self.mink.free = True
        self.mink = mink
        self.mink.free = False
        self.sp = randint(1, 3)
        self.rect.x, self.rect.y = self.mink.rect.x, self.mink.rect.y + 10
        self.anim = 1
        self.count = 0
        self.img = pygame.image.load(f"bobr{self.anim}.png")
        self.rect.h = 8

    def anim_bobr(self):
        """Анімація появи бобра"""
        self.count += self.sp
        if self.count % 10 == 0 and self.anim < 8:
            self.anim += 1
            self.img = pygame.image.load(f"bobr{self.anim}.png")
            self.rect.h += 8
            self.rect.y -= 8

        if self.count >= 90:
            self.random_mink()


class Molot(Sprite):
    """Клас молота"""

    def __init__(self, x, y, w, h, img):
        super().__init__(x, y, w, h, img)
        self.count = 0
        self.anim = 0

    def update(self, event):
        """Оновлення положення молота та перевірка на удар бобра"""
        if event.type == pygame.MOUSEMOTION:
            """Оновлення положення молота за курсором миші"""
            self.rect.x, self.rect.y = event.pos
            self.rect.x -= self.rect.w // 2
            self.rect.y -= self.rect.h // 2

        if event.type == pygame.MOUSEBUTTONDOWN:
            """Перевірка на удар бобра"""
            self.img = pygame.image.load("molot_down.png")
            self.anim = 1
            for bobr in bobrs:
                if self.rect.colliderect(bobr.rect) and bobr.anim > 1:
                    bobr.random_mink()
                    self.count += 1

        """Малювання молота - анімація удару"""
        if self.anim > 0:
            self.anim += 1
            if self.anim == 5:
                self.img = pygame.image.load("molot.png")
                self.anim = 0


class Label:
    def __init__(self, x, y, text, img, font_size=30, color=(0, 0, 0)):
        """Клас для відображення тексту з іконкою"""
        self.font = pygame.font.SysFont("Arial", font_size)
        if img:
            self.img = pygame.image.load(img)
        else:
            self.img = None
        self.text = text
        self.color = color
        self.x = x
        self.y = y

    def draw(self, surface):
        """Малювання тексту з іконкою"""
        label = self.font.render(self.text, True, self.color)
        surface.blit(label, (self.x, self.y))
        if self.img:
            surface.blit(self.img, (self.x - 50, self.y - 5))


minks = []  # Список нірок
x, y = 50, 200
for _ in range(3):
    for _ in range(3):
        minks.append(Mink(x, y, 64, 40, "nirka.png"))
        x += 168
    x = 50
    y += 100

bobrs = []  # Список бобрів
"""створити об'єкти бобрів і додати їх до списку bobrs"""
for _ in range(3):
    bobrs.append(Bobr(0, 0, 64, 64, "bobr1.png"))

"""створити обєкти молота"""
molot = Molot(0, 0, 64, 64, "molot.png")

"""створити об'єкт для відображення рахунку"""
score_label = Label(70, 10, "0", "b.png", 40, (255, 0, 0))

"""створити об'єкт для відображення часу"""
time_label = Label(420, 10, "30", "timer.png", 40, (255, 0, 0))

# ---------------- Ініціалізація ----------------

screen = pygame.display.set_mode((500, 500))
fon = pygame.image.load("fon.png")
clock = pygame.time.Clock()
running = True

start_ticks = pygame.time.get_ticks()
end_game = False
result_label = None

# ---------------- Основний цикл ----------------
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not end_game:
            """оновлення молота"""
            molot.update(event)

    screen.blit(fon, (0, 0))

    if not end_game:
        # підрахунок часу (відлічуємо назад від 30)
        seconds_passed = (pygame.time.get_ticks() - start_ticks) // 1000
        time_left = 30 - seconds_passed

        for bobr in bobrs:
            """оновлення бобра"""
            bobr.anim_bobr()
            """малювання бобра"""
            bobr.draw(screen)

        """малювання нірок"""
        for mink in minks:
            mink.draw(screen)

        """малювання молота"""
        molot.draw(screen)

        """малювання тексту з іконками"""
        score_label.text = str(molot.count)
        time_label.text = str(max(0, time_left))
        score_label.draw(screen)
        time_label.draw(screen)

        """перевірка на кінець гри - час вийшов, або всі бобри побиті"""
        if time_left <= 0:
            end_game = True
            if molot.count >= 10:
                result_label = Label(130, 220, "Ти виграв!", None, 50, (0, 200, 0))
            else:
                result_label = Label(130, 220, "Ти програв!", None, 50, (255, 0, 0))
    else:
        """малювання кінцевого екрану"""
        if result_label:
            result_label.draw(screen)

    pygame.display.flip()
    clock.tick(40)

pygame.quit()

