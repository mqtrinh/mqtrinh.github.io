import itertools

log = open("cells_hilb_00.txt", "w")

def main():
    output = ""
    
    output += semigroups(3, 4)
    output += semigroups(3, 5)
    # output += semigroups(3, 7)

    # output += semigroups(4, 3)
    output += semigroups(4, 5)
    # output += semigroups(4, 7)

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

    A = [M * i for i in range(N)]
    B = [int((A[i] + M - A[(i + 1) % N]) / N) for i in range(N)]

    count = 0
    ngen = []
    sumlist = []
    dimlist = []
    gen_zeroed = []
    jordan = []

    for cochar in itertools.product(range(MILNOR + 1), repeat=N):
        flag = False

        sum = 0
        for i in range(0, N):
            sum += cochar[i]
            if cochar[(i + 1) % N] - cochar[i] > B[i]:
                flag = True
        if sum > MILNOR:
            flag = True

        if flag == False:
            count += 1

            sumlist.append(sum)

            ng = []
            for i in range(N):
                temp = A[i] + N * cochar[i]
                ng.append(temp)
            ngen.append(ng)

            c = 0
            for i in range(N):
                for j in range(1, M):
                    temp = ng[i] + j
                    remainder = (M_INVERSE * temp) % N
                    if temp >= A[remainder] and temp < ng[remainder]:
                        if temp in G or temp >= MILNOR:
                            c += 1
            dimlist.append(c)

            jord = [0 for i in range(M)]
            g_zeroed = [M * N for i in range(M)]
            for k in ng:
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

    # https://stackoverflow.com/a/9764364
    sumlist, dimlist, ngen, gen_zeroed, jordan = (list(t) for t in zip(*sorted(zip(sumlist, dimlist, ngen, gen_zeroed, jordan))))

    string += "Ngen" + " " * 16
    string += "sum" + " " * 5 
    string += "dim" + " " * 5
    string += "Gen - 0" + " " * 8
    string += "Jordan"
    string += "\n\n"
    for i in range(count):
        string += "{:<20}".format(str(ngen[i]))
        string += "{:<8}".format(str(sumlist[i]))
        string += "{:<8}".format(str(dimlist[i]))
        string += "{:<15}".format(str(gen_zeroed[i])) 
        string += "{:<15}".format(str(jordan[i]))
        string += "\n"
    string += "\n\n"

    return string

main()

