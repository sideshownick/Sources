#!/bin/bash
rm -rf Ivecs_old
mv Ivecs Ivecs_old
mkdir Ivecs
sort -g alldata.txt > alldata2.txt
i=10
exec < alldata2.txt
while read line
do
  echo $line > alldataV.txt
  g=`echo "scale=1;($i-10)/10" | bc -l`
  echo $g
  echo "set title '{/itallic f}=10^{$g}'" > vectors.gnuplot
  echo "set xlabel 'Real(I)'" >> vectors.gnuplot
  echo "set ylabel 'Imag(I)'" >> vectors.gnuplot
  cat vectors0.gnuplot >> vectors.gnuplot
  gnuplot vectors.gnuplot
  convert -rotate 90 vecs.ps Ivecs/ivecs$i.png
  let i=$i+1
done
