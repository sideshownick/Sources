#!python
from numpy import *
from scipy import *
from scipy.linalg import *
from scipy import sparse, concatenate
from scipy.sparse.linalg import *
import os, subprocess, time, sys, shutil
from numpy import loadtxt, savetxt
from scoop import futures
from random import random

ratio=50
ratioC=ratio/100.0

C=1e-9
R=1.0e3
R1=1/R

sizes=[2048] 
#sizes=[8, 16, 32, 64, 128, 256, 512, 1024, 2048]
nruns=1


my_parameters=[]
for s in sizes:
    for r in range(nruns):
        my_parameters.append((s,r))
njobs=len(my_parameters)


def mainFunc(paramIndex):    
    size,rn = my_parameters[paramIndex]
    
    os.chdir(str(size))

    os.mkdir(str(rn))
    os.chdir(str(rn))

    ft=open("timer_"+str(size)+".txt", "w")
    ft.write("size run gentime1 gentime2 s1time runtime nsteps\n")    
    
    with open("out_all.txt", "w") as fout:       
        t1=time.time()
        
        Cfull, Rfull = generate(size, ratioC)
        t1a=time.time()
        
        LRsp = Rfull[1:-1, 1:-1]
        R_left= Rfull[1:-1, 0].toarray()
        R_right= Rfull[1:-1, -1].toarray()

        LCsp = Cfull[1:-1, 1:-1]
        C_left= Cfull[1:-1, 0].toarray()
        C_right= Cfull[1:-1, -1].toarray()
       
        t2=time.time()
        
        gentime1=t1a-t1
        gentime2=t2-t1

        def solve3(h):
            M = R1*LRsp + C*1j*h*LCsp #full RC network matrix
            BV_l = R1*R_left + C*1j*h*C_left #left boundary vector
            L_inv = linsolve.spsolve(M, BV_l)
            #L_inv = cg(M, BV_l)[0]

            BV_r = (R1*R_right+C*1j*h*C_right).transpose() #right boundary vector
            Y = dot(BV_r, L_inv) #complex admittance
            return Y
       
        t3=time.time()
        Y0=solve3(10)#(1e-20)
        t4=time.time()
        s1time=t4-t3
        e0=abs(Y0.real)
        
        logfreqs=arange(1,11,1)
        
        runvals=[[]]*len(logfreqs)
        t5=time.time()
        for i,h1 in enumerate(logfreqs): #(-3,3,0.01):
            h=10**h1
            Y=solve3(h)
            
            realpart=float(Y.real)
            imagpart=float(Y.imag)

            runvals[i] = h1, realpart, imagpart
        t6=time.time()
        runtime=t6-t5
        
        for vals in runvals:
            for val in vals:
                fout.write(str(val) + " ")
            fout.write("\n")
        fout.write("\n\n")
        
    shutil.copy("out_all.txt", "../Results/out%.3d.txt"%rn)
        
    os.chdir("../")
    shutil.rmtree(str(rn))
        
    with open("Timings/run%.3d.txt"%rn, "w") as tfile:
        tfile.write(" ".join(map(str, [size, rn, gentime1, gentime2, s1time, runtime, len(logfreqs)])))
    os.chdir("../")


    return size, rn, gentime1, gentime2, s1time, runtime, len(logfreqs)


def generate(size,ratioC):
    N=2*size**2 #=size*(size+1) + size*(size-1) #=H + V 
    
    nnodes=(size+1)*(size-1) + 2 
    
    #max possible if all are one component, include diagonal
    LCi=zeros(2*N + nnodes) 
    LCj=zeros(2*N + nnodes) 
    LCv=zeros(2*N + nnodes) 
    LRi=zeros(2*N + nnodes) 
    LRj=zeros(2*N + nnodes) 
    LRv=zeros(2*N + nnodes) 
    
    Ccount = zeros(nnodes) #counter for diagonal elements
    Rcount = zeros(nnodes)
    
    k=0 #counter
    #horizontal "X" components 
    for cy in range(0,size+1):
        rowstart=cy*(size-1)
        
        #left V=0 boundary
        n1=0; n2=rowstart+1; #start at node 0 (internal nodes)
        if random()<ratioC:
            LCi[k]=n1; LCj[k]=n2; LCv[k]-=1; k+=1
            LCi[k]=n2; LCj[k]=n1; LCv[k]-=1; k+=1
            Ccount[n1]+=1; Ccount[n2]+=1
        else:
            LRi[k]=n1; LRj[k]=n2; LRv[k]-=1; k+=1
            LRi[k]=n2; LRj[k]=n1; LRv[k]-=1; k+=1
            Rcount[n1]+=1; Rcount[n2]+=1
        #end of left boundary

        #internal edges
        for cx in range(1,size-1):
            n1=rowstart+cx; n2=rowstart+cx+1;
            if random() < ratioC:
                LCi[k]=n1; LCj[k]=n2; LCv[k]-=1; k+=1
                LCi[k]=n2; LCj[k]=n1; LCv[k]-=1; k+=1
                Ccount[n1]+=1; Ccount[n2]+=1
            else:
                LRi[k]=n1; LRj[k]=n2; LRv[k]-=1; k+=1
                LRi[k]=n2; LRj[k]=n1; LRv[k]-=1; k+=1
                Rcount[n1]+=1; Rcount[n2]+=1
        #end of internal edges
        
        #V=V0 RHS boundary 
        n1=(cy+1)*(size-1); n2=nnodes-1;
        if random()<ratioC:
            LCi[k]=n1; LCj[k]=n2; LCv[k]-=1; k+=1
            LCi[k]=n2; LCj[k]=n1; LCv[k]-=1; k+=1
            Ccount[n1]+=1; Ccount[n2]+=1
        else:
            LRi[k]=n1; LRj[k]=n2; LRv[k]-=1; k+=1
            LRi[k]=n2; LRj[k]=n1; LRv[k]-=1; k+=1
            Rcount[n1]+=1; Rcount[n2]+=1
        #end of RHS boundary
    #end of X components
    
    #vertical Y components
    for cy in range(0,size):
        rowstart=cy*(size-1);
        
        for cx in range(1,size):
            n1=rowstart+cx; n2=rowstart+cx + (size-1); 
            if random < ratioC:
                LCi[k]=n1; LCj[k]=n2; LCv[k]-=1; k+=1
                LCi[k]=n2; LCj[k]=n1; LCv[k]-=1; k+=1
                Ccount[n1]+=1; Ccount[n2]+=1
            else:
                LRi[k]=n1; LRj[k]=n2; LRv[k]-=1; k+=1
                LRi[k]=n2; LRj[k]=n1; LRv[k]-=1; k+=1
                Rcount[n1]+=1; Rcount[n2]+=1
    #end of Y components
    
    #diagonals
    for nn in range(0, nnodes):
        if Ccount[nn]>0: LCi[k]=nn; LCj[k]=nn; LCv[k]=Ccount[nn];
        if Rcount[nn]>0: LRi[k]=nn; LRj[k]=nn; LRv[k]=Rcount[nn]; 
        k+=1                
		
    LC = sparse.coo_matrix((LCv,(LCi,LCj))).tocsr() #not including boundary data
    LR = sparse.coo_matrix((LRv,(LRi,LRj))).tocsr() #except in diagonals

    return LC, LR







if __name__ == '__main__':
    indices=range(njobs) #a list of index numbers from 0 to njobs-1
    p = futures.map(mainFunc, indices)
    
    with open("alltimes.txt", "a") as of:
        for line in p:
            of.write(" ".join(map(str, line)) + "\n")

    











