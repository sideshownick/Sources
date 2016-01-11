//generate random 3D R-C array for SPICE
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

double gaus();

int
main()
{
   double rnd_x, rnd_y, gauss, ratioC, Csig, Rsig, Cn, Rn, C0, R0;
   double e = 2.7182818, rmax=2147483647;
   int i, cz, cy, cx, size, sizez, seed;
   FILE *f0, *f1, *f2, *f3;

   if( f0=fopen("parameters.ini","r") )
   	fscanf(f0,"%d %d %lf %lf %lf %lf %lf",&size,&sizez,&ratioC,&C0,&Csig,&R0,&Rsig);
   else
   {
	f0=fopen("parameters.ini","w");

	fprintf(f0,"20 10 0.4 1 0.333 1 0.333\nN_vert_comps N_Z_comps ratio_C C0 sigma_C(fraction of C0) R0 sigma_R(fraction of R0)");

	printf("Edit Values in \"parameters.ini\" then rerun");

	return 0;
   }
//   size = 50;
//   ratioC=0.4;
//   Csig=0.333;
//   Rsig=0.333;

//   fscanf(f0,"%d %lf %lf %lf %lf %lf",&size,&ratioC,&C0,&Csig,&R0,&Rsig);


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

//do size of these
for(cz=0;cz<sizez;cz++)
{

//horizontal "X" components (not edges)
   for(cy=0;cy<size+1;cy++)
   	for(cx=1;cx<size-1;cx++)
	{
		if((rand()/rmax)<ratioC)
		{
			Cn=C0*(1+gaus()*3*Csig);
			fprintf(f0,"Cx%dy%dz%dX x%dy%dz%d x%dy%dz%d %en\n",cx,cy,cz,cx,cy,cz,cx+1,cy,cz,Cn);
			fprintf(f0,"Rx%dy%dz%dX x%dy%dz%d x%dy%dz%d 1G\n",cx,cy,cz,cx,cy,cz,cx+1,cy,cz);
		//	fprintf(f1,"%d %d - - %e\n%d %d - - %e\n\n",cx,cy,Cn,cx+1,cy,Cn);
			fprintf(f2,"%d %d %d %e\n%d %d %d %e\n\n",cx,cy,cz,Cn,cx+1,cy,cz,Cn);
		}
		else
		{	Rn=R0*(1+gaus()*3*Rsig);	
			fprintf(f0,"Rx%dy%dz%dX x%dy%dz%d x%dy%dz%d %ek\n",cx,cy,cz,cx,cy,cz,cx+1,cy,cz,Rn);
		//	fprintf(f1,"- - %d %d %e\n- - %d %d %e\n\n",cx,cy,-1.0,cx+1,cy,-1.0);
			fprintf(f3,"%d %d %d %e\n%d %d %d %e\n\n",cx,cy,cz,Rn,cx+1,cy,cz,Rn);
		}
	//	fprintf(f1,"\n");
		fprintf(f2,"\n");
		fprintf(f3,"\n");
	}
//	fprintf(f1,"\n");
	fprintf(f2,"\n");
	fprintf(f3,"\n");

//vertical "Y" components
   for(cy=0;cy<size;cy++)
   	for(cx=1;cx<size;cx++)
	{
		if((rand()/rmax)<ratioC)
		{
			Cn=C0*(1+gaus()*3*Csig);
			fprintf(f0,"Cx%dy%dz%dY x%dy%dz%d x%dy%dz%d %en\n",cx,cy,cz,cx,cy,cz,cx,cy+1,cz,Cn);
			fprintf(f0,"Rx%dy%dz%dY x%dy%dz%d x%dy%dz%d 1G\n",cx,cy,cz,cx,cy,cz,cx,cy+1,cz);
	//		fprintf(f1,"%d %d - - %e\n%d %d - - %e\n\n",cx,cy,Cn,cx,cy+1,Cn);
			fprintf(f2,"%d %d %d %e\n%d %d %d %e\n\n",cx,cy,cz,Cn,cx,cy+1,cz,Cn);
		}
		else
		{	
			Rn=R0*(1+gaus()*3*Rsig);
			fprintf(f0,"Rx%dy%dz%dY x%dy%dz%d x%dy%dz%d %ek\n",cx,cy,cz,cx,cy,cz,cx,cy+1,cz,Rn);
	//		fprintf(f1,"- - %d %d %e\n- - %d %d %e\n\n",cx,cy,-1.0,cx,cy+1,-1.0);
			fprintf(f3,"%d %d %d %e\n%d %d %d %e\n\n",cx,cy,cz,Rn,cx,cy+1,cz,Rn);
		}
//		fprintf(f1,"\n");
		fprintf(f2,"\n");
		fprintf(f3,"\n");
	}
//	fprintf(f1,"\n");
	fprintf(f2,"\n");
	fprintf(f3,"\n");

//edge components 
   for(cy=0;cy<size+1;cy++)
   {
	if((rand()/rmax)<ratioC)
	{
		Cn=C0*(1+gaus()*3*Csig);
		fprintf(f0,"Cx0y%dz%dX 0 x1y%dz%d %en\n",cy,cz,cy,cz,Cn);
		fprintf(f0,"Rx0y%dz%dX 0 x1y%dz%d 1G\n",cy,cz,cy,cz);
//		fprintf(f1,"0 %d - - %e\n1 %d - - %e\n\n",cy,Cn,cy,Cn);
		fprintf(f2,"0 %d %d %e\n1 %d %d %e\n\n",cy,cz,Cn,cy,cz,Cn);
	}
	else
	{	
		Rn=R0*(1+gaus()*3*Rsig);
		fprintf(f0,"Rx0y%dz%dX 0 x1y%dz%d %ek\n",cy,cz,cy,cz,Rn);
//		fprintf(f1,"- - 0 %d %e\n- - 1 %d %e\n\n",cy,-1.0,cy,-1.0);
		fprintf(f3,"0 %d %d %e\n1 %d %d %e\n\n",cy,cz,Rn,cy,cz,Rn);
	}
//	fprintf(f1,"\n");
	fprintf(f2,"\n");
	fprintf(f3,"\n");

	if((rand()/rmax)<ratioC)
	{	
		Cn=C0*(1+gaus()*3*Csig);
		fprintf(f0,"Cx%dy%dz%dX x%dy%dz%d VOUT %en\n",size-1,cy,cz,size-1,cy,cz,Cn);
		fprintf(f0,"Rx%dy%dz%dX x%dy%dz%d VOUT 1G\n",size-1,cy,cz,size-1,cy,cz);
//		fprintf(f1,"%d %d - - %e\n%d %d - - %e\n\n",size-1,cy,Cn,size,cy,Cn);
		fprintf(f2,"%d %d %d %e\n%d %d %d %e\n\n",size-1,cy,cz,Cn,size,cy,cz,Cn);
	}
	else
	{
		Rn=R0*(1+gaus()*3*Rsig);
		fprintf(f0,"Rx%dy%dz%dX x%dy%dz%d VOUT %ek\n",size-1,cy,cz,size-1,cy,cz,Rn);
//		fprintf(f1,"- - %d %d %e\n- - %d %d %e\n\n",size-1,cy,-1.0,size,cy,-1.0);
		fprintf(f3,"%d %d %d %e\n%d %d %d %e\n\n",size-1,cy,cz,Rn,size,cy,cz,Rn);
	}

	

//	fprintf(f1,"\n");
	fprintf(f2,"\n");
	fprintf(f3,"\n");

   }

}

//Z components
for(cz=0;cz<sizez-1;cz++)
   for(cy=0;cy<size+1;cy++)
   	for(cx=1;cx<size;cx++)
	{
		if((rand()/rmax)<ratioC)
		{
			Cn=C0*(1+gaus()*3*Csig);
			fprintf(f0,"Cx%dy%dz%dZ x%dy%dz%d x%dy%dz%d %en\n",cx,cy,cz,cx,cy,cz,cx,cy,cz+1,Cn);
			fprintf(f0,"Rx%dy%dz%dZ x%dy%dz%d x%dy%dz%d 1G\n",cx,cy,cz,cx,cy,cz,cx,cy,cz+1);
	//		fprintf(f1,"%d %d - - %e\n%d %d - - %e\n\n",cx,cy,Cn,cx,cy+1,Cn);
			fprintf(f2,"%d %d %d %e\n%d %d %d %e\n\n",cx,cy,cz,Cn,cx,cy,cz+1,Cn);
		}
		else
		{	
			Rn=R0*(1+gaus()*3*Rsig);
			fprintf(f0,"Rx%dy%dz%dZ x%dy%dz%d x%dy%dz%d %ek\n",cx,cy,cz,cx,cy,cz,cx,cy,cz+1,Rn);
	//		fprintf(f1,"- - %d %d %e\n- - %d %d %e\n\n",cx,cy,-1.0,cx,cy+1,-1.0);
			fprintf(f3,"%d %d %d %e\n%d %d %d %e\n\n",cx,cy,cz,Rn,cx,cy,cz+1,Rn);
		}
//		fprintf(f1,"\n");
		fprintf(f2,"\n");
		fprintf(f3,"\n");
	}
//	fprintf(f1,"\n");
	fprintf(f2,"\n");
	fprintf(f3,"\n");

//   for(i=0;i<1000;i++)
// 		printf("%e\n",gaus());

//footers
     fprintf(f0,"V1 R1_N 0 AC 50\nR1 VOUT R1_N 100Meg\n");
//   fprintf(f0,".AC DEC 10 1 1G\n.print AC VR(0,VOUT) VI(0,VOUT)\n.END\n");

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
