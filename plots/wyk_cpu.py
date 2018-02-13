#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib

a=[
(3,64.25),
(4,121.62),
(5,196.0),
(6,273.88),
(7,379.43),
(8,508.86),
(9,629.66),
(10,765.59),
(11,936.41),
(12,1118.29)
]

b = [
(3,86.17),
(4,194.32),
(5,353.97),
(6,616.37),
(7,986.72),
(8,1558.71)
]

font = {'size' : 22}

matplotlib.rc('font', **font)
matplotlib.rc('xtick', labelsize=16)
matplotlib.rc('ytick', labelsize=16)

n = [a[x][0]**2 for x in range(len(a))]
t = [a[x][1] for x in range(len(a))]

nb = [b[x][0]**2 for x in range(len(b))]
tb = [b[x][1] for x in range(len(b))]

plt.plot(nb,tb, color="r", linestyle="-", linewidth=2,label=u'Without neighbor list')
plt.plot(n,t, color="b", linestyle="-", linewidth=2,label=u'With neighbor list')
plt.xlabel(u"Particle number $n$")
plt.ylabel(u"Time $t[s]$")
plt.legend(loc=1,prop={'size':16})
fig = plt.gcf()
fig.set_size_inches(17,14)

plt.savefig('cpuBoth.png',dpi=100)
