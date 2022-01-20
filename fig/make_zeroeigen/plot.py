#!/usr/bin/env python3
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.image as mim
import pandas as pd
import pyutils.latexify as lt
from mpl_toolkits.axes_grid1.inset_locator import mark_inset

lt.update_width(246) # Double column: 510 pt, single column: 246 pt

### Plot parameters
aspect = 0.5
ax_size = [[0.15, 0.2, 0.83, 0.78],
           [0.42, 0.25, 0.48, 0.38]]
# axin_size = [0.05, 0.53, 0.2, 0.4]
axin_bounds = np.array([[0.675, 0.8], [-2,-1.45]])
axin_scale = 50

y0 = 0.3
dx = 2.5
dy = dx * ax_size[1][3] / ax_size[1][2] * aspect

cmin = 'r'
cpath = 'b'
cts = 'm'
ms = 4
lw = 1.2


### Potential parameters
cut1 = -0.5
cut2 = 0.3
w = 0.5
peaks = [[-3., -1.414, 0., 1., 1.],
         [-2., 1.414, 0., 1., 1.],
         [-1., 0.07, 1.06, 1., 1.]]


def energy(x, y):
    def adjust_x(x):
        x = np.array(x)
        reg1 = x < (cut1-w)
        reg2 = np.logical_and(x>(cut1-w), x<cut1)
        reg3 = x > (cut2+w)
        reg4 = np.logical_and(x<(cut2+w), x>cut2)
        xp = x.copy()
        xp[reg1] = x[reg1] + w
        xp[reg2] = cut1
        xp[reg3] = x[reg3] - w
        xp[reg4] = cut2
        return xp
    xp = adjust_x(x)
    e = np.zeros_like(x)
    for peak in peaks:
        e += peak[0] * np.exp( -((xp-peak[1])/peak[3])**2 - ((y-peak[2])/peak[4])**2 )
    return e


### Make potential
def make_potential():
    xlim = (-dx, dx)
    ylim = (y0-dy, y0+dy)
    x, y = np.mgrid[xlim[0]:xlim[1]:100j, ylim[0]:ylim[1]:100j]
    e = energy(x, y)

    fig = plt.figure(frameon=False, figsize=(xlim[1]-xlim[0], ylim[1]-ylim[0]))
    ax = fig.add_axes([0,0,1,1])
    plt.contourf(x, y, e, cmap='Greys_r', levels=10)
    ax.axis('off')
    plt.savefig(f'potential.png', dpi=500)


### Read data
def read_data():
    data = pd.read_csv('path.csv')
    path = np.reshape([np.array(data['path1']),
                       np.array(data['path2'])], (2,-1,2))
    return path


### Make axes
def make_axes():
    fig = lt.figure(1, aspect)
    fig.text(0, 1, '(a)', ha='left', va='top')
    ax1 = fig.add_axes(ax_size[0])
    ax1.set_ylabel('Energy')
    ax1.set_xlabel('Normalised pathlength')
    ax2 = fig.add_axes(ax_size[1])
    ax2.set_xticks([])
    ax2.set_yticks([])
    # ax2.set_aspect('equal')
    return fig, ax1, ax2


def plot_path_energy(ax, path):
    path = np.concatenate((path[0], path[1,::-1]))
    e = energy(path[:,0], path[:,1])
    dist = np.cumsum(np.linalg.norm(np.diff(path, axis=0, prepend=0), axis=1))
    dist = dist / np.max(dist)
    ax.plot(dist, e, c=cpath, lw=lw)
    ax.plot(dist[0] , e[0] , c=cmin, marker='o', ms=ms)
    ax.plot(dist[-1] , e[-1] , c=cmin, marker='o', ms=ms)
    ax.plot(dist[np.argmax(e)], np.max(e), c=cts , marker='o', ms=ms)

    # dcenter = dist - dist[np.argmax(e)]
    # in_ins = np.logical_and(dcenter>-0.045, dcenter<0.06)
    # axin = ax.inset_axes(axin_size)
    # axin.plot(dist[in_ins], e[in_ins], c=cpath, lw=lw)
    in_ins = np.logical_and(dist>axin_bounds[0,0], dist<axin_bounds[0,1])
    axin_ycenter = (np.max(e[in_ins]) + np.min(e[in_ins])) / 2
    axin_ylim = axin_ycenter + np.array([-1, 1]) * 0.5*(axin_bounds[1,1]-axin_bounds[1,0]) / axin_scale
    axin_size = [axin_bounds[0,0], axin_bounds[1,0],
                 axin_bounds[0,1]-axin_bounds[0,0], axin_bounds[1,1]-axin_bounds[1,0]]

    axin = ax.inset_axes(axin_size, transform=ax.transData)
    axin.plot(dist, e, c=cpath, lw=lw)
    axin.plot(dist[np.argmax(e)], np.max(e), c=cts , marker='o', ms=ms)
    axin.set_xlim(axin_bounds[0])
    axin.set_ylim(axin_ylim)
    axin.set_xticks([])
    axin.set_yticks([])
    axin.margins(0, 0.2)
    axin.text(0.98, 0.95, f'$\\times{axin_scale}$',
              ha='right', va='top', transform=axin.transAxes)
    box, _ = ax.indicate_inset_zoom(axin, edgecolor='k')#, alpha=1)
    box.set_visible(False)

    ax.text(0.54, -1.83, 'i', ha='center')
    ax.text(0.91, -1.95, 'iii', ha='center')
    axin.text(0.75, 0, 'ii', ha='center', va='bottom', transform=axin.transAxes)


def plot_potential(ax):
    img = mim.imread('potential.png')
    ax.imshow(img, extent=(-dx, dx, y0-dy, y0+dy))
    ax.axvline(cut1-w, ls=':', c='k')
    ax.axvline(cut1, ls=':', c='k')
    ax.axvline(cut2, ls=':', c='k')
    ax.axvline(cut2+w, ls=':', c='k')
    ax.text(0.35, 0.29, 'i', ha='center', va='center', transform=ax.transAxes)
    ax.text(0.62, 0.55, 'ii', ha='center', va='center', transform=ax.transAxes)
    ax.text(0.78, 0.22, 'iii', ha='center', va='center', transform=ax.transAxes)


def plot_path(ax, path):
    x1 = path[0]
    x2 = path[1]
    ax.plot(x1[:,0] , x1[:,1] , c=cpath, lw=lw)
    ax.plot(x2[:,0] , x2[:,1] , c=cpath, lw=lw)
    ax.plot(x1[0,0] , x1[0,1] , c=cmin, marker='o', ms=ms)
    ax.plot(x2[0,0] , x2[0,1] , c=cmin, marker='o', ms=ms)
    ax.plot(x1[-1,0], x1[-1,1], c=cts , marker='o', ms=ms)
    ax.plot(x2[-1,0], x2[-1,1], c=cts , marker='o', ms=ms)


def main():
    make_potential()
    path = read_data()

    fig, ax1, ax2 = make_axes()
    plot_path_energy(ax1, path)
    plot_potential(ax2)
    plot_path(ax2, path)

    lt.savefig('../zeroeigen')


if (__name__ == '__main__'):
    main()
