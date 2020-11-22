import pygame, sys, wx
wapp = wx.App()
frm = wx.Frame(None, -1, '')

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

class Button:
	def __init__(self, picFile, bg, x, y, appID, **txt):
		self.img = pygame.image.load(picFile).convert()
		self.bg = pygame.image.load(bg).convert()
		self.w, self.h = self.bg.get_width() // 3, self.bg.get_height()
		self.x, self.y = x, y
		self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
		self.status = 0
		self.appID = appID
		self.txt = txt

	def draw(self, screen):
		screen.blit(self.bg, (self.x, self.y),
					(self.status * self.rect.w, 0,
					 self.rect.w, self.rect.h))
		screen.blit(self.img, (self.x + 8, self.y + 8))
		if self.txt:
			screen.blit(self.txt["font"].render(self.txt["content"], True, (0,0,0)), \
						(self.x + self.w // 2 - 4 * len(self.txt["content"]), self.y + self.h // 2 - 8))
	def onClick(self, app):
		pass
	def mouseDown(self, pos, button, app):
		if self.rect.collidepoint(pos):
			self.status = 2
			self.onClick(self, app)
	def mouseUp(self, pos, button):
		self.status = 0
		if not self.rect.collidepoint(pos):
			return
		framework.apps[self.appID].pic.draw(framework.screen, framework.speed)
		framework.appID = self.appID
	def mouseMove(self, pos):
		if self.rect.collidepoint(pos):
			self.status = 1
		else:
			self.status = 0

class Framework:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((1280, 720))
		pygame.display.set_caption("GENOCIDE")
		self.clock = pygame.time.Clock()
		self.mono = pygame.font.Font("res/JetBrainsMono-Regular.ttf", 18)
		self.speed = 5
		self.mousePos = (0, 0)
		self.apps = []
		self.appID = 0
	def launch(self):
		for app in self.apps:
			app.draw(self.screen)
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

class App:
	def __init__(self, picName):
		self.pic = Pic(picName)
		self.appID = 0
		self.btnList = []
		self.tooltipList = []
		self.txtField = TxtField(0, 0, 0, 0)
		self.txtFieldEnabled = False
	def draw(self, screen):
		if framework.appID != self.appID:
			return
		screen.blit(self.pic.img, (0, 0))
		for button in self.btnList:
			button.draw(screen)
		for tooltip in self.tooltipList:
			tooltip.draw(screen)
		if self.txtFieldEnabled:
			self.txtField.content = self.txtField.wrap(self.txtField.txtBuffer)
			self.txtField.content = self.txtField.content[-self.txtField.h:]
			self.txtField.draw(screen, self.txtField.content, self.txtField.y)
	def addButton(self, b):
		self.btnList.append(b)
	def addTooltip(self, txt, font, x, y, c, rect):
		tt = Tooltip(txt, font, x, y, c, rect)
		self.txtList.append(tt)
	def enableTxtField(self, x, y, w, h):
		self.txtFieldEnabled = True
		self.txtField.x, self.txtField.y = x, y
		self.txtField.w, self.txtField.h = w, h
	def mouseDown(self, pos, button):
		for btn in self.btnList:
			btn.mouseDown(pos, button, self)
	def mouseUp(self, pos, button):
		for button in self.btnList:
			button.mouseUp(pos, button)
	def mouseMotion(self, pos):
		framework.mousePos = pos
		for btn in self.btnList:
			btn.mouseMove(pos)
	def keyUp(self, key):
		if self.txtFieldEnabled:
			self.txtField.keyUp(key)
	def keyDown(self, key):
		if self.txtFieldEnabled:
			self.txtField.keyDown(key)

class TxtField:
	def __init__(self, x, y, w, h):
		self.x, self.y = x, y
		self.w, self.h = w, h
		self.txtBuffer = []
		self.content = []
		# MAGIC #
		self.caps = { '`': '~', '1': '!', '2': '@', '3': '#', '4': '$', '5': '%', '6': '^', '7': '&', '8': '*', '9': '(', '0': ')', '-': '_', '=': '+', '[': '{', ']': '}', '\\': '|', ';': ':', '\'': '"', ',': '<', '.': '>', '/': '?', 'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D', 'e': 'E', 'f': 'F', 'g': 'G', 'h': 'H', 'i': 'I', 'j': 'J', 'k': 'K', 'l': 'L', 'm': 'M', 'n': 'N', 'o': 'O', 'p': 'P', 'q': 'Q', 'r': 'R', 's': 'S', 't': 'T', 'u': 'U', 'v': 'V', 'w': 'W', 'x': 'X', 'y': 'Y', 'z': 'Z' }
		self.shift, self.capsLock = False, False
		self.currentChar, self.loc, self.maxIndex = 0, 0, 0
		self.lineNum = 0; self.maxLine = 0
		self.cLineStr = ""
		self.mono = pygame.font.Font("res/JetBrainsMono-Regular.ttf", 18)

		self.fileName = ''
		
		class Cursor(pygame.sprite.Sprite):
			def __init__(self):
				pygame.sprite.Sprite.__init__(self)

				self.image = pygame.Surface((2, 16))
				self.image.fill(pygame.Color(252, 252, 252))

				self.rect = self.image.get_rect()

		self.cursor = Cursor()
		self.frame = 0
	def wrap(self, txtBuffer):
		self.frame += 1
		lines = []
		ptr = 0
		prev_i = 0
		ph = []
		if self.loc > self.maxIndex:
			self.loc = self.maxIndex
		if self.loc < 0: self.loc = 0
		if self.maxIndex < 0: self.loc = 0
		for i in range(len(txtBuffer)):
			if txtBuffer[i][0] == '\n':
				self.currentChar = i + 1
				lines.append([])
				for ch, clr in ph:
					lines[-1].append((ch, clr))
				ptr += 1
				ph = []
				prev_i = i
			elif txtBuffer[i][0] == '\r' or (i != 0 and (i - prev_i) % self.w == 0):
				ph += txtBuffer[i] if txtBuffer[i][0] not in ('\n', '\r', ' ', '') else ''
				self.currentChar = i + 1
				lines.append(ph)
				ph = ''
				prev_i = i
			elif txtBuffer[i][0] == '\t':
				for _ in range(4): ph.append((' ', (0, 0, 0)))
			else:
				ph.append(txtBuffer[i])
		lines.append(ph)
		return lines
	def draw(self, screen, lines, y = 0):
		for line in lines:
			for i, ch in enumerate(line):
				img = self.mono.render(ch[0], True, ch[1])
				screen.blit(img, (self.x + i * 9, y))
			y += 16

		if self.frame % 50 <= 25: self.cursor.image.fill(pygame.Color(252, 252, 252))
		else: self.cursor.image.fill(pygame.Color(0, 0, 0))

		lines = 0
		for elem in self.txtBuffer:
			if elem[0] in ('\r', '\n'):
				lines += 1
		if lines > 39: lines = 39

		self.cursor.rect.center = (self.x + (self.loc - 1) * 9 + 12,
								   self.y + self.lineNum * 16 + 10)
		screen.blit(self.cursor.image, self.cursor.rect)
	def keyUp(self, key):
		if key == pygame.K_LSHIFT or key == pygame.K_RSHIFT:
			self.shift = False
		elif key == pygame.K_CAPSLOCK:
			self.capsLock = 1 - self.capsLock
	def changeLine(self, l):
		s = ''
		for ch, clr in self.txtBuffer:
			s += ch
		self.lineNum = l
		self.maxIndex = len(s.split('\n')[l])
		self.loc = min(self.loc, self.maxIndex)
	def keyDown(self, key):
		i = 0; ct = 0
		for ch, clr in self.txtBuffer:
			if i == self.lineNum: break
			ct += 1
			if ch == '\n': i += 1
		if key == pygame.K_BACKSPACE:
			try:
				self.txtBuffer.pop(ct + self.loc - 1)
				if self.loc - 1 != -1:
					self.maxIndex -= 1
					self.loc -= 1
				else:
					self.changeLine(self.lineNum - 1)
					self.loc = self.maxIndex
					self.maxLine -= 1
			except: pass
		elif key == pygame.K_DELETE:
			try:
				if self.loc > self.maxIndex:
					self.loc = self.maxIndex
				self.txtBuffer.pop(ct + self.loc)
				self.maxIndex -= 1
			except: pass
		elif key == pygame.K_RETURN:
			cmd = ''
			self.loc = 0
			self.maxIndex = 0
			i = -1
			while len(self.txtBuffer) > - i - 1 and self.txtBuffer[i][0] != '\n':
				cmd = self.txtBuffer[i][0] + cmd
				i -= 1
			self.lineNum += 1
			self.txtBuffer.append(('\n', (0, 0, 0)))
			self.maxLine += 1
		elif key == pygame.K_TAB:
			for _ in range(4):
				self.txtBuffer.insert(self.loc + ct, (' ', (0, 0, 0)))
			self.loc += 4; self.maxIndex += 4
		elif key == pygame.K_LSHIFT or key == pygame.K_RSHIFT:
			self.shift = True
		elif key == pygame.K_CAPSLOCK:
			self.capsLock = 1 - self.capsLock
		elif key == pygame.K_UP:
			if self.lineNum != 0:
				self.changeLine(self.lineNum - 1)
		elif key == pygame.K_DOWN:
			if self.lineNum != self.maxLine:
				self.changeLine(self.lineNum + 1)
		elif key == pygame.K_LEFT:
			if self.loc != 0:
				self.loc -= 1
		elif key == pygame.K_RIGHT:
			if self.loc + 1 <= self.maxIndex:
				self.loc += 1
		else:
			if 32 <= key <= 126:
				if (key == 39 or 44 <= key <= 57 or key == 59 or key == 61 or key == 96 or 91 <= key <= 93) and self.shift:
					self.txtBuffer.insert(self.loc + ct, (self.caps[chr(key)], (255, 255, 255)))
				elif 97 <= key <= 122 and (self.shift or self.capsLock):
					self.txtBuffer.insert(self.loc + ct, (self.caps[chr(key)], (255, 255, 255)))
				else:
					self.txtBuffer.insert(self.loc + ct, (chr(key), (255, 255, 255)))
				self.loc += 1
				self.maxIndex += 1

def new(self, app):
	pass   # TODO: integrate new file w/ multitabing

def open_file(self, app):
	with wx.FileDialog(frm, "Open file", wildcard="Any file|*",
					   style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
		if fileDialog.ShowModal() == wx.ID_CANCEL:
			return
		path = fileDialog.GetPath()
		app.txtField.fileName = path
		with open(path, 'r') as fr:
			for ch in fr.read():
				app.txtField.txtBuffer.append((ch, (255, 255, 255)))
				if ch == '\n':
					app.txtField.maxLine += 1
		app.txtField.changeLine(0)

def save_as(self, app):
	with wx.FileDialog(frm, "Save as", wildcard="Any file|*",
					   style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
		if fileDialog.ShowModal() == wx.ID_CANCEL:
			return
		path = fileDialog.GetPath()
		app.txtField.fileName = path
		with open(path, 'w') as fw:
			s = ''
			for ch, clr in app.txtField.txtBuffer:
				s += ch
			fw.write(s)
			
def save(self, app):
	s = ''
	for ch, clr in app.txtField.txtBuffer:
		s += ch
	if app.txtField.fileName:
		with open(app.txtField.fileName, 'w') as fw:
			fw.write(s)
	else:
		save_as(self, app)

framework = Framework()
ide = App("res/bg.jpg")
new_btn = Button("res/icons/new.jpg", "res/icons/btn_bg.jpg", 10, 10, ide.appID)
new_btn.onClick = new
open_btn = Button("res/icons/open.jpg", "res/icons/btn_bg.jpg", 60, 10, ide.appID)
open_btn.onClick = open_file
save_btn = Button("res/icons/save.jpg", "res/icons/btn_bg.jpg", 110, 10, ide.appID)
save_btn.onClick = save
save_as_btn = Button("res/icons/save_as.jpg", "res/icons/btn_bg.jpg", 160, 10, ide.appID)
compile_btn = Button("res/icons/compile.jpg", "res/icons/btn_bg.jpg", 210, 10, ide.appID)
# TODO: compile
run_btn = Button("res/icons/run.jpg", "res/icons/btn_bg.jpg", 260, 10, ide.appID)
# TODO: run
compile_run_btn = Button("res/icons/compile_run.jpg", "res/icons/btn_bg.jpg", 310, 10, ide.appID)
# TODO: compile & run
ide.addButton(new_btn)
ide.addButton(open_btn)
def compilecpp(flags):
	flags.insert(0, "./build")
	if int(flags[2]) == 0:
		subprocess.run(flags)
	elif int(flags[2]) == 1:
		subprocess.run(flags, creationflags=subprocess.CREATE_NEW_CONSOLE)

ide.addButton(save_btn)
ide.addButton(save_as_btn)
ide.addButton(compile_btn)
ide.addButton(run_btn)
ide.addButton(compile_run_btn)
framework.appID = ide.appID
framework.addApp(ide)
ide.enableTxtField(150, 160, 100, 40)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			framework.keyDown(event.key)
		elif event.type == pygame.KEYUP:
			framework.keyUp(event.key)
		if event.type == pygame.MOUSEBUTTONDOWN:
			framework.mouseDown(event.pos, event.button)
		elif event.type == pygame.MOUSEBUTTONUP:
			framework.mouseUp(event.pos, event.button)
		elif event.type == pygame.MOUSEMOTION:
			framework.mouseMotion(event.pos)
	framework.launch()
