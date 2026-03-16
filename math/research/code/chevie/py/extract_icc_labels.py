import re

with open(f'labels.txt') as f:
    labels = re.split('\n+', f.read().strip())

for label in labels:
    filepath = f'chevie/chevie_icc_{label}.txt'
    x_path = f'x/x_{label}.txt'
    y_path = f'y/y_{label}.txt'
    
    with open(filepath) as f:
        lines = f.read().strip().split('\n')

    # Find separator line
    sep_idx = next(i for i, l in enumerate(lines) if re.match(r'^_+', l))
    
    # Column label line is immediately above the separator
    col_line = lines[sep_idx - 1]
    # Strip the row-label area: everything up to and including the '|'
    col_line = col_line.split('|', 1)[1]
    # Split on whitespace to get individual labels
    col_labels = col_line.split()

    with open(y_path, 'w') as f:
        f.write('\n'.join(col_labels) + '\n')

    row_lines = lines[sep_idx+1:]

    row_labels = []
    for line in row_lines:
        if not line.strip():
            continue
        row_labels.append(line.split('|', 1)[0].strip())

    with open(x_path, 'w') as f:
        f.write('\n'.join(row_labels) + '\n')
    
    print(f"[{label}]: {len(row_labels)} irreducible characters")