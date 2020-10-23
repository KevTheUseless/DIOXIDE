# TextDraw.py
# A place to test

import pygame, sys

def wrap(txtBuffer):
	lines = []
	temp = ""
	color = []
	for c in txtBuffer:
		if c[0] == '\t':
			temp += "    ";
		elif c[0] == '\n':
			lines.append(temp)
			temp = ""
		else:
			temp += c[0]
		try: color.append((c[1][0], c[1][1], c[1][2]))
		except: pass
	lines.append(temp)
	return lines, color

def drawTxt(screen, lines, colors, y = 0):
	for i in range(len(lines)):
		try: img = raster.render(lines[i], True, colors[i])
		except: img = raster.render(lines[i], True, (0, 0, 0))
		screen.blit(img, (0, y))
		y += 16


width, height = 800, 600

txtBuffer = []
caps = {
	'`': '~',
	'1': '!',
	'2': '@',
	'3': '#',
	'4': '$',
	'5': '%',
	'6': '^',
	'7': '&',
	'8': '*',
	'9': '(',
	'0': ')',
	'-': '_',
	'=': '+',
	'[': '{',
	']': '}',
	'\\': '|',
	';': ':',
	'\'': '"',
	',': '<',
	'.': '>',
	'/': '?',
	'a': 'A',
	'b': 'B',
	'c': 'C',
	'd': 'D',
	'e': 'E',
	'f': 'F',
	'g': 'G',
	'h': 'H',
	'i': 'I',
	'j': 'J',
	'k': 'K',
	'l': 'L',
	'm': 'M',
	'n': 'N',
	'o': 'O',
	'p': 'P',
	'q': 'Q',
	'r': 'R',
	's': 'S',
	't': 'T',
	'u': 'U',
	'v': 'V',
	'w': 'W',
	'x': 'X',
	'y': 'Y',
	'z': 'Z'
}

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("TextDraw")
clock = pygame.time.Clock()

raster = pygame.font.Font("res/Perfect_DOS_VGA_437.ttf", 16)

shift = False
capsLock = False

while True:
	screen.fill((0, 0, 0))
	wrapped = wrap(txtBuffer)
	print(wrapped)
	if txtBuffer != []:
		drawTxt(screen, wrapped[0], wrapped[1])
	pygame.display.update()
	clock.tick(50)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_BACKSPACE:
				try:
					txtBuffer.pop()
				except: pass
			elif event.key == pygame.K_RETURN:
				txtBuffer.append('\n')
			elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
				shift = True
			elif event.key == pygame.K_CAPSLOCK:
				capsLock = 1 - capsLock
			else:
				if 32 <= event.key <= 126 or event.key == pygame.K_TAB:
					if (44 <= event.key <= 57 or event.key == 59 or event.key == 61 or 91 <= event.key <= 93 or event.key == 96) and shift:
						txtBuffer.append((caps[chr(event.key)], (0, 255, 0)))
					elif 97 <= event.key <= 122 and (shift or capsLock):
						txtBuffer.append((caps[chr(event.key)], (0, 255, 0)))
					else:
						txtBuffer.append((chr(event.key), (0, 255, 0)))
		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
				shift = False
			elif event.key == pygame.K_CAPSLOCK:
				capsLock = 1 - capsLock