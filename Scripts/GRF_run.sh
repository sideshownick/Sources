#!/bin/bash
#gcc -lm -ogen generate_from_map.c
##cat Untitled.txt | gawk '/black/ { print "0 0 0" } /white/ { print "0 0 1" }' > spd.txt
./field_demo field.ini
cat sphd.txt | grep -v "#" > spd.txt

#get system size from "parameters.ini"
size=`cat parameters.ini | echo \`cat\` | gawk '{print $1}'`
let size1=2*$size-1
let size2=$size+$size+1

#backup old files
rm out.txt
rm -rf Images_old
mv Images Images_old
mv -b alldata.txt alldata.bak
mkdir Images

#generate RC-network and gnuplot script
./gen

#run ngspice
ngspice -b circuit.cir > out_all.txt

#extract total output to out.txt
exec < out_all.txt
while read line
do
  for word in $(echo $line)
  do
    if [ $word = vout ]
    then
    	read line
        read line

	while [ `echo $line | awk '{print $5}'` ]
        do
		echo $line >> out.txt
		read line
	done
    fi
  done
done

#plot network diagram, total conductance and phase
echo "set yrange[$size:-1]; set term postscript color; set title 'Components';set out 'comps.ps'; p 'capacitors.txt' title 'C' w l lw 2, 'resistors.txt' title 'R' w l lw 3" | gnuplot
echo "set yrange[-3:0]; set term postscript enhanced color; set title 'Conductivity'; set ylabel 'log_{10}({/Symbol e})'; set xlabel \"log_{10}({/Itallic f})\"; set out 'cond.ps'; p 'out.txt' u (log10(\$2)):(log10(1e-5/sqrt(\$4**2+\$5**2))) notitle w lp" | gnuplot
echo "set yrange[-90:0]; set term postscript enhanced color; set title 'Phases'; set ylabel 'log_{10}({/Symbol f})'; set xlabel \"log_{10}({/Itallic f})\"; set angles degrees; set out 'phase.ps'; p 'out.txt' u (log10(\$2)):(atan(\$5/\$4)) notitle w lp" | gnuplot

#sort out_all.txt for plotting
mkdir Tmp_Data
exec < out_all.txt
while read line
do

  for word in $(echo $line)
  do

    if [ $word = frequency ]
    then

#get node name
      node=`echo $line | awk '{print $3}'`

#exclude v1#branch
      if [ $node = "v1#branch" ]
      then
        break
      fi

#exclude r1_n
      if [ $node = "r1_n" ]
      then
        break
      fi

      read line
      read line

#check for 5 entries before parsing
      while [ `echo $line | awk '{print $5}'` ]
      do
	echo $line | awk '{print $4 " " $5}' >> Tmp_Data/`echo $line | awk '{print $2}'`
	read line
      done

    fi

  done

done

for i in $( ls Tmp_Data )
do
  echo `cat Tmp_Data/$i` >> Tmp_Data/$i.tmp
  echo "$i `cat Tmp_Data/$i.tmp`" >> alldata.txt
done

rm -rf Tmp_Data


#make series of images for node voltages and current flows
i=10
while [ $i -lt 90 ]
do
  j=`echo "scale=1;$i/10" | bc -l`
  k=`echo "scale=1;$i/10+0.2" | bc -l`
  echo "set title '{/Itallic f}=10^{$j} (Hz)'" > gp.tmp
  echo "set zrange[$j:$k]" >> gp.tmp
  cat gnuplot_map0 >> gp.tmp
  gnuplot gp.tmp
  convert -rotate 90 new.ps Images/0$i.png
  rm new.ps
  let i=$i+1
done

rm gp.tmp
rm seed

