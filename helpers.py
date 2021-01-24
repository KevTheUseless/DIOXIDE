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
	if app.txtField.fileName:
		with open(app.txtField.fileName, 'w') as fw:
			fw.write(s)
	else:
		save_as(self, app)

def compile_cpp(self, app):
	if not app.txtField.fileName:
		save_as(self, app)
	compileFlags = ['buildsys/build', app.txtField.fileName.rstrip(".cpp")]
	print(compileFlags)
	cmd = " ".join(compileFlags)
	subprocess.run(cmd)

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

def calc_pos(pos):
	px, py = pos
	x = max((px - 145) // 10, 0)
	y = max((py - 155) // 20, 0)
	return x, y
