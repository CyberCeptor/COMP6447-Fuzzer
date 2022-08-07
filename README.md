# Alt-F5 Fuzzer

## Description
This project aims to be a fuzzer for programs that take in data from stdin and
will attempt to crash that program in a meaninful way that could potentially be
exploited.

## Installation
This fuzzer is written in Python 3 and runs on a Linux operating system.

1. Installing dependencies
   `pip3 install defusedxml` - for xml based mutations.
2. Clone the repository

## Usage
The general usage of the fuzzer is `./fuzzer <binary> <sample input>`. The binary
should be marked as executable. Sample input should be a file containing non-crashing
input to the binary.

## Authors and acknowledgment
Written by Aleesha Bunrith, Cameron McGowan, Jenson Morgan and Matthew Richards.

## Functionality
Our fuzzer design consists of three components. Firstly, there is a format finder. This simply takes in the given sample input for the program and runs some basic tests on them to try and determine the format of the input (i.e. csv, json, xml etc). The binary is also examined to find all the addresses of conditional jump instructions and their two paths. 

Next are the mutation strategies. These consist of specific ones for each format and a generic plaintext one. The purpose of these is to take in a byte string and mutate it. Within each strategy there are many sub-mutators. Plaintext has 4: repeated input, substring selection, bit flips and byte flips. Json contains 7: integer corruption, extreme integer values, float infinities, float nans, repeated lists, repeated entries and type changes. CSV has 7 as well: repeated rows, empty rows, repeated columns, empty columns, missing header, cell multiplication and missing cells. XML has 6 mutation strategies: very deep nesting of tags, repeated attributes, href attribute corruption, tag repetition, root tag manipulation and repeated children.

The way we measure how much of the binary has been explored is by using gdb. For this, we added scripts to generate all the addresses of conditional jumps for their two paths in the binary. This is then fed as breakpoints to gdb. However, we don't want to actually stop at them, but instead just record that we touched those addresses which is why the commands to continue are added to the breakpoints. Then there is some code to count up the breakpoints that were hit.

One of the main design choices made was to have the mutators be deterministic in their output. This lets us use the excellent scipy library to try and find the best way to explore the binary through the optimization package. However, scipy works in floats and vectors, not integer parameters that are usually required for mutation. 

Finally, there is the testing component of the fuzzer. For this stage, the fuzzer starts up many threads (limit based on cpu count) and each one has different tasks to carry out. There are also some simple cases that can be done separately as seen in the `try_simple` function. Half of the other threads are dedicated to just trying many things as fast as possible with many mutation strategies in the allocated 180 seconds. The last group of threads work with gdb to change their mutations based on the branch coverage of their inputs. This uses the `scipy.optimize.minimize` function to guide the exploration of inputs. For each attempt of input there is a check at the end for the return code. If this is not 0 or 1, bad.txt is written with the offending input. Care has been taken to kill the fuzzer almost instantly in this case and to not allow multiple writers to the file. 

All aspects of the fuzzer internals include timeouts in order to make sure that nothing gets stuck at some points. This also allows the fuzzer to attempt many different strategies without much compromise. It should also be noted that the number of threads chosen aims to saturate the available cpu power and it is unlikely that other program will be usable in this time. 

Each mutator strategy comes with a human readable description of what it does. When an offending input is discovered, the strategy that produced it is displayed to the user with details on the order of operations performed to make it happen. The gdb led mutation strategy also prints out its progress with the breakpoint 'score'. The higher this score is, the more code paths that were taken in the binary. 

