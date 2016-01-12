from scipy import sparse, sqrt, array, multiply

##define ode (original)
def mimura2(x,timepoints,a,b,c,d,epsilon,sigma,S):
	u=x[0:len(x)/2]
	v=x[len(x)/2:len(x)]

	udot = u * ((a + b*u - u**2)/c - v) - epsilon*(S*u)
	vdot = v * (u - (1 + d*v)) - sigma*epsilon*(S*v)
	
	xdot=[]
	xdot[0:len(x)] = udot
	xdot[len(x)/2:len(x)] = vdot
	
	return xdot

##re-centred to zero
def mimura(x,timepoints,params,S):
	a,b,c,d,epsilon,sigma=params
	u=x[0:len(x)/2]
	v=x[len(x)/2:len(x)]

	t=-(2.0*d+c-b*d)/(2*d**2)
        vb=t+sqrt(t**2+(a+b-1.0)/d**2)
        ub=1+d*vb

	udot = (u+ub) * ((a + b*(u+ub) - (u+ub)**2)/c - (v+vb)) - epsilon*(S*(u+ub))
	vdot = (v+vb) * ((u+ub) - (1 + d*(v+vb))) - sigma*epsilon*(S*(v+vb))
	
	xdot=[]
	xdot[0:len(x)] = udot
	xdot[len(x)/2:len(x)] = vdot
	
	return xdot

##version to use in fsolve
def mimura3(x,params,S):
	a,b,c,d,epsilon,sigma=params
	u=x[0:len(x)/2]
	v=x[len(x)/2:len(x)]

	t=-(2.0*d+c-b*d)/(2*d**2)
        vb=t+sqrt(t**2+(a+b-1.0)/d**2)
        ub=1+d*vb

	udot = (u+ub) * ((a + b*(u+ub) - (u+ub)**2)/c - (v+vb)) - epsilon*(S*(u+ub))
	vdot = (v+vb) * ((u+ub) - (1 + d*(v+vb))) - sigma*epsilon*(S*(v+vb))
	
	xdot=[]
	xdot[0:len(x)] = udot
	xdot[len(x)/2:len(x)] = vdot
	
	return array(xdot)
	

##version holding nodes constant
def mimura1(x,timepoints,convec,params,S):
	a,b,c,d,epsilon,sigma=params
	
	u=x[0:len(x)/2]
	v=x[len(x)/2:len(x)]

	t=-(2.0*d+c-b*d)/(2*d**2)
        vb=t+sqrt(t**2+(a+b-1.0)/d**2)
        ub=1+d*vb

	udot = (u+ub) * ((a + b*(u+ub) - (u+ub)**2)/c - (v+vb)) - epsilon*(S*(u+ub))
	vdot = (v+vb) * ((u+ub) - (1 + d*(v+vb))) - sigma*epsilon*(S*(v+vb))
	
	xdot=[]
	xdot[0:len(x)] = udot
	xdot[len(x)/2:len(x)] = vdot
	
	xdot=multiply(xdot,convec)

	return array(xdot)

















###
