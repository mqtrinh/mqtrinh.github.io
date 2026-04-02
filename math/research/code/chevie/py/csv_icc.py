import re

def eval_poly_at_1(token):
    expr = re.sub(r'(\d)(x)', r'\1*\2', token)
    expr = expr.replace('^', '**')
    expr = expr.replace('x', '1')
    return str(eval(expr))

with open(f'labels.txt') as f:
    labels = re.split('\n+', f.read().strip())

for label in labels:
    input = f'chevie/chevie_icc_{label}.txt'
    csv1 = f'icc/icc_{label}.txt'

    print(f"[{label}])")

    # Convert table format to CSV

    with open(input, 'r') as f:
        lines = f.read().strip().split('\n')

    # Find separator line
    sep_idx = next(i for i, l in enumerate(lines) if re.match(r'^_+', l))
    data_lines = lines[sep_idx+1:]

    rows_poly = []
    for line in data_lines:
        if not line.strip():
            continue
        after_pipe = line.split('|', 1)[1]
        tokens = after_pipe.split()
        rows_poly.append(','.join(tokens))

    output_poly = '\n'.join(rows_poly)

    # Evaluate polynomials at x=1 and write to new CSV

    lines = output_poly.strip().split('\n')

    rows1 = []
    for line in lines:
        tokens = line.split(',')
        rows1.append(','.join(eval_poly_at_1(t) for t in tokens))

    output1 = '\n'.join(rows1)

    with open(csv1, 'w') as f:
        f.write(output1)
    print(f"  at x = 1: {csv1}")


