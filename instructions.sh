#!/bin/bash

lines=$(curl --location --silent https://www.felixcloutier.com/x86/jcc -o /tmp/instructions)

echo $(grep -E '<td>J[A-Z]+ <em>.*' /tmp/instructions | sed -E 's/<td>(.*) <em>.*/\1/') > "/tmp/instructions"
