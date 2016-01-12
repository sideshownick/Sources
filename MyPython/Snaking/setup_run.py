import subprocess, sys, os, shutil, time
sys.path.append("Scripts")
sys.path.append("autopython")
import numpy as np
from make_function_runfile import gen_IC
from scoop import futures
from auto import *

'''sigvals=range(24,34) #(14,45)
runvals=range(100)

parvals=[]
for sig in sigvals:
    for rn in runvals:
        parvals.append((sig,rn))
'''

N=50
M=5
lapfilename="lap_BA_"+str(N)+"_"+str(M)+".txt"

parvals=np.arange(15.55,15.99,0.01) 

def runAuto(paramIndex):
    t1=time.time()
    sigma,rn=parvals[paramIndex],11
    tag='s%.2f-r%.3d'%(sigma,rn)
    tag=tag.replace(".", "_")
    tempdir="TEMP"+tag
    os.mkdir(tempdir)
    shutil.copy("c.workfile", tempdir+"/c.workfile")
    gen_IC(sigma,rn,lapfile=lapfilename, N=N, M=M, outfile=tempdir+"/workfile", tries=20)	
    runfilename=tag+'.auto.py'
    os.chdir(tempdir)
    parameters = [35.0, 16.0, 9.0, 0.4, 0.12, sigma]
    job=ld('workfile')
    r1=run(job,DS=1e-03,STOP=['LP50','BP1'])#, DSMAX=1e-2)
    r1=dsp(r1,1)##remove startpoint solution
    r1=dlb(r1,1)##and corresponding label
    r2=run(job,DS=-1e-03,STOP=['LP2','BP1'])#, DSMAX=1e-2)
    r2=dsp(r2,1)##remove startpoint solution
    r2=dlb(r2,1)##and corresponding label
    bd=merge(r1+r2)
    bd=rl(bd)
    sv(bd,tag)

    #p=plot(bd, hide=True, stability=True, use_symbols = False, xlabel='$\sigma$')
    #p.savefig("BifFigs/bifdiag"+tag+".png")

    shutil.copy("b."+tag, "../Results/b."+tag)
    shutil.copy("s."+tag, "../Results/s."+tag)
    os.chdir("../")
    shutil.rmtree(tempdir)
    return tag, t1, time.time()
	


if __name__ == '__main__':
    p = futures.map(runAuto, range(len(parvals)))
    of=open("output.txt", "w")
    of.write("\n".join(map(str, p)))
    of.close()



