import pygame
import constants
import random


class Enemy(pygame.sprite.Sprite):
    """docstring for Enemy."""
    def __init__(self):
        super(Enemy, self).__init__()
        self.type = type
        self.change_x = 0.0
        self.change_y = 0.0
        self.level = None
        width = 40
        height = 40
        self.image = pygame.Surface([width, height])
        R = random.randint(0, 255)
        G = random.randint(0, 255)
        B = random.randint(0, 255)
        color = (R, G, B)
        self.jumppower = random.randint(0, 20)
        self.speed = random.uniform(1, constants.ENEMY_MOVE_SPEED)
        self.image.fill(color)
        # We need to tell pygame about the image we had it make.
        self.rect = self.image.get_rect()

    def update(self):
        self.calc_grav()
        self.rect.x += self.change_x
        pos = self.rect.x + self.level.world_shift
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
                self.change_x = 1
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right
                self.change_x = -1
            self.jump(self.jumppower)
        self.rect.y += self.change_y
        # Y collision
        # Check and see if we hit anything
        # we can't reuse the list because we have moved since it was made
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
            # Stop our vertical movement
            self.change_y = 0
        player = self.level.player
        if self.change_y == 0:
            if player.rect.x > self.rect.x:
                self.change_x = self.speed
            elif player.rect.x < self.rect.x:
                self.change_x = -self.speed
            if player.rect.y < self.rect.y and self.change_y == 0 and bool(random.getrandbits(1)):
                self.jump(self.jumppower)
            if self.rect.colliderect(player.rect):
                if not player.invul:
                    player.health -= 1
                    player.killcount += 1
                    print(player.health)
                    self.kill()

    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35
        # see if we are on the bottom of the screen.
        if self.rect.y >= constants.SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = constants.SCREEN_HEIGHT - self.rect.height

    def jump(self, power):
        # make sure we have something to jump off of
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= constants.SCREEN_HEIGHT:
            self.change_y = -power
