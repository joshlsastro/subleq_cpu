#!/usr/bin/env python3

__doc__ = """\
Each command here is interpreted as an implied subleq command. Variables are treated normally. ? means address of this instruction.
"""

# Imports
import sys
import json

def error(message):
  """Function called when there's an error."""
  #raise SyntaxError(message)
  print("asq2sq.py:", message, file=sys.stderr)
  exit()

#Start
t = sys.stdin.read()
t = t.split("\n0\n")
if len(t) != 2:
  error("Not a valid ASQ file!")
try:
  stuff = json.loads(t[1])
except:
  error("Variables initalized incorrectly!")
program = t[0].split("\n")

#Memory Allocation
lines_prgm = len(program)+1
data_loc = {}
for i in stuff.keys():
  data_loc[i] = lines_prgm
  lines_prgm += 1
loc_data = {}
for i in stuff.keys():
  loc_data[data_loc[i]] = i

#Changing Program to Numbers
output = ""
for i in range(len(program)):
  line = program[i]
  line = line.split()
  if len(line) < 3:
    error("Line %s: Wrong Line Length!" % i)
  if line[0] in stuff.keys():
    line[0] = data_loc[line[0]]
    line[0] = str(line[0])
  if line[1] in stuff.keys():
    line[1] = data_loc[line[1]]
    line[1] = str(line[1])
  if "?" in line[2]:
    line[2] = line[2].replace("?", str(i))
    line[2] = str(eval(line[2])) # Python errors are likely more useful here
  for j in range(3):
    # Special sq2hex values
    if line[j] in ["#IN", "#OUT"]:
      pass
    else:
      try:
        int(line[0])
        int(line[1])
        int(line[2])
      except ValueError:
        error("Line {i}: Uninitialized variables or bad jump: {a} {b} {c}".format(i=i, a=line[0], b=line[1], c=line[2]))
  line = line[0]+" "+line[1]+" "+line[2]+"\n"
  output += line
output += "0 0 0\n"

#Putting in variables
loc_data = {}
for i in data_loc.keys():
  loc_data[data_loc[i]] = i
locations = list(loc_data.keys())
locations.sort()
for i in range(len(locations)):
  loc = locations[i]
  cur_varname = loc_data[loc]
  cur_num = stuff[cur_varname]
  output += "0 0 "+str(cur_num)+"\n"

#Final
print(output)
