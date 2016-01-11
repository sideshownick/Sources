# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 09:52:41 2015

@author: nm268
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

plt.rcParams.update({'font.size': 16, 'figure.autolayout': True})

fig = plt.figure(figsize=(8,8))
ax = fig.add_subplot(111)

df = pd.read_table('b.workfile', header=16, delimiter='\s*', engine="python")


#print df.keys()
"""
Index([u'0', u'PT', u'TY', u'LAB', u'PAR(6)', u'L2-NORM', u'U(1)', u'U(2)',
       u'U(3)', u'U(4)', u'U(5)', u'U(6)'],
      dtype='object')
"""

points = np.array([df['PT'], df['LAB'], df['PAR(6)'], df['L2-NORM']]).T.reshape(-1, 1, 4)
segments = np.concatenate([points[:-1], points[1:]], axis=1)


pointlab=["(b)","(c)","(d)"]
#ll is the turning point label
ll=0
maxturns=15
lab1,lab2="Stable","Unstable"
for seg in segments:
    [p1,l1,x1,y1],[p2,l2,x2,y2]=seg
    ll=max(ll,l1)
    if p1<0: 
        ax.plot([x1,x2],[y1,y2],'b-', linewidth=2, label=lab1, zorder=5)
        lab1=None
    else: 
        ax.plot([x1,x2],[y1,y2],'r--', linewidth=0.7, label=lab2, zorder=1)
        lab2=None
    if 13.99<x1<14.01 and p1<0 and ll<7: 
        ax.plot(x1,y1, 'ro', zorder=10)
        ax.text(x1-0.05, y1-0.3, pointlab[int(ll/2)-1])
    if ll==maxturns: break

    
ax.set_xlabel("$\sigma$", size=20)
ax.set_ylabel("$||u,v||$", size=20)
ax.legend(ncol=1, fontsize=16, loc=2)
ax.text(12.1, 9.0, "(a)", size=20)

fig.savefig("snaking.pdf")


