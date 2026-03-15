import re

def parse_x_file(filepath):
    """Return list of labels (strings after 'X') in order, 1-indexed."""
    labels = []
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if line.startswith('X'):
                labels.append(line[1:])  # strip the 'X' prefix
    return labels

def is_separator(line):
    s = line.strip()
    return len(s) > 0 and set(s) == {'_'}

def parse_families_file(filepath):
    """
    Parse a chevie_families file and return a list of tables.
    Each table is a list of row labels (strings, with '*' stripped).

    Structure:
      Line 0: "Unipotent characters for ..."
      Line 1: column label row (contains 'gamma')
      Line 2: separator (underscores)  <- global header ends here
      Then alternating: data rows / separator lines.
      Each separator line ends one table and begins the next.
    """
    with open(filepath) as f:
        lines = f.readlines()

    # Skip the global header (title + column labels + first separator)
    i = 0
    while i < len(lines) and not lines[i].strip().startswith('Unipotent'):
        i += 1
    i += 1  # skip title
    while i < len(lines) and 'gamma' not in lines[i]:
        i += 1
    i += 1  # skip column label row
    while i < len(lines) and not is_separator(lines[i]):
        i += 1
    i += 1  # skip first separator

    # Now parse: data rows accumulate into current_table;
    # a separator line commits current_table and starts a new one.
    tables = []
    current_table = []

    while i < len(lines):
        line = lines[i].rstrip('\n')
        stripped = line.strip()

        if stripped == '':
            pass  # blank lines are ignored
        elif is_separator(stripped):
            # Separator: commit current table (if non-empty) and start fresh
            if current_table:
                tables.append(current_table)
                current_table = []
        else:
            # Data row
            if '|' in line:
                label_part = line.split('|')[0].strip()
                label = label_part.lstrip('*').strip()
                current_table.append(label)
        i += 1

    if current_table:
        tables.append(current_table)

    return tables

labels = ['b2', 'g2', 'b3', 'b4', 'd4', 'f4', 'b5', 'd5', 'b6', 'd6', 'e6', 'e7', 'e8']

for label in labels:
    x_file = f'x/x_{label}.txt'
    fam_file = f'chevie/chevie_families_{label}.txt'
    out_file = f'families/families_{label}.txt'

    x_labels = parse_x_file(x_file)
    # Build a lookup: label -> 1-based line number
    label_to_line = {label: idx + 1 for idx, label in enumerate(x_labels)}

    tables = parse_families_file(fam_file)

    lines_out = []
    for table in tables:
        line_numbers = []
        for row_label in table:
            if row_label in label_to_line:
                line_numbers.append(label_to_line[row_label])
            # Labels absent from x file are simply skipped
        lines_out.append(','.join(str(n) for n in line_numbers))

    with open(out_file, 'w') as f:
        f.write('\n'.join(lines_out) + '\n')

    print(f"{label} families:")
    for i, line in enumerate(lines_out):
        print(f"  family #{i+1}: {line}")
