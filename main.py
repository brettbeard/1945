import math, os, pygame, random
from pygame.locals import *

#define constants
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
OCEAN_BLUE = (0,67,171)

# Utility functions
def load_sound(filename):
    filename = os.path.join('data', filename)
    return pygame.mixer.Sound(filename)


def imgcolorkey(image, colorkey):
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image


def load_image(filename, colorkey = None):
    filename = os.path.join('data', filename)
    image = pygame.image.load(filename).convert()
    return imgcolorkey(image, colorkey)

# Sprite sheet class
class SpriteSheet:
    def __init__(self, filename):
        self.sheet = load_image(filename)

    def imgat(self, rect, colorkey = None):
        rect = Rect(rect)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        return imgcolorkey(image, colorkey)

    def imgsat(self, rects, colorkey = None):
        imgs = []
        for rect in rects:
            imgs.append(self.imgat(rect, colorkey))
        return imgs


# Plane class
class Plane(pygame.sprite.Sprite):
    speed = 5
    reloadtime = 15
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)

        #self.image = self.images[0]
        self.rect = self.image.get_rect()

        self.rect.center = (320, 240)
        self.reloadtimer = 0

    def update(self):
        if self.reloadtimer > 0:
            self.reloadtimer -= 1

    def move_left(self):
        self.rect.move_ip(-self.speed, 0)

    def move_right(self):
        self.rect.move_ip(self.speed, 0)

    def move_up(self):
        self.rect.move_ip(0, -self.speed)

    def move_down(self):
        self.rect.move_ip(0, self.speed)

    def shoot(self):
        if self.reloadtimer == 0:
            Shot((self.rect.left + 17, self.rect.top))
            Shot((self.rect.left + 39, self.rect.top))
            self.reloadtimer = self.reloadtime


# Shot class
class Shot(pygame.sprite.Sprite):
    speed = 5

    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self, self.containers)

        self.rect = self.image.get_rect()

        self.rect.center = pos

    def update(self):
        self.rect.move_ip(0, -self.speed)
        if self.rect.top < 0:
            self.kill()

# Main loop
def main():
    pygame.init()

    # create a display screen: 640 x 480 pixels
    screen = pygame.display.set_mode((640, 480))

    spritesheet = SpriteSheet('1945.bmp')

    Plane.image = spritesheet.imgat((305, 113, 61, 49), OCEAN_BLUE)
    Shot.image = spritesheet.imgat((48, 176, 9, 20), -1)

    # Init sprite groups
    shots = pygame.sprite.Group()
    all = pygame.sprite.RenderPlain()

    Plane.containers = all
    Shot.containers = shots, all

    clock = pygame.time.Clock()

    # Instantiate plane
    plane = Plane()

    done = False  # we're not done displaying
    while not done:
        for event in pygame.event.get():  # check the events list
            if event.type == pygame.QUIT:  # if the user clicks the X
                done = True  # now we're done displaying

        pressed = pygame.key.get_pressed()
        if pressed[K_LEFT]:
            plane.move_left()

        if pressed[K_RIGHT]:
            plane.move_right()

        if pressed[K_UP]:
            plane.move_up()

        if pressed[K_DOWN]:
            plane.move_down()

        if pressed[K_SPACE]:
            plane.shoot()

        screen.fill(BLUE)

        # update all the sprites
        all.update()

        # draw the scene
        all.draw(screen)
        pygame.display.flip()

        # cap the frame rate
        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()