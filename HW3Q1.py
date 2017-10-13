import random
import pylab as plt
import numpy as np
import matplotlib.animation as animation
from copy import deepcopy

size=10
particles=16
T=1
delta=.01
time=5
minsep=1

def InitializeParticles(number,boxsize,temperature):
    xcoords=[]
    ycoords=[]
    sigma=np.sqrt(temperature)
    xvel=[]
    yvel=[]
    for i in range(number):
        suitable = False
        while not suitable: 
            suitable = True
            tempxcoords=random.uniform(0,boxsize)
            tempycoords=random.uniform(0,boxsize)
            for i in range(len(xcoords)):
                if np.sqrt((tempxcoords-xcoords[i])**2+(tempycoords-ycoords[i])**2) < minsep:
                    suitable = False
                    break
        xcoords.append(tempxcoords)
        ycoords.append(tempycoords)
        xvel.append(random.gauss(0,sigma))
        yvel.append(random.gauss(0,sigma))
    return xcoords,ycoords,xvel,yvel;

def InitializeLattice(number,boxsize,temperature):
    xcoords=[]
    ycoords=[]
    sigma=np.sqrt(temperature)
    xvel=[]
    yvel=[]
    for i in np.arange(0,boxsize,1):
        for j in np.arange(0,boxsize,1):
            xcoords.append(i+.5)
            ycoords.append(j+.5)
    for k in range(number):
        xvel.append(random.gauss(0,sigma))
        yvel.append(random.gauss(0,sigma))
    return xcoords,ycoords,xvel,yvel;

def Energy(xpts,ypts,xprev,yprev):
    energy=0
    for i in range(len(xpts)):
        for j in range(len(ypts)):
            a = np.sqrt((xpts[i]-xpts[j])**2+(ypts[i]-ypts[j])**2)
            if a != 0 and a < 3:
                energy+= 4*(a**-12 - a**-6) + 0.5*((xpts[j]-xprev[j])/delta)**2+0.5*((ypts[j]-ypts[j])/delta)**2
    return energy;

def ForceFinder(xpts,ypts):
    force=[]
    for i in range(len(xpts)):
        temp=[]
        components=[]
        vals=[-1,0,1]
        xptstemp=deepcopy(xpts)
        yptstemp=deepcopy(ypts)
        for k in vals:
            for l in vals:
                xptstemp.append(xptstemp[i]+k*size)
                yptstemp.append(yptstemp[i]+l*size)
        for j in range(len(xpts)):
            a = np.sqrt((xptstemp[i]-xptstemp[j])**2+(yptstemp[i]-yptstemp[j])**2)
            if a != 0 and a < 3:
                components.append([(xptstemp[i]-xptstemp[j])/a,(yptstemp[i]-yptstemp[j])/a]) 
                temp.append([24*(2*a**-13 - a**-7)*components[j][0],24*(2*a**-13 - a**-7)*components[j][1]])
            else:
                components.append([0,0])
                temp.append([0,0])
        force.append(temp)
    net=[]
    for i in range(len(force)):
        forcex=0
        forcey=0
        for j in range(len(force[i])):
            forcex+=force[i][j][0]
            forcey+=force[i][j][1]
        net.append([forcex,forcey])
    return net;

def Evolve(timestep,tmax,xcoord,ycoord,xinit,yinit,boxsize):
    steps=np.arange(0,tmax,timestep)
    info=[]
    info.append([xcoord,ycoord])
    foo=[]
    bar=[]
    energy=[]
    for j in range(len(xcoord)):
        foo.append(xcoord[j]+xinit[j]*timestep)
        bar.append(ycoord[j]+yinit[j]*timestep)
    info.append([foo,bar])
    for i in range(1,len(steps)):
        xnew=[]
        ynew=[]
        force=ForceFinder(info[i][0],info[i][1])
        energy.append(Energy(info[i][0],info[i][1],info[i-1][0],info[i-1][1]))
        for j in range(len(xcoord)):
            xnew.append((2*info[i][0][j]-info[i-1][0][j]+force[j][0]*timestep**2)%boxsize)
            ynew.append((2*info[i][1][j]-info[i-1][1][j]+force[j][1]*timestep**2)%boxsize)
        info.append([xnew,ynew])
    return info,energy;

def animate(i, points):
    points.set_data(xtime[i],ytime[i])
    return points,


[x,y,xvel,yvel]=InitializeParticles(particles,size,T)
#[x,y,xvel,yvel]=InitializeLattice(particles,size,T)

[solution,energy]=Evolve(delta,time,x,y,xvel,yvel,size)

#Plotting

xtime=[solution[i][0] for i in range(len(solution))]
ytime=[solution[i][1] for i in range(len(solution))]


fig=plt.figure(1)
points=plt.plot([],[],'o',)
plt.xticks([])
plt.yticks([])
plt.xlim(0,size)
plt.ylim(0,size)
a=animation.FuncAnimation(fig,animate,frames=len(xtime),fargs=(points), interval=15,blit=True)
i=0
while i < len(energy):
    E=energy[i]
    if E < 100:
        E=energy[i]
    else:
        energy[i]=0
    i+=1


plt.figure(2)
plt.plot(np.arange(0,time-delta,delta),energy)
plt.show()