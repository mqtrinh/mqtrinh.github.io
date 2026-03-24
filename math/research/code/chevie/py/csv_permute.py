import re, sys

type = sys.argv[1]

def permute_rows(rows, perm):
    result = [''] * len(rows)
    for k, dest in enumerate(perm):
        result[dest] = rows[k]
    return result

def permute_cols(rows, perm):
    result = []
    for row in rows:
        tokens = row.split(',')
        permuted = [''] * len(tokens)
        for k, dest in enumerate(perm):
            permuted[dest] = tokens[k]
        result.append(','.join(permuted))
    return result

with open(f'labels.txt') as f:
    labels = re.split('\n+', f.read().strip())

with open(f'permutations.txt') as f:
    perms = re.split('\n+', f.read())

for label in labels:
    input = f'{type}/{type}_{label}_raw.txt'
    output = f'{type}/{type}_{label}.txt'

    label_index = perms.index(f'[{label}]')
    perm_str = re.split(r'\s', perms[label_index + 1])
    perm = [n - 1 for n in map(int, perm_str)]

    with open(input, 'r') as f:
        input_lines = re.split('\n', f.read().strip())

    output_lines = permute_rows(permute_cols(input_lines, perm), perm)

    with open(output, 'w') as f:
        f.write('\n'.join(output_lines))

    print(f"[{label}])")
    print(f"  permuted: {output}")