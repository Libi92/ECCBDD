import datetime
from functools import reduce

from algo import curve
from algo.ecc import EC, Coord


class CryptoSystem:
    def __init__(self, g, ec):
        self.g = g
        self.ec = ec

    def bit_invert(self, b):
        inv = map(lambda x: '0' if x == '1' else '1', b)
        return reduce(lambda x, y: x + y, inv)

    def constructPxPyMetrix(self, decimal_list):
        pxy_list = []
        list_5 = [Coord(0, 0) for i in range(5)]
        for i in range(len(decimal_list)):
            if i != 0 and i % 5 == 0:
                pxy_list.append(list_5)
                list_5 = [Coord(0, 0) for i in range(5)]
            py = i
            px = decimal_list[i] + i
            list_5[i % 5] = Coord(px, py)

        pxy_list.append(list_5)

        return pxy_list

    def get_gMatrix(self):
        return [self.ec.mul(self.g, i) for i in range(1, 6)]

    def add(self, a, b):
        return [self.ec.add(m, n) for m, n in zip(a, b)]

    def sub(self, a, b):
        return [self.ec.add(m, self.ec.neg(n)) for m, n in zip(a, b)]

    def matrixShiftAdd(self, a_list, b):
        c_list = []
        for a in a_list:
            c = self.add(a, b)
            b.append(b.pop(0))
            c_list.append(c)

        return c_list

    def matrixShiftSub(self, a_list, b):
        c_list = []
        for a in a_list:
            c = self.sub(a, b)
            b.append(b.pop(0))
            c_list.append(c)

        return c_list

    def print_matrix(self, matrix):
        for x in matrix:
            print(str(x.x) + ', ' + str(x.y))

    def extractPx(self, pxy_list):
        extracted = []
        for list_5 in pxy_list:
            ext = map(lambda p: Coord(p.x - p.y, p.y), list_5)
            extracted.append(list(ext))

        return extracted

    def encode(self, message):
        start_time = datetime.datetime.now().microsecond
        eq_ascii = [ord(x) for x in message]
        print('ascii: ', eq_ascii)
        bin_array = [format(x, '08b') for x in eq_ascii]
        num_append = len(bin_array) % 5
        if num_append != 0:
            num_append = 5 - num_append
            for i in range(num_append):
                bin_array.append(format(0, '08b'))
        print('binary: ', bin_array)

        inv_array = [self.bit_invert(b) for b in bin_array]
        print('inverse binary: ', inv_array)

        decimal_arr = [int(x, 2) for x in inv_array]
        print('decimal: ', decimal_arr)

        pxy_matrix = self.constructPxPyMetrix(decimal_arr)
        print('PxPy (5x2)matrix: ', pxy_matrix)
        g_matrix = self.get_gMatrix()
        print('(5x2)g matrix: ')
        self.print_matrix(g_matrix)

        mapped_list = self.matrixShiftAdd(pxy_matrix, g_matrix)
        print('encoded matrix: ')
        for x in mapped_list: self.print_matrix(x)

        end_time = datetime.datetime.now().microsecond

        execution_time = end_time - start_time
        print('Encoding time: ', execution_time, 'μs')

        return mapped_list

    def decode(self, encoded_list):
        start_time = datetime.datetime.now().microsecond
        g_matrix = self.get_gMatrix()
        subs_matrix = self.matrixShiftSub(encoded_list, g_matrix)
        print('Subtracted Matrix: ')
        for x in subs_matrix: self.print_matrix(x)
        extracted = self.extractPx(subs_matrix)
        print('Px Extracted: ')
        for x in extracted: self.print_matrix(x)

        temp = []
        for x in extracted: temp.extend(x)
        extracted = temp

        bin_array = [format(x.x, '08b') for x in extracted]
        print(bin_array)

        inv_bits = [self.bit_invert(b) for b in bin_array]
        decimal_arr = [int(x, 2) for x in inv_bits]
        print(decimal_arr)
        chars = [chr(d) for d in decimal_arr]
        plain_text = reduce(lambda x, y: x + y, chars)

        end_time = datetime.datetime.now().microsecond
        execution_time = end_time - start_time
        print("Decoding time: ", execution_time, 'μs')
        return plain_text


if __name__ == '__main__':
    plain_text = input("Enter your message: ")
    curve = curve.P256
    g = Coord(curve.gy, curve.gy)
    ec = EC(curve.a, curve.b, curve.p)
    crypto = CryptoSystem(g, ec)
    encoded = crypto.encode(plain_text)
    decoded = crypto.decode(encoded)
    print(decoded)
