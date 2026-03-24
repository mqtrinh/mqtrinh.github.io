import re, sys
from fractions import Fraction

type = sys.argv[1]

with open(f'test/labels_min.txt') as f:
    labels = re.split('\n+', f.read().strip())

for label in labels:
    csv1 = f'{type}/{type}_{label}.txt'
    csv2 = f'{type}/{type}_{label}_inverted.txt'

    with open(csv1, 'r') as f:
        output1 = f.read()

    rows2 = [[x for x in line.split(',')] for line in output1.strip().split('\n')]

    n = len(rows2)
    # Build augmented matrix [M | I] with exact rational entries
    aug = [[Fraction(rows2[i][j]) for j in range(n)] + 
        [Fraction(1 if i == j else 0) for j in range(n)]
        for i in range(n)]

    # Gauss-Jordan elimination
    for col in range(n):
        # Find pivot
        pivot = next(r for r in range(col, n) if aug[r][col] != 0)
        aug[col], aug[pivot] = aug[pivot], aug[col]
        # Scale pivot row
        scale = aug[col][col]
        aug[col] = [x / scale for x in aug[col]]
        # Eliminate column
        for row in range(n):
            if row != col and aug[row][col] != 0:
                factor = aug[row][col]
                aug[row] = [aug[row][k] - factor * aug[col][k] for k in range(2*n)]

    # Extract right half — entries are exact Fractions
    M_inv = [[aug[i][n + j] for j in range(n)] for i in range(n)]

    output2 = '\n'.join(','.join(str(v) for v in row) for row in M_inv)
    with open(csv2, 'w') as f:
        f.write(output2)

    print(f"[{label}])")
    print(f"  inverted: {csv2}")


