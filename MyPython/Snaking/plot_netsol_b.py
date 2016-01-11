"""
NJM: 2015-07-30a 
Takes a file of solutions and plots them as network of nodes, ordered either spectrally or by degree.
"""

import networkx as nx
import scipy as sp
from scipy import sort, shape, array
import pylab as py
import matplotlib.pyplot as plt
import os

plt.rcParams.update({'font.size': 18, 'figure.autolayout': True})

fig = plt.subplots(1, 1, figsize=(8,8))




#ordering='degree' #'index_by_degree' #'spectral'
ordering='index_by_degree'
#ordering='spectral'

workingdir='.'
ymin,ymax=-5,3

#the network laplacian
lapn=sp.loadtxt('lap1_BA_50_10.txt')
G=nx.Graph(-lapn)
G.remove_edges_from(G.selfloop_edges())



if ordering=='spectral':
    figdir='Figures_Spectral'
    xlabel='Spectrally determined node ordering'
    posx=nx.spectral_layout(G, dim=1)
elif ordering=='index_by_degree':
    figdir='Figures_Degree'
    xlabel='Node index $i$'
    posx={}
    for i in range(len(G)):
        posx[i]=sp.array([i])   
elif ordering=='degree':
    xlabel='Node degree'
    posx={}
    for i in range(len(G)):
        posx[i]=sp.array([G.degree(i)])
    
degrees=G.degree().values()

degr1=[degrees[0]]
degr2=[degrees[0]]

for i in range(1,len(degrees)):
     if degrees[i]!=degr1[-1]: 
         degr1.append(degrees[i])
         degr2.append(degrees[i])
     else: 
         degr2.append('')

os.chdir(workingdir)

try: os.mkdir(figdir)
except: pass

pos={}
posa={} ##reverse lookup dictionary
for n1 in G:
	posa[float(posx[n1][0])] = n1

degreeseq=sp.array(G.degree().values())
degcols=degreeseq#*1.0/max(degreeseq)

optdegval=9./max(degreeseq)
dddif=1./max(degreeseq)

cmap = plt.cm.jet
# define the cmap bins 
bounds = range(min(degreeseq),max(degreeseq)+1)



def get_cmap():
    from matplotlib.colors import LinearSegmentedColormap
    '''
    Label the 3 elements in each row in the cdict entry for a given color as
    (x, y0, y1).  Then for values of x between x[i] and x[i+1] the color
    value is interpolated between y1[i] and y0[i+1].
    '''
    cdict = {'red':   ((0.0, 0.0, 0.0),
    		       (0.2, 0.0, 0.0),
                       (1.0, 1.0, 1.0)),

             'green': ((0.0, 0.0, 0.0),
             	       (optdegval-3*dddif, 0.0, 0.0),
             	       (optdegval, 1.0, 1.0),
             	       (optdegval+3*dddif, 0.0, 0.0),
                       (1.0, 0.0, 0.0)),

             'blue':  ((0.0, 0.0, 1.0),
             	       (0.8, 0.0, 0.0),
                       (1.0, 0.0, 0.0))
             }

    colormap = LinearSegmentedColormap('newmap1', cdict)
    return colormap

lab=["(b)", "(c)", "(d)", "(e)"]

soldir='NewSols'
ffname=["B", "C", "D", "E"]
for j,icfile in enumerate(sort(os.listdir(soldir))):
    print icfile
    data=sp.loadtxt(soldir+'/'+icfile)

    u=data[0:50]
    v=data[50:100]
    L2=u
    
    colormap=get_cmap()
    
    if ordering=='spectral':
        for i,val in enumerate(sp.sort(map(float, posx.values()))):
            n1=posa[val]
            pos[n1] = [i, float(L2[n1])]
    else:
        for key in posx.keys():
            pos[key]=[posx[key][0], float(L2[key])]   
    py.ylabel('Activity $u_i$')
    py.xlabel(xlabel)

    nodes=nx.draw_networkx_nodes(G, with_labels=False, pos=pos, node_color=degcols, 
                     vmin=1, vmax=max(degreeseq), cmap=colormap, node_size=100)
    edges=nx.draw_networkx_edges(G, pos=pos, width=0.5)               
    py.ylim(ymin,ymax)
    py.xlim(-1,50)
    py.colorbar(nodes, ticks=bounds, boundaries=bounds, label="Node Degree $k_i$")
    
    py.text(-10, 3, lab[j], size=20)
    
    if ordering=='index_by_degree':
        py.xticks() #range(len(degr2)),degr2,fontsize=8
         

    if ordering=='degree':
        py.xlim(min(degr1)-0.5,max(degr1)+0.5)
        py.xticks(degr1)
        
    figname=icfile.replace('.txt','.png')
    py.savefig(figname)
    py.savefig("../sol68.pdf")

    py.clf()
