#!/bin/bash
#gcc -lm -ogen generate_from_map.c
##cat Untitled.txt | gawk '/black/ { print "0 0 0" } /white/ { print "0 0 1" }' > spd.txt

#size=9
for size in $( echo "20" )
do

ps=`echo "scale=2; 5/$size" | bc -l`

echo $size

rm spd.txt

#get system size from "parameters.ini"
#size=`cat parameters.ini | echo \`cat\` | gawk '{print $1}'`
let size1=2*$size-1
let size2=$size+$size+1
let size1a=2*$size-3
let size2a=$size+$size-1
let size0=$size+1

echo "$size 0.5 1 0.0 1 0.0 1 1" > parameters.ini

#field_demo field.ini

#convert x-bitmap file to "x y 1/0" file
#echo "convert -crop ${size2a}x${size1a} Untitled.xbm UntitledX.xbm"
#convert -crop ${size2a}x${size1a} Untitled.xbm UntitledX.xbm
#convert -border 1x1 -bordercolor black UntitledX-0.xbm Untitled.xbm
#rm UntitledX*

#convert -negate Untitled.xbm Untitled.txt
cat sphd.txt | grep -v "#" > spd1.txt
#exec < Untitled.txt
exec < spd1.txt
read line
i=0
while [ $i -lt $size1 ]
do
  j=0
  while [ $j -lt $size2 ]
  do
	read line
	j=`echo $line | gawk '{print $1}'`
	i=`echo $line | gawk '{print $2}'`
	val1=`echo $line | gawk '{print $3}'`
	val=`echo $val1 | gawk '/1/ { print "1" } /0/ { print "0" }'`
#val=`echo $line | gawk '/black/ { print "0" } /white/ { print "1" }'`
	echo "$j $i $val" >> spd.txt
	let j=$j+1
  done
  let i=$i+1
done

#generate RC-network and gnuplot script
gen

echo ".AC DEC 10 1 10G
.print AC V(VOUT)
.END" >> circuit.cir

ngspice -b circuit.cir | grep 0.000000 > out.txt

echo "%%MatrixMarket matrix coordinate real symmetric" > matrixC.mtx
echo "%%MatrixMarket matrix coordinate real symmetric" > matrixR.mtx

c1=`wc matrixC.txt | awk '{print $1}'`
r1=`wc matrixR.txt | awk '{print $1}'`
s=`cat parameters.ini | echo \`cat\` | awk '{print $1}'`
s2=`echo "$s*($s-1)+2" | bc`; s3=`echo "$s2+1" | bc`
echo "$s2 $s2 $c1" >> matrixC.mtx
echo "$s2 $s2 $r1" >> matrixR.mtx
cat matrixC.txt >> matrixC.mtx
cat matrixR.txt >> matrixR.mtx

matlabR16 -nodesktop -nosplash -nojvm -nodisplay < evals.m

cat eigsCD.txt | grep -v "Inf" >> eCD.tmp
cat eigsDC.txt | grep -v "Inf" >> eDC.tmp
cat eigsRD.txt | grep -v "Inf" >> eRD.tmp

mv eCD.tmp eigsCD.txt
mv eDC.tmp eigsDC.txt
mv eRD.tmp eigsRD.txt


echo "set term table; set out 'eigs_cd.txt'; p 'eigsCD.txt' u 0:(1/\$1)" | gnuplot

cat eigs_cd.txt | grep -v "#" | cut -d' ' -f 3 > polesCD.txt

makehist -i "eigsCD.txt" -o "histoCD.txt" -x -1.01 -y 0.01 -n 200
makehist -i "eigsRD.txt" -o "histoRD.txt" -x -1.01 -y 0.01 -n 200
makehist -i "eigsDC.txt" -o "histoDC.txt" -x -10 -y -1 -n 100
makehist -i "polesCD.txt" -o "histopoles.txt" -x -10 -y -1 -n 100
#echo " set style fill pattern 1; p 'histopoles.txt' title 'DC' w boxes" | gnuplot -persist
#echo " set style fill pattern 1; p 'histoCD.txt' title 'CD' w boxes" | gnuplot -persist


echo "set term postscript enhanced eps color; set size 1,1; set out 'eigenvaluesCb.eps'; set multi; set size 0.5,0.5; set style fill pattern 1; set size 0.5,0.5; set yrange[0:5]; set origin 0.5,0; p 'histoCD.txt' u (\$1+1):2 notitle w boxes; reset; set size 0.5,0.5; set origin 0.5,0.5; set yrange[-5:0]; p 'out.txt' u (log10(\$2)):(log10(5e-7/sqrt(\$4**2+\$5**2))) notitle w l; reset; set origin 0,0; set size 0.5,0.5; unset border; unset xtics; unset ytics; p 'capacitors.txt' title '' w l lt 3 lw 3, 'resistors.txt' title '' w l lt 1 lw 3; set origin 0,0.5; set view map; set cbrange[-1:5]; set palette defined (-1 'black', 0 'white', 1 'yellow', 2 'green', 3 'blue', 4 'purple', 5 'red'); sp 'fullC.txt' matrix title '' w p palette pt 5 ps $ps" | gnuplot -persist

##do again for complimentary case...
rm spd.txt
cat sphd.txt | grep -v "#" > spd1.txt
exec < spd1.txt
read line
i=0
while [ $i -lt $size1 ]
do
  j=0
  while [ $j -lt $size2 ]
  do
	read line
	j=`echo $line | gawk '{print $1}'`
	i=`echo $line | gawk '{print $2}'`
	val1=`echo $line | gawk '{print $3}'`
	val=`echo $val1 | gawk '/1/ { print "0" } /0/ { print "1" }'`
#val=`echo $line | gawk '/black/ { print "0" } /white/ { print "1" }'`
	echo "$j $i $val" >> spd.txt
	let j=$j+1
  done
  let i=$i+1
done

#generate RC-network and gnuplot script
gen

echo ".AC DEC 10 1 10G
.print AC V(VOUT)
.END" >> circuit.cir


ngspice -b circuit.cir | grep 0.000000 > out.txt

echo "%%MatrixMarket matrix coordinate real symmetric" > matrixC.mtx
echo "%%MatrixMarket matrix coordinate real symmetric" > matrixR.mtx

c1=`wc matrixC.txt | awk '{print $1}'`
r1=`wc matrixR.txt | awk '{print $1}'`
s=`cat parameters.ini | echo \`cat\` | awk '{print $1}'`
s2=`echo "$s*($s-1)+2" | bc`; s3=`echo "$s2+1" | bc`
echo "$s2 $s2 $c1" >> matrixC.mtx
echo "$s2 $s2 $r1" >> matrixR.mtx
cat matrixC.txt >> matrixC.mtx
cat matrixR.txt >> matrixR.mtx

matlabR16 -nodesktop -nosplash -nojvm -nodisplay < evals.m

cat eigsCD.txt | grep -v "Inf" >> eCD.tmp
cat eigsDC.txt | grep -v "Inf" >> eDC.tmp
cat eigsRD.txt | grep -v "Inf" >> eRD.tmp
mv eCD.tmp eigsCD.txt
mv eDC.tmp eigsDC.txt
mv eRD.tmp eigsRD.txt

echo "set term table; set out 'eigs_cd.txt'; p 'eigsCD.txt' u 0:(1/\$1+1)" | gnuplot

cat eigs_cd.txt | grep -v "#" | cut -d' ' -f 3 > polesCD.txt

makehist -i "eigsCD.txt" -o "histoCD.txt" -x -1.01 -y 0.01 -n 200
makehist -i "eigsRD.txt" -o "histoRD.txt" -x -1.01 -y 0.01 -n 200
makehist -i "eigsDC.txt" -o "histoDC.txt" -x -10 -y -1 -n 100
makehist -i "polesCD.txt" -o "histopoles.txt" -x -10 -y -1 -n 100
#echo " set style fill pattern 1; p 'histopoles.txt' title 'DC' w boxes" | gnuplot -persist
#echo " set style fill pattern 1; p 'histoCD.txt' title 'CD' w boxes" | gnuplot -persist

echo "set term postscript enhanced eps color; set size 1,1; set out 'eigenvaluesRb.eps'; set multi; set size 0.5,0.5; set style fill pattern 1; set size 0.5,0.5; set yrange[0:5]; set origin 0.5,0; p 'histoCD.txt' u (\$1+1):2 notitle w boxes; reset; set size 0.5,0.5; set origin 0.5,0.5; set yrange[-4:-1]; p 'out.txt' u (log10(\$2)):(log10(5e-7/sqrt(\$4**2+\$5**2))) notitle w l; reset; set origin 0,0; set size 0.5,0.5; unset border; unset xtics; unset ytics; p 'capacitors.txt' title '' w l lt 3 lw 3, 'resistors.txt' title '' w l lt 1 lw 3; set origin 0,0.5; set view map; set cbrange[-1:5]; set palette defined (-1 'black', 0 'white', 1 'yellow', 2 'green', 3 'blue', 4 'purple', 5 'red'); sp 'fullC.txt' matrix title '' w p palette pt 5 ps $ps" | gnuplot -persist


cd ../
done
