import re

LABEL = 'd6'

with open(f'sage/sage-to-gap.txt', 'r') as f:
    converter = re.split('\n+', f.read())
    
def sage_to_gap(i):
    start = converter.index(f'[{LABEL}]')
    return int(converter[start + i])

def gap_formatter(list):
    return '[ ' + ', '.join(str(x) for x in list) + ' ]'

label_letter = LABEL[0].upper()
label_number = Integer(LABEL[1:])

W = WeylGroup([label_letter, label_number])

coxeter_list = W.standard_coxeter_elements()

seen = set()

output = ''

for c in coxeter_list:
    sage_coxeter_word = c.reduced_word()
    gap_coxeter_word = [sage_to_gap(i) for i in sage_coxeter_word]
    
    header = 'c = ' + gap_formatter(gap_coxeter_word)
    print(header)

    output += header 
    lines = []
    for w in W:
        if w.is_coxeter_sortable(c):
            seen.add(w)
            sage_word = w.reduced_word()
            gap_word = [sage_to_gap(i) for i in sage_word]
            lines.append(gap_formatter(gap_word))
    output += '\n\n' + '\n'.join(lines) + '\n\n'

output = str(len(lines)) + '\n' + str(len(seen)) + '\n\n' + output

with open(f'sortable/{LABEL}_sortable.txt', 'w') as f:
    f.write(output)
