from scipy import sparse, exp, sin

##define 2 osc ode
def osc2(v, t, alpha1, beta1, coupling, S):
	x=v[0:len(v)/3]
	y=v[len(v)/3:2*len(v)/3]
	z=v[2*len(v)/3:len(v)]
	signal=1e-3*sin(100*t)
	print x[0], signal
	xdot = 3.9*(beta1*(y-x)\
		+ 1.87e-6*( exp(3.9*(y-x)) - exp(-3.9*(y-x)) )\
		- 0.0072 + alpha1*(x-coupling*(S*x)) )+ signal
		#+ alpha1*(x-coupling*(S*x)) ) #NO IMPERFECTION!

	ydot = - z\
		- beta1*(y-x)\
		- 1.87e-6*( exp(3.9*(y-x)) - exp(-3.9*(y-x)) )

	zdot = y - 0.042*z
	
	vdot=[]
	vdot[0:len(v)/3] = xdot
	vdot[len(v)/3:2*len(v)/3] = ydot
	vdot[2*len(v)/3:len(v)] = zdot
	
	return vdot		

