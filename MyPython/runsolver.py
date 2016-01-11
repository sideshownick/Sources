#!python
from numpy import *
from scipy import *
from scipy.linalg import *
from scipy import sparse, concatenate
from scipy.sparse.linalg import *
import os, subprocess, time, sys
from numpy import loadtxt, savetxt


ratio=50
ratioC=ratio/100.0

C=1e-9
R=1.0e3
R1=1/R

#sizes=[4, 8, 16, 32, 64, 128]
sizes=[128]#256, 512]
nruns=1


with open("solvetimes.txt", "w") as ttf:
 with open("out_all.txt", "w") as fout:
  for size in sizes: 
    ft=open("timer_"+str(size)+".txt", "w")
    ft.write("size run gentime s1time runtime nsteps\n")
    
    with open("parameters.ini", "w") as initfile:
        initfile.write(str(size)+" "+str(ratioC)+" 1 "+" 1 ")
           
    t0=time.time()
    for run in range(nruns):
        t1=time.time()

        #full and sparse Laplacian matrices for capacitors and resistors 
        subprocess.call("./genmat")
        
        #coo_matrix((data, (i, j)), [shape=(M, N)])
        i, j, data = loadtxt("matrixR.mat").transpose()
        Rfull=sparse.coo_matrix((data, (i,j))).tocsr()
        LRsp = Rfull[1:-1, 1:-1]
        R_left= Rfull[1:-1, 0] #.toarray()
        R_right= Rfull[1:-1, -1] #.toarray()
        
        i, j, data = loadtxt("matrixC.mat").transpose()
        Cfull=sparse.coo_matrix((data, (i,j))).tocsr()
        LCsp = Cfull[1:-1, 1:-1]
        C_left= Cfull[1:-1, 0].toarray()
        C_right= Cfull[1:-1, -1].toarray()
       
        t2=time.time()
        
        #print >>ft, "s", size, "run ", run, "generated in ", time.time()-tick, "s"
        gentime=t2-t1

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

        ft.write(" ".join(map(str, [size, run, gentime, s1time, runtime, len(logfreqs)])) + "\n")
    
    fout.close()
    ft.close()
    
    ttime=t6-t0
    print(size, ttime)
    ttf.write(" ".join(map(str, [size, nruns, len(logfreqs)+1, ttime])))
ttf.close()







