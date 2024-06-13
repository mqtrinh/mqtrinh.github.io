# import itertools
import numpy as np
from numpy import exp, pi

def main():
    log = open("g-mod-u_10.txt", "w")
    output = ""

    p = 5
    f1 = sl3_mod_u(p)
    f2 = sl3_mod_u(p)
    f3 = sl3_mod_u(p)

    ###################################################################

    # f1.indicator(0, 0, 1, 1, 0, 0)
    # f1.operate(1, 1, 0, 0)
    # output += "Values of I operator:\n\n" + f1.str() + "\n"

    # f1.indicator(0, 0, 1, 1, 0, 0)
    # f1.operate(1, 0, 1, 0)
    # output += "Values of F_s operator:\n\n" + f1.str() + "\n"

    # f1.indicator(0, 0, 1, 1, 0, 0)
    # f1.operate(2, 0, 1, 0)
    # output += "Values of F_t operator:\n\n" + f1.str() + "\n"

    # f1.indicator(0, 0, 1, 1, 0, 0)
    # f1.operate(1, 0, 0, 1)
    # output += "Values of S_s operator:\n\n" + f1.str() + "\n"
    # f1.operate(2, 0, 1, 0)
    # output += "Values of F_tS_s operator:\n\n" + f1.str() + "\n"

    # f1.indicator(0, 0, 1, 1, 0, 0)
    # f1.operate(1, p * (p - 1), 1 - p, -1)
    # output += "Values of E_s operator:\n\n" + f1.str() + "\n"
    # f1.operate(1, p * (p - 1), 1 - p, -1)
    # output += "Values of E_s^2 operator:\n\n" + f1.str() + "\n"

    ###################################################################

    # SF = -S and F^2 = p^2 + k S (for fixed k) together imply (F^2 - p^2)(F + 1) = 0

    list1 = [[1, 0, 1, 0], [1, 0, 0, 1]]
    list2 = [[1, 0, 0, -1]]
    output += "Testing SF = -S:\n\n" + test_relation_custom(f1, f2, list1, list2, 1) + "\n"

    list1 = [[1, 0, 1, 0], [1, 0, 1, 0]]
    list2 = [[1, p * p, 0, -1]]
    output += "Testing F^2 relation:\n\n" + test_relation_custom(f1, f2, list1, list2, 1) + "\n"

    output += "Testing idempotent relation:\n\n" + test_relation_idempotent(f1, f2) + "\n"
    output += "Testing braid relation:\n\n" + test_relation_braid(f1, f2) + "\n"

    # output += f1.str() + "\n"
    # output += "Testing 1st tangle relation:\n\n" + test_relation_tangle_1(f1, f2) + "\n"
    # output += "Testing E-braid relation:\n\n" + test_relation_braid_e(f1, f2) + "\n"
    # output += "Testing 2nd tangle relation:\n\n" + test_relation_tangle_2(f1, f2) + "\n"
    # output += f1.str() + "\n"

    ###################################################################

    # list1 = [[1, 0, 1, 0], [2, 0, 0, 1], [1, 0, 1, 0]]
    # list2 = [[2, 0, 1, 0], [1, 0, 0, 1], [2, 0, 1, 0]]
    # output += "Testing FSF relation:\n\n" + test_relation_custom(f1, f2, list1, list2, 1)

    # list1 = [[1, 0, 0, 1], [2, 0, 0, 1]]
    # list2 = [[2, 0, 0, 1], [1, 0, 0, 1]]
    # output += "Testing SS relation:\n\n" + test_relation_custom(f1, f2, list1, list2, 1)

    list1 = [[1, 0, 1, 0], [2, 0, 0, 1], [1, 0, 0, 1]]
    list2 = [[2, 0, 1, 0], [1, 0, 0, 1], [2, 0, 0, 1]]
    # output += "Testing SSF relation:\n\n" + test_relation_custom(f1, f2, list1, list2, 1) + "\n"

    '''
    f3.indicator(0, 0, 1, 1, 0, 0)
    f3.operate(1, 0, 1, 0)
    f3.operate(2, 0, 0, 1)
    f3.operate(1, 0, 1, 0)
    f3.scale(-1)
    f1.add(f3)
    f3.indicator(0, 0, 1, 1, 0, 0)
    f3.operate(1, 0, 0, 1)
    f3.operate(2, 0, 0, 1)
    f3.scale(p)
    f1.add(f3)

    f3.indicator(0, 0, 1, 1, 0, 0)
    f3.operate(2, 0, 1, 0)
    f3.operate(1, 0, 0, 1)
    f3.operate(2, 0, 1, 0)
    f3.scale(-1)
    f2.add(f3)
    f3.indicator(0, 0, 1, 1, 0, 0)
    f3.operate(2, 0, 0, 1)
    f3.operate(1, 0, 0, 1)
    f3.scale(p)
    f2.add(f3)

    output += "Testing S_sS_tF_s - F_sS_tF_s + pS_tS_s == S_tS_sF_t - F_tS_sF_t + pS_sS_t:\n\n" + f1.equals(f2) + "\n"
    '''

    # list1 = [[1, 0, 0, 1], [2, 0, 1, 0], [1, 0, 0, 1]]
    # list2 = [[2, 0, 0, 1], [1, 0, 1, 0], [2, 0, 0, 1]]
    # output += "Testing SFS relation:\n\n" + test_relation_custom(f1, f2, list1, list2, 1) + "\n"

    # list1 = [[1, 0, 0, 1], [2, 0, 0, 1], [1, 0, 0, 1]]
    # list2 = [[2, 0, 0, 1], [1, 0, 0, 1], [2, 0, 0, 1]]
    # output += "Testing SSS relation:\n\n" + test_relation_custom(f1, f2, list1, list2, 1) + "\n"

    list1 = [[1, 0, 1, 0], [2, 0, 0, 1], [1, 0, 1, -1]]
    list2 = [[2, 0, 1, 0], [1, 0, 0, 1], [2, 0, 1, -1]]
    test_relation_custom(f1, f2, list1, list2, 1) + "\n"

    f3.indicator(0, 0, 1, 1, 0, 0)
    f3.operate(2, 0, 0, 1)
    f3.operate(1, 0, 0, 1)
    f3.scale(p)
    f1.add(f3)

    f3.indicator(0, 0, 1, 1, 0, 0)
    f3.operate(1, 0, 0, 1)
    f3.operate(2, 0, 0, 1)
    f3.scale(p)
    f2.add(f3)

    output += "Testing p^2F_s^{-1}S_tF_s + pS_sS_t == p^2F_t^{-1}S_sF_t + pS_tS_s:\n\n" + f1.equals(f2) + "\n"

    ###################################################################

    log.write(output)
    log.close()
    print(output)

#

def test_relation_idempotent(f1, f2):
    p = f1.p
    list1 = [[1, p * (p - 1), 1 - p, -1], [1, p * (p - 1), 1 - p, -1]]
    list2 = [[1, p * (p - 1), 1 - p, -1]]
    constant = 2 * p * (p - 1)
    return test_relation_custom(f1, f2, list1, list2, constant)

def test_relation_braid(f1, f2):
    list1 = [[1, 0, 1, 0], [2, 0, 1, 0], [1, 0, 1, 0]]
    list2 = [[2, 0, 1, 0], [1, 0, 1, 0], [2, 0, 1, 0]]
    return test_relation_custom(f1, f2, list1, list2, 1)

def test_relation_tangle_1(f1, f2):
    p = f1.p
    list1 = [[1, p * (p - 1), 1 - p, -1], [2, p * (p - 1), 1 - p, -1], [1, p * (p - 1), 1 - p, -1]]
    list2 = [[1, p * (p - 1), 1 - p, -1]]
    return test_relation_custom(f1, f2, list1, list2, p * p * (p - 1) * (p - 1))

def test_relation_braid_e(f1, f2):
    p = f1.p
    list1 = [[1, p * (p - 1), 1 - p, -1], [2, p * (p - 1), 1 - p, -1], [1, p * (p - 1), 1 - p, -1]]
    list2 = [[2, p * (p - 1), 1 - p, -1], [1, p * (p - 1), 1 - p, -1], [2, p * (p - 1), 1 - p, -1]]
    return test_relation_custom(f1, f2, list1, list2, 1)

def test_relation_tangle_2(f1, f2):
    p = f1.p
    list1 = [[1, p * (p - 1), 1 - p, -1], [2, 0, 1, 0], [1, 0, 1, 0]]
    list2 = [[1, p * (p - 1), 1 - p, -1], [2, p * (p - 1), 1 - p, -1]]
        # constant = p - 1
    constant = -(p - 2)
    return test_relation_custom(f1, f2, list1, list2, constant)

def test_relation_custom(f1, f2, list1, list2, scalar):
    length1 = len(list1)
    length2 = len(list2)
    f1.indicator(0, 0, 1, 1, 0, 0)
    f2.indicator(0, 0, 1, 1, 0, 0)
    for i in range(0, length1):
        f1.operate(list1[i][0], list1[i][1], list1[i][2], list1[i][3])
    for i in range(0, length2):
        f2.operate(list2[i][0], list2[i][1], list2[i][2], list2[i][3])
    f2.scale(scalar)
    return f1.equals(f2)

#

def formatter(z):
    # https://docs.python.org/2/library/string.html#formatspec
    real = z.real
    imag = z.imag
    if np.isclose(real, 0) and np.isclose(imag, 0):
        return " " * 9 + "   " + " " * 7 + " "
    elif np.isclose(real, 0):
        return " " * 9 + "   " + "{:7.2f}I".format(z.imag)
    elif np.isclose(imag, 0):
        return "{:9.2f}".format(z.real) + "   " + " " * 7 + " "
    else:
        return "{0:9.2f} + {1:7.2f}I".format(z.real, z.imag)

#

def mod_inverse(p, n):
    return pow(n, -1, p)

#

def root_of_unity(n, i):
    return exp(2j * pi * i / n)

#

def symppairing(left_1, left_2, right_1, right_2):
    return -left_1 * right_2 + left_2 * right_1

#

class sl2_mod_u:
    def __init__(self, p):
        self.p = p
        self.array = np.zeros((p, p), dtype=complex)

    def str(self):
        string = ""
        for x1 in range(0, self.p):
            for x2 in range(0, self.p):
                if x1 != 0 or x2 != 0:
                    z = self.array[x1, x2]
                    # https://docs.python.org/2/library/string.html#formatspec
                    string += formatter(z)
                    string += " " * 5
                else:
                    string += " " * 19
            string += "\n"
        return string

    def indicator(self, x1, x2):
        self.array.fill(0)
        self.array[x1, x2] = 1

    def f(self):
        self.operate(0, 1, 0)

    def e(self):
        p = self.p
        self.operate(p * (p - 1), 1 - p, -1)

    def operate(self, coeff_constant, coeff_fourier, coeff_uniform):
        temp = np.zeros((self.p, self.p), dtype=complex)
        for y1 in range(0, self.p):
            for y2 in range(0, self.p):
                if (y1 != 0 or y2 != 0):
                    temp[y1, y2] += coeff_constant * self.array[y1, y2]
                    for x1 in range(0, self.p):
                        for x2 in range(0, self.p):
                            if (x1 != 0 or x2 != 0):
                                root = root_of_unity(self.p, symppairing(x1, x2, y1, y2))
                                temp[y1, y2] += (coeff_fourier * root + coeff_uniform) * self.array[x1, x2]
        self.array = temp

#

def cell_1(p):
    list = []
    for x1 in range(0, p):
        list.append([0, 0, 1, x1, 1, 0])
    return list

def cell_2(p):
    list = []
    for y3 in range(0, p):
        list.append([0, 1, y3, 1, 0, 0])
    return list

def cell_21(p):
    list = []
    for x1 in range(0, p):
        for y3 in range(0, p):
            list.append([1, (-x1) % p, y3, x1, 1, 0])
    return list

def cell_12(p):
    list = []
    for x1 in range(0, p):
        for y3 in range(0, p):
            list.append([0, 1, y3, x1, (-y3) % p, 1])
    return list

def cell_121(p):
    list = []
    for x1 in range(0, p):
        for x2 in range(0, p):
            for y2 in range(0, p):
                y3 = (-x1 - x2 * y2) % p
                list.append([1, y2, y3, x1, x2, 1])
    return list

#

def sl3_coset_rep(p, left_1, left_2, left_3, right_1, right_2, right_3):
    # (a, d, g) = (right_1, right_2, right_3)
    # (C, F, I) = (left_1, left_2, left_3)
    #           = (d * h - e * g, b * g - a * h, a * e - b * d)

    #  0      -  g * e  +  d * h  =  left_1
    #  g * b  +  0      -  a * h  =  left_2
    # -d * b  +  a * e  +  0      =  left_3

    #  0   -g    d
    #  g    0   -a
    # -d    a    0

    if right_1 != 0:
        r = mod_inverse(p, right_1)
        # b = 0
        e = (left_3 * r) % p
        h = (-left_2 * r) % p
        if left_3 != 0:
            ell = mod_inverse(p, left_3)
            return [right_1, 0, 0, right_2, e, 0, right_3, h, ell] # id
        else:
            #e == 0
            ell = mod_inverse(p, left_2)
            return [right_1, 0, 0, right_2, 0, ell, right_3, h, 0] # s2
    else:
        if right_2 != 0:
            r = mod_inverse(p, right_2)
            b = (-left_3 * r) % p
            # e = 0
            h = (left_1 * r) % p
            if left_3 != 0:
                ell = mod_inverse(p, left_3)
                return [0, b, 0, right_2, 0, 0, right_3, h, ell] # s1
            else:
                # b == 0
                ell = mod_inverse(p, left_1)
                return [0, 0, ell, right_2, 0, 0, right_3, h, 0] # s2 s1
        else:
            # left_3 == 0
            r = mod_inverse(p, right_3)
            b = (left_2 * r) % p
            e = (-left_1 * r) % p
            # h = 0
            if left_2 != 0:
                ell = mod_inverse(p, left_2)
                return [0, b, 0, 0, e, ell, right_3, 0, 0] # s1 s2
            else:
                # b == 0
                ell = mod_inverse(p, left_1)
                return [0, 0, ell, 0, e, 0, right_3, 0, 0] # s1 s2 s1 = s2 s1 s2

def sl3_act(p, coord, matrix):
    a = matrix[0]
    b = matrix[1]
    c = matrix[2]
    d = matrix[3]
    e = matrix[4]
    f = matrix[5]
    g = matrix[6]
    h = matrix[7]
    i = matrix[8]

    x1 = coord[3]
    x2 = coord[4]
    x3 = coord[5]
    y1 = coord[0]
    y2 = coord[1]
    y3 = coord[2]

    # https://en.wikipedia.org/wiki/Invertible_matrix#Inversion_of_3_%C3%97_3_matrices

    ai = e * i - f * h
    di = c * h - b * i
    gi = b * f - c * e
    bi = f * g - d * i
    ei = a * i - c * g
    hi = c * d - a * f
    ci = d * h - e * g
    fi = b * g - a * h
    ii = a * e - b * d

    return [(ai * y1 + bi * y2 + ci * y3) % p,
        (di * y1 + ei * y2 + fi * y3) % p,
        (gi * y1 + hi * y2 + ii * y3) % p,
        (a * x1 + b * x2 + c * x3) % p,
        (d * x1 + e * x2 + f * x3) % p,
        (g * x1 + h * x2 + i * x3) % p]

#

class sl3_mod_u:
    def __init__(self, p):
        # self.COL_WIDTH = 24
        self.COL_SPACE = 10
        # self.STAGGER = 3

        self.p = p
        self.array = np.zeros((p, p, p, p, p, p), dtype=complex)

    #

    def str(self):
        p = self.p
        string = self.str_scalings([[0, 0, 1, 1, 0, 0]], "  e") + "\n"
        string += self.str_scalings(cell_1(p), "  s") + "\n"
        string += self.str_scalings(cell_2(p), "  t") + "\n"
        string += self.str_scalings(cell_21(p), " ts") + "\n"
        string += self.str_scalings(cell_12(p), " st") + "\n"
        string += self.str_scalings(cell_121(p), "sts") + "\n"
        return string

    def str_scalings(self, list, label):
        p = self.p
        length = len(list)
        string = label + " "
        trivial = True
        string_temp = ""
        for i in range(0, length):
            for t1 in range(1, p):
                if i != 0 or t1 != 1:
                    string_temp += " " * 3 + " "
                v = list[i]
                w3 = (v[3] * t1) % p
                w4 = (v[4] * t1) % p
                w5 = (v[5] * t1) % p
                for t2 in range(1, p):
                    w0 = (v[0] * t2) % p
                    w1 = (v[1] * t2) % p
                    w2 = (v[2] * t2) % p
                    val = self.array[w0, w1, w2, w3, w4, w5]
                    if not np.isclose(val, 0):
                        trivial = False
                    string_temp += formatter(val) + " "
                string_temp += "\n"
        if trivial == False:
            string += string_temp
        else:
            string += "\n"
        return string

    #

    def equals(self, other):
        p = self.p
        string = self.equals_scalings(other, [[0, 0, 1, 1, 0, 0]], "  e") + "\n"
        # count = 0
        string += self.equals_scalings(other, cell_1(p), "  s") + "\n"
        string += self.equals_scalings(other, cell_2(p), "  t") + "\n"
        string += self.equals_scalings(other, cell_21(p), " ts") + "\n"
        string += self.equals_scalings(other, cell_12(p), " st") + "\n"
        string += self.equals_scalings(other, cell_121(p), "sts") + "\n"
        return string

    def equals_scalings(self, other, list, label):
        p = self.p
        length = len(list)
        string = label + " "
        count = 0
        first = True
        for i in range(0, length):
            for t1 in range(1, p):
                string_temp = ""
                count_temp = 0
                if not first:
                    string_temp += " " * 3 + " "
                v = list[i]
                w3 = (v[3] * t1) % p
                w4 = (v[4] * t1) % p
                w5 = (v[5] * t1) % p
                for t2 in range(1, p):
                    w0 = (v[0] * t2) % p
                    w1 = (v[1] * t2) % p
                    w2 = (v[2] * t2) % p
                    val_self = self.array[w0, w1, w2, w3, w4, w5]
                    val_other = other.array[w0, w1, w2, w3, w4, w5]
                    if not np.isclose(val_self, val_other):
                        string_temp += formatter(val_self) + " != " + formatter(val_other) + " "
                        count_temp += 1
                        count += 1
                if count_temp != 0:
                    if first:
                        first = False
                    string += string_temp + "\n"
        total = length * (p - 1) * (p - 1)
        if count == 0:
            string += "\n"
        string += "\n" + "Total number of mismatches: " + str(count) + " out of " + str(total) + "\n"
        return string

    #

    def scale(self, a):
        self.array = self.array * a

    #

    def add(self, other):
        self.array = np.add(self.array, other.array)

    #

    def indicator(self, y1, y2, y3, x1, x2, x3):
        self.array.fill(0)
        self.array[y1, y2, y3, x1, x2, x3] = 1

    #

    def f(self, i):
        self.operate(i, 0, 1, 0)

    def e(self, i):
        p = self.p
        self.operate(i, p * (p - 1), 1 - p, -1)

    def operate(self, i, a, b, c):
        p = self.p
        temp = np.zeros((p, p, p, p, p, p), dtype=complex)
        temp = self.operate_scalings(i, a, b, c, temp, [[0, 0, 1, 1, 0, 0]])
        temp = self.operate_scalings(i, a, b, c, temp, cell_1(p))
        temp = self.operate_scalings(i, a, b, c, temp, cell_2(p))
        temp = self.operate_scalings(i, a, b, c, temp, cell_21(p))
        temp = self.operate_scalings(i, a, b, c, temp, cell_12(p))
        temp = self.operate_scalings(i, a, b, c, temp, cell_121(p))
        self.array = temp

    def operate_scalings(self, i, a, b, c, temp, list):
        p = self.p
        for v in list:
            for t1 in range(1, p):
                for t2 in range(1, p):
                    x1 = (v[3] * t1) % p
                    x2 = (v[4] * t1) % p
                    x3 = (v[5] * t1) % p
                    y1 = (v[0] * t2) % p
                    y2 = (v[1] * t2) % p
                    y3 = (v[2] * t2) % p
                    val = self.array[y1, y2, y3, x1, x2, x3]
                    if val != 0:
                        matrix = sl3_coset_rep(self.p, y1, y2, y3, x1, x2, x3)
                        temp = self.operate_local(i, a, b, c, temp, matrix, val)
        return temp

    def operate_local(self, i, coeff_constant, coeff_fourier, coeff_uniform, temp, matrix, val):
        p = self.p
        aux = sl2_mod_u(p)
        aux.indicator(1, 0)
        aux.operate(coeff_constant, coeff_fourier, coeff_uniform)
        for z1 in range(0, p):
            for z2 in range(0, p):
                if (z1 != 0 or z2 != 0):
                    for t in range(1, p):
                        if i == 1:
                            coord_sl2 = [0, 0, t, z1, z2, 0]
                        elif i == 2:
                            coord_sl2 = [0, (-t * z2) % p, (t * z1) % p, t, 0, 0]
                        else:
                            print("ERROR")
                        coord = sl3_act(p, coord_sl2, matrix)
                        c0 = coord[0]
                        c1 = coord[1]
                        c2 = coord[2]
                        c3 = coord[3]
                        c4 = coord[4]
                        c5 = coord[5]
                        if t == 1:
                            # temp[c0, c1, c2, c3, c4, c5] += coeff_constant * val # / ((p - 1) * (p - 1))
                            temp[c0, c1, c2, c3, c4, c5] += val * aux.array[z1, z2]
                        # / (p - 1)
                        # * root_of_unity(p - 1, t)
        return temp

#

main()
