#!/usr/bin/env python3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mim
import pyutils.latexify as lt
# Get default style for paper
import sys; sys.path.insert(0, '..')
import style
lt.update_width('r4-double')

# Data generated by energyLandscapes/bits_test/speed_test/{system}/view_convergence.py

def str_converter(instr):
    return np.fromstring(instr[1:-1],sep=' ')

hd11 = 0.045
hd12 = 0.01
hd2 = -0.01
h1 = 0.4/3 # height of lower axes relative to width
h2 = 1/9 # height of upper axes relative to width
h = hd11 + hd12 + hd2 + 2*h1 + h2
fig = lt.figure(1, h)

for isub, subfig in enumerate(['a', 'b', 'c']):

    ### Load data
    if (subfig == 'a'):
        file = 'lj_data'
    elif (subfig == 'b'):
        file = 'cb_data'
    elif (subfig == 'c'):
        file = 'sw_data'
    df = pd.read_csv(file, converters={'calls':str_converter, 'distance':str_converter})

    bits_data = df[df['method']=='bits']
    bits_calls = bits_data['calls'][0]
    bits_dist = bits_data['distance'][0]

    string_data = df[df['method']=='string']
    string_n = np.array(string_data['n'])
    string_calls = np.array(string_data['calls'])
    string_dist = np.array(string_data['distance'])

    dneb_data = df[df['method']=='dneb']
    dneb_n = np.array(dneb_data['n'])
    dneb_calls = np.array(dneb_data['calls'])
    dneb_dist = np.array(dneb_data['distance'])


    ### Plot data
    x0 = isub/3
    xd0 = 0.055
    w1 = 1/3-0.005 - xd0
    if (isub == 0):
        x0 = x0 + 0.01
        w1 = w1 - 0.01
    ax1 = plt.axes((x0+xd0, hd11/h, w1, h1/h))
    ax2 = plt.axes((x0+xd0, (hd11+h1+hd12)/h, w1, h1/h), sharex=ax1, sharey=ax1)
    fig.text(x0, 1, f'({subfig})', va='top', ha='left')

    # Plot lines
    for i, n in enumerate(string_n):
        ax1.plot(string_calls[i], string_dist[i], lw=1, label=n, c=style.colors[i])
    for i, n in enumerate(dneb_n):
        ax2.plot(dneb_calls[i], dneb_dist[i], lw=1, label=n, c=style.colors[i])
    ax1.plot(bits_calls, bits_dist, c='k', lw=1.5)#, label='BITSS')
    ax2.plot(bits_calls, bits_dist, c='k', lw=1.5)#, label='BITSS')

    # Axes
    ax1.semilogy()
    ax2.semilogy()
    ax1.set_xlabel('Gradient evalulations')
    if (subfig == 'a'):
        ax1.set_xlim(0, 1600)
        ax1.set_ylim(bottom=1e-5)
    elif (subfig == 'b'):
        ax1.set_xlim(0, 55000)
        ax1.set_ylim(bottom=1e-4)
    elif (subfig == 'c'):
        ax1.set_xlim(0, 50000)
        ax1.set_ylim(bottom=1e-4)
        ax1.set_xticks([0,20000,40000])
        ax1.legend(loc='best')
    ax1.minorticks_on()
    ax2.tick_params(labelbottom=False)

    if (subfig == 'a'):
        # Labels
        ax1.annotate('BITSS', [0.1, 0.08], [0.2, 0.1], xycoords='axes fraction',
                     arrowprops={'arrowstyle':'-'}, bbox={'pad':0, 'fc':'none', 'ec':'none'})
        ax1.annotate('String', [0.37, 0.35], [0.51, 0.48], xycoords='axes fraction',
                     arrowprops={'arrowstyle':'-'}, bbox={'pad':0, 'fc':'none', 'ec':'none'})
        ax1.annotate('String', [0.4, 0.455], [0.51, 0.48], xycoords='axes fraction', alpha=0,
                     arrowprops={'arrowstyle':'-'}, bbox={'pad':0, 'fc':'none', 'ec':'none'})
        ax1.annotate('String', [0.4, 0.595], [0.51, 0.48], xycoords='axes fraction', alpha=0,
                    arrowprops={'arrowstyle':'-'}, bbox={'pad':0, 'fc':'none', 'ec':'none'})
        ax2.annotate('BITSS', [0.1, 0.08], [0.2, 0.1], xycoords='axes fraction',
                     arrowprops={'arrowstyle':'-'}, bbox={'pad':0, 'fc':'none', 'ec':'none'})
        ax2.annotate('DNEB', [0.48, 0.29], [0.53, 0.53], xycoords='axes fraction',
                     arrowprops={'arrowstyle':'-'}, bbox={'pad':0, 'fc':'none', 'ec':'none'})
        ax2.annotate('DNEB', [0.38, 0.42], [0.53, 0.53], xycoords='axes fraction', alpha=0,
                     arrowprops={'arrowstyle':'-'}, bbox={'pad':0, 'fc':'none', 'ec':'none'})
        ax2.annotate('DNEB', [0.4, 0.7], [0.53, 0.53], xycoords='axes fraction', alpha=0,
                    arrowprops={'arrowstyle':'-'}, bbox={'pad':0, 'fc':'none', 'ec':'none'})
        # Big hidden axes for y label
        ax_tmp = plt.axes((x0+xd0, hd11/h, w1, (2*h1+hd12)/h), sharey=ax1, frameon=False)
        ax_tmp.tick_params(labelcolor='none', which='both', top=False, bottom=False, left=False, right=False)
        ax_tmp.set_ylabel('Distance error / $d_0$', labelpad=-0.1)

    # Snapshots
    for i in range(3):
        tmp_ax = plt.axes((x0+(0.035+i*0.31)/3, 1-h2/h, 0.1, h2/h))
        img = mim.imread(f'{subfig}{i}.png')
        plt.imshow(img)
        tmp_ax.axis('off')
        tmp_ax.set_zorder(ax1.get_zorder()-1)
        if (i==1):
            tmp_ax.text(0.25, 1, '*', va='top', ha='center', size='xx-large', transform=tmp_ax.transAxes)

lt.savefig(f'../speedtest.pdf', dpi=300)
