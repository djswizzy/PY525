import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation

n=50 #Number of Birds
sep=1;align=.125;coh=.01; strength=.05 #Interaction Strength for each rule
birdsize=.25
area=4 #Initial Flock area
steps=1000
dt=.1

place=[]
change=[]
a=[]
#Initialize birds
for i in range(n):
    too_close = True
    while too_close:
        too_close = False
        if len(place) > 0:
            x_temp = area*np.random.rand()
            y_temp = area*np.random.rand()
            for i in range(len(place)):
                if np.sqrt((x_temp-place[0][i][0])**2+(y_temp-place[0][i][1])**2) < birdsize:
                    too_close = True
                    break
        else:
            x_temp = area*np.random.rand()
            y_temp = area*np.random.rand()
#            vx_temp= np.random.poisson
#            vy_temp= np.random.poisson
            a.append([x_temp,y_temp])
place.append(a)
#q=[]
#for j in range(len(place[0])):
#    l=np.random.rand()
#    vix=vi*l;viy=vi*(1-l)
#    q.append([place[0][j][0]+vix*dt,place[0][j][1]+viy*dt])
#place.append(q)

def rule1(time,number):
    #Birds move towards center of mass of other birds
    xc=0;yc=0;
    for i in range(len(time)):
        if i != number:
            xc+=time[i][0]; yc+=time[i][1]
        xc /= float(n-1); yc /= float(n-1);
    v1x=(xc-time[number][0])*coh
    v1y=(yc-time[number][1])*coh
    return [v1x,v1y]

def rule2(time,number):
    #Birds avoid getting too close to other birds
    v2x=0;v2y=0;
    for i in range(len(time)):
        if i != number:
            rad=np.sqrt((time[i][0]-time[number][0])**2+(time[i][1]-time[number][1])**2)
            rx=(time[i][0]-time[number][0])/rad
            ry=(time[i][1]-time[number][1])/rad
            if rad < birdsize:
                v2x-=rx
                v2y-=ry
    return [v2x*sep,v2y*sep]

def rule3(vel,number):
    #Birds move towards avg velocity of other birds
    vxc=0;vyc=0;
    for i in range(len(vel)):
        if i != number:
           vxc+=vel[i][0]; vyc+=vel[i][1]
        vxc /= float(n-1); vyc /= float(n-1);
    v3x=(vxc-vel[number][0])*align
    v3y=(vyc-vel[number][1])*align
    return [v3x,v3y]


def move(timeslice,oldtime):
    v=[]
    delta=[]
    for j in range(len(timeslice)):
        v.append([(timeslice[j][0]-oldtime[j][0]),(timeslice[j][1]-oldtime[j][1])])
    for j in range(len(timeslice)):
        v1=rule1(timeslice,j)
        v2=rule2(timeslice,j)
        v3=rule3(v,j)
        
        #Poisson Random Kick
        prob2=np.random.rand()
        kick=[0,0]
#        if prob2 < .25:
#            sign=[-1,1]
#            kick=[strength*np.random.choice(sign)*np.random.poisson(),strength*np.random.choice(sign)*np.random.poisson()]
        
        
        delta.append([(v1[0]+v2[0]+v3[0])*dt+kick[0],(v1[1]+v2[1]+v3[1])*dt])
    return delta

for i in range(steps):
    b=[]
    if i==0:
        change=[]
        for _ in range(n):
            change.append([.1,.1])
    else:
        change=move(place[i],place[i-1])
    for j in range(n):
        b.append([place[i][j][0]+change[j][0],place[i][j][1]+change[j][1]])
    place.append(b)

###############################--Graphing--######################################
 
    
x=[]
y=[]
dx=[]
dy =[]
for i in range(steps):
    pidgeon=[]
    albatross=[]
    for j in range(n):
        pidgeon.append(place[i][j][0])
        albatross.append(place[i][j][1])
    x.append(pidgeon)
    y.append(albatross)
    
    
centers = []
for timestep in place:
    xavg=0; yavg=0;
    for point in timestep:
        xavg += point[0]; yavg += point[1]
    xavg /= float(n); yavg /= float(n);
    centers.append([xavg,yavg])


def animate(i):
    points.set_data(x[i],y[i])
    ax.set_xlim([centers[i][0]-5,centers[i][0]+5])
    ax.set_ylim([centers[i][1]-5,centers[i][1]+5])
    return points,

fig=plt.figure()
ax = fig.add_subplot(111)
points = ax.plot([],[],'.',color='k')[0]
ax.set_xticklabels([])
ax.set_yticklabels([])
ax.grid(color='k',linestyle='-',linewidth=.5,alpha=.8)
anim = animation.FuncAnimation(fig, animate,frames=len(place), interval=10, blit=False)
plt.show
