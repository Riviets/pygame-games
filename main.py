from random import choice, randint

import pygame

pygame.init()


# ---------------- Базовий клас ----------------
class Sprite:
    """Базовий клас для всіх спрайтів"""

    def __init__(self, x, y, img, w=24, h=24):
        self.img = pygame.image.load(img)
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self, surface):
        surface.blit(self.img, (self.rect.x, self.rect.y))


# ---------------- Класи  ворога ----------------
class Enemy(Sprite):
    """Клас ворога"""

    def __init__(self, x, y, img):
        super().__init__(x, y, img)
        self.dx, self.dy = 2, 0
        self.dr = [-2, 2]

    def move(self, maze):
        """Рух ворога"""
        self.rect.x += self.dx
        self.rect.y += self.dy
        for wall in maze.walls:
            if self.rect.colliderect(wall):
                self.dx *= -1
                self.dy *= -1
                self.rect.x += self.dx
                self.rect.y += self.dy
        if randint(1, 30) == 1:
            self.change_dir()

    def change_dir(self):
        """Зміна напрямку руху ворога"""
        if self.dx != 0:
            self.dx = 0
            self.dy = choice(self.dr)
        else:
            self.dx = choice(self.dr)
            self.dy = 0


# ---------------- Клас гравця ----------------
class Player(Sprite):
    def __init__(self, x, y):
        """Клас гравця"""
        super().__init__(x, y, "pR_open.png")
        self.dx, self.dy = 0, 0
        self.dots = 0
        self.hp = 5
        self.anim_frame = 0

    def animate(self):
        """Анімація руху гравця"""
        if self.dx != 0 or self.dy != 0:
            self.anim_frame += 1
            if self.anim_frame % 6 == 0:
                self.img = pygame.image.load("pR_close.png")
            elif self.anim_frame % 3 == 0:
                self.img = pygame.image.load("pR_open.png")

    def update(self, maze):
        """Оновлення положення гравця"""
        """Анімація, рух, збір точок"""
        self.animate()
        self.move()

        for dot in maze.dots[:]:
            if self.rect.colliderect(dot):
                maze.dots.remove(dot)
                self.dots -= 1

        """Перевірка зіткнень зі стінами, точками, ворогами"""
        for wall in maze.walls:
            if self.rect.colliderect(wall):
                self.rect.x -= self.dx
                self.rect.y -= self.dy

        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                self.rect.x, self.rect.y = 40, 418
                self.hp -= 1

    def move(self):
        """Рух гравця"""
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.dx, self.dy = -2, 0
        elif key[pygame.K_RIGHT]:
            self.dx, self.dy = 2, 0
        elif key[pygame.K_UP]:
            self.dx, self.dy = 0, -2
        elif key[pygame.K_DOWN]:
            self.dx, self.dy = 0, 2
        else:
            self.dx, self.dy = 0, 0

        self.rect.x += self.dx
        self.rect.y += self.dy


# ---------------- Клас лабіринту ----------------
class Maze:
    def __init__(self):
        """Лабіринт із стінами"""
        self.walls = []  # список зі стінами
        self.dots = []  # список із точками
        self.w = pygame.image.load("wall.png")  # зображення стіни
        self.d = pygame.image.load("dot.png")  # зображення точки
        self.create_wall()  # створення лабіринту зі стінами

    def create_wall(self):
        """Створення лабіринту зі стінами"""
        x, y = 10, 10
        count = 0
        for line in maze_map:
            for num in line:
                if num == "1":
                    """Додавання стіни до списку зі стінами"""
                    self.walls.append(pygame.Rect(x, y, 32, 32))
                elif num == "0":
                    """Додавання точки до списку з точками"""
                    self.dots.append(pygame.Rect(x + 6, y + 6, 18, 18))
                elif num == "2":
                    """Додавання ворога до списку з ворогами"""
                    enemies.append(Enemy(x, y, f"g{count + 1}.png"))
                    count += 1
                x += 32
            y += 32
            x = 10

    def draw(self, surface):
        """Відображення лабіринту на екрані"""
        for wall in self.walls:
            surface.blit(self.w, (wall.x, wall.y))
        for dot in self.dots:
            surface.blit(self.d, (dot.x, dot.y))


# ---------------- Клас для відображення тексту ----------------
class Label:
    """Клас для відображення тексту на екрані"""

    def __init__(self, x, y, img, text, font_size=20, color=(255, 255, 255)):
        self.font = pygame.font.SysFont("Arial", font_size)
        self.font.bold = True
        self.img = pygame.image.load(img)
        self.text = text
        self.color = color
        self.x = x
        self.y = y

    def update(self, text):
        """Оновлення тексту"""
        self.text = text

    def draw(self, surface):
        """Відображення тексту на екрані"""
        img_text = self.font.render(self.text, True, self.color)
        surface.blit(img_text, (self.x, self.y))
        surface.blit(self.img, (self.x - 25, self.y))


# ---------------- Лабіринт ----------------
"""Мапа лабіринту"""
maze_map = [
    "111111111111111",
    "100000001000001",
    "101101101011011",
    "100000000000001",
    "110010111010111",
    "100010010010001",
    "110011000110111",
    "100000020000001",
    "110001121100111",
    "100101222100001",
    "110001111100111",
    "100100000001001",
    "101101111101101",
    "130000010000001",
    "111111111111111",
]

# ---------------- Ініціалізація ----------------
screen = pygame.display.set_mode((500, 500))
FON = (17, 12, 92)
clock = pygame.time.Clock()
running = True

enemies = []  # список із ворогами
maze = Maze()  # створення лабіринту

"""Створення гравця"""
pacman = Player(40, 418)
pacman.dots = len(maze.dots)

"""Створення підписів для відображення кількості точок і здоров'я"""
hp_label = Label(40, 10, "hp.png", f": {pacman.hp}")
dots_label = Label(440, 10, "dot.png", f": {pacman.dots}")

"""Створення шрифту для відображення кінцевого тексту"""
end_font = pygame.font.SysFont("Arial", 45)
end_font.bold = True

"""Завантаження зображення кінцевого екрану"""
end_bg = pygame.image.load("end.png")

end_game = False
result_text = None

# ---------------- Основний цикл ----------------
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(FON)

    if not end_game:
        maze.draw(screen)

        for enemy in enemies:
            enemy.move(maze)
            enemy.draw(screen)

        """Оновлення і відображення гравця"""
        pacman.update(maze)
        pacman.draw(screen)

        """Оновлення і відображення підписів"""
        hp_label.update(f": {pacman.hp}")
        dots_label.update(f": {pacman.dots}")
        hp_label.draw(screen)
        dots_label.draw(screen)

        """Перевірка кінця гри і відображення кінцевого екрану"""
        if pacman.hp <= 0:
            end_game = True
            result_text = end_font.render("GAME OVER", True, (255, 0, 0))

        if pacman.dots == 0:
            end_game = True
            result_text = end_font.render("YOU WIN!", True, (0, 255, 0))
    else:
        screen.blit(end_bg, (0, 0))
        if result_text:
            screen.blit(result_text, (110, 430))

    pygame.display.flip()
    clock.tick(40)

pygame.quit()

