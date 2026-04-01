data:=["e", 6, 1];

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
ratlsmooth:=[]; t:=0; for w in elts do l_w:=CoxeterLength(W,w);
	#if Coefficient(T(C(w)), ()) = x^(-CoxeterLength(W,w)) then Add(ratlsmooth, w); fi;
	defect_flag:=False;
	for y in elts do if defect_flag = False and Bruhat(W,y,w) then
		refl_count:=0;
		for r in Reflections(W) do z:=r*y;
			if Bruhat(W,y,z) and Bruhat(W,z,w) then refl_count:=refl_count + 1; fi; od;
		if l_w - CoxeterLength(W,y) < refl_count then defect_flag:=True; fi;
		fi; od;
	if defect_flag = False then t:=t + 1; Print(t, "."); Add(ratlsmooth, w); fi; od;
num_ratlsmooth:=Length(ratlsmooth);

list_path:=Concatenation("chevie_test/", data[1], String(data[2]), "_ratlsmooth_list.txt");
PrintTo(list_path, num_ratlsmooth, "\n\n");
for w in ratlsmooth do
	AppendTo(list_path, CoxeterWord(W,w), "\n"); od;

len:=Length(ChevieCharInfo(W).charnames);
fourier:=List([1..len], i->List([1..len], j->UnipotentCharacter(W,i)*AlmostCharacter(W,j)));

x:=Indeterminate(Rationals); x.name:="x"; H:=Hecke(W, List([1..data[3]], i->x^2)); C:=Basis(H, "C'");
raw_path:=Concatenation("chevie_test/", data[1], String(data[2]), "_ratlsmooth_raw.txt");
PrintTo(raw_path, "");

for t in [1..num_ratlsmooth] do
	Print(t, ".");
	w:=ratlsmooth[t];
	#if w=() then w_name:="[  ]"; else w_name:=String(CoxeterWord(W,w)); fi;
	AppendTo(raw_path, "#", t, " ", CoxeterWord(W,w), "\n\n");
	
	vals:=HeckeCharValues(C(w));
	for i in [1..len] do 
		AppendTo(raw_path, FormatLaTeX(fourier[i]*vals), "\n"); od;
	AppendTo(raw_path, "\n"); od;

quit;

