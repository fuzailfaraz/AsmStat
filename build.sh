#!/bin/bash
nasm -f elf64 math.asm -o math.o
ld -shared -o libmath.so math.o
