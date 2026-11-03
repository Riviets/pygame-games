from random import randint

import pygame

pygame.init()


# ---------------- Базовий клас ----------------
class Sprite:
    def __init__(self, x, y, w, h, img):
        self.img = pygame.image.load(img)
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self, surface):
        surface.blit(self.img, (self.rect.x, self.rect.y))


class Eat(Sprite):
    """Клас для їжі"""

    def __init__(self, x, y, w, h, img, good=True):
        super().__init__(x, y, w, h, img)
        self.good = good

    def update(self):
        """Оновлення таймера і позиції їжі"""
        pass

    def random_position(self):
        """Встановлення випадкової позиції їжі"""
        self.rect.x = randint(1, 13) * 32
        self.rect.y = randint(2, 13) * 32


class Head(Sprite):
    """Клас для голови змійки"""

    def __init__(self, x, y, w, h, img):
        super().__init__(x, y, w, h, img)
        self.dx = 0
        self.dy = -2
        self.bum = pygame.image.load("bum.png")
        self.anim = 0

    def move(self):
        """Рух голови"""
        self.rect.x += self.dx
        self.rect.y += self.dy

    def update(self):
        """Оновлення напрямку руху голови"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.dx == 0:
            self.img = pygame.image.load("head_l.png")
            self.dx = -2
            self.dy = 0
        if keys[pygame.K_RIGHT] and self.dx == 0:
            self.img = pygame.image.load("head_r.png")
            self.dx = 2
            self.dy = 0
        if keys[pygame.K_UP] and self.dy == 0:
            self.img = pygame.image.load("head_u.png")
            self.dx = 0
            self.dy = -2
        if keys[pygame.K_DOWN] and self.dy == 0:
            self.img = pygame.image.load("head_d.png")
            self.dx = 0
            self.dy = 2

    def check_bounds(self):
        """Перевірка виходу за межі екрану"""
        if (
            self.rect.x < 0
            or self.rect.x > 500 - self.rect.width
            or self.rect.y < 0
            or self.rect.y > 500 - self.rect.height
        ):
            return True
        return False

    def draw(self, surface):
        """Малювання голови і анімації зіткнення"""
        super().draw(surface)
        if self.anim > 0:
            self.anim += 1
            surface.blit(self.bum, (self.rect.x, self.rect.y))
        if self.anim > 20:
            self.anim = 0


class Snake:
    """Клас для змійки"""

    def __init__(self):
        # список сегментів хвоста
        self.tail = []
        self.head = Head(200, 200, 32, 32, "head_u.png")  # початкова позиція голови
        # кількість з'їденої їжі
        self.count = 0
        # історія руху голови
        self.history = []
        # відстань між сегментами (кадрів)
        self.spacing = 16

    def update(self):
        """Оновлення стану змійки"""
        # рухаємо голову
        self.head.move()
        self.head.update()

        # перевіряємо зіткнення з межами та хвостом
        if self.head.check_bounds() or self.bounds_tail():
            # якщо зіткнення було, запускаємо анімацію і скидаємо змійку
            self.head.anim = 1
            return True

        # записуємо координати голови в історію
        self.history.insert(0, (self.head.rect.x, self.head.rect.y))

        # зберігаємо історію достатньо довгою для всіх сегментів
        max_len = (len(self.tail) + 1) * self.spacing
        if len(self.history) > max_len:
            self.history = self.history[:max_len]

        # рухаємо хвіст
        self.move_tail()
        return False

    def draw(self, surface):
        """Малювання змійки"""
        # малюємо хвіст
        for segment in self.tail:
            segment.draw(surface)
        # малюємо голову
        self.head.draw(surface)

    def move_tail(self):
        """Рух хвоста"""
        # кожен сегмент рухається за своїм "відставанням"
        for i, segment in enumerate(self.tail):
            # індекс в історії для цього сегмента
            idx = (i + 1) * self.spacing
            # якщо індекс в межах історії, оновлюємо позицію сегмента
            if idx < len(self.history):
                # беремо позицію з історії
                segment.rect.x, segment.rect.y = self.history[idx]

    def bounds_tail(self):
        """Перевірка зіткнення голови з хвостом"""
        # перевіряємо зіткнення з хвостом, пропускаючи перші сегменти (близькі до голови)
        if len(self.tail) > 3:
            for segment in self.tail[3:]:
                if self.head.rect.colliderect(segment.rect):
                    return True
        return False

    def eat(self, food):
        """Перевірка зіткнення з їжею і збільшення змійки"""
        """Якщо голова зіткнулася з їжею"""
        if self.head.rect.colliderect(food.rect):
            """Якщо їжа корисна, додаємо сегмент до хвоста і збільшуємо лічильник"""
            self.count += 1
            # створюємо новий сегмент поза екраном, щоб він не викликав суперечок у колізії
            segment = Sprite(-50, -50, 32, 32, "tail.png")
            self.tail.append(segment)
            food.random_position()


class Label(Sprite):
    """Клас для відображення тексту"""

    def __init__(self, x, y, w, h, img, font_size=30):
        super().__init__(x, y, w, h, img)
        self.font = pygame.font.SysFont("Arial", font_size)
        self.color = (158, 42, 5)

    def draw(self, surface, text):
        """Малювання тексту на екрані"""
        super().draw(surface)
        text_img = self.font.render(text, True, self.color)
        surface.blit(text_img, (self.rect.x + 40, self.rect.y + 10))


class Button(Sprite):
    """Клас для кнопки"""

    def __init__(self, x, y, w, h, img):
        super().__init__(x, y, w, h, img)

    def is_clicked(self, event):
        """Перевірка, чи була кнопка натиснута"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False


# ---------------- Ініціалізація ----------------
screen = pygame.display.set_mode((500, 500))
fon = pygame.image.load("fon.png")
clock = pygame.time.Clock()
running = True

snake = Snake()  # створюємо змійку
"""Створюємо корисну і шкідливу їжу в випадкових позиціях"""
good_Eat = Eat(100, 100, 32, 32, "good_eat.png")
good_Eat.random_position()

"""Таймер і лічильник"""
count = Label(10, 10, 140, 50, "count.png", 30)

"""Створюємо фон і кнопку старту"""
end_font = pygame.font.SysFont("Arial", 50)
game_over = False

# ---------------- Основний цикл ----------------
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(fon, (0, 0))

    if not game_over:
        is_dead = snake.update()
        if is_dead:
            game_over = True

        snake.draw(screen)

        """Малюємо їжу і перевіряємо зіткнення"""
        good_Eat.draw(screen)
        snake.eat(good_Eat)

        """Малюємо таймер і лічильник"""
        count.draw(screen, f"{snake.count}")
    else:
        """Якщо гра закінчена, показуємо екран кінця гри"""
        over_text = end_font.render("GAME OVER", True, (158, 42, 5))
        screen.blit(over_text, (110, 220))

    pygame.display.flip()
    clock.tick(40)

pygame.quit()

