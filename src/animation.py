import pygame


class Animation:
    def __init__(self, images, frame_duration, status=""):
        self.images = images
        self.status = status
        self.frame_duration = frame_duration
        self.image_idx = 0
        self.done = False
        self.animation_duration = len(self.images) * self.frame_duration

    def update(self):
        self.image_idx += 1
        if self.image_idx == self.animation_duration:
            self.done = True
        self.image_idx %= self.animation_duration

    def is_animation_done(self):
        return self.done

    def get_anim_index(self):
        return int(self.image_idx / self.frame_duration)

    def get_image(self):
        return self.images[self.get_anim_index()]
