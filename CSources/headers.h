void oscND (double *, double *, int);
void RKfour (double *, int);
double gaus();
void get_args();
double R1, R2, R22, coupling,null;
//double k1[9], k2[9], k3[9], k4[9], x1_RK[9];
double *k1, *k2, *k3, *k4, *x1_RK;
double temp_map[6], mae[6], h, lya_pnt[6];
FILE *f0,*f1,*f2;
int COUNTer, niterlya1, step_map, i_RK;
