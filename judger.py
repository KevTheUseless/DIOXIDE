import sys, re, subprocess as s
import os

def judge(filename):
	sample_in_list = []
	sample_out_list = []
	for file in os.listdir("judge"):
		if file.endswith('.in') and os.path.isfile("judge/%sout" % file[:-2]):
			sample_in_list.append(os.path.join("judge", file))
			sample_out_list.append(os.path.join("judge", file[:-2] + "out"))
	print(sample_in_list, sample_out_list)
	return "python vis.py %s" % ''.join(_judge(filename, sample_in_list, sample_out_list))


def _judge(filename, sample_in_list: list, sample_out_list: list):
	res = ["A"] * len(sample_in_list)
	for i, sample_in in enumerate(sample_in_list):
		sample_out = sample_out_list[i]
		sout = []; out = []
		with open(sample_out) as fr:
			for line in fr.read().split('\n'):
				l = line.lstrip().rstrip()
				if l:
					sout.append(l)
		with open(sample_in) as fr:
			processedIn = s.Popen("%s %s" % ("type" if sys.platform == "win32" else "cat", sample_in), shell=True, stdout=s.PIPE)
			o = s.Popen("%s --timeout 1000 -q %s" % (os.path.join("judger", "procgov"), filename), shell=True, stdin=processedIn.stdout, stdout=s.PIPE)
			r = o.stdout.read().decode()
			if not r:
				res[i] = "T"
				continue
			o2 = s.Popen("%s --maxmem 256M -q %s" % (os.path.join("judger", "procgov"), filename), shell=True, stdin=processedIn.stdout, stdout=s.PIPE)
			r2 = o2.stdout.read().decode()
			if not r2:
				res[i] = "M"
				continue

			if o.returncode or o2.returncode:
				res[i] = "R"
				continue
			for line in r.split('\n'):
				l = line.lstrip().rstrip()
				if l:
					out.append(l)
		print(out)
		if sout != out:
			res[i] = "W"
	return res
