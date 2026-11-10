from random import choice, randint, uniform

import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60
SPAWN_INTERVAL = 600
START_LIVES = 3

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

SCREEN_RECT = pygame.Rect(0, 0, WIDTH, HEIGHT)


class Sprite:
    def __init__(self, x, y, width, height, color):
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.image.fill(color)
        self.rect = pygame.Rect(x, y, width, height)

    def update(self):
        pass

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class TextLabel(Sprite):
    def __init__(self, x, y, size, color, anchor="topleft"):
        super().__init__(x, y, 1, 1, None)
        self.font = pygame.font.Font(None, size)
        self.color = color
        self.pos = (x, y)
        self.anchor = anchor
        self.text = None
        self.set_text("")

    def set_text(self, text):
        if text != self.text:
            self.text = text
            self.image = self.font.render(text, True, self.color)
            self.rect = self.image.get_rect(**{self.anchor: self.pos})


class Player(Sprite):
    SIZE = 20
    SPEED = 5

    def __init__(self):
        super().__init__(
            WIDTH // 2 - self.SIZE // 2,
            HEIGHT // 2 - self.SIZE // 2,
            self.SIZE,
            self.SIZE,
            RED,
        )
        self.lives = START_LIVES

    def update(self):
        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_RIGHT] or keys[pygame.K_d]) - (
            keys[pygame.K_LEFT] or keys[pygame.K_a]
        )
        dy = (keys[pygame.K_DOWN] or keys[pygame.K_s]) - (
            keys[pygame.K_UP] or keys[pygame.K_w]
        )
        self.rect.x += dx * self.SPEED
        self.rect.y += dy * self.SPEED
        self.rect.clamp_ip(SCREEN_RECT)

    def collide(self, bullet):
        return self.rect.colliderect(bullet.rect)


class Bullet(Sprite):
    RADIUS = 8
    MARGIN = 100

    def __init__(self, target):
        size = self.RADIUS * 2
        super().__init__(0, 0, size, size, None)
        pygame.draw.circle(self.image, WHITE, (self.RADIUS, self.RADIUS), self.RADIUS)

        side = choice(("top", "bottom", "left", "right"))
        if side == "top":
            self.pos = pygame.math.Vector2(randint(0, WIDTH), -self.RADIUS)
        elif side == "bottom":
            self.pos = pygame.math.Vector2(randint(0, WIDTH), HEIGHT + self.RADIUS)
        elif side == "left":
            self.pos = pygame.math.Vector2(-self.RADIUS, randint(0, HEIGHT))
        else:
            self.pos = pygame.math.Vector2(WIDTH + self.RADIUS, randint(0, HEIGHT))

        aim = pygame.math.Vector2(target) + pygame.math.Vector2(
            randint(-60, 60), randint(-60, 60)
        )
        self.velocity = (aim - self.pos).normalize() * uniform(3, 6)
        self.rect.center = self.pos

    def update(self):
        self.pos += self.velocity
        self.rect.center = self.pos

    def is_outside(self):
        return not SCREEN_RECT.inflate(self.MARGIN * 2, self.MARGIN * 2).colliderect(
            self.rect
        )


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Undertale MVP")
clock = pygame.time.Clock()

lives_label = TextLabel(10, 10, 36, WHITE, "topleft")
score_label = TextLabel(WIDTH - 10, 10, 36, WHITE, "topright")
game_over_label = TextLabel(WIDTH // 2, HEIGHT // 2 - 50, 80, RED, "center")
final_score_label = TextLabel(WIDTH // 2, HEIGHT // 2 + 20, 48, WHITE, "center")
restart_label = TextLabel(WIDTH // 2, HEIGHT // 2 + 80, 30, WHITE, "center")
game_over_label.set_text("GAME OVER")
restart_label.set_text("Press R to restart")

player = Player()
bullets = []
score = 0
game_over = False
last_spawn = pygame.time.get_ticks()

running = True
while running:
    now = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r and game_over:
            player = Player()
            bullets = []
            score = 0
            game_over = False
            last_spawn = now

    if not game_over:
        player.update()

        if now - last_spawn >= SPAWN_INTERVAL:
            bullets.append(Bullet(player.rect.center))
            last_spawn = now

        for bullet in bullets[:]:
            bullet.update()
            if player.collide(bullet):
                player.lives -= 1
                bullets.remove(bullet)
            elif bullet.is_outside():
                score += 1
                bullets.remove(bullet)

        if player.lives <= 0:
            player.lives = 0
            game_over = True

        lives_label.set_text(f"Lives: {player.lives}")
        score_label.set_text(f"Score: {score}")
        final_score_label.set_text(f"Final score: {score}")

    screen.fill(BLACK)

    if game_over:
        game_over_label.draw(screen)
        final_score_label.draw(screen)
        restart_label.draw(screen)
    else:
        player.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)
        lives_label.draw(screen)
        score_label.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
