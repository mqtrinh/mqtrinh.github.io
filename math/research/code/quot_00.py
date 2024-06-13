import itertools

log = open("quot_00.txt", "w")

def main():
    output = ""

    # 2/3

    output += quot(2, 3, [0, 2, 4])
    output += quot(2, 3, [0, 2, 1])

    # 4/3

    output += quot(4, 3, [0, 4, 8])
    # output += quot(4, 3, [0, 4, 5])
    # output += quot(4, 3, [0, 1, 5])
    # output += quot(4, 3, [0, 4, 2])
    output += quot(4, 3, [0, 1, 2])

    # 5/3

    output += quot(5, 3, [0, 5, 10])
    # output += quot(5, 3, [0, 5, 7])
    # output += quot(5, 3, [0, 2, 7])
    # output += quot(5, 3, [0, 5, 4])
    # output += quot(5, 3, [0, 5, 1])
    # output += quot(5, 3, [0, 2, 4])
    output += quot(5, 3, [0, 2, 1])

    # 5/4

    output += quot(5, 4, [0, 5, 10, 15])

    # output += quot(5, 4, [0, 5, 10, 11])
    # output += quot(5, 4, [0, 5, 6, 11])
    # output += quot(5, 4, [0, 1, 6, 11])

    # output += quot(5, 4, [0, 5, 10, 7])
    # output += quot(5, 4, [0, 5, 10, 3])
    # output += quot(5, 4, [0, 1, 6, 7])

    # output += quot(5, 4, [0, 5, 6, 7])
    # output += quot(5, 4, [0, 5, 2, 7])
    # output += quot(5, 4, [0, 1, 2, 7])

    # output += quot(5, 4, [0, 5, 6, 3])
    # output += quot(5, 4, [0, 1, 6, 3])

    # output += quot(5, 4, [0, 5, 2, 3])

    output += quot(5, 4, [0, 1, 2, 3])

    # 7/4

    output += quot(7, 4, [0, 7, 14, 21])
    output += quot(7, 4, [0, 3, 2, 1])

    # 8/5

    # output += quot(8, 5, [0, 3, 1, 4, 2])


    log.write(output)
    log.close()
    print(output)

def quot(d, n, A):
    milnor = (d - 1) * (n - 1)
    delta = int(milnor / 2)
    string = ""
    #string += "d = " + str(d) + "\n"
    #string += "n = " + str(n) + "\n"
    #string += "delta = " + str(delta) + "\n"
        #string += "Gamma' = " + str(A) + "\n\n"

    B = []
    for i in range(0, n):
        entry = int((A[i] + d - A[(i + 1) % n]) / n)
        B.append(entry)

    string += str(B) + "\n\n"

    count = 0
    Q = []
    L = []
    D = []
    dim_max = 0

    for gridpoint in itertools.product(range(milnor + 1), repeat=n):
        flag = False

        for i in range(0, n):
            if gridpoint[(i + 1) % n] - gridpoint[i] > B[i]:
                flag = True

        sum = 0
        if flag == False:
            for i in range(n):
                sum += gridpoint[i]
            if sum > milnor:
                flag = True

        if flag == False:
            count += 1
            Q.append(gridpoint)
            L.append(sum)

            #string += str(gridpoint) + "\t"

            dim = 0
            C = [A[i] + n * gridpoint[i] for i in range(n)]
            e = pow(d, -1, n)

            #string += str(C) + "\t"

            for i in range(n):
                for j in range(1, d):
                    temp = C[i] + j
                    rem = (e * temp) % n

                    if temp >= A[rem] and temp < C[rem]:
                        #string += str(temp) + " "
                        dim += 1

            D.append(dim)
            if dim > dim_max:
                dim_max = dim

    picture = [[0 for j in range(milnor + 1)] for i in range(dim_max + 1)]
    for i in range(count):
        picture[D[i]][L[i]] += 1

    for i in range(dim_max + 1):
        for j in range(milnor + 1):
            entry = picture[dim_max - i][j]
            if entry == 0:
                string += "\t"
            else:
                string += str(entry) + "\t"
        string +=" \n"
    string += "\n"

    return string

main()
