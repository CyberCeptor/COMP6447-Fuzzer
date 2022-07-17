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
Our fuzzer design consists of three components. Firstly, there is a format finder. This simply takes in the given sample input for the program and runs some basic tests on them to try and determine the format of the input (i.e. csv, json, xml etc).

Next we have different methods of creating inputs. These consist of two types and currently we have implemented the first one being our plaintext mutator. This takes in a sample input of any format and manipulates it to create a new input we can manipulate. Currently we have created a basic mutator which contains 5 sub-mutators. These are providing an empty file, a variable super long length file, random substrings of the input, random bit flips and random byte flips. The basic mutator implements an iterable interface and so it can be used in a for loop to get the next tests.

The other method of creating inputs which is not currently implemented consists of creating input type specific inputs. Which type to create will depend on the results of our format finder. This will generate sample inputs which utilise creating the structures available for that input type. This will allow us to utilise features of the input type which were not present in the original sample input (or were only used a limited number of times etc). This would generate data which could be used for any program which takes in data of that input type.
Finally, we have our testing component of our fuzzer. In this stage, the fuzzer just keeps trying the inputs generated from the mutators or type specific generators until a non-zero exit code is reached. Once it finds an input that causes a crash, the fuzzer writes out the input that caused it to ‘bad.txt’. The fuzzer also has a timeout for each run of the binary and a timeout for each generator type. The aim of this is to get it to spend ‘equal’ amounts of time on each input method to try and find something that makes it crash, rather than disproportionately allocating time to methods which take longer to generate or run. 

Currently, the fuzzer also prints out the length of the offending input which can be useful in determining whether the problem is simply due to a specific length input. In future we plan to print out further details, particularly in the case of the input type specific data (such as the number of a certain structure used etc).
