import pygame


class HandleKeyBoardInput:
    __old__button_input = {}

    @staticmethod
    def is_pressed(key_num):
        keys = pygame.key.get_pressed()
        if key_num not in HandleKeyBoardInput.__old__button_input:
            HandleKeyBoardInput.__old__button_input[key_num] = False

        return (
            HandleKeyBoardInput.__old__button_input[key_num] != keys[key_num]
            and keys[key_num]
        )

    @staticmethod
    def updated_old_button_input_list(num_list):
        keys = pygame.key.get_pressed()
        for key_num in num_list:
            if key_num in HandleKeyBoardInput.__old__button_input:
                HandleKeyBoardInput.__old__button_input[key_num] = keys[key_num]
