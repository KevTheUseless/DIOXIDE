from helpers import *
from regex import parse
import pygame, sys


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
	def scroll(self, y):
		self.apps[self.appID].scroll(y)

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
			self.txtField.draw(screen)
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
		print(pos)
		for btn in self.btnList:
			btn.mouseDown(pos, button, self)
		self.txtField.mouseDown(pos, button)
	def mouseUp(self, pos, button):
		for button in self.btnList:
			button.mouseUp(pos, button)
		self.txtField.mouseUp(pos, button)
	def mouseMotion(self, pos):
		framework.mousePos = pos
		for btn in self.btnList:
			btn.mouseMove(pos)
		self.txtField.mouseMotion(pos)
	def keyUp(self, key):
		if self.txtFieldEnabled:
			self.txtField.keyUp(key)
	def keyDown(self, key):
		if self.txtFieldEnabled:
			self.txtField.keyDown(key)
	def scroll(self, y):
		self.txtField.scroll(y)

class TxtField:
	def __init__(self, x, y, w, h):
		self.x, self.y = x, y
		self.w, self.h = w, h
		self.txtBuffer = [[]]
		# MAGIC #
		self.caps = { '`': '~', '1': '!', '2': '@', '3': '#', '4': '$', '5': '%', '6': '^', '7': '&', '8': '*', '9': '(', '0': ')', '-': '_', '=': '+', '[': '{', ']': '}', '\\': '|', ';': ':', '\'': '"', ',': '<', '.': '>', '/': '?', 'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D', 'e': 'E', 'f': 'F', 'g': 'G', 'h': 'H', 'i': 'I', 'j': 'J', 'k': 'K', 'l': 'L', 'm': 'M', 'n': 'N', 'o': 'O', 'p': 'P', 'q': 'Q', 'r': 'R', 's': 'S', 't': 'T', 'u': 'U', 'v': 'V', 'w': 'W', 'x': 'X', 'y': 'Y', 'z': 'Z' }
		self.shift, self.capsLock = False, False
		self.currentChar, self.loc = 0, 0
		self.lineNum = 0; self.startLine = 0
		self.cLineStr = ""
		self.mono = pygame.font.Font("res/JetBrainsMono-Regular.ttf", 18)

		self.fileName = ''

		self.selecting = False
		self.selection_fixed, self.selection_branch = (), ()
		self.selection_start, self.selection_end = (), ()

		self.autocomplete = {'(': ')', '[': ']', '{': '}', '<': '>'}
		
		class Cursor(pygame.sprite.Sprite):
			def __init__(self):
				pygame.sprite.Sprite.__init__(self)

				self.image = pygame.Surface((1, 16))
				self.image.fill(pygame.Color(252, 252, 252))

				self.rect = self.image.get_rect()

		self.cursor = Cursor()
	def get_selection_rects(self):
		if not self.selection_start or not self.selection_end: return []
		start_x, start_y = self.selection_start
		end_x, end_y = self.selection_end
		#start_x, start_y, end_x, end_y = min(ax, bx), min(ay, by), max(ax, bx), max(ay, by)
		span = end_y - start_y
		if span == 0:
			begin_sf = pygame.Surface(((end_x - start_x) * 10, 20))
			begin_sf.fill((120, 120, 120))
			begin = begin_sf.get_rect()
			begin.center = (self.x + start_x * 10 + (end_x - start_x) * 5,
			                self.y + start_y * 20 + 5 - self.startLine * 20)
			return [(begin_sf, begin)]
		elif span == 1:
			begin_sf = pygame.Surface(((self.w - start_x) * 10, 20))
			begin_sf.fill((120, 120, 120))
			begin = begin_sf.get_rect()
			begin.center = (self.x + start_x * 10 + (self.w - start_x) * 5,
			                self.y + start_y * 20 + 5 - self.startLine * 20)
			end_sf = pygame.Surface((end_x * 10, 20))
			end_sf.fill((120, 120, 120))
			end = end_sf.get_rect()
			end.center = (self.x + end_x * 5, self.y + end_y * 20 + 5 - self.startLine * 20)
			return [(begin_sf, begin), (end_sf, end)]
		else:
			begin_sf = pygame.Surface(((self.w - start_x) * 10, 20))
			begin_sf.fill((120, 120, 120))
			begin = begin_sf.get_rect()
			begin.center = (self.x + start_x * 10 + (self.w - start_x) * 5,
			                self.y + start_y * 20 + 5 - self.startLine * 20)
			end_sf = pygame.Surface((end_x * 10, 20))
			end_sf.fill((120, 120, 120))
			end = end_sf.get_rect()
			end.center = (self.x + end_x * 5, self.y + end_y * 20 + 5 - self.startLine * 20)
			mid_sf = pygame.Surface((self.w * 10, 20 * (span - 1)))
			mid_sf.fill((120, 120, 120))
			mid = mid_sf.get_rect()
			mid.center = (700, self.y + start_y * 20 + (end_y - start_y) * 10 + 5 - self.startLine * 20)
			return [(begin_sf, begin), (end_sf, end), (mid_sf, mid)]
	def draw(self, screen):
		if pygame.time.get_ticks() % 1000 <= 500: self.cursor.image.fill(pygame.Color(252, 252, 252))
		else: self.cursor.image.fill(pygame.Color(0, 0, 0))

		for sf, rt in self.get_selection_rects():
			screen.blit(sf, rt)

		self.cursor.rect.center = (self.x + self.loc * 10,
								   self.y + (self.lineNum-self.startLine) * 20 + 5)
		screen.blit(self.cursor.image, self.cursor.rect)

		for j, line in enumerate(self.txtBuffer[self.startLine:self.startLine+28]):
			for i, ch in enumerate(line):
				img = self.mono.render(ch[0], True, ch[1])
				screen.blit(img, (self.x + i * 10, j * 20 + self.y - 5))
	def keyUp(self, key):
		if key == pygame.K_LSHIFT or key == pygame.K_RSHIFT:
			self.shift = False
		elif key == pygame.K_CAPSLOCK:
			self.capsLock = 1 - self.capsLock
	def changeLine(self, l):
		l = min(l, len(self.txtBuffer) - 1)
		self.lineNum = l
		self.loc = min(self.loc, len(self.txtBuffer[self.lineNum]))
	def goto(self, *pos):
		if len(pos) == 2:
			x, y = pos
		else:
			x, y = pos[0]
		self.changeLine(y)
		self.loc = min(len(self.txtBuffer[self.lineNum]), x)
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
				self.loc -= 1
			elif self.lineNum != 0:
				self.lineNum -= 1
				self.loc = len(self.txtBuffer[self.lineNum])
		elif key == pygame.K_RIGHT:
			if self.loc + 1 <= len(self.txtBuffer[self.lineNum]):
				self.loc += 1
			elif self.lineNum < len(self.txtBuffer) - 1:
				self.lineNum += 1
				self.loc = 0
		elif (not (self.shift or self.capsLock)) and chr(key) in self.autocomplete:
			self.txtBuffer[self.lineNum].insert(self.loc, [chr(key), (255, 255, 255)])
			self.txtBuffer[self.lineNum].insert(self.loc + 1, [self.autocomplete[chr(key)], (255, 255, 255)])
			self.loc += 1
		elif (self.shift or self.capsLock) and (self.caps[chr(key)] in self.autocomplete):
			self.txtBuffer[self.lineNum].insert(self.loc, [self.caps[chr(key)], (255, 255, 255)])
			self.txtBuffer[self.lineNum].insert(self.loc + 1, [self.autocomplete[self.caps[chr(key)]], (255, 255, 255)])
			self.loc += 1
		elif (((not (self.shift or self.capsLock)) and chr(key) in self.autocomplete.values()) \
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
		parse(self, self.lineNum)
	def mouseDown(self, pos, button):
		print('msd')
		if pos[0] < 146:
			self.loc = 0
			return
		if pos[1] < 160: return
		x, y = calc_pos(pos)
		y += self.startLine
		self.goto(x, y)
		if pos[0] >= 146 and pos[1] >= 160:
			self.selecting = True
			self.selection_fixed = (self.loc, y)
			self.selection_branch = (self.loc, y)
			self.selection_start = (self.loc, y)
			self.selection_end = (self.loc, y)
	def mouseUp(self, pos, button):
		if pos[0] >= 146 and pos[1] >= 160:
			self.selecting = False
			if self.selection_fixed == self.selection_branch:
				self.selection_fixed = ()
				self.selection_branch = ()
				self.selection_start = ()
				self.selection_end = ()
	def mouseMotion(self, pos):
		if not self.selecting: return
		try: x, y = calc_pos(pos)
		except: return
		y += self.startLine
		self.goto(x, y)
		self.selection_branch = (self.loc, self.lineNum)
		if (y < self.selection_fixed[1]) or (y == self.selection_fixed[1] and self.loc < self.selection_fixed[0]):
			self.selection_start, self.selection_end = self.selection_branch, self.selection_fixed
		else:
			self.selection_start, self.selection_end = self.selection_fixed, self.selection_branch
	def scroll(self, y):
		print('scrl')
		self.startLine += -y
		self.startLine = max(min(self.startLine, len(self.txtBuffer)), 0)

framework = Framework()
ide = App("res/bg.jpg")
new_btn = Button("res/icons/new.jpg", "res/icons/btn_bg.jpg", 10, 10, ide.appID)
new_btn.onClick = new

open_btn = Button("res/icons/open.jpg", "res/icons/btn_bg.jpg", 60, 10, ide.appID)
open_btn.onClick = open_file

save_btn = Button("res/icons/save.jpg", "res/icons/btn_bg.jpg", 110, 10, ide.appID)
save_btn.onClick = save

save_as_btn = Button("res/icons/save_as.jpg", "res/icons/btn_bg.jpg", 160, 10, ide.appID)
save_as_btn.onClick = save_as

compile_btn = Button("res/icons/compile.jpg", "res/icons/btn_bg.jpg", 210, 10, ide.appID)
compile_btn.onClick = compile_cpp

run_btn = Button("res/icons/run.jpg", "res/icons/btn_bg.jpg", 260, 10, ide.appID)
run_btn.onClick = run_cpp

compile_run_btn = Button("res/icons/compile_run.jpg", "res/icons/btn_bg.jpg", 310, 10, ide.appID)
compile_run_btn.onClick = compile_run_cpp

ide.addButton(new_btn)
ide.addButton(open_btn)

ide.addButton(save_btn)
ide.addButton(save_as_btn)
ide.addButton(compile_btn)
ide.addButton(run_btn)
ide.addButton(compile_run_btn)
framework.appID = ide.appID
framework.addApp(ide)
ide.enableTxtField(150, 160, 110, 40)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
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
