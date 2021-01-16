import wx, subprocess
from regex import parse
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
	pass  # TODO: integrate new file w/ multitabbing

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
	parse(app.txtField)

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
	if app.txtField.fileName:
		with open(app.txtField.fileName, 'w') as fw:
			fw.write(s)
	else:
		save_as(self, app)

def compile_cpp(self, app, run=0):
	if not app.txtField.fileName:
		save_as(self, app)
	compileFlags = ['./build', str(run), app.txtField.fileName.rstrip(".cpp")]
	print(compileFlags)
	cmd = " ".join(compileFlags)
	for i in range(3): compileFlags.pop(0)
	if run == 0:
		subprocess.run(cmd)
	elif run:
		subprocess.run(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)

def compile_run_cpp(self, app, compileFlags=[]):
	compile_cpp(self, app, 2)

def run_cpp(self, app):
	compile_cpp(self, app, 1)

def get_skin(self, app):
	skin = ''
	with wx.FileDialog(frm, "Choose skin file", wildcard="GENOCIDE skin file (*.gskin)|*.gskin",
					   style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
		if fileDialog.ShowModal() == wx.ID_CANCEL:
			return
		skin = open(fileDialog.GetPath())
	with open("current_skin.gskin", 'w') as fw:
		fw.write(skin.read())
	skin.close()

def calc_pos(pos):
	px, py = pos
	x = max((px - 145) // 10, 0)
	y = max((py - 155) // 20, 0)
	return x, y
