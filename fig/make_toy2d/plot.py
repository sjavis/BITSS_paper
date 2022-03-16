#!/usr/bin/env python3
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.image as mim
import matplotlib.patheffects as mpe
import json
import pyutils.latexify as lt
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
# Get default style for paper
import sys; sys.path.insert(0, '..')
import style

# Data generated using energyLandscapes/bits_test/2peaks/view.py

### Plot parameters
dt = 0.06
de = 0.02
ar1 = 0.4
ar2 = 0.5
ldx = 0#.008

cbits = style.c1
cts = style.c2
cmin = style.c3
cenergy = style.c3
cdist = style.c2
cmap = 'Greys_r'
mec = 'k'
ms = 6
clw = 1
tau_len = 1.5


### Make potential
peaks = [[-3., -1.414, 0., 1., 1.],
         [-2., 1.414, 0., 1., 1.],
         [-1., 0.07, 1.06, 1., 1.]]
def energy(x, y):
    e = np.zeros_like(x)
    for peak in peaks:
        e += peak[0] * np.exp( -((x-peak[1])/peak[3])**2 - ((y-peak[2])/peak[4])**2 )
    return e
def gradient(x, y):
    x = np.array(x)
    y = np.array(y)
    g = np.zeros((x.size, 2))
    for peak in peaks:
        g[:,0] -= peak[0] * 2*(x-peak[1])/peak[3] * np.exp( -((x-peak[1])/peak[3])**2 - ((y-peak[2])/peak[4])**2 )
        g[:,1] -= peak[0] * 2*(y-peak[2])/peak[4] * np.exp( -((x-peak[1])/peak[3])**2 - ((y-peak[2])/peak[4])**2 )
    return g

dx = 2.25
y0 = 0.27
xlim = (-dx, dx)
ylim = (y0-dx*ar1, y0+dx*ar1)
x, y = np.mgrid[xlim[0]:xlim[1]:100j, ylim[0]:ylim[1]:100j]
e = energy(x, y)

fig = plt.figure(frameon=False, figsize=(xlim[1]-xlim[0], ylim[1]-ylim[0]))
ax = fig.add_axes([0,0,1,1])
plt.contourf(x, y, e, cmap=cmap, levels=10)
ax.axis('off')
plt.savefig(f'potential.png', dpi=500)


### Read data
with open('data.json', 'r') as f:
    d = json.load(f)
minima = np.array(d['min'])
ts = np.array(d['ts'])
bits = np.array(d['bits'])
path = np.array(d['path'])


#### Plot
w1 = 1 - dt - de
h1 = ar1 * w1
w2 = 0.5 - dt - de
h2 = ar2 * w2
htot = h1 + h2 + 3*de
y1 = h2 + 2*de
y2 = de

fig = lt.figure(1, htot)
plt.figtext(    ldx,         1-de, '(a)', va='top', ha='left')
plt.figtext(    ldx, (h2+de)/htot, '(b)', va='top', ha='left')
plt.figtext(0.5+ldx, (h2+de)/htot, '(c)', va='top', ha='left')

axa = plt.axes((dt, y1/htot, w1, h1/htot))
axb = plt.axes((dt, y2/htot, w2, h2/htot))
#axb = axa.inset_axes((dt, y2/htot, w2, h2/htot), transform=fig.transFigure)
axc = axa.inset_axes((0.5+dt, y2/htot, w2, h2/htot), transform=fig.transFigure)
axa.set_aspect('equal')
axb.set_aspect('equal')
axc.set_aspect('equal')
axa.set_xticks([])
axa.set_yticks([])
axb.set_xticks([])
axb.set_yticks([])
axc.set_xticks([])
axc.set_yticks([])
mark_inset(axa, axc, loc1=3, loc2=1)
# mark_inset(axa, axc, loc1=4, loc2=2)

# Potential
img = mim.imread('potential.png')
axa.imshow(img, extent=(xlim[0],xlim[1],ylim[0],ylim[1]))

# Minima & TS
axa.plot(minima[:,0], minima[:,1], c=cmin, marker='o', mec=mec, ms=ms, ls='none', zorder=99)
axa.plot(ts[0], ts[1], c=cts, marker='o', mec=mec, ms=ms, zorder=99)

# BITS
axa.plot(bits[:,0,0], bits[:,0,1], c=cbits, zorder=2)
axa.plot(bits[:,1,0], bits[:,1,1], c=cbits, zorder=2)

# Pathway
axa.plot(path[:,0], path[:,1], ls='--', c='k', zorder=1)


### Plot midway
i = 80
x1 = np.array([-0.22, 0.7])
x2 = np.array([0.4, 0.55])

dx = 0.55
center = (x1 + x2) / 2
center = [0.15, 0.67]
xlim = (center[0]-dx, center[0]+dx)
ylim = (center[1]-dx*ar2, center[1]+dx*ar2)
x, y = np.mgrid[xlim[0]:xlim[1]:100j, ylim[0]:ylim[1]:100j]
e = energy(x,y)

e0 = 0.5*np.min(e) + 0.5*np.max(e)
levels = np.delete(np.arange(np.min(e), np.max(e), (e0-np.min(e))/6), 6)
cnt = axb.contourf(x, y, e, cmap=cmap, levels=levels)
for c in cnt.collections:
    c.set_edgecolor('face')
# axb.contour(x, y, e, levels=levels, colors='k', linestyles='solid', linewidths=clw)
# axb.contour(x, y, e, levels=[e0], colors='k', linestyles='solid', linewidths=1.5*clw)

axb.plot(x1[0], x1[1], c=cbits, marker='o', mec=mec, ms=ms, zorder=99)
axb.plot(x2[0], x2[1], c=cbits, marker='o', mec=mec, ms=ms, zorder=99)
arrow_args = {'units':'xy', 'width':0.018, 'headwidth':4, 'headlength':4, 'headaxislength':3.5, 'scale':2, 'zorder':98}
g1 = gradient(x1[0], x1[1])
g2 = gradient(x2[0], x2[1])
ge_factor = 1.5
axb.quiver(x1[0], x1[1], ge_factor*g1[:,0], ge_factor*g1[:,1], color=cenergy, **arrow_args)
axb.quiver(x2[0], x2[1], -ge_factor*g2[:,0], -ge_factor*g2[:,1], color=cenergy, **arrow_args)
# axb.quiver(x1[0], x1[1], -g1[:,0], -g1[:,1], **arrow_args)
# axb.quiver(x2[0], x2[1], -g2[:,0], -g2[:,1], **arrow_args)

gd = (x2 - x1) * 0.65
axb.quiver(x1[0], x1[1], gd[0], gd[1], color=cdist, **arrow_args)
axb.quiver(x2[0], x2[1], -gd[0], -gd[1], color=cdist, **arrow_args)

# axb.text(0.03, 0.35, '$F_P$', transform=axb.transAxes).set_path_effects([mpe.withStroke(linewidth=2, foreground='w')])
axb.text(0.38, 0.7, r'$\bm{F}_E$', c=cenergy, transform=axb.transAxes)#.set_path_effects([mpe.withStroke(linewidth=2, foreground='w')])
axb.text(0.35, 0.5, r'$\bm{F}_D$', c=cdist, transform=axb.transAxes)#.set_path_effects([mpe.withStroke(linewidth=2, foreground='w')])

axb.text(x1[0], x1[1]-0.03, r'$\bm{x}_1$', va='top', ha='center')
axb.text(x2[0], x2[1]-0.03, r'$\bm{x}_2$', va='top', ha='center')


### Plot final
dx = 0.0045
xlim = (ts[0]-dx, ts[0]+dx)
ylim = (ts[1]-dx*ar2, ts[1]+dx*ar2)
x, y = np.mgrid[xlim[0]:xlim[1]:100j, ylim[0]:ylim[1]:100j]
# axc.contour(x, y, energy(x,y), colors='k', linestyles='solid', linewidths=clw)
cnt = axc.contourf(x, y, energy(x,y), cmap=cmap)
for c in cnt.collections:
    c.set_edgecolor('face')

i = -1
tau = np.array([tau_len*bits[i,0]-(tau_len-1)*bits[i,1], tau_len*bits[i,1]-(tau_len-1)*bits[i,0]])
axc.plot(tau[:,0], tau[:,1], ls=':', c='k')
axc.plot(bits[i,:,0], bits[i,:,1], c=cbits, marker='o', mec=mec, ms=ms, ls='none')
axc.plot(ts[0], ts[1], c=cts, marker='o', mec=mec, ms=ms)
        
axc.text(0.78, 0.4, r'$\bm{\hat\tau}$', transform=axc.transAxes)#.set_path_effects([mpe.withStroke(linewidth=2, foreground='w')])

#arrow_args = {'units':'xy', 'width':0.02, 'headlength':3, 'headaxislength':2.5, 'scale':3}
#g = gradient(bits[i,:,0], bits[i,:,1])
#plt.quiver(bits[i,:,0], bits[i,:,1], -g[:,0], -g[:,1], **arrow_args)
#gdm = np.linalg.norm(g[0] - g[1])/2
#gd = g / np.linalg.norm(g, axis=1) * gdm
#plt.quiver(bits[i,:,0], bits[i,:,1], gd[:,0], gd[:,1], **arrow_args)

# plt.show()
lt.savefig('../toy2d.pdf', dpi=400)
