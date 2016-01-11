#include<stdio.h>
#include<stdlib.h>
#include<math.h>
#include<string.h>
#include"headers.h"

void
oscND (double *x1, double *x, int Nosc)
{
	int i, Nosc1;

	Nosc1=Nosc-1;

	for (i=0;i<Nosc1;i++)
	{
		x1[3*i+0] = 3.9*(2276.4161*1.0/R2*(x[3*i+1]-x[3*i+0])
		+ 1.868662e-6*( exp(3.9*(x[3*i+1]-x[3*i+0])) 
					- exp(-3.9*(x[3*i+1]-x[3*i+0])) )
		- 0.0072845315 + 2299.1803/R1*(x[3*i+0]-coupling*x[3*i+3])
		    );

		x1[3*i+1] = - x[3*i+2]
		- 2276.4161*1.0/R2*(x[3*i+1]-x[3*i+0])
		- 1.868662e-6*( exp(3.9*(x[3*i+1]-x[3*i+0])) - exp(-3.9*(x[3*i+1]-x[3*i+0])) );

		x1[3*i+2] =  x[3*i+1] - 0.041726631*x[3*i+2];
	}

	i=Nosc1;

	x1[3*i+0] = 3.9*(2276.4161*1.0/R2*(x[3*i+1]-x[3*i+0])
		+ 1.868662e-6*( exp(3.9*(x[3*i+1]-x[3*i+0])) 
					- exp(-3.9*(x[3*i+1]-x[3*i+0])) )
		- 0.0072845315 + 2299.1803/R1*(x[3*i+0]-coupling*x[0])
		    );

	x1[3*i+1] = - x[3*i+2]
		- 2276.4161*1.0/R2*(x[3*i+1]-x[3*i+0])
		- 1.868662e-6*( exp(3.9*(x[3*i+1]-x[3*i+0])) - exp(-3.9*(x[3*i+1]-x[3*i+0])) );

	x1[3*i+2] =  x[3*i+1] - 0.041726631*x[3*i+2];


}


void
RKfour (double *x, int Nosc)
{

//double k1[9], k2[9], k3[9], k4[9], x1_RK[9];

	oscND (x1_RK, x, Nosc);

	for (i_RK = 0; i_RK < 3*Nosc; i_RK++)
	{
		k1[i_RK] = h * x1_RK[i_RK];
		x[i_RK] = x[i_RK] + k1[i_RK] / 2;
	}
	
	oscND (x1_RK, x, Nosc);
	
	for (i_RK = 0; i_RK < 3*Nosc; i_RK++)
	{
		k2[i_RK] = h * x1_RK[i_RK];
		x[i_RK] = x[i_RK] + k2[i_RK] / 2;
	}
	
	oscND (x1_RK, x, Nosc);

	for (i_RK = 0; i_RK < 3*Nosc; i_RK++)
	{
		k3[i_RK] = h * x1_RK[i_RK];
		x[i_RK] = x[i_RK] + k3[i_RK];
	}
	
	oscND (x1_RK, x, Nosc);

	for (i_RK = 0; i_RK < 3*Nosc; i_RK++)
	{
		k4[i_RK] = h * x1_RK[i_RK];
		x[i_RK] = x[i_RK] + k1[i_RK] / 6 + k2[i_RK] / 3 + k3[i_RK] / 3 + k4[i_RK] / 6;
	}

}

double
gaus()
{	
	double rnd_x, rnd_y, gauss;
	double e = 2.7182818, rmax=2147483647;

	for (;;)
	{
		rnd_x = (rand ()/rmax*2-1);
 		rnd_y = (rand ()/rmax);
 
 		gauss = pow(e,-0.5*9*rnd_x*rnd_x);
 
 		if (rnd_y < gauss)
 			return rnd_x;
	}
}

void get_args(int argc, char** argv, int* Nosc, double* stepsize, int* trans, int* length, int* jump, double* coupling, double* parameter, char** fnamein, char** fnameout)
{
    int i;

    /* Start at i = 1 to skip the command name. */

    for (i = 1; i < argc; i++) {

	/* Check for a switch (leading "-"). */

	if (argv[i][0] == '-') {

	    /* Use the next character to decide what to do. */

	    switch (argv[i][1]) {

		case 'n':	*Nosc = atoi(argv[++i]);
				break;

		case 's':	*stepsize = atof(argv[++i]);
				break;

		case 't':	*trans = atoi(argv[++i]);
				break;

		case 'l':	*length = atoi(argv[++i]);
				break;

		case 'j':	*jump = atoi(argv[++i]);
				break;

		case 'c':	*coupling = atof(argv[++i]);
				break;

		case 'b':	*parameter = atof(argv[++i]);
				break;

		case 'i':	*fnamein = argv[++i];
				break;

		case 'o':	*fnameout = argv[++i];
				break;

		default:	fprintf(stderr,"\nUsage:\n\n./osc -[switch] [value]\n\n(don't forget the space!)\n\nswitches:\n-i \"IC_filename\" (default \"ic.txt\")\n-o \"output_filename\"(default \"out.txt\")\n-n number_of_oscillators\n-b parameter_value (default = 3.47)\n-s integration_stepsize (default 0.01)\n-t length_of_transient (default 0)\n-l length_of_run (default=1000)\n-j jumpsteps (print every jth value, default=1)\n-c coupling_strength (default=0.0909)\n");
	    }
	}
    }
}
