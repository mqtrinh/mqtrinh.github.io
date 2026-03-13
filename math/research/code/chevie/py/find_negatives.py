"""
find_negatives.py

Usage:
    python3 find_negatives.py <input_file> <output_file>

Reads a file of column vectors with headers of the form "#[number] [label]".
Outputs a list of vectors that contain negative entries, and for each,
the 1-based indices of those negative entries.
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

if __name__ == '__main__':
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    labels, vectors_raw = read_vectors(input_file)

    results = []
    for label, v in zip(labels, vectors_raw):
        neg_indices = [i+1 for i, entry in enumerate(v) if entry.startswith('-')]
        if neg_indices:
            results.append(f"{label}\nnegative entries at indices: {neg_indices}")

    output = '\n\n'.join(results) + '\n' if results else "No vectors with negative entries.\n"

    with open(output_file, 'w') as f:
        f.write(output)
    print(f"Found {len(results)} vector(s) with negative entries. Written to {output_file}")
