import subprocess, msvcrt

compiler = "g++"
srcname = "test.cpp"
outname = "test.exe"

output = subprocess.Popen("%s" % outname, shell=True, encoding="utf-8")
while True:
	if output.poll() is not None:
		print("\nProcess terminated with return code %d." % output.poll())
		print("Press any key to continue. . . ")
		msvcrt.getch()
		break