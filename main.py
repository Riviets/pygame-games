import pygame

pygame.init()


class Sprite:
    """Базовий клас для всіх об'єктів гри"""

    def __init__(self, x, y, img):
        """Ініціалізація спрайта"""
        self.img = pygame.image.load(img)
        self.rect = pygame.Rect(x, y, 24, 24)

    def draw(self, surface):
        """Малює спрайт на вказаній поверхні"""
        surface.blit(self.img, (self.rect.x, self.rect.y))

    def collide_list(self, list_obj):
        """Перевіряє зіткнення з будь-яким об'єктом зі списку"""
        for obj in list_obj:
            if self.rect.colliderect(obj.rect):
                return True
        return False


class Player(Sprite):
    """Клас гравця, наслідує Sprite"""

    def __init__(self, x, y, img):
        """Ініціалізація гравця"""
        super().__init__(x, y, img)
        self.keys = 0
        self.hp = 5

    def move(self):
        """Обробка руху гравця на основі натиснутих клавіш"""
        keys_pressed = pygame.key.get_pressed()

        if keys_pressed[pygame.K_LEFT]:
            self.rect.x -= 4
            if self.collide_list(maze) or (self.collide_list(doors) and self.keys == 0):
                self.rect.x += 4
        if keys_pressed[pygame.K_RIGHT]:
            self.rect.x += 4
            if self.collide_list(maze) or (self.collide_list(doors) and self.keys == 0):
                self.rect.x -= 4
        if keys_pressed[pygame.K_UP]:
            self.rect.y -= 4
            if self.collide_list(maze) or (self.collide_list(doors) and self.keys == 0):
                self.rect.y += 4
        if keys_pressed[pygame.K_DOWN]:
            self.rect.y += 4
            if self.collide_list(maze) or (self.collide_list(doors) and self.keys == 0):
                self.rect.y -= 4

    def update(self):
        """Оновлення стану гравця, наприклад анімації"""
        """Перевірка дотику до ключів і дверей"""
        for door in doors[:]:
            if self.rect.colliderect(door.rect) and self.keys > 0:
                doors.remove(door)
                all_sprites.remove(door)
                self.keys -= 1

        for key in keys[:]:
            if self.rect.colliderect(key.rect):
                keys.remove(key)
                all_sprites.remove(key)
                self.keys += 1

        """Перевірка дотику до ворогів"""
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                self.rect.x, self.rect.y = 24, 24
                self.hp -= 1
                if self.hp >= 0 and self.hp < len(hp):
                    hp[self.hp].img = pygame.image.load("hp_broken.png")


class Enemy(Sprite):
    """Клас ворога, наслідує Sprite"""

    def __init__(self, x, y, img, dx, dy):
        """Ініціалізація ворога з напрямком руху"""
        super().__init__(x, y, img)
        self.dx = dx
        self.dy = dy

    def move(self):
        """Рух ворога і перевірка зіткнень зі стінами"""
        self.rect.x += self.dx
        self.rect.y += self.dy
        if self.collide_list(maze):
            self.dx *= -1
            self.dy *= -1
            self.rect.x += self.dx
            self.rect.y += self.dy


# 24x48 - door
# 24x24 - wall, player, heart, key

# 1 — стіна
# 0 — прохід
# 2 — двері (декілька)
# 3 — ключі
# 4 — вороги рух ліво-право
# 5 — вороги рух вгору-вниз
"""Мапа лабіринту"""
map_maze = [
    "101111111111111111111",
    "100000100000100000001",
    "101110101010101011101",
    "101000101010101010101",
    "111011101011101010101",
    "100010001000001010201",
    "101110111111111010111",
    "100010140000000010151",
    "111010101110111110101",
    "100010101030100010001",
    "101110101111101011101",
    "101000100010001013101",
    "101011111020111010101",
    "102010001010001010001",
    "101111101111111010111",
    "101000100010000010031",
    "101010101010111111111",
    "101010001010000010001",
    "101011111011111010111",
    "10001400000031000002",
    "111111111111111111111",
]
"""Списки для зберігання об'єктів гри"""
maze = []  # стіни
doors = []  # двері
keys = []  # ключі
enemies = []  # вороги
hp = []  # здоров'я

"""Ініціалізація здоров'я гравця"""
x, y = 350, 0
for i in range(5):
    hp.append(Sprite(x, y, "hp.png"))
    x += 26


def draw_maze():
    """Функція для створення лабіринту на основі текстового представлення"""
    x_maze, y_maze = 0, 0
    x, y = x_maze, y_maze
    for line in map_maze:
        for num in line:
            if num == "1":
                maze.append(Sprite(x, y, "wall.png"))
            elif num == "2":
                doors.append(Sprite(x, y, "door.png"))
            elif num == "3":
                keys.append(Sprite(x, y, "key.png"))
            elif num == "4":
                """тут створюємо ворога з рухом вліво-вправо"""
                enemies.append(Enemy(x, y, "enemy.png", 2, 0))
            elif num == "5":
                """тут створюємо ворога з рухом вгору-вниз"""
                enemies.append(Enemy(x, y, "enemy.png", 0, 2))
            x += 24
        x = x_maze
        y += 24


"""підготовка до запуску гри"""
FON = (133, 230, 255)  # колір фону
draw_maze()  # створення лабіринту
all_sprites = maze + doors + keys + enemies + hp  # всі об'єкти гри


screen = pygame.display.set_mode((500, 500))  # розмір вікна
clock = pygame.time.Clock()  # для контролю частоти кадрів
running = True


"""Ініціалізація гравця"""
hero = Player(24, 24, "hero_start.png")


"""Основний цикл гри"""
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(FON)  # заливка
    # малювання всіх об'єктів гри: стін, дверей, ключів, ворогів, здоров'я
    for obj in all_sprites:
        obj.draw(screen)

    # малювання гравця
    hero.draw(screen)

    # оновлення стану гравця
    hero.update()

    # рух гравця
    hero.move()

    # рух ворогів
    for enemy in enemies:
        enemy.move()

    # перевірка кінця гри
    if hero.hp <= 0:
        running = False

    # перевірка виграшу
    if hero.rect.y > 480:
        running = False

    pygame.display.flip()
    clock.tick(40)

pygame.quit()

