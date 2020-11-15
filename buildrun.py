import subprocess, contextlib, os, sys, ctypes, msvcrt

compiler = "g++"
srcname = "test.cpp"
outname = "test.exe"

def isAdmin():
	try:
		return ctypes.windll.shell32.IsUserAnAdmin()
	except:
		return False

if not isAdmin():
	ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
	compileLog = subprocess.Popen("%s %s -o %s" % (compiler, srcname, outname), shell=True, encoding="utf-8")
	sys.exit()
	
output = subprocess.Popen("%s" % outname, shell=True, encoding="utf-8")
while True:
	if output.poll() is not None:
		print("\nProcess terminated with return code %d." % output.poll())
		print("Press any key to continue. . . ")
		msvcrt.getch()
		break