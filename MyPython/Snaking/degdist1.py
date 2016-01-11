import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

L=np.loadtxt("lap1_BA_50_10.txt")

ks=[]
for i,l in enumerate(L):
    k=l[i]
    ks.append(k)

fig = plt.figure(figsize=(8,8))
ax = fig.add_subplot(111)    
    
histo = ax.hist(ks, bins=np.arange(0, max(ks)+2))

with open("deg-seq.txt", "w") as of:
    for i in range(len(histo[0])):
        for j in range(int(histo[0][i])):
                of.write(str(histo[1][i]) + "\n")

with open("deg-dist.txt", "w") as of:
    for i in range(len(histo[0])):
        of.write(str(histo[1][i]) + " " + str(int(histo[0][i])) + "\n")

with open("degdist0.txt", "w") as of:
    for i in range(len(histo[0])):
        of.write(str(int(histo[0][i])) + "\n")
    
plt.rcParams.update({'font.size': 16, 'figure.autolayout': True})

ax.set_xticks(np.arange(min(ks),max(ks)+1)+0.5)
ax.set_xticklabels(np.arange(int(min(ks)),int(max(ks))+1))
a=ax.axis()     
ax.axis([min(ks)-0.5, max(ks)+1.5, a[2], a[3]])
ax.set_xlabel("Degree $k_i$")
ax.set_ylabel("Distribution $d_k$")

plt.savefig("degdist.pdf")


fig = plt.figure(figsize=(8,8))
ax = fig.add_subplot(111) 

G=nx.Graph(L)
pos=nx.spectral_layout(G)
pos2=nx.random_layout(G)
for i,key in enumerate(sorted(pos)):
    #pos[key]+=[np.random.random()/2, np.random.random()/2]
    xx,yy=pos2[key]
    pos2[key] = [(xx-0.5)*2/G.degree()[i],(yy-0.5)*2/G.degree()[i]]
nx.draw_networkx(G, pos=pos2)
ax.set_xticks([])
ax.set_yticks([])
ax.set_frame_on(False)
plt.savefig("network.pdf")






