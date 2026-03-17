import re, sys

mode = sys.argv[1]

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
    abs_coeffs = [abs(c) for c in coeffs]
    for i in range(1, len(coeffs) // 2 + 1):
        if abs_coeffs[i] < abs_coeffs[i-1]:
            return True
    return False

def check_signs(coeffs):
    if all(c <= 0 for c in coeffs):
        return True, False
    if any(c > 0 for c in coeffs) and any(c < 0 for c in coeffs):
        return False, True
    return False, False

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

def formatter(list, x, y, fam_to_special):
    if list:
        sublist = []
        for i in list:
            special = fam_to_special[i + 1] # 1-indexing to 1-indexing!
            sublist.append("      family " + "{:<12}".format(x[special - 1]) + " = " + "{:<20}".format(y[special - 1]))
        return sublist
    else:
        return ["      none"]

with open(f"test/labels_{mode}.txt") as f:
    labels = re.split("\n+", f.read().strip())

for label in labels:
    with open(f"families/families_{label}.txt") as f:
        families = re.split("\n", f.read().strip())
    with open(f"x/x_{label}.txt") as f:
        x = [s[1:] for s in re.split("\n", f.read().strip())]
    with open(f"y/y_{label}.txt") as f:
        y = re.split("\n", f.read().strip())
    
    # fam_to_special takes 1-indexing to 1-indexing!
    fam_to_special = [None] * (len(families) + 1) 
    for i in range(len(families)):
        family_elts = re.split(",", families[i].strip())

        for j in range(len(family_elts)):
            elt = family_elts[j]
            if elt[0] == "*": # each family contains exactly one special element
                fam_to_special[i + 1] = int(elt[1:])

    # INPUT

    headers, vectors_raw = read_vectors(f"test/{mode}/{label}_{mode}_summed.txt")

    nonunimodal_list, mixed_list, negative_list = [], [], []
    nonunimodal_fam, mixed_fam, negative_fam = set(), set(), set()

    for header, v in zip(headers, vectors_raw):
        nonunimodal_v, mixed_v, negative_v = [], [], []

        for i in range(len(v)):
            s = v[i].strip()
            if s != "0":
                poly = parse_lp(s)
                coeffs = list(poly.values())
                if check_unimodal(coeffs):
                    nonunimodal_fam.add(i)
                    nonunimodal_v.append(i)
                fneg, fmixed = check_signs(coeffs)
                if fmixed:
                    mixed_fam.add(i)
                    mixed_v.append(i)
                if fneg: 
                    negative_fam.add(i)
                    negative_v.append(i)
            
        if nonunimodal_v: nonunimodal_list.append((header, nonunimodal_v))
        if mixed_v: mixed_list.append((header, mixed_v))
        if negative_v: negative_list.append((header, negative_v))
    
    # OUTPUT

    str_nonunimodal = " where some sequence of nonzero coeffs is not unimodal in abs value"
    str_mixed = " where some polynomial has both positive and negative coeffs"
    str_negative = " where some polynomial has strictly negative coeffs"

    lines = []

    lines.append(f"total num of chars: {len(x)}")
    lines.append(f"total num of families: {len(families)}")
    lines.append("")
    
    lines.append("families" + str_nonunimodal + ":")
    lines.extend(formatter(nonunimodal_fam, x, y, fam_to_special))
    lines.append("families" + str_mixed + ":")
    lines.extend(formatter(mixed_fam, x, y, fam_to_special))
    lines.append("families" + str_negative + ":")
    lines.extend(formatter(negative_fam, x, y, fam_to_special))
    lines.append("")

    if mode == "all":
        with open(f"sortable/{label}_sortable.txt", "r") as f:
            sortable_lines = re.split("\n+", f.read().strip())
        sortable_per_c = int(sortable_lines[0])
        sortable_total = int(sortable_lines[1])

        lines.append(str(sortable_per_c) + " elements of W are c-sortable for a given c.")
        lines.append(str(sortable_total) + " elements of W are c-sortable for some c.")
        lines.append("")

        for index in range(len(sortable_lines)):
            c = sortable_lines[index]

            if c[0] == "c":
                lines.append(c)

                lines_nonunimodal_c, lines_mixed_c, lines_negative_c = [], [], []

                for e in range(sortable_per_c):
                    elt = sortable_lines[index + 1 + e]
                    for (header, v) in nonunimodal_list:
                        if elt in header:
                            lines_nonunimodal_c.append("    " + header)
                            lines_nonunimodal_c.extend(formatter(v, x, y, fam_to_special))
                    for (header, v) in mixed_list:
                        if elt in header:
                            lines_mixed_c.append("    " + header)
                            lines_mixed_c.extend(formatter(v, x, y, fam_to_special))
                    for (header, v) in negative_list:
                        if elt in header:
                            lines_negative_c.append("    " + header)
                            lines_negative_c.extend(formatter(v, x, y, fam_to_special))
                
                if lines_nonunimodal_c:
                    lines.append("  c-sortables" + str_nonunimodal + ":")
                    lines.extend(lines_nonunimodal_c)
                if lines_mixed_c:
                    lines.append("  c-sortables" + str_mixed + ":")
                    lines.extend(lines_mixed_c)
                if lines_negative_c:
                    lines.append("  c-sortables" + str_negative + ":")
                    lines.extend(lines_negative_c)
                if not (lines_nonunimodal_c or lines_mixed_c or lines_negative_c):
                    lines.append("  no exceptions")
                
                lines.append("")
    
    lines_full = []

    lines_full.append(str(len(nonunimodal_list)) + " entries" + str_nonunimodal + ".")
    if nonunimodal_list:
        for header, nonunimodal_v in nonunimodal_list:
            lines_full.append(f"  {header}")
            for i in nonunimodal_v:
                lines_full.append(f"    {x[i]}: {vectors_raw[headers.index(header)][i]}")
    lines_full.append(str(len(mixed_list)) + " entries" + str_mixed + ".")
    if mixed_list:
        for header, mixed_v in mixed_list:
            lines_full.append(f"  {header}")
            for i in mixed_v:
                lines_full.append(f"    {x[i]}: {vectors_raw[headers.index(header)][i]}")
    lines_full.append(str(len(negative_list)) + " entries" + str_negative + ".")
    if negative_list:
        for header, negative_v in negative_list:
            lines_full.append(f"  {header}")
            for i in negative_v:
                lines_full.append(f"    {x[i]}: {vectors_raw[headers.index(header)][i]}")

    output = "\n".join(lines) + "\n" + "\n".join(lines_full) + "\n"

    with open(f"test/{mode}/{label}_{mode}_summed_test.txt", "w") as f:
        f.write(output)

    print(f"[{label}]\n\n  " + "\n  ".join(lines))