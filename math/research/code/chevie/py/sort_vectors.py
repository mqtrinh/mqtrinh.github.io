import re

def read_vectors(filepath):
    with open(filepath) as f:
        raw = f.read()
    blocks = re.split(r'(#[0-9]+ [^\n]*)\n', raw)
    headers, vectors_raw = [], []
    i = 1
    while i < len(blocks):
        headers.append(blocks[i].strip())
        content = blocks[i+1].strip().split('\n')
        vectors_raw.append([l.strip() for l in content if l.strip()])
        i += 2
    return headers, vectors_raw

def permute_vector(v, perm):
    """
    perm is 0-indexed: perm[k] = destination index for element k.
    Returns a new vector where result[perm[k]] = v[k].
    """
    result = [''] * len(v)
    for k, dest in enumerate(perm):
        result[dest] = v[k]
    return result

labels = ['b2', 'g2', 'b3', 'b4', 'd4', 'f4', 'd5']

perms_file = f'chevie_permutations.txt'
with open(perms_file) as f:
    perms = re.split('\n+', f.read())

for label in labels:
    input_file = f'exotic/exotic_{label}.txt'
    output_file = f'exotic/exotic_{label}_sorted.txt'

    label_index = perms.index(f'[{label}]')
    perm_str = re.split('\s', perms[label_index + 1])
    perm = [n - 1 for n in map(int, perm_str)]

    headers, vectors_raw = read_vectors(input_file)

    N = len(vectors_raw[0])
    assert len(perm) == N, f"Permutation length {len(perm)} doesn't match vector length {N}"

    output_blocks = []
    for header, v in zip(headers, vectors_raw):
        permuted = permute_vector(v, perm)
        output_blocks.append(header + '\n\n' + '\n'.join(permuted))

    output = '\n\n'.join(output_blocks) + '\n'

    with open(output_file, 'w') as f:
        f.write(output)
    print(f"[{label}] sorted.")
