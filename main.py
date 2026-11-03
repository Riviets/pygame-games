import pygame as pg

YELLOW = (200, 200, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

WIDTH = 500
HEIGHT = 500

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))

# завантаження картинок

image_ball = pg.image.load("Ball.png").convert_alpha()

image_block1 = pg.image.load("Block1.png").convert_alpha()
image_block2 = pg.image.load("Block2.png").convert_alpha()
image_block3 = pg.image.load("Block3.png").convert_alpha()

# додайте потрібні зображення
image_bg = pg.image.load("background.png")
image_platform = pg.image.load("Platform1.png")
image_platform_left = pg.image.load("Platform3.png")
image_platform_right = pg.image.load("Platform2.png")

#####################################
#    елементи з попередніх уроків   #
#####################################


class TextLabel:
    # Текстова позначка
    def __init__(self, x, y, size=32, color=BLACK):
        self.x = x
        self.y = y
        self.color = color
        self.image = None
        self.font = pg.font.Font(None, size)

    def set_text(self, text):
        self.image = self.font.render(text, True, self.color)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))


#####################################
#          ігрові класи             #
#####################################
class Sprite:
    # базовий клас для спадкування класами гри
    def __init__(self, x, y, image):
        self.image = image
        self.rect = pg.Rect(x, y, self.image.get_width(),
                            self.image.get_height())
    def collide(self, sprite):
        return self.rect.colliderect(sprite.rect)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.left, self.rect.top))

class Player(Sprite):
    def __init__(self,x, y, image_base):
        super().__init__(x,y, image_base)
        self.image_base = image_platform
        self.dir = "stop"
        self.lives = 3
        
    def update(self):
        keys = pg.key.get_pressed()
        
        if keys[pg.K_a]:
            self.dir = "left"
            self.rect.x -= 8
        elif keys[pg.K_d]:
            self.dir = "right"
            self.rect.x += 8
        else:
            self.dir = "stop"
        
class Ball(Sprite):
    def __init__(self, x, y, image_ball, velocity):
        super().__init__(x,y,image_ball)
        self.base_image = image_ball
        self.SPEED = velocity
        self.velocityx = velocity
        self.velocityy = -velocity
        self.angle = 0
        self.dir = "stop"
        
    def update(self):
        self.rect.left += self.velocityx
        self.rect.top += self.velocityy


        if self.dir == "right":
            self.angle += 10
            self.image = pg.transform.rotate(self.base_image, self.angle)
        elif self.dir == "left":
            self.angle -= 10
            self.image = pg.transform.rotate(self.base_image, self.angle)


            if self.angle > 360:
                self.angle -= 360
            if self.angle < 0:
                self.angle += 360


        if self.rect.left < 0:
            self.velocityx = -self.velocityx
        if self.rect.right > WIDTH:
            self.velocityx = -self.velocityx


        if self.rect.top < 0:
            self.velocityy = self.SPEED
        if self.rect.bottom > HEIGHT:
            self.velocityy = -self.SPEED


    def change_velocity(self, player):
        self.velocityy = -self.SPEED
        self.dir = player.dir


        if player.dir == "right":
            self.velocityx += 2


        elif player.dir == "left":
            self.velocityx -= 2


        if self.velocityx < -6:
            self.velocityx = -6
        if self.velocityx > 6:
            self.velocityx = 6

    
#####################################
#    ігрові об'єкти та цикл         #
#####################################
blocks = []
block_images = [image_block1, image_block2, image_block3]
for i in range(15):
    row = i // 5
    col = i % 5
    
    blocks.append(Sprite(50 + col*80, 20 + row*40, block_images[row]))


clock = pg.time.Clock()
running = True

player = Player(WIDTH // 2 - 60, HEIGHT - 60, image_platform)
ball = Ball(100, HEIGHT // 2, image_ball, 4)

score = 0
label = TextLabel(350, 450, 28)
label.set_text(f"Score: {score}")
lives_label = TextLabel(20, 450, 32)
lives_label.set_text(player.lives * "❤️")

def reset_positions():
    player.rect.x = WIDTH // 2 - 60
    player.rect.y = HEIGHT - 60
    ball.rect.x = WIDTH // 2
    ball.rect.y = HEIGHT // 2
    ball.velocityx = ball.SPEED
    ball.velocityy = -ball.SPEED

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False


    screen.fill(WHITE)
    screen.blit(image_bg, (0,0))
    player.update()
    ball.update()

    if player.collide(ball):
        ball.change_velocity(player)

    for b in blocks:
        if b.collide(ball):
            blocks.remove(b)
            ball.velocityy = ball.SPEED
            score += 100
            label.set_text(f"Score: {score}")
    
    for b in blocks:
        b.draw(screen)
        
    if not len(blocks):
        print("Перемога")
        running = False
        
    if ball.rect.y > player.rect.y:
        player.lives -= 1
        lives_label.set_text(player.lives * "❤️")
        reset_positions()
        if player.lives <= 0:
            running = False
            print("Поразка")
            

    ball.draw(screen)
    player.draw(screen)
    label.draw(screen)
    lives_label.draw(screen)
    pg.display.flip()

    clock.tick(50)

pg.quit()

