import pygame, sys, wx, subprocess, re, time, os
from io import TextIOWrapper
from button import Button

# FILE: helpers.py
wapp = wx.App()
frm = wx.Frame(None, -1, '')

def getch():
    # Code from https://blog.csdn.net/damiaomiao666/article/details/50494581
    # by user 小杰666, with minor modifications

    import sys, termios

    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    new = termios.tcgetattr(fd)
    # turn off echo and press-enter
    new[3] = new[3] & ~termios.ECHO & ~termios.ICANON

    try:
        termios.tcsetattr(fd, termios.TCSADRAIN, new)
        sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

def new(self, app):
    # TODO: integrate new file w/ multitabbing
    temp = ""
    flag = 0
    try:
        f = open(app.txtField.fileName)
        temp = f.read()
        f.close()
    except: flag = 1
    if app.txtField.getContents().rstrip() != temp.rstrip(): 
        with wx.MessageDialog(frm, "Do you want to save the changes you made to %s?\nYour changes will be lost if you dont save them." % ("Untitled.cpp" if not app.txtField.fileName else app.txtField.fileName), "DIOXIDE", style=wx.OK|wx.CANCEL) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                if flag: save_as(None, app)
                else: save(None, app)
    app.enableTxtField(150, 160, 110, 40)

def open_file(self, app):
    app.txtField.txtBuffer = [[]]
    with wx.FileDialog(frm, "Open file", wildcard="Any file|*",
                       style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
        if fileDialog.ShowModal() == wx.ID_CANCEL:
            return
        path = fileDialog.GetPath()
        app.txtField.fileName = path
        with open(path, 'r') as fr:
            for ch in fr.read():
                if ch == '\n':
                    app.txtField.txtBuffer.append([])
                else: app.txtField.txtBuffer[-1].append([ch, (255, 255, 255)])
        app.txtField.changeLine(0)
    parse(app.txtField, app.txtField.palette)

def save_as(self, app):
    with wx.FileDialog(frm, "Save As...", wildcard="C++ Source Files (*.cpp)|*.cpp|All Files (*.*)|*.*",
                       style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
        if fileDialog.ShowModal() == wx.ID_CANCEL:
            return
        path = fileDialog.GetPath()
        app.txtField.fileName = path
        with open(path, 'w') as fw:
            s = ''
            for line in app.txtField.txtBuffer:
                for ch, clr in line:
                    s += ch
                s += '\n'
            fw.write(s)

def save(self, app):
    s = ''
    for line in app.txtField.txtBuffer:
        for ch, clr in line:
            s += ch
        s += '\n'
    s = s[:-1]
    if app.txtField.fileName:
        with open(app.txtField.fileName, 'w') as fw:
            fw.write(s)
    else:
        save_as(self, app)

def compile_cpp(self, app):
    if not app.txtField.fileName:
        save_as(self, app)
    else: save(self, app)
    cStats.onCompile(app.txtField.fileName)

def compile_run_cpp(self, app, compileFlags=[]):
    compile_cpp(self, app)
    run_cpp(self, app)

def run_cpp(self, app):
    if not app.txtField.fileName:
        save_as(self, app)
    compileFlags = ['buildsys/run', app.txtField.fileName.rstrip(".cpp")]
    print(compileFlags)
    cmd = " ".join(compileFlags)
    subprocess.run(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)

def get_skin(self, app):
    skin = ''
    with wx.FileDialog(frm, "Choose skin file", wildcard="GENOCIDE skin file (*.gskin)|*.gskin",
                       style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
        if fileDialog.ShowModal() == wx.ID_CANCEL:
            return
        with open(fileDialog.GetPath()) as fr:
            skin = fr.read()
    app.txtField.palette = eval(skin)
    with open("current_skin.gskin", 'w') as fw:
        fw.write(skin)
    skin.close()

    parse(app.txtField, app.txtField.palette)

def judge():
    import judger
    print(judger.judge())

def calc_pos(pos, x, y):
    px, py = pos
    x = max((px - x) // 10, 0)
    y = max((py - y) // 20, 0)
    return x, y

def copy(string):
    from tkinter import Tk
    r = Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(string)
    r.update()
    r.destroy()

def paste():
    from tkinter import Tk
    r = Tk()
    r.withdraw()
    res = r.clipboard_get()
    r.update()
    r.destroy()
    return res


# FILE: regex.py
call = re.compile(r"\b\S+(?=\()")
preproc = re.compile(r"^#\S+\b")
keyword = re.compile(r"\b(break|case|catch|const|const_cast|continue|default|delete|do|dynamic_cast|else|explicit|export|extern|for|friend|goto|if|inline|mutable|namespace|new|operator|private|protected|public|register|reinterpret_cast|return|sizeof|static|static_cast|switch|this|throw|try|typeid|typename|using|virtual|volatile|while)\b")
datatype = re.compile(r"\b(asm|auto|bool|char|double|enum|float|int|long|class|short|signed|struct|template|typedef|union|unsigned|void|wchar_t)\b")
numeral = re.compile(r"\b(true|false|\d+)\b")
literal = re.compile(r"(\"|\').*(\"|\')")
comment = re.compile(r"//.*$")               # nvm about /* */ right now

ex = ["call", "preproc", "keyword", "datatype", "numeral", "literal", "comment"]

def parse(self, palette, lineNum=-1):
    if lineNum < 0:
        for i in range(len(self.txtBuffer)):
            parse(self, palette, i)
    line = ''
    for i, pack in enumerate(self.txtBuffer[lineNum]):
        line += pack[0]
        self.txtBuffer[lineNum][i][1] = (255, 255, 255)
    for expr_name in ex:
        expr = eval(expr_name)
        clr = palette[expr_name]
        for match in expr.finditer(line):
            for i in range(match.start(), match.end()):
                self.txtBuffer[lineNum][i][1] = clr


# FILE: ide.py
class Pic:
    def __init__(self, fileName):
        img = pygame.image.load(fileName)
        self.img = pygame.transform.scale(img, (1280, 720))
        self.x, self.y = 0, 0
        self.w, self.h = self.img.get_size()
    def draw(self, screen, speed = 5):
        screen.blit(self.img, (self.x, self.y), (0, 0, self.w, self.h))
        pygame.draw.rect(screen, (0, 255, 0), (0, 0, speed * 8, 8), 0)
    def getPixelGrid(self, x0, y0, sideLen, pixelGrid):
        n = sideLen // 2
        for y in range(-n, n + 1):
            for x in range(-n, n + 1):
                pixelGrid[y + n][x + n] = self.img.get_at((x + x0, y + y0))

class Framework:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("DIOXIDE")
        self.clock = pygame.time.Clock()
        self.mono = pygame.font.Font("res/JetBrainsMono-Regular.ttf", 18)
        self.speed = 5
        self.mousePos = (0, 0)
        self.apps = []
        self.appID = 0
    def launch(self):
        for app in self.apps:
            app.draw(self.screen)
        cStats.draw(self.screen)
        pygame.display.update()
        self.clock.tick(50)
    def addApp(self, app):
        app.appID = len(self.apps)
        self.apps.append(app)
    def keyUp(self, key):
        self.apps[self.appID].keyUp(key)
    def keyDown(self, key):
        self.apps[self.appID].keyDown(key)
    def mouseDown(self, pos, button):
        self.apps[self.appID].mouseDown(pos, button)
    def mouseUp(self, pos, button):
        self.apps[self.appID].mouseUp(pos, button)
    def mouseMotion(self, pos):
        self.apps[self.appID].mouseMotion(pos)
    def scroll(self, y):
        self.apps[self.appID].scroll(y)

framework = Framework()

class App:
    def __init__(self, picName):
        self.pic = Pic(picName)
        self.appID = 0
        self.btnList = []
        self.tooltipList = []
        self.menus = []
        self.txtField = TxtField(0, 0, 0, 0, self)
        self.txtFieldEnabled = False
        self.cursor_in_txt = False
        self.cursor_img = pygame.image.load("res/cursor.png").convert_alpha()
        self.cursor_rect = self.cursor_img.get_rect()
    def draw(self, screen):
        if framework.appID != self.appID:
            return
        screen.blit(self.pic.img, (0, 0))
        for button in self.btnList:
            button.draw(screen)
        for tooltip in self.tooltipList:
            tooltip.draw(screen)
        for menu in self.menus:
            menu.draw(screen)
        if self.txtFieldEnabled:
            self.txtField.draw(screen)
        pygame.mouse.set_visible(not self.cursor_in_txt)
        if self.cursor_in_txt:
            self.cursor_rect.center = pygame.mouse.get_pos()
            screen.blit(self.cursor_img, self.cursor_rect)
    def addButton(self, b):
        self.btnList.append(b)
    def addTooltip(self, txt, font, x, y, c, rect):
        tt = Tooltip(txt, font, x, y, c, rect)
        self.txtList.append(tt)
    def add_menu(self, menu):
        self.menus.append(menu)
    def enableTxtField(self, x, y, w, h):
        self.txtFieldEnabled = True
        self.txtField = TxtField(x, y, w, h, self)
    def mouseDown(self, pos, button):
        for btn in self.btnList:
            btn.mouseDown(pos, button, self)
        for menu in self.menus:
            menu.mouse_down(pos, button, self)
        self.txtField.mouseDown(pos, button)
    def mouseUp(self, pos, button):
        for button in self.btnList:
            button.mouseUp(pos, button)
        self.txtField.mouseUp(pos, button)
    def mouseMotion(self, pos):
        framework.mousePos = pos
        for btn in self.btnList:
            btn.mouseMove(pos)
        for menu in self.menus:
            menu.mouse_move(pos)
        self.txtField.mouseMotion(pos)
        if 145 <= pos[0] and 150 <= pos[1]:
            self.cursor_in_txt = True
        else: self.cursor_in_txt = False
    def keyUp(self, key):
        if self.txtFieldEnabled:
            self.txtField.keyUp(key)
    def keyDown(self, key):
        if self.txtFieldEnabled:
            self.txtField.keyDown(key)
    def scroll(self, y):
        self.txtField.scroll(y)

class TxtField:
    def __init__(self, x, y, w, h, app):
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.app = app
        self.txtBuffer = [[]]
        # MAGIC #
        self.caps = { '`': '~', '1': '!', '2': '@', '3': '#', '4': '$', '5': '%', '6': '^', '7': '&', '8': '*', '9': '(', '0': ')', '-': '_', '=': '+', '[': '{', ']': '}', '\\': '|', ';': ':', '\'': '"', ',': '<', '.': '>', '/': '?', 'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D', 'e': 'E', 'f': 'F', 'g': 'G', 'h': 'H', 'i': 'I', 'j': 'J', 'k': 'K', 'l': 'L', 'm': 'M', 'n': 'N', 'o': 'O', 'p': 'P', 'q': 'Q', 'r': 'R', 's': 'S', 't': 'T', 'u': 'U', 'v': 'V', 'w': 'W', 'x': 'X', 'y': 'Y', 'z': 'Z' }
        self.shift, self.capsLock, self.ctrl = False, False, False
        self.currentChar, self.loc = 0, 0
        self.lineNum = 0; self.start_y, self.start_x = 0, 0
        self.cLineStr = ""
        self.mono = pygame.font.Font("res/JetBrainsMono-Regular.ttf", 18)

        self.fileName = ""

        self.selecting = False
        self.selection_fixed, self.selection_branch = (), ()
        self.selection_start, self.selection_end = (), ()

        self.autocomplete = {'(': ')', '[': ']', '{': '}'}

        f = open("current_skin.gskin")
        self.palette = eval(f.read())
        f.close()
        
        class Cursor(pygame.sprite.Sprite):
            def __init__(self):
                pygame.sprite.Sprite.__init__(self)

                self.image = pygame.Surface((1, 16))
                self.image.fill(pygame.Color(252, 252, 252))

                self.rect = self.image.get_rect()

        self.cursor = Cursor()
    def getContents(self):
        fileContents = ""
        for line in self.txtBuffer:
            for charPack in line:
                fileContents += charPack[0]
            fileContents += '\n'
        return fileContents
    def get_selection_rects(self):
        if not self.selection_start or not self.selection_end: return []
        start_x, start_y = self.selection_start
        end_x, end_y = self.selection_end
        if start_y < self.start_y:
            start_y = self.start_y
            start_x = self.start_x
        if end_y > self.start_y + self.h:
            end_y = self.start_y + self.h
            end_x = self.start_x + self.w
        start_x = max(start_x, self.start_x)
        end_x = max(min(end_x, self.start_x + self.w), self.start_x)
        span = end_y - start_y
        if span == 0:
            begin_sf = pygame.Surface(((end_x - start_x) * 10, 20))
            begin_sf.fill((120, 120, 120))
            begin = begin_sf.get_rect()
            begin.center = (self.x + (start_x - self.start_x) * 10 + (end_x - start_x) * 5,
                            self.y + (start_y - self.start_y) * 20 + 5)
            return [(begin_sf, begin)]
        elif span == 1:
            begin_sf = pygame.Surface(((self.w + 1 - start_x + self.start_x) * 10, 20))
            begin_sf.fill((120, 120, 120))
            begin = begin_sf.get_rect()
            begin.center = (self.x + (start_x - self.start_x) * 10 + (self.w + 1 - start_x + self.start_x) * 5,
                            self.y + (start_y - self.start_y) * 20 + 5)
            end_sf = pygame.Surface(((end_x - self.start_x) * 10 + 5, 20))
            end_sf.fill((120, 120, 120))
            end = end_sf.get_rect()
            end.center = (self.x + (end_x - self.start_x - 0.5) * 5,
                          self.y + (end_y - self.start_y) * 20 + 5)
            return [(begin_sf, begin), (end_sf, end)]
        else:
            begin_sf = pygame.Surface(((self.w + 1 - start_x + self.start_x) * 10, 20))
            begin_sf.fill((120, 120, 120))
            begin = begin_sf.get_rect()
            begin.center = (self.x + (start_x - self.start_x) * 10 + (self.w + 1 - start_x + self.start_x) * 5,
                            self.y + (start_y - self.start_y) * 20 + 5)
            end_sf = pygame.Surface(((end_x - self.start_x) * 10 + 5, 20))
            end_sf.fill((120, 120, 120))
            end = end_sf.get_rect()
            end.center = (self.x + (end_x - self.start_x - 0.5) * 5,
                          self.y + (end_y - self.start_y) * 20 + 5)
            mid_sf = pygame.Surface((1290 - self.x, 20 * (span - 1)))
            mid_sf.fill((120, 120, 120))
            mid = mid_sf.get_rect()
            mid.center = (1275 - self.w * 5, self.y + (start_y + end_y) * 10 + 5 - self.start_y * 20)
            return [(begin_sf, begin), (end_sf, end), (mid_sf, mid)]
    def get_selection_content(self):
        res = ''
        for i in range(self.selection_start[1], self.selection_end[1] + 1):
            if i == self.selection_start[1]:
                line = self.txtBuffer[i][self.selection_start[0]:self.selection_end[0]] \
                       if self.selection_start[1] == self.selection_end[1] \
                       else self.txtBuffer[i][self.selection_start[0]:]
            elif i == self.selection_end[1]:
                line = self.txtBuffer[i][:self.selection_end[0]]
            else:
                line = self.txtBuffer[i][:]
            for pack in line:
                if pack: res += pack[0]
            if i < self.selection_end[1]:
                res += '\n'
        return res
    def del_selected(self):
        new_line = (self.txtBuffer[self.selection_start[1]][:self.selection_start[0]]
                    + self.txtBuffer[self.selection_end[1]][self.selection_end[0]:])
        del self.txtBuffer[self.selection_start[1]:self.selection_end[1] + 1]
        self.txtBuffer.insert(self.selection_start[1], new_line)
        self.goto(self.selection_start)
        self.selection_fixed = ()
        self.selection_branch = ()
        self.selection_start = ()
        self.selection_end = ()
    def draw(self, screen):
        if pygame.time.get_ticks() % 1000 <= 500: self.cursor.image.fill(pygame.Color(252, 252, 252))
        else: self.cursor.image.fill(pygame.Color(0, 0, 0))

        for sf, rt in self.get_selection_rects():
            screen.blit(sf, rt)

        self.cursor.rect.center = (self.x + (self.loc-self.start_x) * 10,
                                   self.y + (self.lineNum-self.start_y) * 20 + 5)
        screen.blit(self.cursor.image, self.cursor.rect)

        for j, line in enumerate(self.txtBuffer[self.start_y:self.start_y + self.h]):
            for i, ch in enumerate(line[self.start_x:self.start_x + self.w]):
                if ch[0] == '\t':
                    img = self.mono.render(' ', True, ch[1])
                else:
                    img = self.mono.render(ch[0], True, ch[1])
                screen.blit(img, (self.x + i * 10, j * 20 + self.y - 5))

        for i in range(min(len(self.txtBuffer), self.h)):
            screen.blit(self.mono.render(str(i+1+self.start_y), True, (100, 100, 100)),
                        (self.x - len(str(i+self.start_y+1)) * 10 - 15, self.y + i * 20 - 5))
    def keyUp(self, key):
        if key == pygame.K_LSHIFT or key == pygame.K_RSHIFT:
            self.shift = False
        elif key == pygame.K_CAPSLOCK:
            self.capsLock = 1 - self.capsLock
        elif key in (pygame.K_LCTRL, pygame.K_RCTRL):
            self.ctrl = False
    def changeLine(self, l):
        self.lineNum = min(l, len(self.txtBuffer) - 1)
        self.loc = min(self.loc, len(self.txtBuffer[self.lineNum]))
        if self.lineNum < self.start_y:
            self.start_y -= 1
        elif self.lineNum >= self.start_y + self.h:
            self.start_y += 1
    def change_loc(self, nloc):
        self.loc = min(nloc, len(self.txtBuffer[self.lineNum]))
        while self.loc < self.start_x:
            self.start_x -= 1
            time.sleep(.1)
        while self.loc >= self.start_x + self.w:
            self.start_x += 1
            time.sleep(.1)
    def goto(self, *pos):
        if len(pos) == 2:
            x, y = pos
        else:
            x, y = pos[0]
        self.changeLine(y)
        self.change_loc(x)
    def keyDown(self, key):
        if key == pygame.K_BACKSPACE:
            try:
                if self.selection_start and self.selection_end and self.selection_start != self.selection_end:
                    new_line = (self.txtBuffer[self.selection_start[1]][:self.selection_start[0]]
                        + self.txtBuffer[self.selection_end[1]][self.selection_end[0]:])
                    del self.txtBuffer[self.selection_start[1]:self.selection_end[1] + 1]
                    self.txtBuffer.insert(self.selection_start[1], new_line)
                    self.goto(self.selection_start)
                    self.selection_fixed = ()
                    self.selection_branch = ()
                    self.selection_start = ()
                    self.selection_end = ()
                elif self.loc != 0:
                    self.txtBuffer[self.lineNum].pop(self.loc - 1)
                    self.loc -= 1
                elif len(self.txtBuffer) > 1:
                    self.txtBuffer[self.lineNum - 1] += self.txtBuffer.pop(self.lineNum)
                    self.changeLine(self.lineNum - 1)
                    self.loc = len(self.txtBuffer[self.lineNum])
            except: pass
        elif key in (pygame.K_LCTRL, pygame.K_RCTRL):
            self.ctrl = True
        elif key == pygame.K_DELETE:
            try:
                if self.selection_start and self.selection_end and self.selection_start != self.selection_end:
                    new_line = (self.txtBuffer[self.selection_start[1]][:self.selection_start[0]]
                        + self.txtBuffer[self.selection_end[1]][self.selection_end[0]:])
                    del self.txtBuffer[self.selection_start[1]:self.selection_end[1] + 1]
                    self.txtBuffer.insert(self.selection_start[1], new_line)
                    self.goto(self.selection_start)
                    self.selection_fixed = ()
                    self.selection_branch = ()
                    self.selection_start = ()
                    self.selection_end = ()
                elif self.loc != len(self.txtBuffer[self.lineNum]):
                    self.txtBuffer[self.lineNum].pop(self.loc)
                elif len(self.txtBuffer) > 1:
                    self.txtBuffer[self.lineNum] += self.txtBuffer.pop(self.lineNum + 1)
            except: pass
        elif key == pygame.K_RETURN:
            self.txtBuffer[self.lineNum], tmp = \
                self.txtBuffer[self.lineNum][:self.loc], self.txtBuffer[self.lineNum][self.loc:]
            if not tmp:
                for ch, clr in self.txtBuffer[self.lineNum]:
                    if ch != ' ': break
                    tmp.append([ch, (226, 201, 94)])
            self.txtBuffer.insert(self.lineNum + 1, tmp)
            self.lineNum += 1
            self.loc = len(tmp) if tmp and tmp[0][1] == (226, 201, 94) else 0
        elif key == pygame.K_TAB:
            for _ in range(4):
                self.txtBuffer[self.lineNum].insert(self.loc, [' ', (0, 0, 0)])
            self.loc += 4
        elif key == pygame.K_LSHIFT or key == pygame.K_RSHIFT:
            self.shift = True
        elif key == pygame.K_CAPSLOCK:
            self.capsLock = 1 - self.capsLock
        elif key == pygame.K_UP:
            if self.lineNum != 0:
                self.changeLine(self.lineNum - 1)
        elif key == pygame.K_DOWN:
            if self.lineNum != len(self.txtBuffer):
                self.changeLine(self.lineNum + 1)
        elif key == pygame.K_LEFT:
            if self.loc != 0:
                self.change_loc(self.loc - 1)
            elif self.lineNum != 0:
                self.goto(self.lineNum - 1, len(self.txtBuffer[self.lineNum - 1]))
        elif key == pygame.K_RIGHT:
            if self.loc + 1 <= len(self.txtBuffer[self.lineNum]):
                self.change_loc(self.loc + 1)
            elif self.lineNum < len(self.txtBuffer) - 1:
                self.goto(self.lineNum + 1, 0)
        elif self.ctrl:
            if key == ord('s'):
                save(None, self.app)
            if key == ord('c'):
                copy(self.get_selection_content())
            if key == ord('x'):
                copy(self.get_selection_content())
                self.del_selected()
            if key == ord('v'):
                ct = self.lineNum
                i = self.loc
                for ch in paste():
                    if ch == '\n':
                        parse(self, self.palette, self.lineNum)
                        ct += 1
                        i = 0
                        continue
                    self.txtBuffer[ct].insert(i, [ch, (255, 255, 255)])
                    i += 1
                self.goto(i, ct)
        elif (not (self.shift or self.capsLock)) and (32 <= key <= 126) and (chr(key) in self.autocomplete):
            self.txtBuffer[self.lineNum].insert(self.loc, [chr(key), (255, 255, 255)])
            self.txtBuffer[self.lineNum].insert(self.loc + 1, [self.autocomplete[chr(key)], (255, 255, 255)])
            self.loc += 1
        elif (self.shift or self.capsLock) and (32 <= key <= 126) and (self.caps[chr(key)] in self.autocomplete):
            self.txtBuffer[self.lineNum].insert(self.loc, [self.caps[chr(key)], (255, 255, 255)])
            self.txtBuffer[self.lineNum].insert(self.loc + 1, [self.autocomplete[self.caps[chr(key)]], (255, 255, 255)])
            self.loc += 1
        elif (((not (self.shift or self.capsLock)) and (32 <= key <= 126) and chr(key) in self.autocomplete.values()) \
            or ((self.shift or self.capsLock) and (self.caps[chr(key)] in self.autocomplete.values()))) \
            and self.loc != len(self.txtBuffer[self.lineNum]) and self.txtBuffer[self.lineNum][self.loc][0] == (self.caps[chr(key)] if self.shift or self.capsLock else chr(key)):
            self.loc += 1
        else:
            if 32 <= key <= 126:
                if self.selection_start and self.selection_end and self.selection_start != self.selection_end:
                    new_line = (self.txtBuffer[self.selection_start[1]][:self.selection_start[0]]
                        + self.txtBuffer[self.selection_end[1]][self.selection_end[0]:])
                    del self.txtBuffer[self.selection_start[1]:self.selection_end[1] + 1]
                    self.txtBuffer.insert(self.selection_start[1], new_line)
                    self.goto(self.selection_start)
                    self.selection_fixed = ()
                    self.selection_branch = ()
                    self.selection_start = ()
                    self.selection_end = ()
                if (key == 39 or 44 <= key <= 57 or key == 59 or key == 61 or key == 96 or 91 <= key <= 93) and self.shift:
                    self.txtBuffer[self.lineNum].insert(self.loc, [self.caps[chr(key)], (255, 255, 255)])
                elif 97 <= key <= 122 and (self.shift or self.capsLock):
                    self.txtBuffer[self.lineNum].insert(self.loc, [self.caps[chr(key)], (255, 255, 255)])
                else:
                    self.txtBuffer[self.lineNum].insert(self.loc, [chr(key), (255, 255, 255)])
                self.loc += 1
        parse(self, self.palette, self.lineNum)
    def mouseDown(self, pos, button):
        if pos[0] < self.x - 5:
            self.loc = 0
            return
        if pos[1] < self.y - 1: return
        x, y = calc_pos(pos, self.x, self.y)
        x += self.start_x
        y += self.start_y
        self.goto(x, y)
        if pos[0] >= self.x - 5 and pos[1] >= self.y - 1:
            self.selecting = True
            self.selection_fixed = (self.loc, self.lineNum)
            self.selection_branch = (self.loc, self.lineNum)
            self.selection_start = (self.loc, self.lineNum)
            self.selection_end = (self.loc, self.lineNum)
    def mouseUp(self, pos, button):
        if pos[0] >= self.x - 5 and pos[1] >= self.y - 1:
            self.selecting = False
            if self.selection_fixed == self.selection_branch:
                self.selection_fixed = ()
                self.selection_branch = ()
                self.selection_start = ()
                self.selection_end = ()
    def mouseMotion(self, pos):
        if not self.selecting: return
        try: x, y = calc_pos(pos, self.x, self.y)
        except: return
        x += self.start_x
        y += self.start_y
        self.goto(x, y)
        self.selection_branch = (self.loc, self.lineNum)
        if (self.lineNum < self.selection_fixed[1]) \
            or (self.lineNum == self.selection_fixed[1] and self.loc < self.selection_fixed[0]):
            self.selection_start, self.selection_end = self.selection_branch, self.selection_fixed
        else:
            self.selection_start, self.selection_end = self.selection_fixed, self.selection_branch
    def scroll(self, y):
        self.start_y -= y
        self.start_y = max(min(self.start_y, len(self.txtBuffer)), 0)

class CompileStats:
    def __init__(self):
        self.x, self.y = 5, 440
        self.w, self.h = 35, 20           # in characters
        self.msg, self.tmp_msg = "", ""
        self.wait = 0
    def onCompile(self, filename):
        cmd = ("compilers/MinGW/bin/gcc" if os.name == "nt" else "gcc") + " -dumpversion"
        compilerVer = subprocess.run(cmd, capture_output=True).stdout.decode('utf-8')

        cmd = ("compilers/MinGW/bin/gcc" if os.name == "nt" else "gcc") + " -dumpmachine"
        compilerBuild = subprocess.run(cmd, capture_output=True).stdout.decode('utf-8')

        compilerName = ("MinGW " if "mingw" in compilerBuild else "") + "GCC " + compilerVer
        self.msg = "Compiling...\n--------\n- Filename: %s\n- Compiler Name: %s\n \nCompilation results..." % (ide.txtField.fileName, compilerName)
        
        compileFlags = ['buildsys/build', filename.rstrip(".cpp")]
        cmd = " ".join(compileFlags)
        self.tmp_msg = subprocess.run(cmd, capture_output=True).stderr.decode('utf-8')
        if not self.tmp_msg:
            self.tmp_msg = self.msg + "\n--------\n- Output Filename: %s\n- Output Size: %f KiB" % \
                (ide.txtField.fileName.rstrip(".cpp") + ".exe" if os.name == "nt" else "", \
                os.stat(ide.txtField.fileName.rstrip(".cpp") + ".exe" if os.name == "nt" else "").st_size / 1024)
        self.wait = 1

    def draw(self, screen):
        if self.wait: self.wait += 1
        if self.wait == 50:
            self.wait = 0
            self.msg = self.tmp_msg
        compileFnt = pygame.font.Font("res/cour.ttf", 16)
        y = 0
        for line in self.msg.split("\n"):
            for i in range(0, len(line), self.w):
                for j, ch in enumerate(line[i : i + self.w]):
                    try:
                        img = compileFnt.render(ch, True, (255, 255, 255))
                        screen.blit(img, (j * 8 + self.x, y + self.y))
                    except pygame.error:
                        pass
                y += 20

class JudgeResults:
    def __init__(self):
        self.x, self.y = 5, 440
        self.w, self.h = 35, 20           # in characters
        self.msg, self.tmp_msg = "", ""
        self.wait = 0
    def onCompile(self, filename):
        cmd = ("compilers/MinGW/bin/gcc" if os.name == "nt" else "gcc") + " -dumpversion"
        compilerVer = subprocess.run(cmd, capture_output=True).stdout.decode('utf-8')

        cmd = ("compilers/MinGW/bin/gcc" if os.name == "nt" else "gcc") + " -dumpmachine"
        compilerBuild = subprocess.run(cmd, capture_output=True).stdout.decode('utf-8')

        compilerName = ("MinGW " if "mingw" in compilerBuild else "") + "GCC " + compilerVer
        self.msg = "Compiling...\n--------\n- Filename: %s\n- Compiler Name: %s\n \nCompilation results..." % (ide.txtField.fileName, compilerName)
        
        compileFlags = ['buildsys/build', filename.rstrip(".cpp")]
        cmd = " ".join(compileFlags)
        self.tmp_msg = subprocess.run(cmd, capture_output=True).stderr.decode('utf-8')
        if not self.tmp_msg:
            self.tmp_msg = self.msg + "\n--------\n- Output Filename: %s\n- Output Size: %f KiB" % \
                (ide.txtField.fileName.rstrip(".cpp") + ".exe" if os.name == "nt" else "", \
                os.stat(ide.txtField.fileName.rstrip(".cpp") + ".exe" if os.name == "nt" else "").st_size / 1024)
        self.wait = 1

    def draw(self, screen):
        if self.wait: self.wait += 1
        if self.wait == 50:
            self.wait = 0
            self.msg = self.tmp_msg
        compileFnt = pygame.font.Font("res/cour.ttf", 16)
        y = 0
        for line in self.msg.split("\n"):
            for i in range(0, len(line), self.w):
                for j, ch in enumerate(line[i : i + self.w]):
                    try:
                        img = compileFnt.render(ch, True, (255, 255, 255))
                        screen.blit(img, (j * 8 + self.x, y + self.y))
                    except pygame.error:
                        pass
                y += 20

ide = App("res/bg.jpg")
new_btn = Button("res/icons/new.png", "res/icons/btn_bg.bmp", 320, 45, ide.appID)
new_btn.onClick = new

open_btn = Button("res/icons/open.png", "res/icons/btn_bg.bmp", 370, 45, ide.appID)
open_btn.onClick = open_file

save_btn = Button("res/icons/save.png", "res/icons/btn_bg.bmp", 420, 45, ide.appID)
save_btn.onClick = save

save_as_btn = Button("res/icons/save_as.png", "res/icons/btn_bg.bmp", 470, 45, ide.appID)
save_as_btn.onClick = save_as

compile_btn = Button("res/icons/compile.png", "res/icons/btn_bg.bmp", 520, 45, ide.appID)
compile_btn.onClick = compile_cpp

run_btn = Button("res/icons/run.png", "res/icons/btn_bg.bmp", 570, 45, ide.appID)
run_btn.onClick = run_cpp

compile_run_btn = Button("res/icons/compile_run.png", "res/icons/btn_bg.bmp", 620, 45, ide.appID)
compile_run_btn.onClick = compile_run_cpp

skin_btn = Button("res/icons/skin.png", "res/icons/btn_bg.bmp", 670, 45, ide.appID)
skin_btn.onClick = get_skin

judge_btn = Button("res/icons/judge.png", "res/icons/btn_bg.bmp", 720, 45, ide.appID)

ide.addButton(new_btn)
ide.addButton(open_btn)

ide.addButton(save_btn)
ide.addButton(save_as_btn)
ide.addButton(compile_btn)
ide.addButton(run_btn)
ide.addButton(compile_run_btn)
ide.addButton(skin_btn)

ide.addButton(judge_btn)

framework.appID = ide.appID
framework.addApp(ide)
ide.enableTxtField(340, 190, 93, 27)
cStats = CompileStats()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            temp = ""
            flag = 0
            try:
                f = open(ide.txtField.fileName)
                temp = f.read()
                f.close()
            except: flag = 1
            if ide.txtField.getContents().rstrip() != temp.rstrip(): 
                with wx.MessageDialog(frm, "Do you want to save the changes you made to %s?\nYour changes will be lost if you dont save them." % ("Untitled.cpp" if not ide.txtField.fileName else ide.txtField.fileName), "DIOXIDE", style=wx.OK|wx.CANCEL) as dlg:
                    if dlg.ShowModal() == wx.ID_OK:
                        if flag: save_as(None, ide)
                        else: save(None, ide)
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            framework.keyDown(event.key)
        elif event.type == pygame.KEYUP:
            framework.keyUp(event.key)
        elif event.type == pygame.MOUSEWHEEL:
            framework.scroll(event.y)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            framework.mouseDown(event.pos, event.button)
        elif event.type == pygame.MOUSEBUTTONUP:
            framework.mouseUp(event.pos, event.button)
        elif event.type == pygame.MOUSEMOTION:
            framework.mouseMotion(event.pos)
    framework.launch()
