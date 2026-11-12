import random
import sys

import pygame

pygame.init()
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Subway Surfers")
clock = pygame.time.Clock()

LANES = [100, 300, 500]


class Sprite:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def get_rect(self):
        return pygame.Rect(
            self.x - self.width // 2, self.y - self.height // 2, self.width, self.height
        )

    def update(self):
        pass

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.get_rect())


class Player(Sprite):
    def __init__(self):
        self.lane_index = 1
        super().__init__(LANES[self.lane_index], HEIGHT - 100, 50, 50, (0, 255, 0))

    def move_left(self):
        if self.lane_index > 0:
            self.lane_index -= 1
            self.x = LANES[self.lane_index]

    def move_right(self):
        if self.lane_index < 2:
            self.lane_index += 1
            self.x = LANES[self.lane_index]


class Obstacle(Sprite):
    def __init__(self, lane_index):
        super().__init__(LANES[lane_index], -100, 60, 100, (255, 50, 50))
        self.speed = 8

    def update(self):
        self.y += self.speed


class TextLabel:
    def __init__(self, text, x, y, font_size=36, color=(255, 255, 255)):
        self.font = pygame.font.SysFont("arial", font_size)
        self.color = color
        self.x = x
        self.y = y
        self.update_text(text)

    def update_text(self, text):
        self.image = self.font.render(text, True, self.color)
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def draw(self, surface):
        surface.blit(self.image, self.rect)


player = Player()
obstacles = []
score = 0
spawn_timer = 0
total_obstacles_to_spawn = 20
spawned_obstacles_count = 0

score_label = TextLabel(f"Бали: {score}", 100, 30, font_size=40)
message_label = TextLabel("", WIDTH // 2, HEIGHT // 2, font_size=60)
game_state = "PLAYING"

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and game_state == "PLAYING":
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player.move_left()
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player.move_right()

    if game_state == "PLAYING":
        spawn_timer += 1
        if spawn_timer >= 40 and spawned_obstacles_count < total_obstacles_to_spawn:
            obstacles.append(Obstacle(random.randint(0, 2)))
            spawn_timer = 0
            spawned_obstacles_count += 1

        player.update()

        for obs in obstacles[:]:
            obs.update()

            if obs.y - obs.height // 2 > HEIGHT:
                obstacles.remove(obs)
                score += 10
                score_label.update_text(f"Бали: {score}")

            if player.get_rect().colliderect(obs.get_rect()):
                game_state = "GAME_OVER"
                message_label.update_text("ПОРАЗКА!")
                message_label.color = (255, 50, 50)

        if spawned_obstacles_count == total_obstacles_to_spawn and len(obstacles) == 0:
            game_state = "WIN"
            message_label.update_text("ПЕРЕМОГА!")
            message_label.color = (50, 255, 50)

    screen.fill((40, 40, 40))

    pygame.draw.line(screen, (200, 200, 200), (200, 0), (200, HEIGHT), 4)
    pygame.draw.line(screen, (200, 200, 200), (400, 0), (400, HEIGHT), 4)

    if game_state == "PLAYING":
        player.draw(screen)
        for obs in obstacles:
            obs.draw(screen)
        score_label.draw(screen)
    else:
        message_label.draw(screen)
        exit_label = TextLabel(
            "Закрий вікно, щоб вийти",
            WIDTH // 2,
            HEIGHT // 2 + 60,
            font_size=30,
            color=(150, 150, 150),
        )
        exit_label.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
