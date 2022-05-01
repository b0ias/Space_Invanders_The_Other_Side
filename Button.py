import pygame

class Button:
    def __init__(self, x_pos, y_pos, text_input, font, font_size, base_color, hovering_color):
        self.x_pos = x_pos
        self.y_pos = y_pos

        self.font = font
        self.font_size = font_size
        self.text_input = text_input
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.text = self.font.render(self.text_input, True, "white")
        self.rect = self.text.get_rect(center=(self.x_pos, self.y_pos))  # position where the image will be center

    def update(self, screen):
        self.rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        screen.blit(self.text, self.rect)

    def check_for_input(self, position):
        if (position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top - self.font_size//2, self.rect.bottom + self.font_size//2)):
            return True
        else:
            return False

    def hovering(self, position):
        if (position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom)):
            self.text = self.font.render(f">>> {self.text_input} <<<", True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)