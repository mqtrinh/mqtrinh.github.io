import re

labels = ['b2', 'g2', 'b3', 'b4', 'd4', 'f4', 'b5', 'd5', 'b6', 'd6', 'e6', 'e7', 'e8']

for label in labels:
    filepath = f'chevie/chevie_icc_{label}.txt'
    with open(filepath) as f:
        lines = f.read().strip().split('\n')

    # Find separator line
    sep_idx = next(i for i, l in enumerate(lines) if re.match(r'^_+', l))
    data_lines = lines[sep_idx+1:]

    row_labels = []
    for line in data_lines:
        if not line.strip():
            continue
        row_labels.append(line.split('|', 1)[0].strip())

    out_path = f'x/x_{label}.txt'
    with open(out_path, 'w') as f:
        f.write('\n'.join(row_labels) + '\n')
    print(f"[{label}]: {len(row_labels)} irreducible characters")