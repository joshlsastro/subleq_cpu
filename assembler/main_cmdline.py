#!/usr/bin/env python3
import argparse
import os
import subprocess as sp
import sys
path = os.path.split(__file__)[0]
try:
    os.chdir(path)
except: #We're already in the right directory anyway
    pass

parser = argparse.ArgumentParser(description="JLM to Logisim file compiler. Compiled JLM files can be run on cpu.circ.")
parser.add_argument("-o",help="Output compiled JLM file. Must be used in assembler directory!")
parser.add_argument("in_file",help="Input JLM file.")
parser.add_argument("-s",help="Make error message sillier.",action="store_true")
args = parser.parse_args()

if args.in_file:
    args = vars(args)
    in_file = args['in_file']
    out_file = args['o']
    py = sys.executable
    with open(in_file, "rb") as f:
        inp = f.read()
    p1 = sp.run([py,"jlm2asq.py"], input=inp, stdout=sp.PIPE)
    p2 = sp.run([py,"asq2sq.py"], input=p1.stdout, stdout=sp.PIPE)
    p3 = sp.run([py,"sq2hex.py"], input=p2.stdout, stdout=sp.PIPE)
    output = p3.stdout
    with open(out_file, "wb") as f:
        f.write(output)

with open(out_file, "r") as f:
    t = f.read()
if t == "v2.0 raw\n":
    # There was an error and nothing was printed
    if args['s']: # If silly mode
        s = "silly"
    else:
        s = "serious"
    # Compile to error message
    sp.run([py,"syntax_error_generator.py",s,out_file])
