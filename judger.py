import sys, subprocess as s
import os

def judge(filename):
    sample_in_list = []
    sample_out_list = []
    for file in os.listdir("judge"):
        if file.endswith('.in') and os.path.isfile("judge/%sout" % file[:-2]):
            sample_in_list.append("judge/" + file)
            sample_out_list.append("judge/%sout" % file[:-2])
    print(sample_in_list, sample_out_list)
    return _judge(filename, sample_in_list, sample_out_list)


def _judge(filename, sample_in_list: list, sample_out_list: list):
    res = ["ac"] * len(sample_in_list)
    for i, sample_in in enumerate(sample_in_list):
        sample_out = sample_out_list[i]
        sout = []; out = []
        with open(sample_out) as fr:
            for line in fr.read().split('\n'):
                l = line.lstrip().rstrip()
                if l:
                    sout.append(l)
        with open(sample_in) as fr:
            o = s.run("judger/procgov --timeout 1000 -q %s" % filename, stdin=fr, capture_output=True)
            o2 = s.run("judger/procgov --maxmem 256M -q %s" % filename, stdin=fr, capture_output=True)
            if not o:
                res[i] = "tle"
                continue
            if not o2:
                res[i] = "mle"
                continue
            if o.returncode or o2.returncode:
                res[i] = "re"
                continue
            for line in o.stdout.decode().split('\n'):
                l = line.lstrip().rstrip()
                if l:
                    out.append(l)
        if sout != out:
            res[i] = "wa"
            continue
    return res
