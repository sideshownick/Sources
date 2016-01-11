//generate random 2D R-C array for SPICE
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

double gaus();

int
main()
{
   double rnd_x, rnd_y, gauss, ratioC, Csig, Rsig, Cn, Rn, C0, R0;
   double e = 2.7182818, rmax=2147483647;
   int i, cy, cx, size, seed;
   FILE *f0, *f1, *f2, *f3;

   if( f0=fopen("parameters.ini","r") )
   	fscanf(f0,"%d %lf %lf %lf %lf %lf",&size,&ratioC,&C0,&Csig,&R0,&Rsig);
   else
   {
	f0=fopen("parameters.ini","w");

	fprintf(f0,"50 0.4 1 0.0 1 0.0\nN_vert_comps ratio_C C0 sigma_C(fraction of C0) R0 sigma_R(fraction of R0)");

	printf("Edit Values in \"parameters.ini\" then rerun");

	return 0;
   }
//   size = 50;
//   ratioC=0.4;
//   Csig=0.0;
//   Rsig=0.0;

   fscanf(f0,"%d %lf %lf %lf %lf %lf",&size,&ratioC,&C0,&Csig,&R0,&Rsig);


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
   

//This gives normally distributed capacitances:
//1+gaus()*3*Csig

//return 0;

//ngspice input file containing circuit data
   f0 = fopen("circuit.cir", "w");

//combined list of components (may remove this)
//   f1 = fopen("comps.txt", "w");

//capactors only
   f2 = fopen("capacitors.txt", "w");

//resistors only
   f3 = fopen("resistors.txt", "w");
   

//headers
   fprintf(f0,"Random RC Network\n");

//horizontal "X" components (not edges)
   for(cy=0;cy<size;cy++)
   	for(cx=1;cx<size-1;cx++)
	{
		if((cy+cx)%2==0)
		{
			Cn=C0*(1+gaus()*3*Csig);
			fprintf(f0,"Cx%dy%dX x%dy%d x%dy%d %en\n",cx,cy,cx,cy,cx+1,cy,Cn);
			fprintf(f0,"Rx%dy%dX x%dy%d x%dy%d 1G\n",cx,cy,cx,cy,cx+1,cy);
		//	fprintf(f1,"%d %d - - %e\n%d %d - - %e\n\n",cx,cy,Cn,cx+1,cy,Cn);
			fprintf(f2,"%d %d %e\n%d %d %e\n\n",cx,cy,Cn,cx+1,cy,Cn);
		}
		else
		{	Rn=R0*(1+gaus()*3*Rsig);	
			fprintf(f0,"Rx%dy%dX x%dy%d x%dy%d %ek\n",cx,cy,cx,cy,cx+1,cy,Rn);
		//	fprintf(f1,"- - %d %d %e\n- - %d %d %e\n\n",cx,cy,-1.0,cx+1,cy,-1.0);
			fprintf(f3,"%d %d %e\n%d %d %e\n\n",cx,cy,Rn,cx+1,cy,Rn);
		}
	//	fprintf(f1,"\n");
		fprintf(f2,"\n");
		fprintf(f3,"\n");
	}
//	fprintf(f1,"\n");
	fprintf(f2,"\n");
	fprintf(f3,"\n");

//vertical "Y" components
   for(cy=0;cy<size-1;cy++)
   	for(cx=1;cx<size;cx++)
	{
		if((cy+cx)%2==1)
		{
			Cn=C0*(1+gaus()*3*Csig);
			fprintf(f0,"Cx%dy%dY x%dy%d x%dy%d %en\n",cx,cy,cx,cy,cx,cy+1,Cn);
			fprintf(f0,"Rx%dy%dY x%dy%d x%dy%d 1G\n",cx,cy,cx,cy,cx,cy+1);
	//		fprintf(f1,"%d %d - - %e\n%d %d - - %e\n\n",cx,cy,Cn,cx,cy+1,Cn);
			fprintf(f2,"%d %d %e\n%d %d %e\n\n",cx,cy,Cn,cx,cy+1,Cn);
		}
		else
		{	
			Rn=R0*(1+gaus()*3*Rsig);
			fprintf(f0,"Rx%dy%dY x%dy%d x%dy%d %ek\n",cx,cy,cx,cy,cx,cy+1,Rn);
	//		fprintf(f1,"- - %d %d %e\n- - %d %d %e\n\n",cx,cy,-1.0,cx,cy+1,-1.0);
			fprintf(f3,"%d %d %e\n%d %d %e\n\n",cx,cy,Rn,cx,cy+1,Rn);
		}
//		fprintf(f1,"\n");
		fprintf(f2,"\n");
		fprintf(f3,"\n");
	}
//	fprintf(f1,"\n");
	fprintf(f2,"\n");
	fprintf(f3,"\n");

//edge components 
   for(cy=0;cy<size;cy++)
   {
	if((cy)%2==0)
	{
		Cn=C0*(1+gaus()*3*Csig);
		fprintf(f0,"Cx0y%dX 0 x1y%d %en\n",cy,cy,Cn);
		fprintf(f0,"Rx0y%dX 0 x1y%d 1G\n",cy,cy);
//		fprintf(f1,"0 %d - - %e\n1 %d - - %e\n\n",cy,Cn,cy,Cn);
		fprintf(f2,"0 %d %e\n1 %d %e\n\n",cy,Cn,cy,Cn);
	}
	else
	{	
		Rn=R0*(1+gaus()*3*Rsig);
		fprintf(f0,"Rx0y%dX 0 x1y%d %ek\n",cy,cy,Rn);
//		fprintf(f1,"- - 0 %d %e\n- - 1 %d %e\n\n",cy,-1.0,cy,-1.0);
		fprintf(f3,"0 %d %e\n1 %d %e\n\n",cy,Rn,cy,Rn);
	}
//	fprintf(f1,"\n");
	fprintf(f2,"\n");
	fprintf(f3,"\n");

	if((cy+size)%2==1)
	{	
		Cn=C0*(1+gaus()*3*Csig);
		fprintf(f0,"Cx%dy%dX x%dy%d VOUT %en\n",size-1,cy,size-1,cy,Cn);
		fprintf(f0,"Rx%dy%dX x%dy%d VOUT 1G\n",size-1,cy,size-1,cy);
//		fprintf(f1,"%d %d - - %e\n%d %d - - %e\n\n",size-1,cy,Cn,size,cy,Cn);
		fprintf(f2,"%d %d %e\n%d %d %e\n\n",size-1,cy,Cn,size,cy,Cn);
	}
	else
	{
		Rn=R0*(1+gaus()*3*Rsig);
		fprintf(f0,"Rx%dy%dX x%dy%d VOUT %ek\n",size-1,cy,size-1,cy,Rn);
//		fprintf(f1,"- - %d %d %e\n- - %d %d %e\n\n",size-1,cy,-1.0,size,cy,-1.0);
		fprintf(f3,"%d %d %e\n%d %d %e\n\n",size-1,cy,Rn,size,cy,Rn);
	}

//	fprintf(f1,"\n");
	fprintf(f2,"\n");
	fprintf(f3,"\n");

   }

//   for(i=0;i<1000;i++)
// 		printf("%e\n",gaus());

//footers
   fprintf(f0,"V1 R1_N 0 AC 50\nR1 VOUT R1_N 100Meg\n");   
//   fprintf(f0,".AC DEC 10 1 1G\n.print AC V(VOUT)\n.END\n");

   fclose(f0);
//   fclose(f1);
   fclose(f2);
   fclose(f3);
   
   return 0;
}

//returns normally distributed values with SD=1/3 between the range -1:1
double
gaus()
{	
	double rnd_x, rnd_y, gauss;
	double e = 2.7182818, rmax=2147483647;
   	int i;

	for (;;)
	{
		rnd_x = (rand ()/rmax*2-1);
 		rnd_y = (rand ()/rmax);
 
 		gauss = pow(e,-0.5*9*rnd_x*rnd_x);
 
 		if (rnd_y < gauss)
 			return rnd_x;
	}
} 
