#!/bin/bash
rm results.txt results0.txt
for i in $( ls -d Size.* )
do
  echo $i
  cd $i/Data
  ~/bin/interp -a -5.5 -b -0.5
#  echo "p 'out.txt' u (log10(\$2)):(log10(5e-7/sqrt(\$4**2+\$5**2))) smooth csplines 2, 'lower.txt' w p 1, 'upper.txt' w p 3" | gnuplot -persist
#  echo "set angles degrees; p 'out.txt' u (log10(\$2)):(atan(\$5/\$4)) smooth csplines 2, 'cut1.txt' w p 1, 'cut2.txt' w p 3" | gnuplot -persist

  echo "$i" >> ../../results0.txt
  echo " " >> ../../results0.txt

  rm fit.log
  echo "f(x)=c; fit f(x) 'cut1.txt' u 2:1 via c" | gnuplot &> /dev/null
  echo "lower phase bound:" >> ../../results0.txt
  grep -A 3 -B 4 "Final set of parameters" fit.log >> ../../results0.txt
  echo "------------------------------------------------------------------" >> ../../results0.txt
  echo " " >> ../../results0.txt

  line1=`grep -A 3 -B 4 "Final set of parameters" fit.log | grep "c               ="`
  line2=`grep -A 3 -B 4 "Final set of parameters" fit.log | grep "rms of residuals"`
  echo $line1
  echo $line2
  lPval=`echo $line1 | awk '{print $3}'`
  lPerr=`echo $line2 | awk '{print $8}'`
  echo " "

  rm fit.log
  echo "f(x)=c; fit f(x) 'cut2.txt' u 2:1 via c" | gnuplot  &> /dev/null
  echo "upper phase bound:" >> ../../results0.txt
  grep -A 3 -B 4 "Final set of parameters" fit.log >> ../../results0.txt
  echo "------------------------------------------------------------------" >> ../../results0.txt
  echo " " >> ../../results0.txt

  line1=`grep -A 3 -B 4 "Final set of parameters" fit.log | grep "c               ="`
  line2=`grep -A 3 -B 4 "Final set of parameters" fit.log | grep "rms of residuals"`
  echo $line1
  echo $line2
  uPval=`echo $line1 | awk '{print $3}'`
  uPerr=`echo $line2 | awk '{print $8}'`
  echo " "

  rm fit.log
  echo "f(x)=c; fit f(x) 'lower.txt' via c" | gnuplot  &> /dev/null
  echo "lower limit:" >> ../../results0.txt
  grep -A 3 -B 4 "Final set of parameters" fit.log >> ../../results0.txt
  echo "------------------------------------------------------------------" >> ../../results0.txt
  echo " " >> ../../results0.txt

  line1=`grep -A 3 -B 4 "Final set of parameters" fit.log | grep "c               ="`
  line2=`grep -A 3 -B 4 "Final set of parameters" fit.log | grep "rms of residuals"`
  echo $line1
  echo $line2
  lLval=`echo $line1 | awk '{print $3}'`
  lLerr=`echo $line2 | awk '{print $8}'`
  echo " "

  rm fit.log
  echo "f(x)=c; fit f(x) 'upper.txt' via c" | gnuplot  &> /dev/null
  echo "upper limit:" >> ../../results0.txt
  grep -A 3 -B 4 "Final set of parameters" fit.log >> ../../results0.txt
  echo " " >> ../../results0.txt

  line1=`grep -A 3 -B 4 "Final set of parameters" fit.log | grep "c               ="`
  line2=`grep -A 3 -B 4 "Final set of parameters" fit.log | grep "rms of residuals"`
  echo $line1
  echo $line2
  uLval=`echo $line1 | awk '{print $3}'`
  uLerr=`echo $line2 | awk '{print $8}'`
  echo " "

  echo "$i $lPval $lPerr $uPval $uPerr $lLval $lLerr $uLval $uLerr"
  echo "============================================="
  echo " "
  echo "$i $lPval $lPerr $uPval $uPerr $lLval $lLerr $uLval $uLerr" >> ../../results.txt
  
  echo "==============================================================" >> ../../results0.txt
  echo " " >> ../../results0.txt
  cd ../../
done

#echo "set term postscript enhanced color; set out 'results.ps'; set xrange[0:21000]; set title 'Width of region (where {/Symbol f}>{/Symbol p}/4). p(C)=0.48'; set xlabel 'N (total comps)'; set ylabel '{/Symbol d}log_{10}(f)'; p 'results.txt' u (\$1**2+(\$1-1)**2):(\$4-\$2):(sqrt(\$3**2+\$5**2)) notitle w err 1, 'results.txt' u (\$1**2+(\$1-1)**2):(\$4-\$2) notitle w p 3" | gnuplot

#gv results.ps &

