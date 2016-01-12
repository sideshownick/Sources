#!/usr/bin/env python
import numpy, sys
sys.path.append('Python')
#import matplotlib
import cmath
import math
#matplotlib.use=('Agg')
#import pylab
#from pylab import *
from scipy import *


def write_mimu(lap,par,ic,outfile='workfile'):
	#lap = loadtxt('lap_BA_'+str(N)+'_'+str(M)+'.txt')

	ndim =  2*shape(lap)[1]

	Id = eye(ndim)
	M = -lap
	f = open(outfile+'.f', 'w+')


	f.write('C--------------------------------------------------------------------\n')
	f.write('C------------  Continuation in Random Networks  ---------------------\n')
	f.write('C------------             (MM)                -----------------------\n')
	f.write('C--------------------------------------------------------------------\n')
	f.write('C\n')
	f.write('      SUBROUTINE FUNC(NDIM,U,ICP,PAR,IJAC,F,DFDU,DFDP)\n')
	f.write('C\n')
	f.write('      IMPLICIT DOUBLE PRECISION (A-H,O-Z)\n')
	f.write('      DIMENSION U(NDIM),PAR(*),F(NDIM),DFDU(NDIM,*),DFDP(NDIM,*) \n')
	f.write('C--------------------------------------------------------------------\n')
	f.write('C\n')
	f.write('      t=-(2.0D0*PAR(4)+PAR(3)-PAR(2)*PAR(4))/(2*PAR(4)**2) \n')
	f.write('      vb=t+DSQRT(t**2+(PAR(1)+PAR(2)-1.0D0)/PAR(4)**2)\n')
	f.write('      ub=1+PAR(4)*vb \n')
	f.write('C \n')
	
	for ii in range(0,ndim/2):
		iss=ii+1
		is2=iss+ndim/2
		f.write('      F('+str(iss)+')=')
		f.write('(U('+str(iss)+')+ub)*((PAR(1)+PAR(2)*(U('+str(iss)+')+ub)\n')
		f.write('     + -(U('+str(iss)+')+ub)**2)/PAR(3)-(U('+str(is2)+')+vb))\n')
		f.write('     + ')
		cnt = 1
		for jj in range(0,ndim/2):
			
			jss=jj+1
			js2=jss+ndim/2
			v=M[ii,jj]
			if v!=0:
				f.write('+PAR(5)*('+str(v)+'D0)*U('+str(jss)+')')
				cnt = cnt+1
			if cnt % 3 ==0:
				f.write('\n')
				f.write('     + ')
				cnt=1
		
		f.write('\n')
		f.write('      F('+str(is2)+')=')
		f.write('(U('+str(is2)+')+vb)*((U('+str(iss)+')+ub)-(1+PAR(4)*(U('+str(is2)+')+vb)))\n')
		f.write('     + ')
		cnt = 1
		for jj in range(0,ndim/2):
			
			jss=jj+1
			js2=jss+ndim/2
			v=M[ii,jj]
			if v!=0:
				f.write('+PAR(5)*PAR(6)*('+str(v)+'D0)*U('+str(js2)+')')
				cnt = cnt+1
			if cnt % 3 ==0:
				f.write('\n')
				f.write('     + ')
				cnt=1
				
		f.write('\n')
	f.write('C\n')
	f.write('      RETURN\n')
	f.write('      END\n')
	f.write('C\n')
	f.write('      SUBROUTINE STPNT(NDIM,U,PAR)\n')
	f.write('C\n')
	f.write('      IMPLICIT DOUBLE PRECISION (A-H,O-Z)\n')
	f.write('      DIMENSION U(NDIM),PAR(*)\n')
	f.write('C---------------------------------------------------------------------\n')
	f.write('C\n')
	f.write('      PAR(1)=%fD0\n'%par[0])
	f.write('      PAR(2)=%fD0\n'%par[1])
	f.write('      PAR(3)=%fD0\n'%par[2])
	f.write('      PAR(4)=%fD0\n'%par[3])
	f.write('      PAR(5)=%fD0\n'%par[4])
	f.write('      PAR(6)=%fD0\n'%par[5])
	f.write('C\n')
	
	for ii in range(0,ndim/2):
		iss=ii+1
		is2=iss+ndim/2
		f.write('      U('+str(iss)+')=%fD0\n'%ic[ii])
		f.write('      U('+str(is2)+')=%fD0\n'%ic[ndim/2+ii])
	f.write('C\n')
	f.write('      RETURN\n')
	f.write('      END\n')
	f.write('C\n')
	f.write('      SUBROUTINE PVLS(NDIM,U,PAR)\n')
	f.write('      IMPLICIT DOUBLE PRECISION (A-H,O-Z)\n')
	f.write('      DIMENSION U(NDIM),PAR(*)\n')
	f.write('      RETURN\n')
	f.write('      END\n')
	f.write('C\n')
	f.write('      SUBROUTINE BCND(NDIM,PAR,ICP,NBC,U0,U1,FB,IJAC,DBC)\n')
	f.write('      IMPLICIT DOUBLE PRECISION (A-H,O-Z)\n')
	f.write('      DIMENSION PAR(*),ICP(*),U0(NDIM),U1(NDIM),FB(NBC)\n')
	f.write('C\n')
	f.write('      RETURN\n')
	f.write('      END\n')
	f.write('C\n')
	f.write('      SUBROUTINE ICND\n')
	f.write('      RETURN\n')
	f.write('      END\n')
	f.write('C\n')
	f.write('      SUBROUTINE FOPT\n')
	f.write('      RETURN\n')
	f.write('      END\n')
	f.write('C\n')
		
	
	
	f.close()
	

