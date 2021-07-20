import pygame

class Button:
    def __init__(self, picFile, bg, x, y, appID, **txt):
        if picFile:
            self.img = pygame.image.load(picFile).convert_alpha()
        else:
            self.img = None
        self.bg = pygame.image.load(bg).convert()
        self.w, self.h = self.bg.get_width() // 3, self.bg.get_height()
        self.x, self.y = x, y
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.status = 0
        self.appID = appID
        self.txt = txt
        self.onClick = None
    def draw(self, screen):
        screen.blit(self.bg, (self.x, self.y),
                    (self.status * self.rect.w, 0,
                     self.rect.w, self.rect.h))
        if self.img:
            screen.blit(self.img, (self.x + 8, self.y + 8))
        if self.txt:
            screen.blit(self.txt["font"].render(self.txt["content"], True, (0, 0, 0) if "color" not in self.txt.keys() else self.txt["color"]), \
                        (self.x + 10, self.y + self.h // 2 - 8))
    def mouseDown(self, pos, button, app):
        if self.rect.collidepoint(pos):
            self.status = 2
            self.onClick(self, app)
    def mouseUp(self, pos, button):
        self.status = 0
        if not self.rect.collidepoint(pos):
            return
        #framework.apps[self.appID].pic.draw(framework.screen, framework.speed)
        #framework.appID = self.appID
    def mouseMove(self, pos):
        if self.rect.collidepoint(pos):
            self.status = 1
        else:
            self.status = 0

"""
class MenuButton(Button):
    def __init__(self, txt, font, x, y, bg='res/icons/menu_btn_bg.bmp'):
        super().__init__(None, bg, x, y, 0, font=font, content=txt)

class DropdownButton(Button):
    def __init__(self, txt, font, x, y, with_subitem=False, bg=None):
        super().__init__(None, bg if bg else ("res/icons/dropdown_btn_bg.bmp" if not with_subitem else "res/icons/dropdown_btn_bg_w_sub.bmp"), x, y, 0, font=font, content=txt)
"""
