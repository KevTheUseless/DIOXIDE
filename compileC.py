import subprocess

compiler = "g++"
srcname = "a.cpp"
outname = "a"

log = open("compile.log", "w")
out = open("out.txt", "w")
compileLog = subprocess.Popen("%s %s -o %s" % (compiler, srcname, outname), shell=True, stderr=log, encoding="utf-8")
output = subprocess.Popen("%s" % outname, shell=True, stdout=out, stderr=out, encoding="utf-8")