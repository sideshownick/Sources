#!python
#from Numeric import *
from numpy import *
from scipy import *
from scipy import zeros
from scipy.linalg import *
from scipy import sparse
import os
#import time
#from pylab import save
from random import random

#global size
#global ratioC

def generate(size,ratioC):
	N=2*size**2 #=size*(size+1) + size*(size-1) #=H + V 

	fval=zeros([4*(size+10)**2])
 
        for i in range(0,(2*size+1)**2):
	    if random() < ratioC:
	      fval[i]=1
	      
	matC=[]
	matR=[]
	#horizontal components:

	for cy in range(0,size+1):
	  for cx in range(1,size-1):
            if random() < ratioC:
	      #os.system('echo "%d %d 1" >> matrixC.mat'%(cx+cy*(size-1)+1,cx+cy*(size-1)))
	      matC.append([cx+cy*(size-1)+1,cx+cy*(size-1)])
	    else:
	      #os.system('echo "%d %d 1" >> matrixR.mat'%(cx+cy*(size-1)+1,cx+cy*(size-1)))
	      matR.append([cx+cy*(size-1)+1,cx+cy*(size-1)])

	#vertical components:
	for cy in range(0,size):
	  for cx in range(1,size):
	    if random() < ratioC:
	      #os.system('echo "%d %d 1" >> matrixC.mat'%(cx+cy*(size-1)+size-1,cx+cy*(size-1)))
	      matC.append([cx+cy*(size-1)+size-1,cx+cy*(size-1)])
	    else:
	      #os.system('echo "%d %d 1" >> matrixR.mat'%(cx+cy*(size-1)+size-1,cx+cy*(size-1)))
	      matR.append([cx+cy*(size-1)+size-1,cx+cy*(size-1)])

	#boundary:
        #note there are (s+1)(s-1) internal nodes, plus 2 boundary nodes
	for cy in range(0,size+1):
	  cx=1
          #boundary 1
          if random() < ratioC:
	    #os.system('echo "%d %d 1" >> matrixC.mat'%((size-1)*(size)+2,cy*(size-1)+1))
	    matC.append([(size+1)*(size-1)+1, cy*(size-1)+(cx-1)])
	  else:
	    #os.system('echo "%d %d 1" >> matrixR.mat'%((size-1)*(size)+2,cy*(size-1)+1))
	    matR.append([(size+1)*(size-1)+1, cy*(size-1)+(cx-1)])

	  #boundary 2
          cx=size-1
          if random() < ratioC:
	    #os.system('echo "%d %d 1" >> matrixC.mat'%((size-1)*(size)+1,(cy+1)*(size-1)))
	    matC.append([(size+1)*(size-1)+2, cy*(size-1)+1])
	  else:
	    #os.system('echo "%d %d 1" >> matrixR.mat'%((size-1)*(size)+1,(cy+1)*(size-1)))
	    matR.append([(size+1)*(size-1)+2, cy*(size-1)+1])
	  
	size1=2*size-1
	size2=size+size+1
	size1a=2*size-3
	size2a=size+size-1
	size0=size+1
    
	spread=0.0
    
	N=(size+1)*(size-1)
	Np=(size+1)*(size-1)+2
	LC=mat(zeros([Np, Np]))
	LR=mat(zeros([Np, Np]))
	LCi=[]
	LCj=[]
	LCv=[]
	LRi=[]
	LRj=[]
	LRv=[]

	for line in matC: #file('matrixC.mat'):
	    values = line[0], line[1], 1 #.split()
	    LC[int(values[0])-1,int(values[1])-1]-=(double(values[2]))
	    LC[int(values[1])-1,int(values[0])-1]-=(double(values[2]))
	    LC[int(values[1])-1,int(values[1])-1]+=(double(values[2]))
	    LC[int(values[0])-1,int(values[0])-1]+=(double(values[2]))
	    #os.system('echo "%d %d %f" >> matrixC.txt' %(double(values[0]),double(values[1]),double(values[2])+randvar))
	    if int(values[0]) < N+1 and int(values[1]) < N+1:
	       	LCi.append(int(values[0])-1)
	    	LCj.append(int(values[1])-1)
	   	LCv.append(-(double(values[2])))
		LCi.append(int(values[1])-1)
	    	LCj.append(int(values[0])-1)
	   	LCv.append(-(double(values[2])))
	    if int(values[0]) < N+1:
		LCi.append(int(values[0])-1)
	    	LCj.append(int(values[0])-1)
	   	LCv.append(double(values[2]))
	    if int(values[1]) < N+1:
		LCi.append(int(values[1])-1)
	    	LCj.append(int(values[1])-1)
	   	LCv.append(double(values[2]))

	for line in matR: #file('matrixR.mat'):
	    values = line[0], line[1], 1 #.split()
	    LR[int(values[0])-1,int(values[1])-1]-=(double(values[2]))
	    LR[int(values[1])-1,int(values[0])-1]-=(double(values[2]))
	    LR[int(values[1])-1,int(values[1])-1]+=(double(values[2]))
	    LR[int(values[0])-1,int(values[0])-1]+=(double(values[2]))
	    #os.system('echo "%d %d %f" >> matrixR.txt' %(double(values[0]),double(values[1]),double(values[2])+randvar))
	    if int(values[0]) < N+1 and int(values[1]) < N+1:
	    	LRi.append(int(values[0])-1)
	    	LRj.append(int(values[1])-1)
	   	LRv.append(-(double(values[2])))
		LRi.append(int(values[1])-1)
	    	LRj.append(int(values[0])-1)
	   	LRv.append(-(double(values[2])))
	    if int(values[0]) < N+1:
		LRi.append(int(values[0])-1)
	    	LRj.append(int(values[0])-1)
	   	LRv.append(double(values[2]))
	    if int(values[1]) < N+1:
		LRi.append(int(values[1])-1)
	    	LRj.append(int(values[1])-1)
	   	LRv.append(double(values[2]))
		

	LC2 = sparse.coo_matrix((LCv,(LCi,LCj)),shape=(N,N)).tocsr()
	LR2 = sparse.coo_matrix((LRv,(LRi,LRj)),shape=(N,N)).tocsr()

	LC1=LC2#.ensure_sorted_indices()
	LR1=LR2#.ensure_sorted_indices()


	return LC, LR, LC1, LR1




if __name__ == '__main__':
    print generate(4, 0.4)












