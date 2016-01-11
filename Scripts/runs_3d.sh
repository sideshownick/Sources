#!/bin/bash
i=1
while [ $i -lt 21 ]
do
#  cp -ax 00_Templates Depth_$i
  mkdir Depth_$i
  cd Depth_$i
  echo "20 $i 0.3 1 0.0 1 0.0" > parameters.ini

mv out.txt out.old
counter=0
nruns=100
while [ $counter -lt $nruns ]
do
  echo "Run: $counter/$nruns"
  gen3d
  echo ".AC DEC 10 1 1G
.print AC V(VOUT)
.END" >> circuit.cir
  ngspice -b circuit.cir 2>/dev/null | grep "0.000000e+00" >> out.txt
  echo " " >> out.txt
  let counter=$counter+1
done

echo "set term table
set out 'out1.txt'
p 'out.txt' u (log10(\$2)):(log10(5e-7/sqrt(\$4**2+\$5**2)))" | gnuplot

grep -v "#" out1.txt > out2.txt

histt -i "out2.txt" -o "histoV.txt" -a 0 -b 9 -c -5 -d 0 -x 90 -y 200 

echo "set title 'Size $i'
set term postscript color enhanced eps
set out 'histoV.eps'
set palette rgbformulae 30,31,32 negative
set pm3d map
set xrange [0:9]
sp 'histoV.txt' notitle w pm3d" | gnuplot

  cd ..
  let i=$i+1
done
