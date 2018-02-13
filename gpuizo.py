#!/usr/bin/env python
# -*- coding: utf-8 -*-
# General libraries
import sys
import numpy as np
import math # OUT/REMOVE IT?
from math import sqrt
import random
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import time

# My libraries
from biblioteka import rysowanie, stale
from gpu_code import source as source # Here we have the whole source code for GPU


# Libraries NVIDIA CUDA
import pycuda.autoinit
import pycuda.driver as cuda
import pycuda.cumath as cumath
import pycuda.gpuarray as gpuarray
from pycuda.curandom import rand as curand
from pycuda.compiler import SourceModule


start = time.clock()

# Get GPU function
mod = SourceModule(source)
get_energy = mod.get_function("energy")
polKroku = mod.get_function("polKroku")
fupdate = mod.get_function("fupdate")
leapfrog = mod.get_function("leapfrog")
repopulate= mod.get_function("repopulate")
#sila = mod.get_function("sila")

# Initialize data
t = 0
particles = []
velocities = []
energy = []
celllist={}
# random velocities
px = curand((stale.particleNumber,)).get().astype(np.float32)
py = curand((stale.particleNumber,)).get().astype(np.float32)
# velocity distribution around 0, not 0.5
px = px - 0.5
py = py - 0.5

# Here we have energy, not velocity ([XXX] needs correction)
v  = np.zeros((stale.particleNumber,)).astype(np.float32)
rx = np.zeros((stale.particleNumber,)).astype(np.float32)
ry = np.zeros((stale.particleNumber,)).astype(np.float32)
fx = np.zeros((stale.particleNumber,)).astype(np.float32)
fy = np.zeros((stale.particleNumber,)).astype(np.float32)

# Initializing a list of neighbors (structure)
# It reduces complexity from O(N^2) to O(N)
nl = (-1)*np.ones((stale.particleNumber,stale.rn)).astype(np.float32)

# Initializing grid of initial coordinates
for i in range(stale.sqpart):
    for j in range(stale.sqpart):
        rx[j+stale.sqpart*i] = 2*i+1
        ry[j+stale.sqpart*i] = 2*j+1
# Center of mass frame
px = px - px.sum()/stale.particleNumber
py = py - py.sum()/stale.particleNumber


# Loading data to GPU (momenta, positions, forces, energy (v), neighbor list)
px_gpu = cuda.mem_alloc(px.nbytes)
cuda.memcpy_htod(px_gpu,px)
py_gpu = cuda.mem_alloc(py.nbytes)
cuda.memcpy_htod(py_gpu,py)
rx_gpu = cuda.mem_alloc(rx.nbytes)
cuda.memcpy_htod(rx_gpu,rx)
ry_gpu = cuda.mem_alloc(ry.nbytes)
cuda.memcpy_htod(ry_gpu,ry)
fx_gpu = cuda.mem_alloc(fx.nbytes)
cuda.memcpy_htod(fx_gpu,fx)
fy_gpu = cuda.mem_alloc(ry.nbytes)
cuda.memcpy_htod(fy_gpu,fy)
v_gpu = cuda.mem_alloc(v.nbytes)
cuda.memcpy_htod(v_gpu,v)
nl_gpu = cuda.mem_alloc(nl.nbytes)
cuda.memcpy_htod(nl_gpu,nl)

# Initialize neighbor list with first data
repopulate(rx_gpu,ry_gpu,nl_gpu,np.array(stale.rn).astype(np.float32), block=(stale.particleNumber,1,1))



energia = np.zeros((stale.particleNumber,))
energia = energia.astype(np.float32)
energia_gpu = cuda.mem_alloc(energia.nbytes)
cuda.memcpy_htod(energia_gpu,energia)

get_energy(px_gpu,py_gpu,energia_gpu, block=(stale.particleNumber,1,1))
cuda.memcpy_dtoh(energia,energia_gpu)

energija = []
temperatura = []

###########
########### The main loop
###########
for i in range(stale.steps):
    if (i%int(stale.steps/1000) == 0): # Shows the progress
        procent =(100.0*i/stale.steps)
        sys.stdout.write("\r")
        sys.stdout.write("Processing: %.1f" % procent)
        sys.stdout.flush()
    # Update of the forces
    fupdate(rx_gpu,ry_gpu,fx_gpu,fy_gpu, block=(stale.particleNumber,1,1))
    # Calculate temporary energy for particles
    polKroku(v_gpu,px_gpu,py_gpu,fx_gpu,fy_gpu, block=(stale.particleNumber,1,1))
    cuda.memcpy_dtoh(v,v_gpu)
    # Use energies and calculate tau parameter
    tau = v.sum()/stale.particleNumber
    eta = np.array(sqrt(stale.temp/tau)).astype(np.float32)
    # LEAPFROG step
    leapfrog(px_gpu,py_gpu,rx_gpu,ry_gpu,fx_gpu,fy_gpu,eta, block=(stale.particleNumber,1,1))
    # Update the neighbor list
    if (i%1000 == 0):
        cuda.memcpy_dtoh(rx,rx_gpu)
        cuda.memcpy_dtoh(ry,ry_gpu)
        repopulate(rx_gpu,ry_gpu,nl_gpu,np.array(stale.rn).astype(np.float32),
        block=(stale.particleNumber,1,1))
    # Every 4000 step get data from GPU memory and plot it
    if (i%4000 == 0):
        cuda.memcpy_dtoh(rx,rx_gpu)
        cuda.memcpy_dtoh(ry,ry_gpu)
        rysowanie(i,rx,ry)



plt.plot(temperatura)

elapsed = (time.clock() - start)
print stale.particleNumber,elapsed

plt.show()
