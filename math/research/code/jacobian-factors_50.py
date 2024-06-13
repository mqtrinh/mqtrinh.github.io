import itertools

log = open("C:/Users/Pabhassara/Dropbox/drafts/math/code/jacobian-factors_50.txt", "w")

def main():
    #hilbert_series(4, 3)
    hilbert_series(4, 5)
    hilbert_series(4, 7)
    hilbert_series(4, 9)
    hilbert_series(4, 11)
    hilbert_series(4, 13)
    hilbert_series(4, 15)
    hilbert_series(4, 17)

    '''
        master series for type BC_3:

        ((1 - q^m)/(1 - q))^3 + ((1 + q^m)/(1 + q))^3
        +   3*((1 - q^m)/(1 - q) + (1 + q^m)/(1 + q))*(1 - q^(2*m))/(1 - q^2)
        +   8*((1 - q^(3*m))/(1 - q^3) + (1 + q^(3*m))/(1 + q^3))
        +   6*(((1 - q^m)/(1 - q) + (1 + q^m)/(1 + q))((1 - q^(2*m))/(1 - q^2) + (1 + q^(2*m))/(1 + q^2)))
    '''

    compare_series(6, 5, [1, 1, 2, 2, 2, 1, 1])
    compare_series(6, 7, [1, 1, 2, 3, 3, 3, 3, 2, 1, 1])
    compare_series(6, 11, [1, 1, 2, 3, 4, 5, 6, 6, 6, 6, 5, 4, 3, 2, 1, 1])
    compare_series(6, 13, [1, 1, 2, 3, 4, 5, 7, 7, 8, 8, 8, 7, 7, 5, 4, 3, 2, 1, 1])
    compare_series(6, 17, [1, 1, 2, 3, 4, 5, 7, 8, 10,11,12,12,13,12,12,11,10,8, 7, 5, 4, 3, 2, 1, 1])

    #hilbert_series(8, 3)
    hilbert_series(8, 5)
    hilbert_series(8, 7)
    #hilbert_series(8, 9)
    #hilbert_series(8, 11)

    #hilbert_series(10, 3)
    hilbert_series(10, 7)
    #hilbert_series(10, 9)

    hilbert_series(12, 5)

# even number goes first

def hilbert_series(m, n):

    #   compute constants and the semigroup

    d = int((m - 1) * (n - 1) / 2)
    m_half = int(m / 2)
    amplitude_max = (m - 1) * n
    amplitude_mid = int(amplitude_max / 2 + 1)
    string = "m = " + str(m) + "\n" + "n = " + str(n) + "\n" + "d = " + str(d) + "\n"

    G = set()
    for a in range(0, m + 1):
        for b in range(0, n + 1):
            element = a * n + b * m
            if element < 2 * d:
                G.add(element)
    for element in range(2 * d, amplitude_max + 1):
            G.add(element)
    H = set(range(0, 2 * d)).difference(G)
    string += "semigroup = "
    for g in G:
        if g < 2 * d + 1:
            string += str(g) + ", "
    string += "...\n"
    #   string += "gaps = " + str(H) + "\n\n"

    #   compute seeds

    bases = []
    seeds = []
    modules = []
    shifts = []
    for A in itertools.combinations(range(amplitude_mid), m_half):
        B = set(A).copy()
        for a in A:
            B.add(amplitude_max - a)
        if is_basis(B, m):
            X = B.copy()
            for b in B:
                x = b + m
                while x <= amplitude_max:
                    X.add(x)
                    x += m
            Y = set(range(amplitude_max + 1)).difference(X)
            if len(Y) == d and max(Y) < 2 * d:
                temp = X.copy()
                S = set()
                flag = False
                while flag == False and len(temp) != 0:
                    s = min(temp)
                    for g in G:
                        element = s + g
                        if element in X:
                            temp.discard(element)
                        elif element in Y:
                            flag = True
                    if flag == False:
                        S.add(s)
                if flag == False:
                    bases.append(B)
                    seeds.append(S)
                    modules.append(X)
                    shifts.append(len(G.difference(X)))

    length = len(bases)
    string += "number of bases = " + str(length) + "\n\n"
    #for i in range(0, length):
    #    string += str(bases[i]) + "\n"
    #string += "\n"

    #   compute counts

    count_max = int((m / 2) * (n - 1) / 2 + 1)
    counts = [0 for j in range(0, count_max)]
    for i in range(0, length):
        counts[shifts[i]] += 1
    for j in range(0, count_max):
        string += "{:3}".format(str(j))
        for i in range(0, length):
            if shifts[i] == j:
                string += "*"
            else:
                string += " "
        string += "\n"
    string += "\n"
    string += "{:17}".format("hilbert series:") + formatter(counts) + "\n\n"

    log.write(string)

    return counts

def is_basis(Y, m):
    remainders = set()
    for y in Y:
        rem = y % m
        if rem in remainders:
            return False
        else:
            remainders.add(rem)
    return True

def compare_series(m, n, list_2):
    list_1 = hilbert_series(m, n)
    length = len(list_1)
    difference = [list_1[i] - list_2[i] for i in range(0, length)]
    log.write("{:17}".format("markov series:") + formatter(list_2) + "\n\n")
    log.write("{:17}".format("difference:") + formatter(difference) + "\n\n")
    net = 0
    for diff in difference:
        net += diff
    log.write("{:17}".format("net difference:") + str(net) + "\n\n")

def formatter(list):
    string = ""
    for i in list:
        if i != 0:
            string += "{:3}".format(str(i))
        else:
            string += "   "
    return string

main()
