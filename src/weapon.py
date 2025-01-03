import math

from pygame import Surface
import pygame
from projectile import Projectile, ProjectileController
from utils import load_image


class Weapon:

    def __init__(
        self,
        image_file_path,
        scale,
        player,
        equipped_angle,
        projectile_controller,
        sound_channel,
        intial_pos=[300, 100],
    ):

        self.projectile_controller: ProjectileController = projectile_controller

        self._pos: [float, float] = intial_pos
        self._vY = 0
        self._scale = scale

        from Characters.player import Player

        self._player: Player = player

        self._image = load_image(f"wepons/{image_file_path}", scale)
        self._rect = self._image.get_rect(
            center=(self._pos[0] + scale[0] / 2, self._pos[1] + scale[1] / 2)
        )
        self._rect.width = 30
        self._rect.height = 30

        # Load a sound file
        self.sound_file = "Assets/Sounds/RpgBrust.mp3"
        self.sound_effect = pygame.mixer.Sound(self.sound_file)
        self.sound_channel = sound_channel

        self._equiped = False
        self._float_angle = 0  # When it is not equipped just hovering
        self._angle = 0  # When Equipped by player
        self._equipped_angle = equipped_angle
        self._flip = False  # Flip with the Player

    def is_colliding_with_player(self):
        return self._player.get_rect().colliderect(self._rect)

    def check_equipped(self):

        if self._player.get_wepon() == self and not self._player.get_equipping():
            self._player.set_wepon(None)
            self._equiped = False
            self._angle = 0
            self._pos = [
                self._player.get_rect().center[0],
                self._player.get_rect().center[1] - 30,
            ]

            print("unEquipped")

        if (
            self._player.get_wepon() == None
            and self.is_colliding_with_player()
            and self._player.get_equipping()
        ):
            self._player.set_wepon(self)
            self._equiped = True
            self._angle = self._equipped_angle

            print("Equipped")

    def update(self):

        self.check_equipped()

        if self._equiped:
            self._float_angle = 0
            if self._player.get_flip():
                self._flip = True
                self._pos = [
                    self._player.get_rect().center[0] - 10,
                    self._player.get_rect().center[1] - 10,
                ]
            else:
                self._flip = False
                self._pos = [
                    self._player.get_rect().center[0] - 10,
                    self._player.get_rect().center[1] - 10,
                ]
        else:
            self._float_angle += 1
            self._float_angle %= 360
            self._pos[1] += 0.3 * math.sin(self._float_angle * math.pi / 180)
            self._rect.center = (
                self._pos[0] + self._scale[0] / 2,
                self._pos[1] + self._scale[1] / 2,
            )

    def launch(self):
        missile_angle = (
            180 - self._equipped_angle if self._flip else self._equipped_angle
        )
        missile = Projectile(
            1, "missile.png", (20, 14), missile_angle, self._flip, self._pos
        )
        # missile.setForceY(0)
        # self.sound_channel.play(self.sound_effect)
        self.sound_effect.play()
        self.projectile_controller.addMissile(missile)

    def render(self, screen: Surface, offset):

        # pygame.draw.rect(screen,(255,0,0),(self._rect[0] - offset[0], self._rect[1] - offset[1], self._rect[2], self._rect[3]))

        screen.blit(
            pygame.transform.flip(
                pygame.transform.rotate(self._image, self._angle), self._flip, False
            ),
            (self._pos[0] - offset[0], self._pos[1] - offset[1]),
        )
