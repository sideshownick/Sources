#!/bin/bash
#gcc -lm -ogen generate_from_map.c
##cat Untitled.txt | gawk '/black/ { print "0 0 0" } /white/ { print "0 0 1" }' > spd.txt

size=21
ratio=0.4

#cd 0${size}_Size$size
#cp ../Untitled.xbm .

rm spd.txt

#get system size from "parameters.ini"
#size=`cat parameters.ini | echo \`cat\` | gawk '{print $1}'`
let size1=2*$size-1
let size2=$size+$size+1
let size1a=2*$size-3
let size2a=$size+$size-1
let size0=$size+1

echo "$size $ratio 1 0.0 1 0.0 1 1" > parameters.ini

convert UntitledH.xbm Untitled.txt
exec < Untitled.txt
read line
i=0
while [ $i -lt $size1 ]
do
  j=0
  while [ $j -lt $size2 ]
  do
	read line
	val=`echo $line | gawk '/black/ { print "0" } /white/ { print "1" }'`
	echo "$j $i $val" >> spd.txt
	let j=$j+1
  done
  let i=$i+1
done

#generate RC-network and gnuplot script
gen
rm circuitRR.cir

echo ".AC DEC 10 1 10G
.print AC VOUT
.END" >> circuit.cir

#run ngspice
ngspice -b circuit.cir | grep 0.000000 > out.txt

echo "set term postscript enhanced eps color
	set size 1.5,1
	set out 'resultsH.eps'
	set multiplot
	set size 0.75,1
	set origin 0.75,0
#	set yrange[-3.5:-2.5]
	set yrange[-5:-1]
	set xrange[1:10]
	p 'out.txt' u (log10(2*pi*\$2)):(log10(5e-7/sqrt(\$4**2+\$5**2))) notitle
	set origin 0,0
	set yrange[$size:-1]
	set xrange[-1:$size0]
	p 'resistors.txt' notitle w l lt 1 lw 3, 'capacitors.txt' notitle w l lt 3 lw 3
	" | gnuplot

mv out.txt outH.txt
mv circuit.cir circuitH.txt
mv capacitors.txt capacitorsH.txt
mv resistors.txt resistorsH.txt
mv matrixC.txt matrixCH.txt
mv matrixR.txt matrixRH.txt

###############################################################################
#do again for rotated case ####################################################
###############################################################################

convert UntitledV.xbm Untitled.txt
exec < Untitled.txt
read line
i=0
while [ $i -lt $size1 ]
do
  j=0
  while [ $j -lt $size2 ]
  do
	read line
	val=`echo $line | gawk '/black/ { print "0" } /white/ { print "1" }'`
	echo "$j $i $val" >> spd.txt
	let j=$j+1
  done
  let i=$i+1
done

#generate RC-network and gnuplot script
gen
rm circuitRR.cir

echo ".AC DEC 10 1 10G
.print AC VOUT
.END" >> circuit.cir

#run ngspice
ngspice -b circuit.cir | grep 0.000000 > out.txt

echo "set term postscript enhanced eps color
	set size 1.5,1
	set out 'resultsV.eps'
	set multiplot
	set size 0.75,1
	set origin 0.75,0
#	set yrange[-3.5:-2.5]
	set yrange[-5:-1]
	set xrange[1:10]
	p 'out.txt' u (log10(2*pi*\$2)):(log10(5e-7/sqrt(\$4**2+\$5**2))) notitle
	set origin 0,0
	set yrange[$size:-1]
	set yrange[$size:-1]
	set xrange[-1:$size0]
	p 'resistors.txt' notitle w l lt 1 lw 3, 'capacitors.txt' notitle w l lt 3 lw 3
	" | gnuplot

mv out.txt outV.txt
mv circuit.cir circuitV.txt
mv capacitors.txt capacitorsV.txt
mv resistors.txt resistorsV.txt
mv matrixC.txt matrixCV.txt
mv matrixR.txt matrixRV.txt

i=0
while [ $i -lt 101 ]
do
#echo `cat outH.txt | grep -m1 ^$i` `cat outV.txt | grep -m1 ^$i`
echo `cat outH.txt | grep -m1 ^$i | gawk '{ print $1 " " $2 " " $4 " " $5 " " }'` `cat outV.txt | grep -m1 ^$i | gawk '{ print $4 " " $5 " " }'` >> out.txt
let i=i+1
done

echo "set term postscript color eps enhanced
      set out 'geomean.eps'
      set xrange[1:10]
      set yrange[-5:-1]
      set key left
      p 'out.txt' u (log10(2*pi*\$2)):(log10(5e-7/sqrt(sqrt(\$3**2+\$4**2)*sqrt(\$5**2+\$6**2)))) notitle w p 3,\
      $ratio*x-5.4 title 'slope=$ratio' w l 2" | gnuplot -persist
