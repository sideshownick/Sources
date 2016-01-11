import os, sys
import numpy as np
#import time
sys.path.append("/home/nm268/auto/07p/python")
from auto import *

N=50
M=10
thresh=-1 ##threshold for identifying differentiated nodes
solutionbank=[]
fouts=open('allbifs_stab.txt','a')
foutu=open('allbifs_unst.txt','a')
fouta=open('allbifs_all.txt','a')
print >>fouts, '#sigma, L2, NDNl, NDNr, lDNs, rDNs, sigma0, ic'
print >>foutu, '#sigma, L2, NDNl, NDNr, lDNs, rDNs, sigma0, ic'
filetag='bifdiag_BA_'+str(N)+'_'+str(M)
for sigma in [16]:#range(14,45):
    for rn in [0]:#range(0,10):
      try:
        #print 'par='+str(sigma)+', run '+str(rn)
        solutions={} ##dictionary for solutions
        fseq=open('sequence.txt','w')
        bifurcations={} ##dictionary for bifurcations
        ##get all solutions for this IC in this continuation direction
        getvals=False
        escape=False
        label=[]
        tag="s%.2f-r%.3d"%(sigma,rn)
        tag=tag.replace(".", "_")
        print "Results/b."+tag; 
        os.chdir("Results")
        bd=loadbd(tag+".txt")
        os.chdir("..")
        fsol=open('Solutions/solutions_s'+str(sigma)+'_run%.3d.txt'%rn,'w')
        solutionbank=[] ##only seach over current set to exclude limit cycling
        for limp in bd(): ##search all solutions to find new ones
            label=limp['Label']
            sol=bd(label).toarray()
            solutions[label]= sol
            #t1=time.time()
            for oldsol in solutionbank: ##escape if repetition found
                if sum((np.array(sol)-np.array(oldsol))**2) < 1e-6:
                    escape=True
                    print 'repetition'
            #print time.time()-t1
            solutionbank.append(sol)
            for thingy in sol:
                print >>fsol, float(thingy),
            print >>fsol, ''
            fsol.flush()
            if escape==True:
                fsol.close()
                break
        fsol.close()
	       				
        ##extract solutions from bifurcation file
        alldata=[]
        for line in file('Results/b.'+tag+".txt"):
            data=line.split()
            if data[0] != '0':
                alldata.append(data)
            
        ##for each of the found solution
        for lab in list(solutions): ##iterate over solution ID
            difnod='' ##initialise differentiated node ID string
            ##iterate over N nodes
            for n in range(0,N):
                if solutions[lab][n]< thresh:
                    difnod+='%.2d'%(n+1) ##append node label to ID string
            ##replace solution with differentiated node data and ID
            if len(difnod)/2 > 0: solutions[lab]=difnod
            else: solutions[lab]='0'
		
        lab=int(alldata[0][3])
        row2=0
        leftlab=lab
        rightlab=lab
        lab2=lab
        for row in range(1,len(alldata)):
            dat0=alldata[row-1]
            data=alldata[row]
            sig0=float(dat0[4])
            sig1=float(data[4])
			
            if int(data[3])**2 > 1: ##ignore starting point
                row1=row2
                row2=row
                lab1=lab2
                lab2=int(data[3])
                ##check if left or right solution
                if sig1 > sig0: 
                    rightlab = int(data[3]) ##get label for solution
                if sig1 < sig0:
                    leftlab = int(data[3]) ##get label for solution
                if leftlab in solutions and rightlab in solutions:
                    ##print to alldata file
                    for line in alldata[row1:row2]:
                        print >>fouta, line[4], line[5],\
                                       len(solutions[leftlab])/2, len(solutions[rightlab])/2,\
                                       solutions[leftlab], solutions[rightlab], sigma
                    print >>fouta, '\n' 
                    ##if stable print to stable solution file
                    if int(alldata[(row1+row2)/2][1]) < 1:
                        print >>fseq, -1,lab1,solutions[lab1],lab2,solutions[lab2]
                        for line in alldata[row1:row2]:
                            ##sigma, L2, lNDN, rNDN, lNDN-ID, rNDN-ID, stab, sigma0, ic	
                            print >>fouts, line[4], line[5],\
                                           len(solutions[leftlab])/2, len(solutions[rightlab])/2,\
                                           solutions[leftlab], solutions[rightlab], sigma
                        print >>fouts, '\n' 
                    else:#print to unstable solution file
                        print >>fseq, 1,lab1,solutions[lab1],lab2,solutions[lab2]
                    for line in alldata[row1:row2]:
                        print >>foutu, line[4], line[5],\
                                       len(solutions[leftlab])/2, len(solutions[rightlab])/2,\
                                       solutions[leftlab], solutions[rightlab], sigma
                        print >>foutu, '\n'
        fseq.close()	
      except: pass
fouts.close()
foutu.close()
fouta.close()




###
