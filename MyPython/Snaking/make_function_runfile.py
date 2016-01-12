import sys, os
from scipy import loadtxt, random, sparse, integrate, savetxt
from scipy.optimize import fsolve
import time
#from matplotlib.pyplot import plot as mpplot
#from matplotlib.pyplot import savefig as mpsavefig
#from matplotlib.pyplot import clf as mpclf
#sys.path.append('../../Scripts/')
from my_write_mimu2 import write_mimu
from mimura2 import *

def gen_IC(sigma,rn,outfile="workfile",icdir="ICs", M=5, N=50, lapfile="Laplacian.txt", tries=10, iclist=[]):
   lap = loadtxt(lapfile)
   spa = sparse.csr_matrix(lap)
   success=0
   attempts=0
   while success==0 and attempts<tries:
     try:
	tag='s%.2fr%.3d'%(sigma,rn)
	tag=tag.replace(".", "")

	parameters = [35.0, 16.0, 9.0, 0.4, 0.12, sigma]
	x0=10*(random.random(2*N)-0.5)

	tic=time.time()
	trajectory = integrate.odeint(mimura, x0, range(0,1000), args=(parameters,spa))
	print "integration took", time.time()-tic, "seconds"

	x1=trajectory[-1]

	sol=fsolve(mimura3, x1, args=(parameters,spa),full_output=True)
	x2=sol[0]
	if x2 not in iclist:
	    savetxt(icdir+'/init_cond_'+tag+'.txt',x2)
	    write_mimu(lap,par=parameters,ic=x2,outfile=outfile)
    	    iclist.append(x2)
	    success=1
	tries+=1
     except: pass
   return iclist

def plotfigs(tag):
	bd=loadbd('workfile_'+tag)
	p=plot(bd, hide=True, stability=True, use_symbols=False)
	p.savefig('bifdiag_'+tag+'.png')

	limp=bd('LP')[0]
	lab=limp['Label']
	solution=bd(lab).toarray()

	mpplot([0,50],[0,0],'k-')
	for i in range(0,50):
        	mpplot([i+1,i+1],[0,solution[i][0]],'r-')
        	mpplot([i+1,i+1],[0,solution[i+50][0]],'b-')
        	mpplot(i+1,solution[i][0],'ro')
        	mpplot(i+1,solution[i+50][0],'bo')
	figname='solution_'+tag+'_'+str(lab)+'.png'
	mpsavefig(figname)
	mpclf()

