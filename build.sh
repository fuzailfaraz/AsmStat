#!/bin/bash
# Compile Assembly code into Linux shared library
nasm -f elf64 math.asm -o math.o
ld -shared -o libmath.so math.o
