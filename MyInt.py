import sys


class MyInt:


    def __init__(self, val=0, bits=8, debug=False):
        self.debug = debug
        limits = (-(2 ** (bits - 1)), 2 ** (bits - 1) - 1)
        if isinstance(val, str):
            self.__list = [int(x) for x in val]
        elif isinstance(val, int):
            if not limits[0] <= val <= limits[1]:
                raise ValueError()
            self.__list = [int(x) for x in MyInt.to_bin(val, bits)]
        elif isinstance(val, list):
            self.__list = val
        elif isinstance(val, MyInt):
            self.__list = list(val)

        if len(self) > bits:
            self.__list = self.__list[len(self) - bits:]
        elif len(self) < bits:
            self.__list = self.__list[:1] * (bits - len(self)) + self.__list


    def __str__(self):
        return "".join([str(x) for x in self.__list])


    def __add__(self, other):
        if not isinstance(other, MyInt):
            other = MyInt(val=other, bits=len(self))
        carry = 0
        if len(self) != len(other):
            longest = len(max(self, other, key=lambda x: len(x)))
            a = MyInt(self, longest)
            b = MyInt(other, longest)
            result = MyInt(bits=longest)
        else:
            a = self
            b = other
            result = MyInt(bits=len(self))
        for i in reversed(range(len(a))):
            if self.debug:
                print(f'C={carry} {a[i]} + {b[i]} = ', end='')
            result[i], carry = MyInt.full_adder(a[i], b[i], carry)
            if self.debug:
                print(f'{result[i]} R={carry}')
        return result


    def add(self, other):
        result = self + other
        if self[0] == other[0] != result[0]:
            raise OverflowError()
        return result


    def __sub__(self, other):
        inv = -other
        if self.debug:
            print(f'{inv}')
        return self + inv


    def __neg__(self):
        if self.debug:
            print(f'{self} -> ', end='')
        return MyInt(-int(self))


    def __mul__(self, other):
        offset = 0

        extended_a = MyInt(self, len(self) * 2)
        extended_b = MyInt(other, len(other) * 2)

        if self.debug:
            print(f"{self} -> {extended_a}")
            print(f"{other} -> {extended_b}")
            print()

        res = MyInt(bits=len(self) * 2)

        for multiplier in reversed(extended_b):
            line = MyInt(bits=len(self) * 2)
            for i in reversed(range(len(line))):
                line[i] = extended_a[i] & multiplier
            if self.debug:
                print(f"{extended_a} & {multiplier} = {line} ({line << offset})")
            res = res + (line << offset)
            offset += 1
        return res


    def __abs__(self):
        return MyInt(abs(int(self)), len(self))


    def __lt__(self, other):
        return int(self) < int(other)


    def __le__(self, other):
        return int(self) <= int(other)


    def __gt__(self, other):
        return int(self) > int(other)


    def __ge__(self, other):
        return int(self) >= int(other)


    def __truediv__(self, other):
        if int(other) == 0:
            raise ZeroDivisionError()

        quot = MyInt()
        shifts = 1
        remainder = MyInt(abs(self))
        divisor = MyInt(abs(other))

        while not divisor[1]:
            divisor = divisor << 1
            shifts += 1

        if self.debug:
            print(f'Частно {quot} Остаток {remainder} Делитель {divisor}')
        while shifts != 0:
            if divisor > remainder:
                quot = quot << 1
                quot[-1] = 0
            elif divisor <= remainder:
                remainder = remainder - divisor
                quot = quot << 1
                quot[-1] = 1
            divisor = divisor >> 1
            shifts -= 1
            if self.debug:
                print(f'Частно {quot} Остаток {remainder} Делитель {divisor}')
        if self[0] ^ other[0]:
            quot = -quot
        return quot


    def __lshift__(self, other):
        return MyInt(self.__list[other:] + [0] * other, len(self))


    def __rshift__(self, other):
        return MyInt([0] * other + self.__list[:len(self) - other], len(self))


    def __eq__(self, other):
        return int(self) == int(other)


    def __getitem__(self, key):
        return self.__list[key]


    def __setitem__(self, key, value):
        self.__list[key] = value


    def __int__(self):
        return MyInt.from_bin(str(self), len(self))


    def __iter__(self):
        return self.__list.__iter__()


    def __len__(self):
        return len(self.__list)


    def copy(self):
        return MyInt(list(self), len(self))


    @staticmethod
    def from_bin(val, bits):
        if (int(val, 2) & (1 << (bits - 1))) != 0:
            return int(val, 2) - (1 << bits)
        return int(val, 2)


    @staticmethod
    def to_bin(n, bits):
        return ("{:0>%s}" % bits).format(bin(n & int("1" * bits, 2))[2:])


    @staticmethod
    def full_adder(a, b, c):
        return ((a ^ b) ^ c, ((a ^ b) & c) | (a & b))


    def bit_length(self):
        return int(self).bit_length()


class Unsigned:


    def __init__(self, val=0, bits=8):
        limits = (-2 ** bits, 2 ** bits - 1)
        if isinstance(val, str):
            self.__list = [int(x) for x in val]
        elif isinstance(val, int):
            if not limits[0] <= val <= limits[1]:
                raise ValueError()
            self.__list = [int(x) for x in MyInt.to_bin(val, bits)]
        elif isinstance(val, list):
            self.__list = val
        elif isinstance(val, MyInt):
            self.__list = list(val)
        if len(self) > bits:
            self.__list = self.__list[len(self) - bits:]
        elif len(self) < bits:
            self.__list = [0] * (bits - len(self)) + self.__list