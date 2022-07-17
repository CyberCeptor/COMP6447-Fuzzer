# Alt-F5 Fuzzer

## Name
Choose a self-explaining name for your project.

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
TODO
