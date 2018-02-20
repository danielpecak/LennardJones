#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import math
from math import sqrt, ceil
import random
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from PIL import Image, ImageDraw

class stale:
    """The class holds all constants and parameters of the program. """
    def __init__(self):
        self.steps = 800000
        self.sqpart = 22
        self.particleNumber = self.sqpart**2
        self.boxsize = self.sqpart*2
        self.eps = 1.0
        self.sigma = 1.0
        self.promien = 0.5
        self.deltat = 0.0002
        self.temp = 0.35
        self.m = 1.
        self.rc = 2.5*self.sigma
        self.rcc = 2.5*self.sigma
        self.rn = ceil((self.rcc/self.promien)**2)

stale = stale()
boxsize=stale.boxsize

def rysowanie(en,rx,ry):
    """Draws picture of particles in the step EN. RX and RY are lists of particles' coordinates."""
    if (en%4000==0):     #  every 4000 step
        plt.clf()        #  clear figure
        F = plt.gcf()    #  define new/blank
        a = plt.gca()    #  "get current axes" (to add smth to them)
        for i in range(stale.particleNumber):    # loop over particles
            cir = Circle((rx[i],ry[i]), radius=stale.promien)  # draw circle where the particle is
            a.add_patch(cir)                     # add the circle to the plot
        plt.plot()                               # draw
        plt.xlim((0,boxsize))                    # range to draw X
        plt.ylim((0,boxsize))                    # range to draw Y
        F.set_size_inches((6,6))                 # size of the picture
        nStr=str(en)     #filename with 5 leading zeros for example 00324.png
        nStr=nStr.rjust(5,'0')
        plt.title("Lennard-Jones gas, step "+nStr)
        plt.savefig('data/img'+nStr+'.png')


class czastka:
    """Describes one particle of a gas."""
    def __init__(self,promien,pos,vel):
        self.promien = promien # radius
        self.r=pos             # position
        self.v=vel             # velocity


def repopulate(particles,celllist):
    """Make new list of the nearest neighbors."""
    for p in particles:
        celllist[p] = []
        for p2 in particles:
            if p != p2 and np.linalg.norm(odleglosc(p.r - p2.r)) < 3.5:
                celllist[p].append(p2)


def skalowanko(particles,sily):
    """Returns a parameters saying if there is heating or cooling."""
    # Half of a step  - without resistance force
    j = 0
    predkosci = []  # velocities
    for p in particles:
        predkosci.append(p.v + sily[j]/stale.m*stale.deltat/2)
        j += 1
    # calculate the average temperature and shift it so the center of mass is in rest
    sumv2 = 0
    for p in predkosci:
        sumv2=sumv2+np.dot(p,p)/2.0
    tau=sumv2/stale.particleNumber  # average kinetic energy
    eta=sqrt(stale.temp/tau)        # scaling factor,  temp = a given temperature
    return (eta,sumv2)

def odleglosc(rrr):
    """Measuring a distance in a periodic boundary conditions (PBC).""" # NOPE, I don't know what is happening
    if rrr[0] > boxsize/2.:
        rrr[0] -= boxsize
    elif rrr[0] < -boxsize/2.:
        rrr[0] += boxsize
    if rrr[1] > boxsize/2.:
        rrr[1] -= boxsize
    elif rrr[1] < -boxsize/2.:
        rrr[1] += boxsize
    return rrr

def sila(r):
    """Calculate force between particles in a distance R."""
    rn0 = odleglosc(r)
    rn = np.linalg.norm(rn0)
    if rn < stale.rc:
        return rn0/rn*48*stale.eps/stale.sigma*((stale.sigma/rn)**13-0.5*(stale.sigma/rn)**7)
    else:
        return np.array([0.,0.])

def potencjal(r):
    """Van der Waals potential. If particles are far enough, it is considered zero."""
    rn0 = odleglosc(r)
    rn = np.linalg.norm(rn0)
    if rn < stale.rc:
        return 4*stale.eps*((stale.sigma/rn)**12-(stale.sigma/rn)**6)
    else:
        return 0

def pbc(r):
    """Measuring a distance in a periodic boundary conditions (PBC)."""
    if r[0] > boxsize:
        r[0] -= boxsize
    if r[0] < 0:
        r[0] += boxsize
    if r[1] > boxsize:
        r[1] -= boxsize
    if r[1] < 0:
        r[1] += boxsize
    return r
