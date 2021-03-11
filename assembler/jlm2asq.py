#!/usr/bin/env python3

# Turns on pdb for opcode replacement
# Note: this only works properly on Unix systems.
debug_on = False

# Imports
import sys
import json

def error(message):
  """Function called when there's an error."""
  #raise SyntaxError(message)
  print("jlm2asq.py:", message, file=sys.stderr)
  exit()

#Start

t = sys.stdin.read()
t = t.split("\nHLT\n")
if len(t) != 2:
  error("Not a valid JLM program. Check for HLT.")
try:
  stuff = json.loads(t[1])
except:
  error("variables initialized incorrectly.")
program = t[0].split("\n")
program.append("HLT")

#Changing stuff

stuff["Z"] = 0
stuff["NEGONE"] = -1
stuff["ASCIIZ"] = 48

#Getting line #s of labels

op_len = {
"SUBLEQ":1,
"ADD":3,
"SUB":1,
"MOV":4,
"OUT":4,
"INP":5,
"#":0,
"GOTO":1,
"BRP":2,
"BRZ":7,
"NOP":1,
"HLT":1
}

lbl_locs = {}
cur_line = 0
for i in range(len(program)):
  line = program[i]
  line = line.split()
  opcode = line[0]
  if opcode == "LBL":
    lbl_locs[line[1]] = str(cur_line)
    program[i] = "# LBL "+line[1]
  elif opcode in op_len.keys():
    cur_line += op_len[opcode]
  else:
    error("Line "+str(i)+": "+opcode+" is not a valid opcode.")

#Defining Non-Branching Functions

def subleq(a, b, lbl):
  """Fundamental Operation!
Subtracts a from b and goes to c if results is less than or equal to zero;
otherwise it goes to the next instruction."""
  global lbl_locs
  try:
    c = lbl_locs[lbl]
  except KeyError:
    error("%s is not a valid label." % lbl)
  return "{a} {b} {c}\n".format(a=a, b=b, c=c)

def add(a, b):
  """Adds a and b and stores the result in a."""
  return "{b} Z ?+1\nZ {a} ?+1\nZ Z ?+1\n".format(a=a, b=b)

def sub(a, b):
  """Subtracts b from a and stores the result in a."""
  return "{b} {a} ?+1\n".format(a=a, b=b)

def mov(a, b):
  """Copies b to a."""
  return sub(a, a) + add(a, b)

def out(a):
  """Copies the value in a to the "output"(address 0xff)."""
  return mov("255", a)

def inp(a):
  """Copies the value in the "input" (address 0xfe) to a once user enters something on keyboard."""
  return mov(a,"254")+"Z "+a+" ?-4\n"

def hlt():
  """Halts the program for coffee break. ALWAYS and only at the very end of the program!"""
  return "\n0\n"

def cmt():
  """For comments."""
  return ""

#Branch Functions

def goto(lbl):
  """Unconditionally goes to label lbl."""
  global lbl_locs
  try:
    q = lbl_locs[lbl]
  except KeyError:
    raise Exception("%s is not a valid label." % q)
  t = "Z Z {q}\n".format(q=q)
  return t

def brp(a, lbl):
  """Goes to label lbl if a>0. Otherwise, continues as normal."""
  global lbl_locs
  try:
    lbl = lbl_locs[lbl]
  except KeyError:
    error("%s is not a valid label." % lbl)
  return "Z {a} ?+2\nZ Z {lbl}\n".format(a=a, lbl=lbl)

def brz(a, lbl):
  """Goes to label lbl if a=0. Otherwise, continues as normal."""
  global lbl_locs
  try:
    lbl = lbl_locs[lbl]
  except KeyError:
    error("%s is not a valid label." % lbl)
  return ("Z {a} ?+2\nZ Z ?+6\n{a} Z ?+2\nZ Z ?+4\nNEGONE Z ?+2\nZ Z {lbl}\n".format(a=a, lbl=lbl))+sub("Z","Z")

#Replacing opcodes

if debug_on:
  sys.stdin = open("/dev/tty")
  import pdb
  pdb.set_trace()
output = ""
for line in program:
  lip = line.split()
  opcode = lip[0]
  try:
    if opcode == "SUBLEQ":
      output += subleq(lip[1], lip[2], lip[3])
    elif opcode == "ADD":
      output += add(lip[1], lip[2])
    elif opcode == "SUB":
      output += sub(lip[1], lip[2])
    elif opcode == "MOV":
      output += mov(lip[1], lip[2])
    elif opcode=="GOTO":
      output += goto(lip[1])
    elif opcode == "OUT":
      output += out(lip[1])
    elif opcode == "INP":
      output += inp(lip[1])
    elif opcode=="BRP":
      output += brp(lip[1], lip[2])
    elif opcode == "BRZ":
      output += brz(lip[1], lip[2])
    elif opcode == "NOP":
      output += "Z Z ?+1\n"
    elif opcode == "#":
      output += cmt()
    elif opcode == "HLT":
      output += "0\n"
    else:
      error("Invalid opcode: %s" % lip[0])
  except IndexError:
    error("Wrong number of operands: %s" % line)

output += json.dumps(stuff)
print(output)
