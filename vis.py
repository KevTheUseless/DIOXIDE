import pygame, sys

width, height = 560, 380
line = 0

if len(sys.argv) < 2:
	print("Missing argument.\nUsage: python3 vis.py <results>")
	sys.exit()

res = [sys.argv[1][i:i + 5] for i in range(0, len(sys.argv[1]), 5)]

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Verdict")
clock = pygame.time.Clock()

noto = pygame.font.Font("res/NotoSans-Regular.ttf", 32)
small = pygame.font.Font("res/NotoSans-Regular.ttf", 14)

def ac(i):
	temp = pygame.Surface((100, 100))
	temp.fill((82, 196, 26))
	txt = noto.render("AC", True, (255, 255, 255))
	temp.blit(txt, (30, 25))
	txt = small.render("#%d" % i, True, (255, 255, 255))
	temp.blit(txt, (5, 5))
	return temp

def wa(i):
	temp = pygame.Surface((100, 100))
	temp.fill((231, 76, 60))
	txt = noto.render("WA", True, (255, 255, 255))
	temp.blit(txt, (24, 25))
	txt = small.render("#%d" % i, True, (255, 255, 255))
	temp.blit(txt, (5, 5))
	return temp

def tle(i):
	temp = pygame.Surface((100, 100))
	temp.fill((5, 34, 66))
	txt = noto.render("TLE", True, (255, 255, 255))
	temp.blit(txt, (22, 25))
	txt = small.render("#%d" % i, True, (255, 255, 255))
	temp.blit(txt, (5, 5))
	return temp

def mle(i):
	temp = pygame.Surface((100, 100))
	temp.fill((5, 34, 66))
	txt = noto.render("MLE", True, (255, 255, 255))
	temp.blit(txt, (18, 25))
	txt = small.render("#%d" % i, True, (255, 255, 255))
	temp.blit(txt, (5, 5))
	return temp

def re(i):
	temp = pygame.Surface((100, 100))
	temp.fill((157, 61, 207))
	txt = noto.render("RE", True, (255, 255, 255))
	temp.blit(txt, (30, 25))
	txt = small.render("#%d" % i, True, (255, 255, 255))
	temp.blit(txt, (5, 5))
	return temp

stats = {
	"A": ac,
	"W": wa,
	"T": tle,
	"M": mle,
	"R": re
}

while True:
	screen.fill((255, 255, 255))
	for i in range(line, line + 3):
		for j in range(5):
			try: screen.blit(stats[res[i][j]](i * 5 + j + 1), (10 + j * 110, 20 + (i - line) * 120))
			except: break
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_DOWN:
				line = min(len(res), line + 3)
			if event.key == pygame.K_UP:
				line = max(0, line - 3)
	pygame.display.update()
	clock.tick(50)
