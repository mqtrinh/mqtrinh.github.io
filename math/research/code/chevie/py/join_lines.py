"""
join_lines.py

Usage:
    python3 join_lines.py <file1> [<file2> ...]

Removes all occurrences of the sequence backslash+newline from each file,
writing the result back to the same file in place.
"""

import sys

for filepath in sys.argv[1:]:
    with open(filepath, 'r') as f:
        content = f.read()
    joined = content.replace('\\\n', '')
    with open(filepath, 'w') as f:
        f.write(joined)
    print(f"Done: {filepath}")
