#!/usr/bin/env python3
import re
import sys
import subprocess

def get_instructions():
    # get jump instructions in a list
    p = subprocess.call(['./instructions.sh'])

    f = open('/tmp/instructions', 'r')
    instructions = f.readlines()[0].split(' ')
    instructions = [instruction.rstrip().lower() for instruction in instructions]
    f.close()

    return set(instructions)

def get_disassembly(program, instructions):
    # get addresses that are jumped to
    subprocess.Popen(f'objdump -d {program} > /tmp/disass', shell=True).communicate()

    with open('/tmp/disass2', 'w') as disass:
        with open('/tmp/disass', 'r') as f:
            for line in f:
                if not (line in ['', '\n'] or re.match(fr'({program}: .*)', line) 
                    or re.match(r'Disassembly of section .*:|[0-9a-f]{8} <.*>:', line) 
                    or '...' in line):
                    if any(instruction in line for instruction in instructions):
                        if re.match(r'.*:.*j[a-z ].*<.*>', line):
                            disass.write(line)

def get(program):
    jmp_addr = []
    breakpoints = []
    instructions = get_instructions()

    get_disassembly(program, instructions)

    subprocess.Popen("cut -f1,3,4 /tmp/disass2 | cut -d'<' -f1 > /tmp/disass3", shell=True).communicate()

    # add addresses that are being jumped to to the breakpoints list
    # add the address of the jmp instruction to the jmp_addr list
    with open('/tmp/disass3', 'r') as f:
        for line in f:
            # print(line, end='')
            jmp_addr.append(line.split(':')[0])

            info = re.split(r'j[a-z ]+', line)
            # print(info)
            breakpoints.append(info[1].strip())

    # add each subsequent instruction after each address in the jmp_addr list
    f = open('/tmp/disass', 'r')
    lines = f.readlines()
    for i, line in enumerate(lines):
        if any(line.startswith(addr) for addr in jmp_addr):
            breakpoints.append(lines[i + 1])
    f.close()

    print(len(jmp_addr))
    print(len(breakpoints))

    return breakpoints

