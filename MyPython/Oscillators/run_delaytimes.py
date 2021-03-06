import MutInf as mi
import numpy as np

fname='2015-09-09_flipflop.txt'

d1=mi.import_data(fname)

ts=5000.0 #points/second
#stt=1.6
#end=2.0
stt=0.0 #start time
end=60.0 #end time

# timestamps
t0=d1[0,stt*ts:end*ts]

# define data vectors/arrays
x1 = d1[2, stt*ts : end*ts] #time series data from osc_1
x2 = d1[4, stt*ts : end*ts] #time series data from osc_2
x3 = d1[6, stt*ts : end*ts] #time series data from osc_3

from matplotlib import pyplot as plt


#smooth by averaging over N points
N=200
t=np.zeros(len(t0)/N)
y1=np.zeros(len(t0)/N)
y2=np.zeros(len(t0)/N)
y3=np.zeros(len(t0)/N)
for i in range(len(t0)/N):
    t[i] = np.mean(t0[i*N:i*N+N])
    y1[i] = np.mean(x1[i*N:i*N+N])
    #c1=(4+y1[i])/8.
    #ax1.plot(t[i], 0, 's', color=(1.-c1, c1, 0), markersize=ms)
    y2[i] = np.mean(x2[i*N:i*N+N])
    #c2=(4+y2[i])/8.
    #ax1.plot(t[i], 1, 's', color=(1.-c2, c2, 0), markersize=ms)
    y3[i] = np.mean(x3[i*N:i*N+N])
    #c3=(4+y3[i])/8.
    #ax1.plot(t[i], 2, 's', color=(1.-c3, c3, 0), markersize=ms)  
bins=(2,2,2)    
delay=1

fig1=plt.figure(figsize=(18,6))
ax1=fig1.add_subplot(111)
#ms=100

mindelay=0.1 #seconds
maxdelay=10.0 #seconds
delaystep=0.1 #seconds

delays=range(int(mindelay*ts/N),int(maxdelay*ts/N),int(delaystep*ts/N))
#print delays

M12=np.zeros(len(delays))
M21=np.zeros(len(delays))
M23=np.zeros(len(delays))
M32=np.zeros(len(delays))
M31=np.zeros(len(delays))
M13=np.zeros(len(delays))

for i in range(len(delays)):
    delay=delays[i]
    M12[i] = mi.MutInf(y1, y2, Nbins=bins, s=delay)
    M21[i] = mi.MutInf(y2, y1, Nbins=bins, s=delay)

    M23[i] = mi.MutInf(y2, y3, Nbins=bins, s=delay)
    M32[i] = mi.MutInf(y3, y2, Nbins=bins, s=delay)

    M31[i] = mi.MutInf(y3, y1, Nbins=bins, s=delay)
    M13[i] = mi.MutInf(y1, y3, Nbins=bins, s=delay)

#print np.array(delays)/ts, M12-M21
    
ax1.plot(np.array(delays)/ts*N, M12-M21, 'o-', label='1->2')
#ax1.plot(delays, M21, label='M21')
ax1.plot(np.array(delays)/ts*N, M23-M32, 'o-', label='2->3')
#ax1.plot(delays, M32, label='M32')
ax1.plot(np.array(delays)/ts*N, M31-M13, 'o-', label='3->1')
ax1.plot([mindelay,maxdelay], [0,0], '-')
#ax1.plot(delays, M13, label='M13')
    
ax1.set_xlabel("delay time (s)")    
ax1.set_ylabel("Difference between TE measures")    
ax1.legend()
#a,b,c,d=ax1.axis()
#ax1.axis([a,b,-1,3])
plt.savefig("test.png")

   
fig2=plt.figure(figsize=(18,6))
ax2=fig2.add_subplot(111)

ax2.plot(t, y1, '.', label="O1")
ax2.plot(t, y2, '.', label="O2")
ax2.plot(t, y3, '.', label="O3")

ax2.set_xlabel("time (s)")    
ax2.set_ylabel("state of Nth Oscillator")    
ax2.legend()

plt.savefig("test1.png")
