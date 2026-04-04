import re, sys

mode = sys.argv[1]

def read_vectors(filepath):
    with open(filepath) as f:
        raw = f.read()
    blocks = re.split(r"(#[0-9]+ [^\n]*)\n", raw)
    headers, vectors_raw = [], []
    i = 1
    while i < len(blocks):
        headers.append(blocks[i].strip())
        content = blocks[i+1].strip().split("\n")
        vectors_raw.append([l.strip() for l in content if l.strip()])
        i += 2
    return headers, vectors_raw

def parse_lp(s):
    """Parse a Laurent polynomial string into a dict {exp: coeff}."""
    s = s.strip()
    s = re.sub(r"\^{([^}]*)}", r"^\1", s)   # x^{-1} -> x^-1
    s = re.sub(r"(?<=[0-9x])-", "+-", s)    # insert + before internal -
    terms = [t for t in s.split("+") if t.strip()]
    poly = {}
    for term in terms:
        term = term.strip()
        if not term:
            continue
        if term.startswith("-"):
            sign = -1
            term = term[1:]
        else:
            sign = 1
        if "x" not in term:
            coeff = int(term) if term else 1
            exp = 0
        else:
            parts = term.split("x", 1)
            c_part, e_part = parts
            coeff = int(c_part) if c_part != "" else 1
            exp = 1 if e_part == "" else int(e_part[1:])
        poly[exp] = poly.get(exp, 0) + sign * coeff
    return {k: v for k, v in poly.items() if v != 0}

def check_unimodal(coeffs):
    """Return True if seq is unimodal (weakly increases then weakly decreases)."""
    if len(coeffs) <= 1:
        return False
    abs_woeffs = [abs(c) for c in coeffs]
    for i in range(1, len(coeffs) // 2 + 1):
        if abs_woeffs[i] < abs_woeffs[i-1]:
            return True
    return False

def check_signs(coeffs):
    if all(c <= 0 for c in coeffs):
        return True, False
    if any(c > 0 for c in coeffs) and any(c < 0 for c in coeffs):
        return False, True
    return False, False

def formatter(i, x, y, x_to_special_x):
    s1 = "    " + "{:<28}".format(f"{x[i]} = {y[i]}")
    special = x_to_special_x[i + 1] # 1-indexing to 1-indexing!
    s2 = "{:<28}".format(f"{x[special - 1]} = {y[special - 1]}")
    return s1 + " in family " + s2

def list_formatter(list, x, y, x_to_special_x):
    if list:
        sublist = []
        for i in list:
            sublist.append(formatter(i, x, y, x_to_special_x))
        return sublist
    else:
        return ["    none"]

with open(f"test/labels_{mode}.txt") as f:
    labels = re.split("\n+", f.read().strip())

for label in labels:
    with open(f"families/families_{label}.txt") as f:
        families = re.split("\n", f.read().strip())
    with open(f"x/x_{label}.txt") as f:
        x = [s[1:] for s in re.split("\n", f.read().strip())]
    with open(f"y/y_{label}.txt") as f:
        y = re.split("\n", f.read().strip())

    num_x = len(x)
    
    # x_to_special_x takes 1-indexing to 1-indexing!
    x_to_special_x = [None] * (num_x + 1) 
    for i in range(len(families)):
        family_elts = re.split(",", families[i].strip())

        for j in range(len(family_elts)):
            elt = family_elts[j]
            if elt[0] == "*": # each family contains exactly one special element
                special = int(elt[1:])
                x_to_special_x[special] = special
        for j in range(len(family_elts)):
            elt = family_elts[j]
            if elt[0] != "*":
                x_to_special_x[int(elt)] = special

    # INPUT

    headers, vectors_raw = read_vectors(f"test/{mode}/{label}_{mode}_solved.txt")

    nonunimodal_x, mixed_x, negative_x = set(), set(), set()
    nonunimodal_count, mixed_count, negative_count = 0, 0, 0
    nonunimodal_list = [[] for i in range(num_x)]
    mixed_list = [[] for i in range(num_x)]
    negative_list = [[] for i in range(num_x)]

    for header, v in zip(headers, vectors_raw):
        nonunimodal_flag, mixed_flag, negative_flag = False, False, False

        for i in range(len(v)):
            s = v[i].strip()
            if s != "0":
                poly = parse_lp(s)
                coeffs = list(poly.values())
                if check_unimodal(coeffs):
                    nonunimodal_x.add(i)
                    nonunimodal_flag = True
                    nonunimodal_list[i].append(header)
                fneg, fmixed = check_signs(coeffs)
                if fmixed:
                    mixed_x.add(i)
                    mixed_flag = True
                    mixed_list[i].append(header)
                if fneg: 
                    negative_x.add(i)
                    negative_flag = True
                    negative_list[i].append(header)
        
        if nonunimodal_flag:
            nonunimodal_count += 1
        if mixed_flag:
            mixed_count += 1
        if negative_flag:
            negative_count += 1 
    
    # OUTPUT

    if mode == "all": mode_str = " elements"
    if mode == "min": mode_str = " good minimal-length representatives"
    if mode == "ratlsmooth": mode_str = " rationally smooth elements"

    str_nonunimodal = " where some sequence of nonzero coeffs is not unimodal in abs value"
    str_mixed = " where some polynomial has both positive and negative coeffs"
    str_negative = " where some polynomial has strictly negative coeffs"

    lines = []

    lines.append(f"total num of chars: {len(x)}")
    lines.append(f"total num of families: {len(families)}")
    lines.append("")
    
    lines.append("chars" + str_nonunimodal + ":")
    lines.extend(list_formatter(nonunimodal_x, x, y, x_to_special_x))
    lines.append("chars" + str_mixed + ":")
    lines.extend(list_formatter(mixed_x, x, y, x_to_special_x))
    lines.append("chars" + str_negative + ":")
    lines.extend(list_formatter(negative_x, x, y, x_to_special_x))
    lines.append("")
    
    lines_full = []

    lines_full.append("| " + str(nonunimodal_count) + mode_str + str_nonunimodal + ".")
    for i in range(num_x):
        if len(nonunimodal_list[i]) > 0:
            lines_full.append(formatter(i, x, y, x_to_special_x))
            for header in nonunimodal_list[i]:
                lines_full.append(f"      {header}")
                #lines_full.append(f"    {header}: {vectors_raw[headers.index(header)][i]}")
    lines_full.append("| " + str(mixed_count) + mode_str + str_mixed + ".")
    for i in range(num_x):
        if len(mixed_list[i]) > 0:
            lines_full.append(formatter(i, x, y, x_to_special_x))
            for header in mixed_list[i]:
                lines_full.append(f"      {header}")
    lines_full.append("| " + str(negative_count) + mode_str + str_negative + ".")
    for i in range(num_x):
        if len(negative_list[i]) > 0:
            lines_full.append(formatter(i, x, y, x_to_special_x))
            for header in negative_list[i]:
                lines_full.append(f"      {header}")

    output = "\n".join(lines) + "\n" + "\n".join(lines_full) + "\n"

    with open(f"test/{mode}/{label}_{mode}_test.txt", "w") as f:
        f.write(output)

    print(f"[{label}]\n\n  " + "\n  ".join(lines))