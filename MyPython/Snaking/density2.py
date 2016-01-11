from numpy import histogram2d, array
import matplotlib.pyplot as plt
import matplotlib
import os

#print (matplotlib.matplotlib_fname())
#print matplotlib.rcParams

plt.rcParams.update({'font.size': 14, 'figure.autolayout': True})

fig,(ax1,ax2) = plt.subplots(nrows=2, ncols=1, 
#sharex=True, 
figsize=(8,8))



name='allbifs_stab10'
xmax=30  
finname=name+'.txt'
sigma=[]
norm=[]
IDlist=[]
for line in file(finname):
    if line[0] != '#':
        if len(line.split()) > 0:
            sig, l2,_,_,ID1,ID2,_  = line.split()
            sig, l2 = float(sig), float(l2)
            if (sig < xmax) and ((ID1,ID2) not in IDlist):        
                sigma.append(sig)
                norm.append(l2)
        else: IDlist.append((ID1,ID2))


n, bins, patches = ax1.hist(array(sigma), 100, normed=0)
plt.setp(patches, 'facecolor', 'r', 'alpha', 0.75)
ax1.set_xlabel('$\sigma$')
ax1.set_ylabel('#Solutions')
ax1.axis([13.5,30,0,800])

H, xedges, yedges = histogram2d(sigma, norm, bins=(100, 100))
extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
p=ax2.imshow(H.transpose(), origin='lower', #cmap=cm.hsv, 
       extent=extent, interpolation='nearest', aspect='auto')
#p=ax2.hexbin(sigma, norm)
ax2.axis([13.5,30,3,18])
#plt.colorbar(p).set_label('#Solutions')
ax2.set_xlabel('$\sigma$')
ax2.set_ylabel('$||u,v||$')

fig.savefig(name+str(xmax)+'-histo3D.png')
        
print IDlist
