# subleq_cpu

# Description of Files

cpu.circ is a Logisim file for a very basic [subleq][1] computer.
`assembler` contains the Python programs for assembling JLM, a language I made up for this processor, into machine code for this computer.
`jlm_programs` contains JLM programs that I've written.
`exe_programs` contains the "executable" versions of those programs; these can be loaded into RAM without running the assembler.

[1]: #how-subleq-works

# Requirements
You need [Java](https://adoptopenjdk.net/) and [Logisim](https://sourceforge.net/projects/circuit/files/2.7.x/2.7.1/) to run cpu.circ. You need [Python 3](https://python.org) to run the assembler.

# How subleq works

Subleq is an instruction set that only has one instruction: subleq. A subleq instruction consists of 3 memory addresses: a, b, and c. It subtracts that value at address a from the value at address b. If the result is less than or equal to 0, it jumps to address c. Otherwise, it goes to the next instruction. In pseudocode:
```c
Mem[b] = Mem[b] - Mem[a];
if (Mem[b] <= 0) {
  goto c;
}
```

Curiously, this instruction is enough to build any program; well, any program that can fit in the memory.

Technical note: The subleq dialect I'm using has all the instruction's addresses inside one memory location.

# How cpu.circ works

## RAM

This is the big chip with all of the numbers in it. It's actually quite simple: a lot of registers indexed with addresses. It exists in 2 modes, read and write. When RAM is in read mode, it outputs the data at the address given  to the A wire. When RAM is in write mode, it takes the address given on A and changes the data at that address to the data given to it on the D wire.

## CPU

This is the chip on the left labeled "CPU". It consists of 4 components: the ALU, the RAM Interface, the registers, and the stepper.

The ALU (Arithmetic and Logic Unit) does all of the CPU's calculations. It has a subtracting circuit to subtract B from A and a comparator to check if B-A is less than or equal to 0.

The RAM Interface is responsible for helping the CPU talk to RAM. It contains the PC (Program Counter) Area, which keeps track of which RAM address holds the next instruction.  The RAM Interface is also responsible for which RAM Address to use and whether the CPU is in Read or Write mode.

The registers hold values from RAM in a more accessible way to the CPU. In particular, the Instruction Register holds which instruction the CPU is executing, and the A and B registers hold the numbers that the ALU is working with.

The last, but arguably most important, part of the CPU is the stepper. It walks the other parts of the CPU through the processing of the instruction by firing 1 of 4 wires at a time. Despite its simplicity, this is what allows the CPU to execute instructions automatically.

## How The CPU Works

The stepper directs the other components through a 4-step process that fetches and executes a subleq instruction. Keep in mind that each instruction is made of 3 8-bit parts: the address of number A, the address of number B, and the jump address. Here are the steps, along with summaries:

1. In Read Mode, get the value in the RAM Address specified by the program counter and put that value into the Instruction Register. **Summary: Fetch Instruction.**
2. In Read Mode, get the value at A (address from Instruction Register) from RAM and put it in Register A. **Summary: Get A.**
3. In Read Mode, get the value at B (address from Instruction Register) from RAM and put it in Register B. **Summary: Get B.**
4. In Write Mode, get the result from the ALU (B-A) and put it in B (address from Instruction Register). Update the PC Area with the jump address from the Instruction Register and Jump flag from the ALU (on iff B-A <= 0). **Summary: Write B-A to RAM and update the program counter.**

## I/O

This is what's responsible for the mess of wiring. There are 2 chips responsible for input and output. The Input chip takes the address from the CPU. If the address is 254 (input), the chip gives the CPU the data from the keyboard. Otherwise, it just gives the data from RAM. The Log chip checks to see when the address from the CPU is 255 (output) and if it's in write mode. When both of these conditions are met, it writes to its own internal memory log and to the screen at the bottom. Both the keyboard and screen use 1-byte ASCII characters.

# Programming

## How to run a Subleq Program
1. Change directory to `assembler`
2. Run the Python 3 program main_easy.py
3. Run ../cpu.circ in Logisim
4. Right-click the RAM Module and click "Load Image"
5. Click the output file.
6. Start the clock; the program's now running.

Example on Linux:
```
$ cd assembler
$ python3 main_easy.py
This program compiles JLM files into files runnable on cpu.circ.
Use main_cmdline.py if you prefer command line flags.
What file do you want to compile? ../jlm_programs/fib.jlm
What do you want to call the output file? ../output.hex
$ logisim ../cpu.circ
```

Note: Both main\_easy.py and main\_cmdline.py change your working directory to assembler and read the files from there.

## JLM Description
Josh's Little Man, or JLM, is a programming language based on the Little Man Computer. It's a series of instructions that are assembled into subleq for the computer to understand.

Each instruction in JLM has to have its own line and vice-versa. Each instruction consists of an opcode and then an instruction (e.g. ADD a b).  
After the program, each variable is initialized in a JSON-like format.  
Example initializing a to 1 and b to 2: `{"a":1, "b":2}`  
Do NOT write over the variables Z, ASCIIZ, or NEGONE! These are special variables used by JLM instructions or libraries.  
You can convert a digit to ASCII by adding ASCIIZ and back to a digit by subtracting ASCIIZ. Also, NEGONE usually has -1 stored, so this can be useful.

Here is a list of all instructions and what they do:

### Foundational Instructions
You can do anything with the following 3 instructions:

#### HLT
  "Stops" machine. Must come ONLY and ALWAYS at the end of the program!  
  Implementation: executes subleq instruction 0 0 0.

#### LBL label
  Marks label as place to go to for other instructions.

#### SUBLEQ a b c
  The fundamental operation of CPU.
  Calculates b-a and stores the result in b.
  If b>0, the CPU goes to the next instruction; otherwise, it goes to label c.

### Other Instructions
Useful instructions that aren't foundational.

#### ADD a b
  Adds a and b and stores the result in a. (a = a + b)

#### SUB a b
  Calculates a minus b and stores the result in a. (a = a - b)

#### MOV a b
  Copies value in b to a. (a = b)

#### OUT a
  Copies value in a to "output" (address 0xff). Adds a to the Log chip's memory. (putchar(a))

#### INP a
  Copies the value in the input to a. This instruction will loop until something is typed. (a = getchar())

#### NOP
  Effectively does nothing. Technically, this sets Z to 0, but it should be 0 between instructions anyway.

#### \# comment
  Used for comments. Yes, the space is required. This is NOT recommended to take up clock cycles. For that, use NOP.

### Branch Instructions
Used for branching.

#### GOTO lbl
  Unconditionally goes to label lbl.

#### BRP a lbl
  Goes to lbl iff a is positive. Otherwise, the computer continues as normal.

#### BRZ a lbl
  Goes to lbl iff a=0. Otherwise, the computer continues as normal.



# Credits

The basic design of the Program Counter Area came from Whiteknight, the idea for the stepper came from the Scott CPU, and parts of the assembler came from David A Roberts. Although I didn't know this when I first built the CPU, the idea for subleq came from a paper by Farhad Mavaddat and Behrooz Parhami. All of these are cited below.

## Works Cited

David A Roberts, "subleq", <https://github.com/davidar/subleq>

Farhad Mavaddat and Behrooz Parhami, "URISC: The Ultimate Reduced Instruction Set Computer", <https://web.ece.ucsb.edu/~parhami/pubs_folder/parh88-ijeee-ultimate-risc.pdf>

J. Clark Scott, *But How Do It Know?*, <http://www.buthowdoitknow.com>

Whiteknight, "PC Branch.svg", <https://commons.wikimedia.org/wiki/File:PC_Branch.svg>

# License

[![Creative Commons License](https://i.creativecommons.org/l/by/4.0/88x31.png)](http://creativecommons.org/licenses/by/4.0/)  
This work by joshlsastro is licensed under a [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/).
