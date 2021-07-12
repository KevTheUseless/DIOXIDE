import sys, re, subprocess as s
import os

resStr = "AWTMR"

def judge(filename = "judge/std"):
	sample_in_list = []
	sample_out_list = []
	for file in os.listdir("judge"):
		if file.endswith('.in') and os.path.isfile("judge/%sout" % file[:-2]):
			sample_in_list.append("judge/" + file)
			sample_out_list.append("judge/%sout" % file[:-2])
	print(sample_in_list, sample_out_list)
	return "python vis.py %s" % ''.join(_judge(filename, sample_in_list, sample_out_list, "2000", "256M"))


def _judge(filename, sample_in_list: list, sample_out_list: list, tLimit: str, mLimit: str):
	res = ["A"] * len(sample_in_list)
	for i, sample_in in enumerate(sample_in_list):
		sample_out = sample_out_list[i]
		ret = os.system("judger/judge %s %s %s %s %s" % (os.path.realpath(filename), os.path.realpath(sample_in), os.path.realpath(sample_out), tLimit, mLimit))
		res[i] = resStr[ret]
	return res