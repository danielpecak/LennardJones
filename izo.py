#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import numpy as np
import math
from math import sqrt
import random
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

from biblioteka import rysowanie, repopulate, odleglosc, sila, potencjal, pbc, czastka, stale, skalowanko

import time
start = time.clock()

## Initialize
t = 0
particles = []
velocities = []
energy = []
celllist={}
for i in range(stale.sqpart): # inicjalizacja siatki
    for j in range(stale.sqpart):
        polozenie = np.array([(2*i+1),(2*j+1)])
        predkosc = np.array([(random.random()-0.5),(random.random()-0.5)])
        particles.append(czastka(stale.promien,polozenie,predkosc))
sumv = 0
for p in particles:
    sumv=sumv+p.v
    sumv=sumv/stale.particleNumber # predkosc srodka masy
for p in particles:
    p.v=(p.v-sumv) # teraz srodek masy spoczywa
repopulate(particles,celllist)

for i in range(stale.steps):
    if (i%int(stale.steps/1000) == 0): # pokazuje ile procent jest wykonane
        procent =(100.0*i/stale.steps)
        sys.stdout.write("\r")
        sys.stdout.write("Processing: %.1f" % procent)
        sys.stdout.flush()
    if (i%4000 == 0):
        rysowanie(i,[particles[x].r[0] for x in range(len(particles))],[particles[x].r[1] for x in range(len(particles))])
    sily=[]
    rif = 0
    for p1 in particles: # przechodzenie po liscie sasiadow i wyliczanie sil
        psila = np.array([0,0])
        epot = 0
        for p2 in celllist[p1]:
            f=sila(p1.r-p2.r)
            epot += potencjal(p1.r-p2.r)
            psila += f
            rif += np.dot(f,p1.r-p2.r)
        sily.append(psila)
    epot /= 2
    j = 0
    eta, ekin = skalowanko(particles,sily)
    for p in particles: # LEAPFROG
        p.v = p.v*(2*eta-1) + eta*stale.deltat*sily[j]/stale.m
        p.r = pbc(p.v*stale.deltat + p.r)
        j += 1
    if (i%1000==0): # update listy sąsiadów
        repopulate(particles,celllist)
        energy.append((stale.deltat*i,ekin,epot,ekin+epot))

elapsed = (time.clock() - start)
print stale.particleNumber,elapsed

#t = [energy[x][0] for x in range(len(energy))]
#Ek = [energy[x][1] for x in range(len(energy))]
#Ep = [energy[x][2] for x in range(len(energy))]
#Ec = [energy[x][3] for x in range(len(energy))]
#plt.clf()
#F = plt.gcf()
#F.set_size_inches((14,9))
#plt.subplot(311)
#plt.title(u"Zależność energii potencjalnej, kinetycznej i całkowitej od czasu")
#plt.xlabel("Czas $t$",fontsize=14 )
#plt.ylabel("Energia ")
#plt.grid(True)
#plt.plot(t,Ek, color="r", linestyle="-", linewidth=2)
#plt.plot(t,Ep, color="g", linestyle="-", linewidth=2)
#plt.plot(t,Ec, color="b", linestyle="-", linewidth=2)
#plt.subplot(312)
#x=np.arange(0.0, 4.0, 0.01)
#y=(stale.m*x/stale.temp)*np.exp(-stale.m*x**2/(2.0*stale.temp))
#plt.plot(x,y)
#plt.title("Rozklad predkosci czastek gazu")
#plt.xlabel("predkosc v")
#plt.hist(velocities, bins=25, normed=True)
##plt.xlabel("Czas $t$",fontsize=14 )
##plt.ylabel("Cisnienie $p$")
##plt.plot(t,p, color="r", linestyle="-", linewidth=2)
#plt.grid(True)
##plt.savefig('img/pt.png')
#plt.subplot(313)
#radials = []
#for p1 in particles:
    #for p2 in particles:
        #if p1 != p2:
            #radials.append(np.linalg.norm(p1.r-p2.r))

#delg=0.1 # grubosc warstwy
#bins=np.arange(0,stale.boxsize/2.0,delg) # zliczamy tylko do boxsize/2
#histp,bin_edges=np.histogram(radials,bins=bins,normed=True) # robimy znormalizowany histogram odleglosci miedzyczastkowych
#histn=[0]*len(histp) # pusta lista
#for i in range(0,len(histp)):
    #fg=math.pi*(((i+1)**2-i**2)*delg**2)*stale.particleNumber/(stale.boxsize**2)
    #histn[i]=histp[i]/(fg)
#plt.plot(.5*(bin_edges[1:]+bin_edges[:-1]), histn) # rysujemy histogram
#plt.savefig('img/radial.png')
