from pylab import *
from scipy import sparse
from scipy.integrate import odeint
import os, time
from osc_eqn import osc2
from my_parameters import *

detune=0.001
alpha0=3.08
alpha1=1e-3*random(Nosc)+alpha0
alpha1=1.0/(alpha1)

length1=length*stepsize+1
tlength=translength*stepsize+1


S1=zeros((Nosc,Nosc))
S1[0,5]=S1[1,4]=S1[2,3]=0.8
S1[3,0]=S1[3,1]=S1[4,0]=S1[4,2]=S1[5,1]=S1[5,2]=0.4

#for i in range(0,Nosc-1):
#    S1[i,i+1]=0.2
#S1[Nosc-1,0]=0.8

print S1

S=sparse.csr_matrix(S1)

#ic1=[]
#for line in file('fc0.txt'):
#	ic1.append(double(line))

for coupling in [0.11]:#arange(0.11,0.115,0.001): #[0.09]:
	try: os.mkdir('Data')
	except: pass

	#arange(3.535,3.55,0.001):
	for beta in [3.5]:
		beta1=1e-3*random(Nosc)+beta
		beta1=1.0/(beta1)
		outname='a%2.3f_b%2.3f_c%2.3f'%(alpha0,beta,coupling)
		print 'running params %s'%outname
		#set initial conditions
		#x=ic1		
		

		x=[]
		for n in range(0, Nosc):
			x.append(0.01*rand()+(-1)**(n+1)*3)
		for n in range(0, Nosc):	
			x.append((-1)**(n+1)*0.3)
		for n in range(0, Nosc):	
			x.append((-1)**(n+1)*1.0) 
		x=array(x)
		   
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
		print "Solved in %e seconds (%e transient + %e printed)" % (time2-time0,time1-time0,time2-time1)  
		
		plot(trajectory[:,0])
		savefig('traj.png')
		
		savetxt('fc.txt',trajectory[-1,:])		

		traj3=reshape(trajectory,(length,Nosc*3))	
		savetxt('data_trajectory.txt',traj3)
		

#end
