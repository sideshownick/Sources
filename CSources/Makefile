genmat:gen_matrix.c
	gcc -lm gen_matrix.c -ogenmat
gen2:generate_square.c
	gcc -lm generate_square.c -ogen2
gen:generate_from_map.c
	gcc -lm generate_from_map.c -ogen
	cp gen ~/bin/
gen3d:generate_3D.c
	gcc -lm -ogen3d generate_3D.c
	cp gen3d ~/local/bin/
makehist:histogram.c
	gcc -lm histogram.c -omakehist
	cp makehist ~/local/bin/
histt:hist3d.c
	gcc -lm hist3d.c -ohistt
	cp histt ~/local/bin/
sites:generate_sites.c
	gcc -lm generate_sites.c -ogenX
	cp genX ~/local/bin/
osc:solver.c functions.c headers.h
	gcc -lm -Wall -oosc solver.c
	cp osc ~/local/bin
backup:
	mkdir Sources_Bak.tmp
	date > backup_date.txt
	cp Makefile *.m *.c *.ini *.sh backup_date.txt Sources_Bak.tmp
	tar -jcf sources.tar.bz2 Sources_Bak.tmp
	mv sources.tar.bz2 ~
	rm -rf Sources_Bak.tmp
