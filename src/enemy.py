import pygame
from animation import Animation
from utils import load_image, load_images
import random
from settings import SCALE, TILE_SIZE


class Enemy:
    def __init__(self, speedx, gravity, intial_pos, tileMap):
        self.speedX = speedx
        self.speedY = 0
        self.tileMap = tileMap
        self.gravity = gravity
        self.dir = [1, 0]
        self.collision = {"down": 0, "top": 0, "left": 0, "right": 0}

        # animation
        self.flip = False
        self.scale = (16, 20)
        self.Animations = {
            "idle": Animation(load_images("Enemy/idle", self.scale), 10, "idle"),
            "run": Animation(load_images("Enemy/run", self.scale), 5, "run"),
        }

        self.currAnimation = self.Animations["idle"]
        self.image = self.currAnimation.get_image()
        self.rect = self.image.get_rect(center=intial_pos)

        self.changeDirCnt = 0

    def getAnimation(self):
        newAnim = ""

        if self.dir[0] == 0:
            newAnim = "idle"
        else:
            newAnim = "run"

        if newAnim == self.currAnimation.status:
            self.currAnimation.update()
        else:
            self.currAnimation.image_idx = 0
            self.currAnimation = self.Animations[newAnim]

        self.image = self.currAnimation.get_image()

    def update(self):
        self.collision = {"down": 0, "top": 0, "left": 0, "right": 0}

        self.changeDirCnt += 1

        if self.changeDirCnt >= 180:
            self.changeDirCnt = 0
            self.dir[0] = random.randint(-1, 1)

        if self.dir[0] == -1:
            self.flip = True
        elif self.dir[0] == 1:
            self.flip = False

        self.rect.x += self.dir[0] * self.speedX

        for rect in self.tileMap.get_around_tiles(self.rect.center):
            if self.rect.colliderect(rect):
                if self.dir[0] == 1:
                    self.collision["right"] = 1
                    self.rect.right = rect.left
                if self.dir[0] == -1:
                    self.collision["left"] = 1
                    self.rect.left = rect.right

        self.rect.y += self.speedY
        colRect = pygame.rect.Rect(self.rect)
        if self.speedY < 0.5 and self.speedY >= 0:
            colRect.y += 1

        for rect in self.tileMap.get_around_tiles(self.rect.center):
            if colRect.colliderect(rect):
                if self.speedY >= 0:
                    self.collision["down"] = 1
                    colRect.bottom = rect.top
                if self.speedY < 0:
                    self.collision["top"] = 1
                    colRect.top = rect.bottom
                self.rect = colRect
                self.speedY = 0

        if not self.collision["down"]:
            self.speedY += self.gravity
            self.speedY = min(9, self.speedY)

        self.getAnimation()

    def render(self, screen, offset):
        screen.blit(
            pygame.transform.flip(self.image, self.flip, False),
            (self.rect.x - offset[0], self.rect.y - offset[1]),
        )
