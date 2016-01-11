#!/bin/bash
#gcc -lm -ogen generate_from_map.c
##cat Untitled.txt | gawk '/black/ { print "0 0 0" } /white/ { print "0 0 1" }' > spd.txt
rm spd.txt

#get system size from "parameters.ini"
size=20
let size1=$size+1

echo "$size 0.5 1 0.0 1 0.0 1 1" > parameters.ini

#backup old files
#rm out.txt
#mv -b spd.txt spd.bak
#rm -rf Images_old
#mv Images Images_old
#mv -b alldata.txt alldata.bak
#mkdir Images

#convert x-bitmap file to "x y 1/0" file
convert Untitled.xbm Untitled.txt
exec < Untitled.txt
read line
i=0
while [ $i -lt $size ]
do
  j=0
  while [ $j -lt $size1 ]
  do
	read line
	val=`echo $line | gawk '/black/ { print "0" } /white/ { print "1" }'`
	echo "$j $i $val" >> spd.txt
	let j=$j+1
  done
  let i=$i+1
done

#generate RC-network and gnuplot script
genX

echo ".AC DEC 10 1 1G
.print AC VR(VOUT) VI(VOUT)
.END" >> circuit.cir

#run ngspice
ngspice -b circuit.cir | grep 0.000000 > out.txt

echo "set term postscript enhanced color
	set size 2,1
	set out 'results.ps'
	set multiplot
	set size 1,1
	p 'resistors.txt' notitle w l lt 1 lw 3, 'capacitors.txt' notitle w l lt 3 lw 3
	set origin 1,0
	set yrange[-5:-2]
	p 'out.txt' u (log10(\$2)):(log10(5e-7/sqrt(\$4**2+\$5**2))) notitle
	" | gnuplot
