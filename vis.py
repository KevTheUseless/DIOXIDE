import pygame, sys

# 100 x 100, 10px, 5 * 3
# AC: rgb(82, 196, 26)
# TLE/MLE: rgb(5, 34, 66)
# WA: rgb(231, 76, 60)
# RE: rgb(157, 61, 207)

def drawBlocks():
	pass

width, height = 600, 380
line = 0
pics = []

if len(sys.argv) < 2:
	print("Missing argument.\nUsage: python3 vis.py <results>")
	sys.exit()

res = [sys.argv[1][i:i + 5] for i in range(0, len(sys.argv[1]), 5)]

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Winnux 58")
clock = pygame.time.Clock()

while True:
	screen.blit(pics[line], (0, 0))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_DOWN:
				line += 1
	pygame.display.update()
	clock.tick(50)