#!/usr/bin/env python3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mim
import pyutils.latexify as lt
# Get default style for paper
import sys; sys.path.insert(0, '..')
import style
lt.update_width('aip-single')

def str_converter(instr):
    return np.fromstring(instr[1:-1],sep=' ')

w = 4/5
hi = [1/3, 1/3, 1/5] # height of axes relative to width
hd = 0
h = np.sum(hi) + 2*hd
fig = lt.figure(w, h)

for isub, subfig in enumerate(['a', 'b', 'c']):

    # Axes
    y0 = 1 - np.sum(hi[:isub+1])/h
    xd0 = 0.055
    fig.text(0.01, y0+hi[isub]/h, f'({subfig})', va='top', ha='left')

    # Snapshots
    for i in range(3):
        x0 = i/3
        tmp_ax = plt.axes((x0, y0, 0.3, hi[isub]/h))
        img = mim.imread(f'{subfig}{i}.png')
        plt.imshow(img)
        tmp_ax.axis('off')
        # tmp_ax.set_zorder(ax1.get_zorder()-1)
        if (i==1):
            tmp_ax.text(0.25, 1, '*', va='top', ha='center', size='xx-large', transform=tmp_ax.transAxes)

lt.savefig(f'../testsystems.pdf')
