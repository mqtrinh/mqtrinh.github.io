import re 

MODES = ["min", "all"]

with open(f"sage/sage-to-gap.txt", "r") as f:
    converter = re.split("\n+", f.read())
    
def sage_to_gap(i, label):
	if label[0] =="a":
		return i
	else:
		start = converter.index(f"[{label}]")
		return int(converter[start + i])

def gap_to_sage(i, label):
	if label[0] =="a":
		return i
	else:
		start = converter.index(f"[{label}]")
		rank = int(label[1:])
		for j in range(1, rank + 1):
			if int(converter[start + j]) == i:
				return j

def gap_formatter(list):
    return "[ " + ", ".join(str(x) for x in list) + " ]"

def search_smooth(entry, elts, seen, lines):
	if "#" in entry:
		start = entry.index("[")

		gap_word_str = ""
		for j in range(start, len(entry)):
			temp = entry[j]
			if temp != " ": gap_word_str += temp
					
		gap_word = eval(gap_word_str)
		w = W.from_reduced_word([gap_to_sage(j, label) for j in gap_word])

		if w in elts and w not in seen:
			seen.add(w)
			lines.append(entry[4:]) # to reduce the indentation
			return True

for mode in MODES:
	if mode == "min":
		mode_str = " minimal-length smooth elements "
	if mode == "all":
		mode_str = " smooth elements "
	
	with open(f"test/labels_{mode}.txt", "r") as f:
		labels = re.split("\n+", f.read().strip())

	for label in labels:
		label_letter = label[0].upper()
		label_number = Integer(label[1:])
		W = WeylGroup([label_letter, label_number])

		elts = set()
		with open(f"smooth/{label}_smooth.txt", "r") as f:
			elts_str = f.read().strip()
		elts_lines = re.split("\n+", elts_str)

		for i in range(1, len(elts_lines)):
			entry = elts_lines[i]

			gap_word_str = ""
			for j in range(len(entry)):
				temp = entry[j]
				if temp != " ": gap_word_str += temp
						
			gap_word = eval(gap_word_str)
			elts.add(W.from_reduced_word([gap_to_sage(j, label) for j in gap_word]))

		nonunimodal_smooth_count, mixed_smooth_count, negative_smooth_count = 0, 0, 0
		nonunimodal_smooth_lines, mixed_smooth_lines, negative_smooth_lines = [], [], []

		with open(f"test/{mode}/{label}_{mode}_solved_test.txt", "r") as f:
			test_str = f.read().strip()
		
		test_blocks = re.split("elements", test_str)
		nonunimodal_str = test_blocks[1]
		mixed_str = test_blocks[2]
		negative_str = test_blocks[3]

		nonunimodal_seen, mixed_seen, negative_seen = set(), set(), set()

		nonunimodal_lines = re.split("\n+", nonunimodal_str)
		mixed_lines = re.split("\n+", mixed_str)
		negative_lines = re.split("\n+", negative_str)

		for i in range(len(nonunimodal_lines)):
			if search_smooth(nonunimodal_lines[i], elts, nonunimodal_seen, nonunimodal_smooth_lines):
				nonunimodal_smooth_count += 1
		for i in range(len(mixed_lines)):
			if search_smooth(mixed_lines[i], elts, mixed_seen, mixed_smooth_lines):
				mixed_smooth_count += 1
		for i in range(len(negative_lines)):
			if search_smooth(negative_lines[i], elts, negative_seen, negative_smooth_lines):
				negative_smooth_count += 1

		lines = [f"{len(elts)} smooth elements in W.", ""]
		lines.append(f"| {nonunimodal_smooth_count}{mode_str}" + "where some sequence of nonzero coeffs is not unimodal in abs value.")
		lines.extend(nonunimodal_smooth_lines)
		lines.append(f"| {mixed_smooth_count}{mode_str}" + "where some polynomial has both positive and negative coeffs.")
		lines.extend(mixed_smooth_lines)
		lines.append(f"| {negative_smooth_count}{mode_str}" + "where some polynomial has strictly negative coeffs.")
		lines.extend(negative_smooth_lines)

		with open(f"test/{mode}/{label}_{mode}_smooth_test.txt", "w") as f:
			f.write("\n".join(lines))
