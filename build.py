import subprocess, sys, ctypes

compiler = "g++"
srcname = "test.cpp"
outname = "test.exe"

def isAdmin():
	try:
		return ctypes.windll.shell32.IsUserAnAdmin()
	except:
		return False

compiler = "g++"
srcname = "test.cpp"
outname = "test.exe"

if not isAdmin():
	ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
	compileLog = subprocess.Popen("%s %s -o %s" % (compiler, srcname, outname), shell=True, encoding="utf-8")
	sys.exit()