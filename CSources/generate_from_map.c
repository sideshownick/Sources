//generate random 2D R-C array for SPICE from a file n*m*(0 0 {1,0})
//also generate template for gnuplot script to show current paths
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

double gaus();

int
main()
{
   double rnd_x, rnd_y, gauss, ratioC, Csig, Rsig, Cn, Rn, C0, R0, ps;
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

   Nsize=size*size+(size-1)*(size-1);

   ps=3*sqrt(3)/(sqrt(size));

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
   f1a = fopen("circuitRR.cir", "w");

//matrix file
   fMC = fopen("matrixC.mat" , "w");
   fMR = fopen("matrixR.mat" , "w");

//image field file
   if ( f1 = fopen("spd.txt", "r") )
   {
	printf ("'spd.txt' found, using as component map\n");
	while(!feof(f1))
	{
		fscanf(f1,"%d %d %d", &j, &i, &null);
		//fval[i*(2*size+1)+j]=null;
		if(!(i%Sx) && !(j%Sy)){fval[i/Sx*(2*size+1)+j/Sy]=null;
		//printf("%d %d\n", i, j);
		}
	}
	fclose(f1);
   }
   else
   {
	printf("no map file 'spd.txt' found, \nusing pseudo-random number generator...\n");
	for (i=0;i<((2*size+1)*(2*size+1));i++)
	{
		if((rand()/rmax)<ratioC)
			fval[i]=1;
		else
			fval[i]=0;
	}
   }



   f1 = fopen("vectors0.gnuplot", "w");

   fprintf(f1,"#!gnuplot\nset out \"vecs.ps\"\nset grid\nscale2(x)=x*1e6*$1*1e-9*2*pi\nscale1(x)=x*1e6/1000\nscale2(x)=real(sqrt(x*1e6*$1*1e-9*2*pi))-imag(sqrt(x*1e6*$1*1e-9*2*pi)); scale1(x)=real(sqrt(x*1e6/1000))-imag(sqrt(x*1e6/1000))\nset term postscript color enhanced\nset xrange[-0.5:%d.5]\nset yrange[%d.5:-0.5]\nset xtics 1\nset ytics 1\np 'capacitors.txt' notitle w l lt 3 lw 2, 'resistors.txt' notitle w l lt 1 lw 2,\\\n",size,size-1);


//capacitors only
   f2 = fopen("capacitors.txt", "w");

//resistors only
   f3 = fopen("resistors.txt", "w");
   

//headers
   fprintf(f0,"Random RC Network\n");
   fprintf(f1a,"Random R1-R2 Network\n");

//horizontal "X" components (not edges)
   for(cy=0;cy<size;cy++)
   	for(cx=1;cx<size-1;cx++)
	{
		if(fval[2*cy*(2*size+1)+2*cx+1])
		{
			Cn=C0*(1+gaus()*3*Csig);
			fprintf(f0,"Cx%dy%dX x%dy%d x%dy%d %en\n",cx,cy,cx,cy,cx+1,cy,Cn);
			fprintf(f0,"Rx%dy%dX x%dy%d x%dy%d 1G\n",cx,cy,cx,cy,cx+1,cy);
			fprintf(f1a,"Rx%dy%dX x%dy%d x%dy%d %e\n",cx,cy,cx,cy,cx+1,cy,Cn);

			
			//fprintf(fMC,"%d %d -1\n",cx+cy*(size-1)+1,cx+cy*(size-1));
			fprintf(fMC,"%d %d 1\n",cx+cy*(size-1),cx+cy*(size-1)+1);
			//fprintf(fMC,"%d %d 1\n",cx+cy*(size-1),cx+cy*(size-1));
			//fprintf(fMC,"%d %d 1\n",cx+cy*(size-1)+1,cx+cy*(size-1)+1);


		////	fprintf(fMC,"%d %d 1\n",cx+cy*(size-1),cx+cy*(size-1)+1);
		////	fprintf(fMC,"%d %d 1\n",cx+cy*(size-1)+1,cx+cy*(size-1));
			
			fprintf(f1,"\'alldataV.txt\' u (%d.5-scale2($%d-$%d)/2):(%d-scale2($%d-$%d)/2):(scale2($%d-$%d)):(scale2($%d-$%d)) notitle w vec lw 2 lt -1,\\\n",cx,((size)*(cx)+(cy+1))*2+2,((size)*(cx-1)+(cy+1))*2+2,cy,((size)*(cx)+(cy+1))*2+3,((size)*(cx-1)+(cy+1))*2+3,((size)*(cx)+(cy+1))*2+2,((size)*(cx-1)+(cy+1))*2+2,((size)*(cx)+(cy+1))*2+3,((size)*(cx-1)+(cy+1))*2+3);

			fprintf(f2,"%d %d %e\n%d %d %e\n\n",cx,cy,Cn,cx+1,cy,Cn);
		}
		else
		{	Rn=R0*(1+gaus()*3*Rsig);	
			fprintf(f0,"Rx%dy%dX x%dy%d x%dy%d %ek\n",cx,cy,cx,cy,cx+1,cy,Rn);
			fprintf(f1a,"Rx%dy%dX x%dy%d x%dy%d %e\n",cx,cy,cx,cy,cx+1,cy,Rn);

			//fprintf(fMR,"%d %d -1\n",cx+cy*(size-1)+1,cx+cy*(size-1));
			fprintf(fMR,"%d %d 1\n",cx+cy*(size-1),cx+cy*(size-1)+1);
			//fprintf(fMR,"%d %d 1\n",cx+cy*(size-1),cx+cy*(size-1));
			//fprintf(fMR,"%d %d 1\n",cx+cy*(size-1)+1,cx+cy*(size-1)+1);

			
////			fprintf(fMR,"%d %d 1\n",cx+cy*(size-1),cx+cy*(size-1)+1);
////			fprintf(fMR,"%d %d 1\n",cx+cy*(size-1)+1,cx+cy*(size-1));
			
			fprintf(f1,"\'alldataV.txt\' u (%d.5-scale1($%d-$%d)/2):(%d-scale1($%d-$%d)/2):(scale1($%d-$%d)):(scale1($%d-$%d)) notitle w vec lw 2 lt -1,\\\n",cx,((size)*(cx)+(cy+1))*2+2,((size)*(cx-1)+(cy+1))*2+2,cy,((size)*(cx)+(cy+1))*2+3,((size)*(cx-1)+(cy+1))*2+3,((size)*(cx)+(cy+1))*2+2,((size)*(cx-1)+(cy+1))*2+2,((size)*(cx)+(cy+1))*2+3,((size)*(cx-1)+(cy+1))*2+3);

			fprintf(f3,"%d %d %e\n%d %d %e\n\n",cx,cy,Rn,cx+1,cy,Rn);
		}
		fprintf(f2,"\n");
		fprintf(f3,"\n");
	}
	fprintf(f2,"\n");
	fprintf(f3,"\n");

//vertical "Y" components
   for(cy=0;cy<size-1;cy++)
   	for(cx=1;cx<size;cx++)
	{

		if(fval[(2*cy+1)*(2*size+1)+2*cx])
		{
			Cn=C0*(1+gaus()*3*Csig);
			fprintf(f0,"Cx%dy%dY x%dy%d x%dy%d %en\n",cx,cy,cx,cy,cx,cy+1,Cn);
			fprintf(f0,"Rx%dy%dY x%dy%d x%dy%d 1G\n",cx,cy,cx,cy,cx,cy+1);

			fprintf(f1a,"Rx%dy%dY x%dy%d x%dy%d %e\n",cx,cy,cx,cy,cx,cy+1,Cn);


			//fprintf(fMC,"%d %d -1\n",cx+cy*(size-1)+size-1,cx+cy*(size-1));
			fprintf(fMC,"%d %d 1\n",cx+cy*(size-1),cx+cy*(size-1)+size-1);
			//fprintf(fMC,"%d %d 1\n",cx+cy*(size-1),cx+cy*(size-1));
			//fprintf(fMC,"%d %d 1\n",cx+cy*(size-1)+size-1,cx+cy*(size-1)+size-1);


	////		fprintf(fMC,"%d %d 1\n",cx+cy*(size-1),cx+cy*(size-1)+size-1);
	////		fprintf(fMC,"%d %d 1\n",cx+cy*(size-1)+size-1,cx+cy*(size-1));

			fprintf(f1,"\'alldataV.txt\' u (%d-scale2($%d-$%d)/2):(%d.5-scale2($%d-$%d)/2):(scale2($%d-$%d)):(scale2($%d-$%d)) notitle w vec lw 2 lt -1,\\\n",cx,((size)*(cx-1)+(cy+2))*2+2,((size)*(cx-1)+(cy+1))*2+2,cy,((size)*(cx-1)+(cy+2))*2+3,((size)*(cx-1)+(cy+1))*2+3,((size)*(cx-1)+(cy+2))*2+2,((size)*(cx-1)+(cy+1))*2+2,((size)*(cx-1)+(cy+2))*2+3,((size)*(cx-1)+(cy+1))*2+3);

			fprintf(f2,"%d %d %e\n%d %d %e\n\n",cx,cy,Cn,cx,cy+1,Cn);
		}
		else
		{	
			Rn=R0*(1+gaus()*3*Rsig);
			fprintf(f0,"Rx%dy%dY x%dy%d x%dy%d %ek\n",cx,cy,cx,cy,cx,cy+1,Rn);
			fprintf(f1a,"Rx%dy%dY x%dy%d x%dy%d %e\n",cx,cy,cx,cy,cx,cy+1,Rn);

			//fprintf(fMR,"%d %d -1\n",cx+cy*(size-1)+size-1,cx+cy*(size-1));
			fprintf(fMR,"%d %d 1\n",cx+cy*(size-1),cx+cy*(size-1)+size-1);
			//fprintf(fMR,"%d %d 1\n",cx+cy*(size-1),cx+cy*(size-1));
			//fprintf(fMR,"%d %d 1\n",cx+cy*(size-1)+size-1,cx+cy*(size-1)+size-1);


	////		fprintf(fMR,"%d %d 1\n",cx+cy*(size-1),cx+cy*(size-1)+size-1);
	////		fprintf(fMR,"%d %d 1\n",cx+cy*(size-1)+size-1,cx+cy*(size-1));

			fprintf(f1,"\'alldataV.txt\' u (%d-scale1($%d-$%d)/2):(%d.5-scale1($%d-$%d)/2):(scale1($%d-$%d)):(scale1($%d-$%d)) notitle w vec lw 2 lt -1,\\\n",cx,((size)*(cx-1)+(cy+2))*2+2,((size)*(cx-1)+(cy+1))*2+2,cy,((size)*(cx-1)+(cy+2))*2+3,((size)*(cx-1)+(cy+1))*2+3,((size)*(cx-1)+(cy+2))*2+2,((size)*(cx-1)+(cy+1))*2+2,((size)*(cx-1)+(cy+2))*2+3,((size)*(cx-1)+(cy+1))*2+3);
			fprintf(f3,"%d %d %e\n%d %d %e\n\n",cx,cy,Rn,cx,cy+1,Rn);

//			fprintf(f3,"%d %d %e\n%d %d %e\n\n",cx,cy,Rn,cx,cy+1,Rn);
		}

		fprintf(f2,"\n");
		fprintf(f3,"\n");
	}

	fprintf(f2,"\n");
	fprintf(f3,"\n");


//edge components 
   for(cy=0;cy<size;cy++)
   {
//	if(fval[(2*cy)*2*size+(2*size+1)])
	if(fval[2*cy*(2*size+1)+1])
	{
		Cn=C0*(1+gaus()*3*Csig);
		fprintf(f0,"Cx0y%dX 0 x1y%d %en\n",cy,cy,Cn);
		fprintf(f0,"Rx0y%dX 0 x1y%d 1G\n",cy,cy);

		fprintf(f1a,"Rx0y%dX 0 x1y%d %e\n",cy,cy,Cn);

		//fprintf(fMC,"%d %d -1\n",(size-1)*(size)+2,cy*(size-1)+1);
		fprintf(fMC,"%d %d 1\n",cy*(size-1)+1,(size-1)*(size)+2);
		//fprintf(fMC,"%d %d 1\n",cy*(size-1)+1,cy*(size-1)+1);
		//fprintf(fMC,"%d %d 1\n",(size-1)*(size)+2,(size-1)*(size)+2);

////		fprintf(fMC,"%d %d 1\n",(size-1)*(size)+2,cy*(size-1)+1);
////		fprintf(fMC,"%d %d 1\n",cy*(size-1)+1,(size-1)*(size)+2);

		fprintf(f1,"\'alldataV.txt\' u (0.5-scale2($%d)/2):(%d-scale2($%d)/2):(scale2($%d)):(scale2($%d)) notitle w vec lw 2 lt -1,\\\n",((cy+1))*2+2,cy,((cy+1))*2+3,((cy+1))*2+2,((cy+1))*2+3);

		fprintf(f2,"0 %d %e\n1 %d %e\n\n",cy,Cn,cy,Cn);
	}
	else
	{	
		Rn=R0*(1+gaus()*3*Rsig);
		fprintf(f0,"Rx0y%dX 0 x1y%d %ek\n",cy,cy,Rn);

		fprintf(f1a,"Rx0y%dX 0 x1y%d %e\n",cy,cy,Rn);

		//fprintf(fMR,"%d %d -1\n",(size-1)*(size)+2,cy*(size-1)+1);
		fprintf(fMR,"%d %d 1\n",cy*(size-1)+1,(size-1)*(size)+2);
		//fprintf(fMR,"%d %d 1\n",cy*(size-1)+1,cy*(size-1)+1);
		//fprintf(fMR,"%d %d 1\n",(size-1)*(size)+2,(size-1)*(size)+2);

//	//	fprintf(fMR,"%d %d 1\n",(size-1)*(size)+2,cy*(size-1)+1);
//	//	fprintf(fMR,"%d %d 1\n",cy*(size-1)+1,(size-1)*(size)+2);
		
		fprintf(f1,"\'alldataV.txt\' u (0.5-scale1($%d)/2):(%d-scale1($%d)/2):(scale1($%d)):(scale1($%d)) notitle w vec lw 2 lt -1,\\\n",((cy+1))*2+2,cy,((cy+1))*2+3,((cy+1))*2+2,((cy+1))*2+3);

		fprintf(f3,"0 %d %e\n1 %d %e\n\n",cy,Rn,cy,Rn);
	}

	fprintf(f2,"\n");
	fprintf(f3,"\n");

	if(fval[2*cy*(2*size+1)+(2*(size-1)+1)])
	{	
		Cn=C0*(1+gaus()*3*Csig);
		fprintf(f0,"Cx%dy%dX x%dy%d VOUT %en\n",size-1,cy,size-1,cy,Cn);
		fprintf(f0,"Rx%dy%dX x%dy%d VOUT 1G\n",size-1,cy,size-1,cy);
			
		fprintf(f1a,"Rx%dy%dX x%dy%d VOUT %e\n",size-1,cy,size-1,cy,Cn);

		//fprintf(fMC,"%d %d -1\n",(size-1)*(size)+1,(cy+1)*(size-1));
		fprintf(fMC,"%d %d 1\n",(cy+1)*(size-1),(size-1)*(size)+1);
		//fprintf(fMC,"%d %d 1\n",(cy+1)*(size-1),(cy+1)*(size-1));
		//fprintf(fMC,"%d %d 1\n",(size-1)*(size)+1,(size-1)*(size)+1);

////		fprintf(fMC,"%d %d 1\n",(size-1)*(size)+1,(cy+1)*(size-1));
////		fprintf(fMC,"%d %d 1\n",(cy+1)*(size-1),(size-1)*(size)+1);

		fprintf(f1,"\'alldataV.txt\' u (%d.5-scale2($2-$%d)/2):(%d-scale2($3-$%d)/2):(scale2($2-$%d)):(scale2($3-$%d)) notitle w vec lw 2 lt -1,\\\n",size-1,((size)*(size-2)+(cy+1))*2+2,cy,((size)*(size-2)+(cy+1))*2+3,((size)*(size-2)+(cy+1))*2+2,((size)*(size-2)+(cy+1))*2+3);

		fprintf(f2,"%d %d %e\n%d %d %e\n\n",size-1,cy,Cn,size,cy,Cn);
	}
	else
	{
		Rn=R0*(1+gaus()*3*Rsig);
		fprintf(f0,"Rx%dy%dX x%dy%d VOUT %ek\n",size-1,cy,size-1,cy,Rn); 

		fprintf(f1a,"Rx%dy%dX x%dy%d VOUT %e\n",size-1,cy,size-1,cy,Rn);

		//fprintf(fMR,"%d %d -1\n",(size-1)*(size)+1,(cy+1)*(size-1));
		fprintf(fMR,"%d %d 1\n",(cy+1)*(size-1),(size-1)*(size)+1);
		//fprintf(fMR,"%d %d 1\n",(cy+1)*(size-1),(cy+1)*(size-1));
		//fprintf(fMR,"%d %d 1\n",(size-1)*(size)+1,(size-1)*(size)+1);

//	//	fprintf(fMR,"%d %d 1\n",(size-1)*(size)+1,(cy+1)*(size-1));
//	//	fprintf(fMR,"%d %d 1\n",(cy+1)*(size-1),(size-1)*(size)+1);

		fprintf(f1,"\'alldataV.txt\' u (%d.5-scale1($2-$%d)/2):(%d-scale1($3-$%d)/2):(scale1($2-$%d)):(scale1($3-$%d)) notitle w vec lw 2 lt -1,\\\n",size-1,((size)*(size-2)+(cy+1))*2+2,cy,((size)*(size-2)+(cy+1))*2+3,((size)*(size-2)+(cy+1))*2+2,((size)*(size-2)+(cy+1))*2+3);

		fprintf(f3,"%d %d %e\n%d %d %e\n\n",size-1,cy,Rn,size,cy,Rn);
	}

	fprintf(f2,"\n");
	fprintf(f3,"\n");

   }

     fprintf(f1,"\'alldataV.txt\' u (0):(0):(0):(0) notitle w vec");
   
//footers
     fprintf(f0,"V1 R1_N 0 AC 50\nR1 VOUT R1_N 100Meg\n");
//     fprintf(f0,".AC DEC 10 1 1G\n.print AC all\n.END\n");

   fclose(f0);
   fclose(f1);
   fclose(f1a);
 //  fclose(f1b);
   fclose(f2);
   fclose(f3);

   free(fval);
   
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
