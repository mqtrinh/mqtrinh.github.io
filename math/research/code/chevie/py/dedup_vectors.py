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

if __name__ == '__main__':
    import sys
    input_path = sys.argv[1]
    output_path = sys.argv[2]

    blocks = parse_blocks(input_path)

    seen = []   # list of entry tuples already written
    output_blocks = []

    for header, entries in blocks:
        key = tuple(entries)
        if key not in seen:
            seen.append(key)
            output_blocks.append((header, entries))
        else:
            print(f"Skipping duplicate: {header}")

    # Write output
    with open(output_path, 'w') as f:
        for i, (header, entries) in enumerate(output_blocks):
            f.write(header + '\n')
            f.write('\n')
            for entry in entries:
                f.write(entry + '\n')
            if i < len(output_blocks) - 1:
                f.write('\n')

    print(f"\nDone. {len(output_blocks)} unique vectors out of {len(blocks)} total.")
