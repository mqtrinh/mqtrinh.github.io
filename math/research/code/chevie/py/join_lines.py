"""
join_lines.py

Usage:
    python3 join_lines.py <input> <output>

Removes all occurrences of the sequence backslash+newline from <input>,
writing the result to <output>.
"""

import sys

if __name__ == '__main__':
    input = sys.argv[1]
    output = sys.argv[2]
    with open(input, 'r') as f:
        content = f.read()
    
    step_1 = content.replace('\\\n', '')
    step_2 = step_1.replace(', \n  ', ', ') # GAP3 weirdness

    with open(output, 'w') as f:
        f.write(step_2)
    print(f"Done: {output}")
