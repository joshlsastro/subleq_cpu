#!/usr/bin/env python3
import sys
import json
import os

# Usage: python3 syntax_error_generator.py [message] [output_filename]

# Possible error messages
serious = "Assembler: Syntax Error!\n"
silly = "Your monkey overlords rejected your code.\n"
error = eval(sys.argv[1])

# Generating JLM code
code = []
vars = {}
for i in range(len(error)):
  code.append("OUT arr%s" % i)
  vars["arr%s" % i] = ord(error[i])
text = "\n".join(code)
text += "\nHLT\n"
text += json.dumps(vars)
with open("syntax_error.jlm", "w") as f:
    f.write(text)

# Compiling code
os.system("{py} main_cmdline.py -o {output} syntax_error.jlm".format(py=sys.executable, output=sys.argv[2]))
os.remove("syntax_error.jlm")
