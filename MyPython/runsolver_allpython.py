#!python
from numpy import *
#from Numeric import *
from scipy import *
from scipy.linalg import *
from scipy import sparse, concatenate
from scipy.sparse.linalg import *
import os
import time
from numpy import savetxt
from random import *
import sys
sys.path.append('Python')
import gen2 as gen


ratio=40
ratioC=ratio/100.0

C=1e-9
R=1.0e3
R1=1/R

#sizes=[4, 8, 16, 32, 64, 128]
sizes=[256]
nruns=100

#for ratio in [30,35,45]:
# ratioC=ratio/100.0
with open("solvetimes.txt", "a") as ttf:
 with open("out_all.txt", "w") as fout:
  for size in sizes: 
    ft=open("timer_"+str(size)+".txt", "w")
    ft.write("size run gentime s1time runtime nsteps\n")
   
    t0=time.time()
    for run in range(nruns):
        t1=time.time()

        #full and sparse Laplacian matrices for capacitors and resistors 
        LC, LR, LCsp, LRsp = gen.generate(size,ratioC)
        t2=time.time()
        #print >>ft, "s", size, "run ", run, "generated in ", time.time()-tick, "s"
        gentime=t2-t1

        R_left=array(-LR[:-2,-1]) #right boundary resistors YR11
        R_right=array(-LR[:-2,-2]) #left boundary resistors YL11
        C_left=array(-LC[:-2,-1]) #right boundary capacitors YRC1
        C_right=array(-LC[:-2,-2]) #left boundary capacitors YLC1

        def solve3(h):
            M = R1*LRsp + C*1j*h*LCsp #full RC network matrix
            BV_l = R1*R_left + C*1j*h*C_left #left boundary vector
            L_inv = linsolve.spsolve(M, BV_l)
            #L_inv = cg(M, BV_l)[0]

            BV_r = (R1*R_right+C*1j*h*C_right).transpose() #right boundary vector
            Y = dot(BV_r, L_inv) #complex admittance
            return Y
       
        t3=time.time()
        Y0=solve3(1e-20)
        t4=time.time()
        s1time=t4-t3
        e0=abs(Y0.real)

        logfreqs=arange(1,11,1)
        
        runvals=[[]]*len(logfreqs)
        t5=time.time()
        for i,h1 in enumerate(logfreqs): #(-3,3,0.01):
            h=10**h1
            Y=solve3(h)
            
            realpart=Y.real[0]
            imagpart=Y.imag[0]

            runvals[i] = [h1, realpart, imagpart]
        t6=time.time()
        runtime=t6-t5
        
        for vals in runvals:
            for val in vals:
                fout.write(str(val) + " ")
            fout.write("\n")
        fout.write("\n\n")

        ft.write(" ".join(map(str, [size, run, gentime, s1time, runtime, len(logfreqs)])) + "\n")
    
    fout.close()
    ft.close()
    
    ttime=t6-t0
    print(size, ttime)
    ttf.write(" ".join(map(str, [size, nruns, len(logfreqs)+1, ttime])))
ttf.close()







