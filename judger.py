import sys, re, subprocess as s
import os

def judge(filename = "std"):
	sample_in_list = []
	sample_out_list = []
	for file in os.listdir("judge"):
		if file.endswith('.in') and os.path.isfile("judge/%sout" % file[:-2]):
			sample_in_list.append("judge/" + file)
			sample_out_list.append("judge/%sout" % file[:-2])
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
			processedIn = s.Popen("type %s" % sample_in.replace("/", "\\"), shell=True, stdout=s.PIPE)
			#print(processedIn.communicate())
			o = s.Popen("judger/procgov --timeout 1000 -q %s" % filename, shell=True, stdin=processedIn.stdout, stdout=s.PIPE)
			o2 = s.Popen("judger/procgov --maxmem 256M -q %s" % filename, shell=True, stdin=processedIn.stdout, stdout=s.PIPE)

			print(o.stdout.read())
			print(o2.stdout.read())
			
			if not o:
				res[i] = "T"
				continue
			if not o2:
				res[i] = "M"
				continue
#			if o.returncode or o2.returncode:
#				res[i] = "re"
#				continue
			for line in o.stdout.read().split('\n'):
				l = line.lstrip().rstrip()
				if l:
					out.append(l)
		if sout != out:
			res[i] = "W"
			continue
	return res
