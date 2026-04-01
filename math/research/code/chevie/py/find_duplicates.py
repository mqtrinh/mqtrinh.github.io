import re

def parse_blocks(filepath):
    """Parse the file into a list of (header, vector_entries) tuples."""
    with open(filepath, 'r') as f:
        content = f.read()

    # Split on header lines "w = ..."
    # Each block: header line, blank line, then entries
    raw_blocks = re.split(r'(?=^#[0-9]+ )', content, flags=re.MULTILINE)
    
    blocks = []
    for block in raw_blocks:
        block = block.strip()
        if not block:
            continue
        lines = block.split('\n')
        header = lines[0].strip()
        # Entries are non-empty lines after the header
        entries = [l.strip() for l in lines[1:] if l.strip()]
        blocks.append((header, entries))
    
    return blocks

# only apply this script in mode 'all'
with open(f'test/labels_all.txt') as f:
    labels = re.split('\n+', f.read().strip())

for label in labels:
    input_path = f'test/all/{label}_all_raw.txt'
    output_path = f'test/all/{label}_all_duplicates.txt'

    blocks = parse_blocks(input_path)

    seen = []   # list of entry tuples already written
    originals = []
    duplicates = []

    for header, entries in blocks:
        key = tuple(entries)
        if key not in seen:
            seen.append(key)
            originals.append(header)
        else:
            duplicates.append((header, entries, originals[seen.index(key)]))

    count_total = f"number of elements: {len(blocks)}"
    count_original = f"number of unique vectors: {len(originals)}"
    summary = count_total + '\n' + count_original + '\n'

    lines = []
    lines.append(summary)
    for i, (header, entries, original) in enumerate(duplicates):
        lines.append(header + ' DUPLICATES ' + original)

    with open(output_path, 'w') as f:
        f.write('\n'.join(lines) + '\n')
    
    print(summary)