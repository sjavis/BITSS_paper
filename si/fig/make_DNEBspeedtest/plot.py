#!/usr/bin/env python3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mim
import pyutils.latexify as lt
# Get default style for si
import sys; sys.path.insert(0, '..')
import style

def str_converter(instr):
    return np.fromstring(instr[1:-1],sep=' ')

y0 = 0.15
h1 = 0.62/3 # height of lower axes relative to width
h2 = 1/9 # height of upper axes relative to width
h = h1 + h2
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

    dneb_data = df[df['method']=='dneb']
    dneb_n = np.array(dneb_data['n'])
    dneb_calls = np.array(dneb_data['calls'])
    dneb_dist = np.array(dneb_data['distance'])


    ### Plot data
    x0 = isub / 3
    ax = plt.axes((x0+0.19/3, y0, 0.26, h1/h-y0+0.03))
    fig.text(x0, 1, f'({subfig})', va='top', ha='left')

    if (subfig == 'a'):
        ax.annotate('BITSS', [0.1, 0.08], [0.2, 0.1], xycoords='axes fraction',
                    arrowprops={'arrowstyle':'-'}, bbox={'pad':0, 'fc':'none', 'ec':'none'})
        ax.annotate('DNEB', [0.48, 0.29], [0.53, 0.53], xycoords='axes fraction',
                    arrowprops={'arrowstyle':'-'}, bbox={'pad':0, 'fc':'none', 'ec':'none'})
        ax.annotate('DNEB', [0.38, 0.42], [0.53, 0.53], xycoords='axes fraction', alpha=0,
                    arrowprops={'arrowstyle':'-'}, bbox={'pad':0, 'fc':'none', 'ec':'none'})
        ax.annotate('DNEB', [0.4, 0.7], [0.53, 0.53], xycoords='axes fraction', alpha=0,
                    arrowprops={'arrowstyle':'-'}, bbox={'pad':0, 'fc':'none', 'ec':'none'})

    # Plot lines
    for i, n in enumerate(dneb_n):
       plt.plot(dneb_calls[i], dneb_dist[i], lw=1, label=n, c=style.colors[i])
    plt.plot(bits_calls, bits_dist, c='k', lw=1.5)#, label='BITSS')

    # Axes
    plt.semilogy()
    plt.tick_params('both', which='minor')
    plt.xlabel('Gradient evalulations')
    plt.ylabel('Distance error / $d_0$', labelpad=-0.2)
    if (subfig == 'a'):
        plt.xlim(0, 1600)
        plt.ylim(bottom=1e-5)
    elif (subfig == 'b'):
        plt.xlim(0, 55000)
        plt.ylim(bottom=1e-4)
    elif (subfig == 'c'):
        plt.xlim(0, 50000)
        plt.ylim(bottom=1e-4)
        plt.legend(loc='best')
        plt.xticks([0,20000,40000])

    # Snapshots
    for i in range(3):
        tmp_ax = plt.axes((x0+(0.035+i*0.31)/3, 1-h2/h, 0.1, h2/h))
        img = mim.imread(f'{subfig}{i}.png')
        plt.imshow(img)
        tmp_ax.axis('off')
        tmp_ax.set_zorder(ax.get_zorder()-1)
        if (i==1):
            tmp_ax.text(0.25, 1, '*', va='top', ha='center', size='xx-large', transform=tmp_ax.transAxes)

lt.savefig(f'../DNEBspeedtest.pdf', dpi=300)
