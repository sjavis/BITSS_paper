#!/usr/bin/env python3
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.image as mim
from pyutils import latexify as lt
# Get default style for SI
import sys; sys.path.insert(0, '..')
import style

c1 = style.c3
c2 = style.c2

h1 = 0.3
h2 = 0.15
arc_angle = 135

def energy(x, y):
    def arc_dist(x, y, direction):
        x0 = np.sin(arc_angle/360*np.pi)
        y0 = np.cos(arc_angle/360*np.pi)
        xp = x + direction*x0
        yp = y + direction*y0
        s = np.abs(x0)
        r = (xp**2 + yp**2)**0.5
        theta = np.arctan2(xp, yp*direction)
        d2ring = (r - 1)**2
        d2tips = ((np.abs(xp) - s)**2 + y**2)
        d2 = np.where(np.abs(theta)<arc_angle*np.pi/360, d2ring, d2tips)
        return d2
    def barrier(x, direction, h):
        x0 = np.sin(arc_angle/360*np.pi)
        xp = x - direction*x0
        e = h * ((xp/x0)**2 - 1)**2
        return e
    e1 = arc_dist(x, y, +1)
    e2 = arc_dist(x, y, -1)
    e = np.where(e1<e2, e1, e2)
    barrier1 = barrier(x, -1, h1)
    barrier2 = barrier(x, +1, h2)
    e = e + np.where(x<0, barrier1, barrier2)
    return e

def plot_potential(ax):
    xlim=[-2.3, 2.3]
    ylim=[-1.1, 1.1]
    # Generate potential.png
    x, y = np.mgrid[xlim[0]:xlim[1]:100j, ylim[0]:ylim[1]:100j]
    e = energy(x, y)
    fig_tmp = plt.figure(figsize=(xlim[1]-xlim[0], ylim[1]-ylim[0]))
    ax_tmp = fig_tmp.add_axes([0,0,1,1])
    ax_tmp.contourf(x, y, e, cmap='Greys_r', levels=np.linspace(np.min(e),np.percentile(e,70),20))
    ax_tmp.axis('off')
    fig_tmp.savefig('potential.png')
    plt.close(fig_tmp)
    # Show png
    img = mim.imread('potential.png')
    ax.imshow(img, extent=(xlim[0],xlim[1],ylim[0],ylim[1]))

    xts = np.sin(arc_angle/360*np.pi)
    yts = 1 - np.cos(arc_angle/360*np.pi)
    ts = np.array([[-xts, yts], [xts, -yts]])
    mn = np.array([[-2*xts, 0], [2*xts,0]])
    ax.plot(mn[:,0], mn[:,1], ls='none', marker='o', c=c1, mec='k')
    ax.plot(ts[:,0], ts[:,1], ls='none', marker='o', c=c2, mec='k')
    ax.annotate('A', ts[0], xytext=(-xts,yts-0.2), ha='center', va='center')
    ax.annotate('B', ts[1], xytext=(xts,-yts+0.2), ha='center', va='center')
    ax.annotate('M1', mn[0], xytext=mn[0]-np.array([0,0.2]), ha='center', va='center', color='w')
    ax.annotate('M2', mn[1], xytext=mn[1]-np.array([0,0.2]), ha='center', va='center', color='w')

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect('equal')

def get_data():
    data = np.loadtxt('results.txt', skiprows=1)
    ediff = (data[:,0] - data[:,1]) / data[:,0]
    dstep = data[:,2]
    results = np.array(data[:,3], dtype=int)
    return dstep, ediff, results

def plot_results(ax, dstep, ediff, results):
    success = (results == 1)
    failure = (results == 2)
    ax.plot(dstep[success], ediff[success], ls='none', marker='s', c=c1, ms=5, label='Only A')
    ax.plot(dstep[failure], ediff[failure], ls='none', marker='s', c=c2, ms=5, label='A \& B')
    ax.legend(loc='upper left', framealpha=1)
    ax.set_xlabel('$f$')
    ax.set_ylabel('$(E_A - E_B)/E_A$')
    ax.semilogy()
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1, symbol='%'))

fig = lt.figure(1, 0.3)
fig.text(0.01, 0.98, '(a)', ha='left', va='top')
fig.text(0.5, 0.98, '(b)', ha='left', va='top')
axa = fig.add_axes((0.02, 0.05, 0.46, 0.9))
axb = fig.add_axes((0.6, 0.15, 0.38, 0.8))

dstep, ediff, results = get_data()
plot_potential(axa)
plot_results(axb, dstep, ediff, results)
lt.savefig(f'../multits.pdf')
