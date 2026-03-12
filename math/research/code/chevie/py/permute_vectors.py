"""
permute_vectors.py

Usage:
    python3 permute_vectors.py <input_file> <output_file> <a_1> <a_2> ... <a_N>

The permutation [a_1, ..., a_N] (1-indexed) means: the kth entry of each
vector is moved to the (a_k)th position of the output vector.
"""

import re
import sys

def read_vectors(filepath):
    with open(filepath) as f:
        raw = f.read()
    blocks = re.split(r'(#[0-9]+ [^\n]*)\n', raw)
    labels, vectors_raw = [], []
    i = 1
    while i < len(blocks):
        labels.append(blocks[i].strip())
        content = blocks[i+1].strip().split('\n')
        vectors_raw.append([l.strip() for l in content if l.strip()])
        i += 2
    return labels, vectors_raw

def permute_vector(v, perm):
    """
    perm is 0-indexed: perm[k] = destination index for element k.
    Returns a new vector where result[perm[k]] = v[k].
    """
    result = [''] * len(v)
    for k, dest in enumerate(perm):
        result[dest] = v[k]
    return result

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print(__doc__)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    # Permutation given as 1-indexed a_1 ... a_N on command line
    perm_1indexed = [int(x) for x in sys.argv[3:]]
    perm = [a - 1 for a in perm_1indexed]  # convert to 0-indexed

    labels, vectors_raw = read_vectors(input_file)

    N = len(vectors_raw[0])
    assert len(perm) == N, f"Permutation length {len(perm)} doesn't match vector length {N}"

    output_blocks = []
    for label, v in zip(labels, vectors_raw):
        permuted = permute_vector(v, perm)
        output_blocks.append(label + '\n\n' + '\n'.join(permuted))

    output = '\n\n'.join(output_blocks) + '\n'

    with open(output_file, 'w') as f:
        f.write(output)
    print(f"Written to {output_file}")
