import random
import pylab as plt
import numpy as np
import matplotlib.animation as animation

size=10
particles=2
T=1
delta=.01
time=5

def InitializeParticles(number,boxsize,temperature):
    xcoords=[]
    ycoords=[]
    sigma=np.sqrt(temperature)
    xvel=[]
    yvel=[]
    for i in range(number):
        xcoords.append(random.uniform(0,boxsize))
        ycoords.append(random.uniform(0,boxsize))
        xvel.append(random.gauss(0,sigma))
        yvel.append(random.gauss(0,sigma))
    print(xcoords)
    return xcoords,ycoords,xvel,yvel;

def ForceFinder(xpts,ypts):
    force=[]
    for i in range(len(xpts)):
        temp=[]
        components=[]
        for j in range(len(xpts)):
            a=np.sqrt((xpts[i]-xpts[j])**2+(ypts[i]-ypts[j])**2)
            if a != 0:
                components.append([(xpts[j]-xpts[j-1])/a,(ypts[j]-ypts[j-1])/a])
                temp.append([24*(2/a**13-1/a**7)*components[j-1][0],24*(2/a**13-1/a**7)*components[j-1][1]])
            else:
                temp.append([0,0])
        force.append(temp)
    forcex=0
    forcey=0
    net=[]
    for i in range(len(force)):
        for j in range(len(force[i])):
            forcex+=force[i][j][0]
            forcey+=force[i][j][1]
        net.append([forcex,forcey])
    return net;

def Evolve(timestep,tmax,xcoord,ycoord,boxsize):
    steps=np.arange(0,tmax,timestep)
    info=[]
    for i in range(len(steps)):
        xnew=[]
        ynew=[]
        force=ForceFinder(xcoord,ycoord)
        for j in range(len(xcoord)):
            xnew.append((2*xcoord[j]-xcoord[j-1]+force[j][0]*(steps[i]-steps[i-1])**2)%boxsize)
            ynew.append((2*ycoord[j]-ycoord[j-1]+force[j][1]*(steps[i]-steps[i-1])**2)%boxsize)
            xcoord[j]=(2*xcoord[j]-xcoord[j-1]+force[j][0]*(steps[i]-steps[i-1])**2)%boxsize
            ycoord[j]=(2*ycoord[j]-ycoord[j-1]+force[j][1]*(steps[i]-steps[i-1])**2)%boxsize
        info.append([xnew,ynew])
    return info;

def animate(i, points):
    points.set_data(xtime[i],ytime[i])
    return points,


[x,y,xvel,yvel]=InitializeParticles(particles,size,T)

solution=Evolve(delta,time,x,y,size)
xtime=[solution[i][0] for i in range(len(solution))]
ytime=[solution[i][1] for i in range(len(solution))]


#Plotting

fig=plt.figure()
points=plt.plot([],[],'o')
plt.xlim(0,size)
plt.ylim(0,size)
a=animation.FuncAnimation(fig,animate,frames=len(xtime),fargs=(points), interval=25,blit=True)
plt.show()