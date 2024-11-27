import itertools

log = open("cells_sl_00.txt", "w")

def main():
    output = ""
    
    output += semigroups(3, 4)
    output += semigroups(3, 5)
    output += semigroups(3, 7)

    # output += semigroups(4, 3)
    output += semigroups(4, 5)
    # output += semigroups(4, 7)
    # output += semigroups(4, 9)

    output += semigroups(5, 6)
    # output += semigroups(5, 7)

    log.write(output)
    log.close()
    print(output)

def semigroups(N, M):
    # for now assume M, N coprime
    MILNOR = (M - 1) * (N - 1)
    DELTA = int(MILNOR / 2)
    M_INVERSE = pow(M, -1, N)
    string = "N = " + str(N) + "\n" + "M = " + str(M) + "\n\n"

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
    ngen_zeroed = []
    area = []
    codinv = []
    cogen = []
    # cogen_count = []
    gen_zeroed = []
    jordan = []
    haglund = []

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
            count += 1

            ng = []
            minimum = DELTA
            for i in range(N):
                temp = A[i] + N * cochar[i]
                ng.append(temp)
                if temp < minimum:
                    minimum = temp
            area.append(DELTA - minimum)

            c = 0
            for i in range(N):
                for j in range(1, M):
                    temp = ng[i] + j
                    remainder = (M_INVERSE * temp) % N
                    if temp >= A[remainder] and temp < ng[remainder]:
                        c += 1
            codinv.append(c)

            # ngen.append(ng)
            ng_zeroed = [ng[i] - minimum for i in range(N)]
            ngen_zeroed.append(ng_zeroed)
            templist = []
            for k in H:
                # M * index - minimum % N == k % N
                i = (M_INVERSE * (k + minimum)) % N
                j = (M_INVERSE * (k + minimum) + 1) % N
                temp_i = ng_zeroed[i]
                temp_j = ng_zeroed[j]
                if temp_i > k and temp_i <= k + N and temp_j <= k + M:
                    templist.append(k)
            cogen.append(templist)

            """

            templist_count = [0 for i in range(len(templist))]
            for i in range(len(templist)):
                k = templist[i]
                for j in range(N):
                    temp = ng_zeroed[j] - N - k
                    if temp >= 1 and temp <= M:
                        templist_count[i] += 1
            cogen_count.append(templist_count)

            """

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
            gen_zeroed.append(g_zeroed)
            jordan.append(jord)

            # now assume M = N + 1
            H_cochar = H.copy()
            for k in ng_zeroed:
                for b in range(M):
                    temp = k + b * N
                    if temp < MILNOR:
                        H_cochar.discard(temp)
            hag = [N - 1 - i for i in range(N)]
            ng_zeroed.sort()
            for i in range(N):
                temp = ng_zeroed[i]
                for j in range(temp, temp + M):
                    if j in H_cochar:
                        hag[i] -= 1
            haglund.append(hag)


    # https://stackoverflow.com/a/9764364
    area, codinv, ngen_zeroed, cogen, gen_zeroed, jordan, haglund = (list(t) for t in zip(*sorted(zip(area, codinv, ngen_zeroed, cogen, gen_zeroed, jordan, haglund), reverse=True)))

    string += "Ngen 0-normalized" + " " * 3 
    string += "area" + " " * 4 
    string += "codinv" + " " * 2 
    string += "Cogen" + " " * 10
    # string += " " * 15
    string += "Gen - 0" + " " * 8
    # string += "Jordan"
    string += "Haglund"
    string += "\n\n"
    for i in range(count):
        string += "{:<20}".format(str(ngen_zeroed[i]))
        string += "{:<8}".format(str(area[i]))
        string += "{:<8}".format(str(codinv[i]))
        string += "{:<15}".format(str(cogen[i]))
        # string += "{:<15}".format(str(cogen_count[i]))
        string += "{:<15}".format(str(gen_zeroed[i])) 
        # string += "{:<15}".format(str(jordan[i]))
        string += "{:<15}".format(str(haglund[i]))
        string += "\n"
    string += "\n\n"

    return string

main()

