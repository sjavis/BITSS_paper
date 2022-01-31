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

def str_converter(instr):
    return np.fromstring(instr[1:-1],sep=' ')

for subfig in ['a', 'b', 'c']:

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
    width = 1/3
    h1 = 1/1.618 # height of lower axes relative to width
    h2 = 1/3 # height of upper axes relative to width
    h = h1 + h2
    fig = lt.figure(width, h)
    ax = plt.axes((0.19, 0.13, 0.78, h1/h-0.1))
    fig.text(0, 1, f'({subfig})', va='top', ha='left')

    if (subfig == 'a'):
        ax.annotate('BITSS', [0.1, 0.08], [0.2, 0.1], xycoords='axes fraction',
                    arrowprops={'arrowstyle':'-'}, bbox={'pad':0, 'fc':'none', 'ec':'none'})
        ax.annotate('String', [0.37, 0.35], [0.51, 0.48], xycoords='axes fraction',
                    arrowprops={'arrowstyle':'-'}, bbox={'pad':0, 'fc':'none', 'ec':'none'})
        ax.annotate('String', [0.4, 0.455], [0.51, 0.48], xycoords='axes fraction', alpha=0,
                    arrowprops={'arrowstyle':'-'}, bbox={'pad':0, 'fc':'none', 'ec':'none'})
        ax.annotate('String', [0.4, 0.595], [0.51, 0.48], xycoords='axes fraction', alpha=0,
                    arrowprops={'arrowstyle':'-'}, bbox={'pad':0, 'fc':'none', 'ec':'none'})

    # Plot lines
    for i, n in enumerate(string_n):
        plt.plot(string_calls[i], string_dist[i], lw=1, label=n, c=style.colors[i])
    # for i, n in enumerate(dneb_n):
    #    plt.plot(dneb_calls[i], dneb_dist[i], lw=1, label=n)
    plt.plot(bits_calls, bits_dist, c='k', lw=1.5)#, label='BITSS')

    plt.semilogy()
    plt.tick_params('both', which='minor')
    plt.xlabel('Gradient evalulations')
    plt.ylabel('Distance error', labelpad=-0.5)
    if (subfig == 'a'):
        plt.xlim(0, 1600)
        plt.ylim(bottom=1e-5)
    elif (subfig == 'b'):
        plt.xlim(0, 60000)
        plt.ylim(bottom=1e-4)
    elif (subfig == 'c'):
        plt.xlim(0, 50000)
        plt.ylim(bottom=1e-4)
        plt.legend(loc='best')
        plt.xticks([0,20000,40000])

    for i in range(3):
        tmp_ax = plt.axes((0.035+i*0.31, 1-0.31, 0.31, 0.31))
        img = mim.imread(f'{subfig}{i}.png')
        plt.imshow(img)
        tmp_ax.axis('off')
        tmp_ax.set_zorder(ax.get_zorder()-1)
    # plt.savefig(f'speedtest-dneb-{subfig}.png')
    lt.savefig(f'../speedtest-{subfig}.pdf', dpi=300)
