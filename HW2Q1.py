import itertools as it
import pylab as plt
import numpy as np
import time
import random
#Generate All Possible spin states of 4x4 lattice
t=time.time()
perms=[]
vals=[-1,1]
for i in vals:
    for j in vals:
        for k in vals:
            for l in vals:
                perms.append([i,j,k,l])
#combs=it.product(perms,repeat=4)
#combs=list(combs)
#Begin calculations
J=1 #Arbitrary
#H = []
#Z=[]
#for comb in combs:
#    total=0
#    for i in range(len(comb)):
#        for j in range(len(comb)):
#            total+=-J*comb[i][j]*comb[(i+1)%len(comb)][j]+-J*comb[i][j]*comb[(i-1)%len(comb)][j]+-J*comb[i][j]*comb[i][(j+1)%len(comb)]+-J*comb[i][j]*comb[i][(j-1)%len(comb)]
#            H.append(total/2) #Remove double count
T=np.linspace(0.2,5,10)
#top=[]
#var=[]
#for i in T:
#    tot=0
#    tot2=0
#    tot3=0
#    for j in range(len(combs)):
#        tot+=np.exp(-H[j]/i)
#        tot2+=np.exp(-H[j]/i)*H[j]
#        tot3+=np.exp(-H[j]/i)*H[j]**2
#    top.append(tot2)
#    Z.append(tot)
#    var.append(tot3)
#U=[]
#C=[]
#for i in range(len(Z)):
#    U.append(top[i]/Z[i])
#    C.append((var[i]/Z[i]-(top[i]/Z[i])**2)/T[i]**2)
#U=[i/16 for i in U]
#C=[i/16 for i in C]
elapsed=time.time()-t
t=time.time()
Hmet=[]
seed=[]
for _ in range(4):
    seed.append([1,1,1,1])
for l in T:
    for k in range(1000):
        Hx=0
        Hy=0
        for i in range(len(seed)):
            for j in range(len(seed)):
                Hx+=(-J*seed[i][j]*seed[(i+1)%len(seed)][j]+-J*seed[i][j]*seed[(i-1)%len(seed)][j]+-J*seed[i][j]*seed[i][(j+1)%len(seed)]+-J*seed[i][j]*seed[i][(j-1)%len(seed)])/2
        a=random.randint(0,3)
        b=random.randint(0,3)
        temp=[x for x in seed]
        temp[a][b]=-temp[a][b]
        for i in range(len(seed)):
            for j in range(len(seed)):
                Hy+=(-J*temp[i][j]*temp[(i+1)%len(seed)][j]+-J*temp[i][j]*temp[(i-1)%len(seed)][j]+-J*temp[i][j]*temp[i][(j+1)%len(seed)]+-J*temp[i][j]*temp[i][(j-1)%len(seed)])/2
        r=np.exp(-(Hx-Hy)/l)
        if r >= 1:
            Hmet.append(Hy)
            seed=[x for x in temp]
        elif r < 1 and r < random.random():
            Hmet.append(Hy)
            seed=[x for x in temp]
top2=[]
Z2=[]
var2=[]
for i in T:
    tot=0
    tot2=0
    tot3=0
    for j in range(len(Hmet)):
        tot+=np.exp(-Hmet[j]/i)
        tot2+=np.exp(-Hmet[j]/i)*Hmet[j]
        tot3+=np.exp(-Hmet[j]/i)*Hmet[j]**2
    top2.append(tot2)
    Z2.append(tot)
    var2.append(tot3)
U2=[]
Cv2=[]
for i in range(len(Z2)):
    U2.append(top2[i]/Z2[i])
    Cv2.append((var2[i]/Z2[i]-(top2[i]/Z2[i])**2)/T[i]**2)
U2=[i/16 for i in U2]
Cv2=[i/16 for i in Cv2]
elapsed2=time.time()-t
print('The Metropolis algorithm saved you',abs(elapsed-elapsed2),'seconds.')
plt.figure(1)
plt.plot(T,U2,'-',label='Metropolis')
#plt.plot(T,U,'-',label='Brute Force')
plt.xlabel('Temperature')
plt.ylabel('U')
plt.title('Internal Energy')
plt.legend()
plt.figure(2)
plt.plot(T,Cv2,'-',label='Metropolis')
#plt.plot(T,C,'-',label='Brute Force',color='orange')
plt.xlabel('Temperature')
plt.ylabel('Cv')
plt.title('Specific Heat')
plt.legend()
