from button import MenuButton, DropdownButton

class Menu:
    def __init__(self, structure, start_x, start_y, font):
        self.structure = structure
        self.font = font
        self.start_x, self.start_y = start_x, start_y
        self.start_btn = MenuButton(list(structure.keys())[0], font, start_x, start_y)
        self.start_btn.onClick = lambda a, b: self.show_substructure(start_x, start_y + 16, ((list(structure.keys())[0]), ))
        self.btns = [self.start_btn]
    def show_until(self, x, y, args):
        a = self.structure
        self.btns = [self.start_btn]
        self.btns[-1].onClick = lambda a, b: self.show_substructure(x, y - 26, args)
        if not args[:-1]: return
        for k in args[:-1]:
            a = a[k]

        for key, item in a.items():
            self.btns.append(DropdownButton(key, self.font, x, y))
            self.btns[-1].onClick = item if type(item) != dict else lambda a, b: self.show_substructure(x + 307, y, args + (key,))
            y += 26
    def show_substructure(self, x, y, args: tuple):
        a = self.structure
        self.tmp = []
        self.btns = [self.start_btn]
        for k in args:
            a = a[k]

        self.btns[-1].onClick = lambda a, b: self.show_until(x, y, args)
        for key, item in a.items():
            self.btns.append(DropdownButton(key, self.font, x, y))
            self.btns[-1].onClick = item if type(item) != dict else lambda a, b: self.show_substructure(x + 307, y, args + (key,))
            y += 26
    def draw(self, screen):
        for btn in self.btns:
            btn.draw(screen)
    def mouse_move(self, pos):
        for btn in self.btns:
            btn.mouseMove(pos)
    def mouse_down(self, pos, btn, app):
        for btn in self.btns:
            btn.mouseDown(pos, btn, app)
