import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm


plt.rcParams.update({'font.size': 16, 'figure.autolayout': True})

fig = plt.figure(figsize=(9,8))
ax = fig.add_subplot(111)

df = pd.read_table('allbifs_stab.txt', header=0, delimiter='\s*', engine="python")

#print df.keys()
"""
Index([u'#sigma,', u'L2,', u'NDNl,', u'NDNr,', u'lDNs,', u'rDNs,', u'sigma0,', u'ic'], dtype='object')
"""

points = np.array([df['#sigma,'], df['L2,'], df['NDNl,']]).T.reshape(-1, 1, 3)
segments = np.concatenate([points[:-1], points[1:]], axis=1)

NDN=np.array(df['NDNl,'])
maxN=max(NDN)

#cmap = cm.jet
cmap = cm.nipy_spectral
# define the cmap bins 
bounds = range(0,maxN)
#ticks = np.arange(0.5,50.5)
norm = mpl.colors.Normalize(vmin=1, vmax=maxN+1)
m = cm.ScalarMappable(norm=norm, cmap=cmap)
m.set_array(NDN)

for seg in segments:
    [sig1,L1,N1],[sig2,L2,N2]=seg
    cval=m.to_rgba(N1-0.5)
    if N1==N2: 
        ax.plot([sig1,sig2],[L1,L2],'-', linewidth=1, c=cval)
        #ax.scatter([sig1,sig2],[L1,L2], linewidth=1, c=cval, cmap=cmap)
    if N1==maxN: break

    
ax.set_xlabel("$\sigma$", size=20)
ax.set_ylabel("$||u,v||$", size=20)
#ax.legend(ncol=1, fontsize=16, loc=2)
cb = plt.colorbar(m, ax=ax, ticks=bounds, boundaries=bounds, label="Number of Differentiated (active) Nodes (NDN)")
labels = np.arange(1, maxN + 1, 1)
loc = labels - .5
cb.set_ticks(loc)
cb.set_ticklabels(labels)
ax.text(11, 14.0, "(b)", size=20)
ax.axis([12.5, 23, 0, 14])

fig.savefig("allstab_2.pdf")



