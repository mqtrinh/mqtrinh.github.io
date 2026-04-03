data:=["d", 7];

if data[1]="a" then letter:="A"; fi;
if data[1]="b" then letter:="B"; fi;
if data[1]="c" then letter:="C"; fi;
if data[1]="d" then letter:="D"; fi;
if data[1]="e" then letter:="E"; fi;
if data[1]="f" then letter:="F"; fi;
if data[1]="g" then letter:="G"; fi;

W:=CoxeterGroup(letter, data[2]);

chn:=ChevieCharInfo(W).charnames;
charinfo_path:=Concatenation("chevie_test/chevie_charinfo_", data[1], String(data[2]), ".txt");
PrintTo(charinfo_path, "");
for c in chn do AppendTo(charinfo_path, FormatLaTeX(c), "\n"); od;

icc_path:=Concatenation("chevie_test/chevie_icc_", data[1], String(data[2]), ".txt");
PrintTo(icc_path, Format(ICCTable(UnipotentClasses(W)),rec(CycPol:=false)), "\n");

families_path:=Concatenation("chevie_test/chevie_families_", data[1], String(data[2]), ".txt");
o:=rec(byFamily:=true,items:=["Name","Degree","FakeDegree","Eigenvalue", "Symbol","Family"]);
PrintTo(families_path, Format(UnipotentCharacters(W),o));
