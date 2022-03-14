import pygame

class Button:
    def __init__(self, text, x, y, color, textColor, width):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.textColor = textColor
        self.width = width
        self.height = width

    def draw(self, win, font):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        text = font.render(self.text, 1, self.textColor)
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False