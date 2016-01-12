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
    
    N=(size+1)*(size-1) #internal nodes
    Np=(size+1)*(size-1)+2 #including boundary nodes
    LC=mat(zeros([Np, Np]))
    LR=mat(zeros([Np, Np]))
    LCi=[]
    LCj=[]
    LCv=[]
    LRi=[]
    LRj=[]
    LRv=[]

    for line in file('matrixC.mat'):
      values = line.split()
      if float(values[2]) < 0:
        LC[int(values[0]),int(values[1])]+=(float(values[2]))
        LC[int(values[0]),int(values[0])]-=(float(values[2]))
        #os.system('echo "%d %d %f" >> matrixC.txt' %(double(values[0]),double(values[1]),double(values[2])+randvar))
        if 1 <= int(values[0]) <= N and 1 <= int(values[1]) <= N:
            LCi.append(int(values[0])-1) #counting from 0 in new matrix
            LCj.append(int(values[1])-1)
            LCv.append(float(values[2]))
        if 1 <= int(values[0]) <= N:
                LCi.append(int(values[0])-1)
                LCj.append(int(values[0])-1)
                LCv.append(-float(values[2]))
                            
    for line in file('matrixR.mat'):
      values = line.split()
      if float(values[2]) < 0:
        LR[int(values[0]),int(values[1])]+=(float(values[2]))
        LR[int(values[0]),int(values[0])]-=(float(values[2]))
        #os.system('echo "%d %d %f" >> matrixR.txt' %(double(values[0]),double(values[1]),double(values[2])+randvar))
        if 1 <= int(values[0]) <= N and 1 <= int(values[1]) <= N:
            LRi.append(int(values[0])-1)
            LRj.append(int(values[1])-1)
            LRv.append(float(values[2]))
        if 1 <= int(values[0]) <= N:
                LRi.append(int(values[0])-1)
                LRj.append(int(values[0])-1)
                LRv.append(-float(values[2]))
		
    LC2 = sparse.coo_matrix((LCv,(LCi,LCj)),shape=(N,N)).tocsr() #not including boundary data
    LR2 = sparse.coo_matrix((LRv,(LRi,LRj)),shape=(N,N)).tocsr() #except in diagonals

    LC1=LC2#.ensure_sorted_indices()
    LR1=LR2#.ensure_sorted_indices()


    return LC, LR, LC1, LR1




if __name__ == '__main__':
    print generate(4, 0.4)












