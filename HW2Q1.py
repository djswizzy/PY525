# -*- coding: utf-8 -*-
import itertools as it
import pylab as plt
import numpy as np
#Generate All Possible spin states of 4x4 lattice
perms=[]
vals=[-1,1]
for i in vals:
    for j in vals:
        for k in vals:
            for l in vals:
                perms.append([i,j,k,l])
combs=it.product(perms,repeat=4)
combs=list(combs)
#Begin calculations
J=1 #Arbitrary
H = []
Z=[]
for comb in combs:
    total=0
    for i in range(len(comb)):
        for j in range(len(comb)):
            total+=-J*comb[i][j]*comb[(i+1)%len(comb)][j]+-J*comb[i][j]*comb[(i-1)%len(comb)][j]+-J*comb[i][j]*comb[i][(j+1)%len(comb)]+-J*comb[i][j]*comb[i][(j-1)%len(comb)]
            H.append(total/2) #Remove double count
T=np.linspace(0.2,5,250)
top=[]
var=[]
for i in T:
    tot=0
    tot2=0
    tot3=0
    for j in range(len(combs)):
        tot+=np.exp(-H[j]/i)
        tot2+=np.exp(-H[j]/i)*H[j]
        tot3+=np.exp(-H[j]/i)*H[j]**2
    top.append(tot2)
    Z.append(tot)
    var.append(tot3)
U=[]
C=[]
for i in range(len(Z)):
    U.append(top[i]/Z[i])
    C.append((var[i]/Z[i]-(top[i]/Z[i])**2)/T[i]**2)
U=[i/16 for i in U]
C=[i/16 for i in C]
plt.figure(1)
plt.plot(T,U,'.')
plt.xlabel('Temperature')
plt.ylabel('U')
plt.title('Internal Energy')
plt.figure(2)
plt.plot(T,C,'.',color='orange')
plt.xlabel('Temperature')
plt.ylabel('Cv')
plt.title('Specific Heat')
