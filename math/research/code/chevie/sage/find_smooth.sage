import re 

LABELS = ['b2', 'b3', 'b4', 'b5', 'b6', 'd4', 'd5', 'd6', 'e6', 'f4', 'g2']

with open(f'sage/sage-to-gap.txt', 'r') as f:
    converter = re.split('\n+', f.read())
    
def sage_to_gap(i, label):
	if label[0] =='a':
		return i
	else:
		start = converter.index(f'[{label}]')
		return int(converter[start + i])

def gap_formatter(list):
    return '[ ' + ', '.join(str(x) for x in list) + ' ]'

for label in LABELS:
	label_letter = label[0].upper()
	label_number = Integer(label[1:])

	W = WeylGroup([label_letter, label_number])

	ref = W.reflections()

	elts = []

	for w in W:
		w_supp = set()
		for r in ref:
			if r.bruhat_le(w):
				w_supp.add(r)

		l = w.length()
		if l == len(w_supp):
			elts.append(w)

	lines = []

	for w in elts:
		sage_word = w.reduced_word()
		gap_word = [sage_to_gap(j, label) for j in sage_word]
		lines.append(gap_formatter(gap_word))

	output = str(len(elts)) + '\n\n' + '\n'.join(lines)

	with open(f'smooth/{label}_smooth.txt', 'w') as f:
		f.write(output)
