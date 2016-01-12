#!python
from scipy import zeros, mat
from scipy import sparse
from random import random 



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
		
    LC = sparse.coo_matrix((LCv,(LCi,LCj)),shape=(N,N)).tocsr() #not including boundary data
    LR = sparse.coo_matrix((LRv,(LRi,LRj)),shape=(N,N)).tocsr() #except in diagonals

    return LC, LR




if __name__ == '__main__':
    LC, LR = generate(3, 0.4)
    print LC, "\n"
    print LR












