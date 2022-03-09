#!/usr/bin/env python3

from dataclasses import dataclass, fields
from enum import IntEnum
from pathlib import Path
from sys import argv
from typing import Type

from jump import Jump


@dataclass(frozen=True)
class BFGrammar:
    POINTER_INCREMENT: str = ">"
    POINTER_DECREMENT: str = "<"
    BYTE_INCREMENT: str = "+"
    BYTE_DECREMENT: str = "-"
    PRINT_BYTE: str = "."
    INPUT_BYTE: str = ","
    LOOP_BEGIN: str = "["
    LOOP_END: str = "]"

    @property
    def valid_codes(self):
        return [
            self.POINTER_INCREMENT,
            self.POINTER_DECREMENT,
            self.BYTE_INCREMENT,
            self.BYTE_DECREMENT,
            self.PRINT_BYTE,
            self.INPUT_BYTE,
            self.LOOP_BEGIN,
            self.LOOP_END,
        ]


class Const(IntEnum):
    NUM_DATA = 256
    TAPE_LENGTH = 256 ** 2


class Char:
    def __init__(self, num: int = 0):
        self._num = int(num % 256)

    def __add__(self, num):
        if isinstance(num, Char):
            return Char(self._num + num._num)
        elif isinstance(num, int):
            return Char(self._num + num)
        else:
            raise ValueError(f"{num} is not a valid type")

    def __sub__(self, num):
        if isinstance(num, Char):
            return Char(self._num - num._num)
        elif isinstance(num, int):
            return Char(self._num - num)
        else:
            raise ValueError(f"{num} is not a valid type")

    def __index__(self):
        return int(self._num)

    def __int__(self):
        return int(self._num)

    def __repr__(self):
        return str(self._num)


class BFIntepreter:
    def __init__(self, code: str):
        self.tape = self.transpile(code)
        self.jumps = self.jumptable(self.tape)
        # self.interpret(self.tape)

    def transpile(self, code) -> str:
        return "".join([c for c in code if c in BFGrammar.valid_codes])

    def jumptable(
        self, tape: str, begin: str = "[", end: str = "]"
    ) -> list[Jump]:
        stack: list[Jump] = []
        jumps: list[Jump] = []
        counter = 0
        for i, char in enumerate(self.tape):
            if char == begin:
                counter += 1
                stack.append(Jump(i, -1))
            elif char == end:
                counter -= 1
                stack[counter].end = i
                jumps.append(stack.pop())

        return sorted(jumps, key=lambda x: x.begin)

    def __repr__(self):
        return f"{self.tape} {self.jumps}"


    def interpret(self, tape: str):
        i, ptr = 0, Char(0)
        data: list[Char] = [Char() for _ in range(Const.NUM_DATA)]

        while i < len(tape):
            match tape[i]:
                case BFGrammar.POINTER_INCREMENT:
                    ptr += 1
                case BFGrammar.POINTER_DECREMENT:
                    ptr -= 1
                case BFGrammar.BYTE_INCREMENT:
                    data[ptr] += 1
                case BFGrammar.BYTE_DECREMENT:
                    data[ptr] -= 1
                case BFGrammar.PRINT_BYTE:
                    print(chr(int(data[ptr])), end="")
                case BFGrammar.INPUT_BYTE:
                    data[ptr] = Char(ord(input("enter: ")[0]))
                case BFGrammar.LOOP_BEGIN if data[ptr] == 0:
                    jump = [j.begin for j in self.jumps].index(i)
                    continue
                case BFGrammar.LOOP_END if data[ptr] != 0:
                    jump = [j.end for j in self.jumps].index(i)
                    continue
            i += 1


if len(argv) == 2:
    code = Path(argv[1]).read_text()
    bf = BFIntepreter(code)
    print(bf)
else:
    print("Usage: bf.py <file>")
