//generate random square 2D R & C array matrices for solving
//2016-01a_NJM
#include <stdio.h>
#include <stdlib.h>
#include <math.h>


int
main()
{
   double ratioC;
   double e = 2.7182818, rmax=2147483647;
   int i, j, cy, cx, size, seed, null, Nsize, nn, n1, n2, nnodes, rowstart;
   int *ncountC, *ncountR;
   FILE *f0, *f1, *fMC, *fMR;

   if( f0=fopen("parameters.ini","r") )
   	fscanf(f0,"%d %lf",&size,&ratioC);
   else
   {
	f0=fopen("parameters.ini","w");

	fprintf(f0,"50 0.4\nN_vert_comps ratio_C");

	printf("Edit Values in \"parameters.ini\" then rerun");

	return 0;
   }

   Nsize=(size+1)*(size+1)+(size-1)*(size-1); //=2*size**2
   
   nnodes=(size+1)*(size-1)+2; //includes boundary nodes
   
   ncountC = calloc(nnodes, sizeof(int));
   ncountR = calloc(nnodes, sizeof(int));
   
   for(nn=0;nn<nnodes;nn++)
   {
	ncountC[nn]=0;
	ncountR[nn]=0;
   }


   fclose(f0);

   rmax=RAND_MAX;
   
   if(f1=fopen("seed","r"))
   {	
   	fscanf(f1,"%d",&seed);
	srand(seed);
	fclose(f1);
   }
   else
      	srand ( time(NULL) );

   f1=fopen("seed","w");
   fprintf(f1,"%d",rand());
   fclose(f1);

//matrix file
   fMC = fopen("matrixC.mat" , "w");
   fMR = fopen("matrixR.mat" , "w");

//horizontal "X" components 
    for(cy=0;cy<size+1;cy++)
    {
        rowstart=cy*(size-1); //starts at 0

        //left V=0 boundary
	    n1=0; n2=rowstart+1; //start at node 1 (internal nodes)
	    if((rand()/rmax)<ratioC)
	    {	
		    fprintf(fMC,"%d %d -1\n", n2, n1);
		    fprintf(fMC,"%d %d -1\n", n1, n2);
	        ncountC[n2]+=1;
	        ncountC[n1]+=1;
	    }
	    else
	    {
		    fprintf(fMR,"%d %d -1\n", n2, n1);
		    fprintf(fMR,"%d %d -1\n", n1, n2);
	        ncountR[n2]+=1;
	        ncountR[n1]+=1;
	    }
	    //end 0

       	for(cx=1;cx<size-1;cx++)
	    {
		    n1=rowstart+cx; n2=rowstart+cx+1;
	        if((rand()/rmax)<ratioC)
	        {	
		        fprintf(fMC,"%d %d -1\n", n2, n1);
		        fprintf(fMC,"%d %d -1\n", n1, n2);
	            ncountC[n2]+=1;
	            ncountC[n1]+=1;
	        }
	        else
	        {
		        fprintf(fMR,"%d %d -1\n", n2, n1);
		        fprintf(fMR,"%d %d -1\n", n1, n2);
	            ncountR[n2]+=1;
	            ncountR[n1]+=1;
	        }
	    //end for cx
	    }

        //V=VOUT boundary
        n1=(cy+1)*(size-1); n2=nnodes-1;
	    if((rand()/rmax)<ratioC)
	    {	
		    fprintf(fMC,"%d %d -1\n", n2, n1);
		    fprintf(fMC,"%d %d -1\n", n1, n2);
	        ncountC[n2]+=1;
	        ncountC[n1]+=1;
	    }
	    else
	    {
		    fprintf(fMR,"%d %d -1\n", n2, n1);
		    fprintf(fMR,"%d %d -1\n", n1, n2);
	        ncountR[n2]+=1;
	        ncountR[n1]+=1;
	    }
	    //end VOUT
	
    //end for cy
    }
	

    //vertical "Y" components
    for(cy=0;cy<size;cy++)
    {
        rowstart=cy*(size-1); //starts at 0
        
        for(cx=1;cx<size;cx++) //increment from 1
        {
            n1=rowstart+cx; n2=rowstart+cx + (size-1); //down to next row
            if((rand()/rmax)<ratioC)
	        {	
		        fprintf(fMC,"%d %d -1\n", n2, n1);
		        fprintf(fMC,"%d %d -1\n", n1, n2);
	            ncountC[n2]+=1;
	            ncountC[n1]+=1;
	        }
	        else
	        {
		        fprintf(fMR,"%d %d -1\n", n2, n1);
		        fprintf(fMR,"%d %d -1\n", n1, n2);
	            ncountR[n2]+=1;
	            ncountR[n1]+=1;
	        }
	    //end for cx	
	    }
	//end for cy
    }

   for(nn=0;nn<nnodes;nn++)
   {
	if(ncountC[nn]>0) fprintf(fMC, "%d %d %d\n", nn, nn, ncountC[nn]);
	if(ncountR[nn]>0) fprintf(fMR, "%d %d %d\n", nn, nn, ncountR[nn]);
   }
   
   fclose(fMC);
   fclose(fMR);
   
   return 0;
}


