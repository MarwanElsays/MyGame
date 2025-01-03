import pygame
from animation import Animation
from utils import SpriteSheet, load_images
from settings import PSCALE, SCALE, GRAVITY
from weapon import Weapon


class Knight:
    def __init__(self, speedx, tile_map):
        self.__speedX, self.__speedY = speedx, 0
        self.__tile_map = tile_map
        self.__gravity = GRAVITY
        self.__dir = [0, 0]
        self.__collision = {
            "down": 0,
            "top": 0,
            "left": 0,
            "right": 0,
        }  # down,top,left,right

        # health
        self.__MAXHEALTH = 100
        self.__health = self.__MAXHEALTH / 2

        # Jumps
        self.__MAXJUMPS = 2
        self.__jumps = self.__MAXJUMPS
        self.__can_jump = True

        # animation
        self.__flip = False
        self.__scale = (PSCALE, PSCALE)
        self.__knight_idle_sheet = SpriteSheet(
            "knight/knightIdle.png", "jsonImages/knight.json", "#71664f", self.__scale
        )
        self.__knight_attack_sheet = SpriteSheet(
            "knight/knightAttack.png", "jsonImages/knight.json", "#71664f", self.__scale
        )
        self.__knight_run_sheet = SpriteSheet(
            "knight/knightRun.png", "jsonImages/knight.json", "#71664f", self.__scale
        )
        self.__animations = {
            "idle": Animation(
                self.__knight_idle_sheet.get_sprite_images("knightIdle"), 6, "idle"
            ),
            "attack": Animation(
                self.__knight_attack_sheet.get_sprite_images("knightAttack"),
                6,
                "attack",
            ),
            "run": Animation(
                self.__knight_run_sheet.get_sprite_images("knightRun"), 4, "run"
            ),
        }

        self.__curr_animation = self.__animations["idle"]
        self.__image = self.__curr_animation.get_image()
        self.__rect = self.__image[0].get_rect(bottomleft=(300, 200))

        # Wall sldie
        self.__WALLSLIDESPEED = 2

        # climb
        self.__CLIMBSPEED = -4
        self.__can_climb = False

        # Wepon
        self.__wepon: Weapon = None
        self.__equipping = False

        # for debugging
        self.col = self.__rect

        self.colcnt = 0

    def get_wepon(self) -> Weapon:
        return self.__wepon

    def get_health(self):
        return self.__health

    def get_flip(self):
        return self.__flip

    def get_rect(self):
        return self.__rect

    def get_equipping(self):
        return self.__equipping

    def set_equipping(self, equipping):
        self.__equipping = equipping

    def set_wepon(self, wepon):
        self.__wepon = wepon

    def get_input(self):

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.__dir[0] = 1
            self.__flip = False
        elif keys[pygame.K_LEFT]:
            self.__dir[0] = -1
            self.__flip = True
        else:
            self.__dir[0] = 0

        if keys[pygame.K_UP]:
            self.__can_climb = True
        else:
            self.__can_climb = False

        if keys[pygame.K_SPACE] and self.__jumps > 0 and self.__can_jump:
            self.__speedY = -6 * PSCALE
            self.__collision["down"] = 0
            self.__jumps -= 1
            self.__can_jump = False

        if not keys[pygame.K_SPACE]:
            self.__can_jump = True

    def launch_missile(self):
        if self.__wepon is not None:
            self.__wepon.launch()

    def anim_move(self, anim):
        if anim == "attack":
            if self.__curr_animation.get_anim_index() in [14, 15, 16]:
                self.__rect.x += -1 if self.__flip else 1

    def get_animation(self):

        new_anim = ""
        if not self.__collision["down"]:
            if any([self.__collision["left"], self.__collision["right"]]):
                if self.__can_climb:
                    new_anim = "idle"  # need to add climb animation
                else:
                    if self.__speedY > 0:
                        new_anim = "idle"
                    else:
                        new_anim = "idle"
            else:
                new_anim = "idle"
        elif self.__dir[0] == 0:
            new_anim = "idle"
        else:
            new_anim = "run"

        if new_anim == self.__curr_animation.status:
            self.__curr_animation.update()

            new_img = self.__curr_animation.get_image()
            new_rect = new_img[0].get_rect()

            # self.anim_move(new_anim)
            if self.__image != new_img:
                self.__rect.y = self.__rect.y - (new_rect.h - self.__rect.h)
                self.__rect.h = new_rect.h
        else:
            self.__curr_animation.image_idx = 0
            self.__curr_animation = self.__animations[new_anim]

        self.__image = self.__curr_animation.get_image()
        if new_anim == "run":
            self.__rect.w = 26
        else:
            self.__rect.w = 36

    def check_collisions(self, direction):

        if direction == "horizontal":
            for rect in self.__tile_map.get_around_tiles(self.__rect.center):
                if self.__rect.colliderect(rect):
                    if self.__dir[0] == 1:
                        self.__collision["right"] = 1
                        self.__rect.right = rect.left
                    if self.__dir[0] == -1:
                        self.__collision["left"] = 1
                        self.__rect.left = rect.right
                    self.col = rect

        elif direction == "vertical":
            for rect in self.__tile_map.get_around_tiles(self.__rect.center):
                if self.__rect.colliderect(rect):
                    self.colcnt += 1
                    if self.__speedY >= 0:
                        # print("tile   ",rect)
                        # print("my_rect",self.__rect)
                        self.__collision["down"] = 1
                        self.__rect.bottom = rect.top
                    if self.__speedY < 0:
                        # print(self.__speedY)
                        self.__collision["top"] = 1
                        self.__rect.top = rect.bottom
                    self.__speedY = 1

    def handle_collision(self):
        if self.__collision["top"]:  # upWall bounce
            self.__speedY += 2

        if self.__collision["left"] or self.__collision["right"]:
            if self.__speedY > 0:  # handle wall slide
                self.__speedY = (
                    self.__WALLSLIDESPEED
                )  # he can jump of wall when sliding

            if self.__can_climb:
                self.__speedY = self.__CLIMBSPEED
                self.__jumps = 0  # prevent player from jumping when climbing
        else:
            self.__can_climb = (
                False  # if player is not on left or right Wall then he cant climb
            )

        if self.__collision["down"]:
            self.__jumps = self.__MAXJUMPS
            self.__speedY, self.__can_climb = (
                1,
                False,
            )  # prevent player from climbing when on ground
        elif not self.__can_climb:
            self.__speedY += self.__gravity
            self.__speedY = min(9 * PSCALE, self.__speedY)

    def update(self):
        prev_col = self.__collision
        self.__collision = {"down": 0, "top": 0, "left": 0, "right": 0}

        self.get_input()

        self.__rect.x += self.__dir[0] * self.__speedX
        self.check_collisions("horizontal")

        self.__rect.y += self.__speedY
        self.check_collisions("vertical")

        self.handle_collision()

        self.get_animation()
        self.check_collisions("vertical")
        # self.handle_collision()

    def render(self, screen, offset):

        # self.debug_rect(screen,offset)
        # print("my rect: ",self.__rect)
        # print("img_rect: ",self.__image[0].get_rect())
        # self.col_rect(screen,offset)
        img_offset = 0
        if self.__flip:
            img_offset = -(self.__image[0].get_rect().w - 35) + self.__image[1] * PSCALE
            if self.__curr_animation.status == "run":
                img_offset -= self.__image[2]
        else:
            img_offset = -self.__image[1] * PSCALE

        screen.blit(
            pygame.transform.flip(self.__image[0], self.__flip, False),
            (self.__rect.x - offset[0] + img_offset, self.__rect.y - offset[1]),
        )

    def debug_rect(self, screen, offset):
        pygame.draw.rect(
            screen,
            "#FF0000",
            pygame.Rect(
                self.__rect.x - offset[0],
                self.__rect.y - offset[1],
                self.__rect.w,
                self.__rect.h,
            ),
        )

    def col_rect(self, screen, offset):
        pygame.draw.rect(
            screen,
            "#00FF00",
            pygame.Rect(
                self.col.x - offset[0], self.col.y - offset[1], self.col.w, self.col.h
            ),
        )
