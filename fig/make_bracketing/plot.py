#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mim
import json
import os
import pyutils.latexify as lt
# Get default style for paper
import sys; sys.path.insert(0, '..')
import style

# Data generated using energyLandscapes/bits_test/hook_potential/view.py

### Plot parameters
ar = 0.6
xlim = [-2.1, 1.8]
ylim = [-1.75, 1.75]

cpath = style.colors[::-1]
cts = 'w'#style.c2
cmin = 'w'#style.c3
cmap = 'Greys_r'
mec = 'k'
ms = 6

def make_potential():
    x, y = np.mgrid[xlim[0]:xlim[1]:100j, ylim[0]:ylim[1]:100j]

    peaks = [[ -1.,  0.,  0., 3.162, 3.162],
             [  1.,  0.,  0.,    1.,    1.],
             [  5.,  2.,  0.,    1., .3162],
             [ -1.,  1.,  1., .3162, .3162],
             [ -1.,  1., -1., .3162, .3162],
             [0.01,  0.,  0.,    1.,    1.],
             [ 0.5, -2.,  0.,    1.,    1.]]

    e = np.zeros_like(x)
    for peak in peaks:
        e += peak[0] * np.exp( -((x-peak[1])/peak[3])**2 - ((y-peak[2])/peak[4])**2 )

    fig = plt.figure(frameon=False, figsize=(xlim[1]-xlim[0], ylim[1]-ylim[0]))
    ax = fig.add_axes([0,0,1,1])
    levels = np.arange(-1.5, 1.5, 0.25)
    plt.contourf(x, y, e, cmap=cmap, levels=levels, extend='both')
    ax.axis('off')
    plt.savefig(f'potential.png')
    plt.close()


def load_data():
    with open('data.json', 'r') as f:
        d = json.load(f)
    bits = np.array(d['bits'])
    dhs = np.array(d['dhs'])
    ss = np.array(d['ss'])
    mep = np.array(d['mep'])
    return bits, dhs, ss, mep

def plot(minima, ts, paths, mep):
    fig = lt.figure(1, ar)
    ax = fig.add_axes([0,0,1,1])
    # Plot potential
    img = mim.imread('potential.png')
    plt.imshow(img, extent=(xlim[0],xlim[1],ylim[0],ylim[1]), aspect=ar*(xlim[1]-xlim[0])/(ylim[1]-ylim[0]))
    # Plot minima and TS
    plt.plot(minima[:,0], minima[:,1], c=cmin, marker='o', mec=mec, ms=ms, ls='none', zorder=99)
    plt.plot(ts[0], ts[1], c=cts, marker='o', mec=mec, ms=ms, ls='none', zorder=99)
    # Plot path
    labels = ['BITSS', 'Step \& Slide', 'DHS']
    for i, path in enumerate(paths):
        plt.plot(path[0,:,0], path[0,:,1], c=cpath[i], zorder=2, label=labels[i])
        plt.plot(path[1,:,0], path[1,:,1], c=cpath[i], zorder=2)
    # Plot MEP
    plt.plot(mep[:,0], mep[:,1], c='k', ls='--', zorder=1)
    plt.legend(loc='upper left')
    plt.xticks([])
    plt.yticks([])
    # plt.tight_layout()
    lt.savefig('../bracketing.pdf')

def main():
    make_potential()

    bits, dhs, ss, mep = load_data()
    minima = bits[:,0]
    ts = np.mean(bits[:,-1], axis=0)

    plot(minima, ts, [bits, ss, dhs], mep)

if (__name__ == "__main__"):
    main()
