//generate random square 2D R-C array for SPICE
//2016-01a_NJM
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

double gaus();

int
main()
{
   double rnd_x, rnd_y, ratioC, Csig, Rsig, Cn, Rn, C0, R0;
   double e = 2.7182818, rmax=2147483647;
   int i, j, cy, cx, size, Sx, Sy, seed, null, Nsize;
   int *fval;
   int fval1;
   FILE *f0, *f1, *f1a, *f1b, *f2, *f3, *fMC, *fMR;

   if( f0=fopen("parameters.ini","r") )
   	fscanf(f0,"%d %lf %lf %lf %lf %lf %d %d",&size,&ratioC,&C0,&Csig,&R0,&Rsig,&Sx,&Sy);
   else
   {
	f0=fopen("parameters.ini","w");

	fprintf(f0,"50 0.4 1 0.333 1 0.333 1 1\nN_vert_comps ratio_C C0 sigma_C(fraction of C0) R0 sigma_R(fraction of R0) x_squash y_squash");

	printf("Edit Values in \"parameters.ini\" then rerun");

	return 0;
   }

   Nsize=(size+1)*(size+1)+(size-1)*(size-1);

   //ps=3*sqrt(3)/(sqrt(size));

   fval = calloc(4*(size+10)*(size+10),sizeof(double));


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

//ngspice input file containing circuit data
   f0 = fopen("circuit.cir", "w");

//headers
   fprintf(f0,"Random RC Network\n");

//horizontal "X" components (not edges)
   for(cy=0;cy<size+1;cy++)
   	for(cx=1;cx<size-1;cx++)
	{
		if((rand()/rmax)<ratioC)
		{

			fprintf(f0,"Cx%dy%dX x%dy%d x%dy%d %en\n",cx,cy,cx,cy,cx+1,cy,C0);
			fprintf(f0,"Rx%dy%dX x%dy%d x%dy%d 1G\n",cx,cy,cx,cy,cx+1,cy);
		}
		else
		{		
			fprintf(f0,"Rx%dy%dX x%dy%d x%dy%d %ek\n",cx,cy,cx,cy,cx+1,cy,R0);
		}

	}

//vertical "Y" components
   for(cy=0;cy<size;cy++)
   	for(cx=1;cx<size;cx++)
	{
	 if((rand()/rmax)<ratioC)
		{
			fprintf(f0,"Cx%dy%dY x%dy%d x%dy%d %en\n",cx,cy,cx,cy,cx,cy+1,C0);
			fprintf(f0,"Rx%dy%dY x%dy%d x%dy%d 1G\n",cx,cy,cx,cy,cx,cy+1);
		}
		else
		{	
			fprintf(f0,"Rx%dy%dY x%dy%d x%dy%d %ek\n",cx,cy,cx,cy,cx,cy+1,R0);
		}
		
	}

//edge components 
   for(cy=0;cy<size+1;cy++)
   {
   //V=0 boundary
    if((rand()/rmax)<ratioC)
	{
		fprintf(f0,"Cx0y%dX 0 x1y%d %en\n",cy,cy,C0);
		fprintf(f0,"Rx0y%dX 0 x1y%d 1G\n",cy,cy);
	}
	else
	{	
		fprintf(f0,"Rx0y%dX 0 x1y%d %ek\n",cy,cy,R0);
	}
	//V=VOUT boundary
	if((rand()/rmax)<ratioC)
	{	
		fprintf(f0,"Cx%dy%dX x%dy%d VOUT %en\n",size-1,cy,size-1,cy,C0);
		fprintf(f0,"Rx%dy%dX x%dy%d VOUT 1G\n",size-1,cy,size-1,cy);
	}
	else
	{
		fprintf(f0,"Rx%dy%dX x%dy%d VOUT %ek\n",size-1,cy,size-1,cy,R0); 
	}
	//endfor
	}
   
//footers
     fprintf(f0,"V1 R1_N 0 AC 50\nR1 VOUT R1_N 100Meg\n");


   fclose(f0);
   free(fval);
   
   return 0;
}


