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
            H.append(total)
T=np.linspace(0.2,5,50)
tot=0
tot2=0
top=[]
for j in T:
    for j in range(len(combs)):
        tot+=np.exp(-H[j]/i)
        tot2+=np.exp(-H[j]/i)*H[j]
    top.append(tot2)
    Z.append(tot)
U=[]
for i in range(len(Z)):
    U.append(top[i]/Z[i])
U=[i/16 for i in U]
print(U)
plt.plot(T,U,'.')