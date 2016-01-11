from pylab import *
from scipy import sparse
from scipy.integrate import odeint
import os, time
from osc_eqn import osc2
from my_parameters import *

detune=0.001
alpha0=3.08
alpha1=[1.0/(alpha0+detune),1.0/(alpha0-detune)]
translength=1000

length1=length*stepsize+1
tlength=translength*stepsize+1

S=sparse.csr_matrix(matrix(((0,1),(1,0))))

#ic1=[]
#for line in file('fc0.txt'):
#	ic1.append(double(line))

for coupling in [0.11]:#arange(0.11,0.115,0.001): #[0.09]:
	try: os.mkdir('Data')
	except: pass
	x=[3.0,-3.1,\
	   0.3,-0.3,\
	   1.0,-1.0]	
	
	for beta in [3.5]:#arange(3.535,3.55,0.001):
		beta1=[1.0/(beta+detune),1.0/(beta)]
		outname='a%2.3f_b%2.3f_c%2.3f'%(alpha0,beta,coupling)
		print 'running params %s'%outname
		#set initial conditions
		#x=ic1		
		
		'''
		x=[]
		for n in range(0, Nosc):
			x.append(0.02*rand()-0.01)
		#x.append(-2.51)	#-2.5*(1+sigma*(2*rand()-1)))
		#x.append(2.5)
		for n in range(0, Nosc):	
			x.append(-1.0) #(0.02*rand()-0.01)	#0.1*(1+sigma*(2*rand()-1)))
		for n in range(0, Nosc):	
			x.append(1.0) #(0.02*rand()-0.01)	#-1.0*(1+sigma*(2*rand()-1)))
		'''
		   
		time0=time.time()

		##transient
		timepoints = arange(1., tlength, stepsize)
		transient = odeint(osc2, x, timepoints, args=(alpha1, beta1, coupling, S))
		tran3=reshape(transient,(translength,Nosc*3))
		savetxt('data_transient.txt',tran3)

		x=transient[-1,:]
		time1=time.time()

		timepoints = arange(1., length1, stepsize)
		trajectory = odeint(osc2, x, timepoints, args=(alpha1, beta1, coupling, S))
		time2=time.time()
		x=trajectory[-1,:]
		
		savetxt('fc.txt',trajectory[-1,:])

		print "Solved in %e seconds (%e transient + %e printed)" % (time2-time0,time1-time0,time2-time1)		

		traj3=reshape(trajectory,(length,Nosc*3))	
		savetxt('data_trajectory.txt',traj3)
		

#end
