import itertools

log = open("cells_triangular.txt", "w")

def main():
    output = ""

    output += semigroups(3, 4, {})
    output += semigroups(3, 4, {1, 2})

    output += semigroups(4, 5, {})

    output += semigroups(4, 7, {})
    output += semigroups(4, 7, {1, 2, 3, 5})

    output += semigroups(5, 7, {})
    output += semigroups(5, 7, {1, 2, 3, 4, 6})

    # output += semigroups(5, 8, {})
    # output += semigroups(5, 8, {1, 2, 3, 4, 6, 7, 9})

    log.write(output)
    log.close()
    print(output)

def semigroups(N, M, X):
    # for now assume M, N coprime
    MILNOR = (M - 1) * (N - 1)
    DELTA = int(MILNOR / 2)
    M_INVERSE = pow(M, -1, N)
    string = "N = " + str(N) + "\n" + "M = " + str(M) + "\n" + "X = " + str(X) + "\n\n"

    G = set()
    for a in range(0, M + 1):
        for b in range(0, N + 1):
            temp = a * N + b * M
            if temp < MILNOR:
                G.add(temp)
    H = set(range(0, MILNOR)).difference(G)
    string += "set of gaps " + str(H) + "\n\n"

    A = [(M * i) % N for i in range(N)]
    B = [int((A[i] + M - A[(i + 1) % N]) / N) for i in range(N)]

    count = 0
    # ngen = []
    ngen = []
    area = []
    codinv = []
    cogen = []
    cogen_exp = []
    gen = []
    gen_exp = []

    for cochar in itertools.product(range(MILNOR + 1), repeat=N):
        flag = False

        sum = 0
        for i in range(0, N):
            sum += cochar[i]
            if cochar[(i + 1) % N] - cochar[i] > B[i]:
                flag = True
        if sum != DELTA:
            flag = True

        if flag == False:
            ng = []
            minimum = DELTA
            for i in range(N):
                temp = A[i] + N * cochar[i]
                ng.append(temp)
                if temp < minimum:
                    minimum = temp
            ng_zeroed = [ng[i] - minimum for i in range(N)]
            for k in ng_zeroed:
                if k in X:
                    flag = True
            
            if flag == False:
                count += 1

                ngen.append(ng_zeroed)
                area.append(DELTA - minimum)
                c = 0
                for i in range(N):
                    for j in range(1, M):
                        temp = ng[i] + j
                        remainder = (M_INVERSE * temp) % N
                        if temp >= A[remainder] and temp < ng[remainder]:
                            c += 1
                codinv.append(c)

                cog = []
                for k in H:
                    i = (M_INVERSE * (k + minimum)) % N
                    j = (M_INVERSE * (k + minimum) + 1) % N
                    temp_i = ng_zeroed[i]
                    temp_j = ng_zeroed[j]
                    if temp_i > k and temp_i <= k + N and temp_j <= k + M:
                        cog.append(k)
                cogen.append(cog)

                cog_exp = []
                for k in cog:
                    ng_count = 0
                    for j in ng_zeroed:
                        if k + N < j and j < k + N + M:
                            ng_count += 1
                    cog_exp.append(ng_count)
                cogen_exp.append(cog_exp)

                jord = [0 for i in range(M)]
                g_zeroed = [M * N for i in range(M)]
                for k in ng_zeroed:
                    remainder = k % M
                    jord[remainder] += 1
                    if k < g_zeroed[remainder]:
                        g_zeroed[remainder] = k
                # https://stackoverflow.com/a/9764364
                jord, g_zeroed = (list(t) for t in zip(*sorted(zip(jord, g_zeroed))))

                while jord[0] == 0:
                    jord.pop(0)
                    g_zeroed.pop(0)
                g_zeroed.sort()
                g_zeroed.pop(0)
                gen.append(g_zeroed)

                g_zeroed_exp = []
                for k in g_zeroed:
                    ng_count = 0
                    for j in ng_zeroed:
                        if k - M < j and j < k:
                            ng_count += 1
                    g_zeroed_exp.append(ng_count)
                gen_exp.append(g_zeroed_exp)


    # https://stackoverflow.com/a/9764364
    area, codinv, ngen, cogen, cogen_exp, gen, gen_exp = (list(t) for t in zip(*sorted(zip(area, codinv, ngen, cogen, cogen_exp, gen, gen_exp), reverse=True)))

    area_max = area[0]
    area_min = area[count - 1]
    codinv_max = codinv[0]
    codinv_min = codinv[count - 1]

    cogen_array = [[[0 for y in range(codinv_max + 1)] for x in range(area_max + 1)] for z in range(N)]
    gen_array = [[[0 for y in range(codinv_max + 1)] for x in range(area_max + 1)] for z in range(N)]
    for i in range(count):
        x = area[i]
        y = codinv[i]
        cogen_count = len(cogen[i])
        for tuple in itertools.product(range(2), repeat=cogen_count):
            y_shift = 0
            z = 0
            for j in range(cogen_count):
                if tuple[j] == 1:
                    y_shift += cogen_exp[i][j]
                    z += 1
            cogen_array[z][x - z][y + y_shift] += 1
        gen_count = len(gen[i])
        for tuple in itertools.product(range(2), repeat=gen_count):
            y_shift = 0
            z = 0
            for j in range(gen_count):
                if tuple[j] == 1:
                    y_shift += gen_exp[i][j]
                    z += 1
            gen_array[z][x][y + y_shift] += 1
    
    diff_array = [[[0 for y in range(codinv_max + 1)] for x in range(area_max + 1)] for z in range(N)]
    for z in range(N):
        for x in range(area_max + 1):
            for y in range(codinv_min, codinv_max + 1):
                diff_array[z][x][y] = cogen_array[z][x][y] - gen_array[z][x][y]

    string += "Ngen_0" + " " * 11
    string += "area" + " " * 3
    string += "codinv" + " " * 1
    string += "Cogen" + " " * 9
    string += " " * 14
    string += "Gen" + " " * 7
    string += " " * 14
    string += "\n\n"
    for i in range(count):
        string += "{:<17}".format(str(ngen[i])[1:-1])
        string += "{:<7}".format(str(area[i]))
        string += "{:<7}".format(str(codinv[i]))
        string += "{:<14}".format(str(cogen[i])[1:-1])
        string += "{:<14}".format(str(cogen_exp[i])[1:-1])
        string += "{:<14}".format(str(gen[i])[1:-1]) 
        string += "{:<14}".format(str(gen_exp[i])[1:-1]) 
        string += "\n"
    string += "\n\n"

    string += array_to_str(N, cogen_array, area_max, codinv_min, codinv_max, True)
    string += array_to_str(N, gen_array, area_max, codinv_min, codinv_max, False)
    string += array_to_str(N, diff_array, area_max, codinv_min, codinv_max, False)

    return string

def array_to_str(N, a, x_max, y_min, y_max, row_label):
    temp = ""
    if row_label == True:
        temp += " " * 4
        for z in range(N):
            for y in range(y_min, y_max + 1):
                temp += "{:<3}".format(str(y))
            temp += " " * 4
        temp += "\n"

    for x in range(x_max + 1):
        temp += "{:<4}".format(str(x))
        for z in range(N):
            for y in range(y_min, y_max + 1):
                val = a[z][x][y]
                if val == 0:
                    temp += " " * 3
                else:
                    temp += "{:<3}".format(str(val))
            temp += " " * 4
        temp += "\n"
    temp += "\n"

    return temp

main()

