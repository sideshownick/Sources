def MutInf(x1, x2, Nbins=(20,20,20), s=1):
    import numpy as np # histogramdd, array, transpose
   
    # define data vectors/arrays
    x = x1[s:] #time series data from osc_1
    y = x1[:-s] #time series data from osc_1 delayed by s
    z = x2[:-s] #time series data from osc_2 delayed by s

    # calculate 3D histogram of size (nx,ny,nz) where nx is the number
    # of bins for x, ny for y, nz for z. This is the tricky part since
    # the size of bins is quite critical. However you could start with
    # say nx=20, i.e. 20 bins evenly spaced between the min and max values
    # of x
    nx,ny,nz = Nbins
    H, edges = np.histogramdd([x,y,z], bins=(nx,ny,nz))

    # add small probability mass everywhere to avoid divide by zeros,
    # e.g. 1e-9 (you can experiment with different values). This part
    # was a bit of a fudge and should be replaced with something more
    # sensible - but I never got round to it
    #H = H + 1e-12

    # renormalise so sums to unity
    P = H  / np.sum(H)

    # now sum along the first dimension to create a 2D array of p(y,z)
    P_yz = np.sum(P, axis=0)

    # replicate the 2D array at each element in the first dimension
    # so as to regain a (nx,ny,nz) array (this is purely for computational
    # ease)
    from numpy.matlib import repmat

    P_yz = repmat(P_yz,nx,1).reshape(nx,ny,nz)

    # now sum along the first and third dimension to give 1D array of p(y)
    P_y = np.sum(P,axis=(0,2))

    # replicate in both the x and z directions
    P_y = repmat(P_y,nx,nz).reshape(nx,ny,nz)

    P_xy = np.sum(P,axis=2)
    P_xy = repmat(P_xy,nz,1).reshape(nx,ny,nz)
    
    # create conditional probability mass functions
    P_x_given_yz = P / P_yz
    P_x_given_y  = P_xy / P_y

    # calculate transfer entropy
    logP = np.log(P_x_given_yz / P_x_given_y)
    logP = np.nan_to_num(logP)

    T = np.sum(P * logP)

    return T
    
def import_data(fname):
    from numpy import transpose
    f1=file(fname)

    filetext=f1.readlines()

    data=[]
    for i in range(len(filetext)):
        data.append(map(float, filetext[i].split()))

    ## vectors t, x1, x2, x3, ...
    d1=transpose(data)   
    return d1
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
