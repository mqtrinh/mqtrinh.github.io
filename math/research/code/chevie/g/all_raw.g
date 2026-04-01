data:=["b", 5, 2];

if data[1]="a" then letter:="A"; fi;
if data[1]="b" then letter:="B"; fi;
if data[1]="c" then letter:="C"; fi;
if data[1]="d" then letter:="D"; fi;
if data[1]="e" then letter:="E"; fi;
if data[1]="f" then letter:="F"; fi;
if data[1]="g" then letter:="G"; fi;

W:=CoxeterGroup(letter, data[2]);

# https://webusers.imj-prg.fr/~jean.michel/gap3/htm/chap093.htm
ReadChv("contr/brbase");
BaseBruhat(W);

elts:=Elements(W);

len:=Length(ChevieCharInfo(W).charnames);
fourier:=List([1..len], i->List([1..len], j->UnipotentCharacter(W,i)*AlmostCharacter(W,j)));

x:=Indeterminate(Rationals); x.name:="x"; H:=Hecke(W, List([1..data[3]], i->x^2)); C:=Basis(H, "C'");
raw_path:=Concatenation("chevie_test/", data[1], String(data[2]), "_all_raw.txt");
PrintTo(raw_path, "");

t:=0;
for w in elts do
	t:=t + 1; Print(t, ".");
	#if w=() then w_name:="[  ]"; else w_name:=String(CoxeterWord(W,w)); fi;
	AppendTo(raw_path, "#", t, " ", CoxeterWord(W,w), "\n\n");
	
	vals:=HeckeCharValues(C(w));
	for i in [1..len] do 
		AppendTo(raw_path, FormatLaTeX(fourier[i]*vals), "\n"); od;
	AppendTo(raw_path, "\n"); od;

quit;

