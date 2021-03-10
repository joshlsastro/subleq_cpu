#!/usr/bin/env python3
import os
import sys
path = os.path.split(__file__)[0]
try:
    os.chdir(path)
except: #We're already in the right directory
    pass

print("This program compiles JLM files into files runnable on cpu.circ.")
print("Use main_cmdline.py if you prefer command line flags.")
in_file = input("What file do you want to compile? ")
out_file = input("What do you want to call the output file? ")
os.system(sys.executable + " main_cmdline.py -o " + out_file + " " + in_file)
