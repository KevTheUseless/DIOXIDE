import os
from const import *
from button import Button

class FolderHierarchy:
    def __init__(self, app, workspace):
        self.app = app
        self.workspace = workspace
        self.data = {}
        self.buttons = []
        def dfs(data, path):
            for item in os.scandir(path):
                if item.is_dir():
                    data[item.name] = {}
                    dfs(data[item.name], item.path)
                else:
                    data[item.name] = None
        dfs(self.data, workspace)
        self.get_buttons(self.data, 0, 150)

    def get_buttons(self, dt, x, y):
        for item in dt:
            self.buttons.append(Button(None, "res/icons/folder_btn_bg.bmp", 0, y, self.app.appID,
                                font=ui_font, content='    ' * x + item, color=(255, 255, 255)))
            if dt[item]:
                y = self.get_buttons(dt[item], x + 1, y + 20)
            else: y += 20
        return y

    def draw(self, screen):
        for btn in self.buttons:
            btn.draw(screen)

    def mouse_down(self, pos, button):
        for btn in self.buttons:
            btn.mouseDown(pos, button, self.app)

    def mouse_up(self, pos, button):
        for btn in self.buttons:
            btn.mouseUp(pos, button)

    def mouse_move(self, pos):
        for btn in self.buttons:
            btn.mouseMove(pos)
