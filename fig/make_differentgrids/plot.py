#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import pyutils.latexify as lt
import json
# Get default style for paper
import sys; sys.path.insert(0, '..')
import style

# Layout parameters with width=1
w1 = 0.24 # width of state boxes
h1 = 0.135 # height of state boxes
w2 = 0.13 # width of zoom box
h3 = 0.05 # height of arrow box
ws0 = 0.09 # horizontal space left of state boxes
ws1 = 0.02 # horizontal space between state boxes
ws2 = 0.03 # horizontal space left of zoom box
hs1 = 0.02 # vertical space between state boxes
hs3 = 0.0 # vertical space above arrow box

zoom_region = [0.595, -0.01, 0.04, 0.08]
cs1 = 'lightgrey' # hydrophobic
cs2 = 'k'         # hydrophilic
cz1 = style.c1
cz2 = style.c2


def load_data(data_file):
    with open(data_file) as f:
        data = json.load(f)
    x11 = np.reshape(data['state11'], [200,201])[:,1:]
    x12 = np.reshape(data['state12'], [400,401])[:,1:]
    x21 = np.reshape(data['state21'], [200,201])[:,1:]
    x22 = np.reshape(data['state22'], [400,401])[:,1:]
    x31 = np.reshape(data['state31'], [200,201])[:,1:]
    x32 = np.reshape(data['state32'], [400,401])[:,1:]
    ts = np.reshape(data['ts'], [400,401])[:,1:]
    return x11, x12, x21, x22, x31, x32, ts


def fig_layout():
    # Parameters
    h2 = w1 * zoom_region[3] / zoom_region[2]
    w3 = 3*w1 + 2*ws1
    h = 2*h1 + h3 + hs1 + hs3
    xa = ws0
    xb = xa + w1 + ws1
    xc = xb + w1 + ws1
    xd = 0.999 - w2
    ya = (h3 + hs3) / h
    yb = 0.999 - h1/h
    yc = ya + 0.5*(1 - ya - h2/h)
    # Axes
    fig = lt.figure(1, h)
    fig.text(0,  1, '(b)', ha='left', va='top')
    ax11 = fig.add_axes([xa, yb, w1, h1/h])
    ax12 = fig.add_axes([xa, ya, w1, h1/h])
    ax13 = fig.add_axes([xb, yb, w1, h1/h])
    ax14 = fig.add_axes([xb, ya, w1, h1/h])
    ax15 = fig.add_axes([xc, yb, w1, h1/h])
    ax16 = fig.add_axes([xc, ya, w1, h1/h])
    ax2 = fig.add_axes([xd, yc, w2, h2/h])
    ax3 = fig.add_axes([xa, 0, w3, h3/h])
    axes = [ax11, ax12, ax13, ax14, ax15, ax16, ax2, ax3]
    for ax in axes[:-1]:
        ax.set_xticks([])
        ax.set_yticks([])
    ax3.axis('off')
    # Zoom indicator
    ind_lw = 0.8
    ax15_trans = fig.add_axes([xc, yb, w1, h1/h], sharex=ax15, sharey=ax15, fc='none')
    params = {'bounds':zoom_region, 'inset_ax':ax2, 'alpha':1, 'lw':ind_lw, 'zorder':99}
    _, conn1 = ax15_trans.indicate_inset(**params, edgecolor=cz1)
    _, conn2 = ax16.indicate_inset(**params, edgecolor=cz2)
    [line.set(lw=ind_lw) for line in conn1]
    [line.set(lw=ind_lw) for line in conn2]
    # State labels
    fig.text(xa, yb+h1/h/2, 'State 1', rotation='vertical', ha='right', va='center')
    fig.text(xa, ya+h1/h/2, 'State 2', rotation='vertical', ha='right', va='center')
    # Arrow
    ax3.set_aspect('equal')
    ax3.arrow(0, 0, 1, 0, width=0.015, color='k')
    # fig.text(xa+0.5*w3,  0, 'BITSS trajectory', ha='center', va='bottom')
    return fig, axes


def plot_state(ax, state):
    # Plot fluid
    dx = 1 / state.shape[0]
    ax.contourf(np.arange(dx/2, 1, dx), np.arange(dx/2, 1, dx), state.T, cmap='Blues', levels=5)
    # Plot surface
    ymin = 0.5 - h1/w1
    y0 = -ymin / (0.5 - ymin)
    ax.axvspan(0, 1, ymax=y0, fc=cs1)
    ax.axvspan(0.125, 0.375, ymax=y0, fc=cs2)
    ax.axvspan(0.625, 0.875, ymax=y0, fc=cs2)
    # Show grid
    for i in np.arange(0, 1, 50*dx):
        ax.plot([i, i], [0, 1], 'k-', lw=0.5, alpha=0.5, zorder=1)
    for i in np.arange(0, 1, 50*dx):
        ax.plot([0, 1], [i, i], 'k-', lw=0.5, alpha=0.5, zorder=1)
    # Axes limits
    ax.set_xlim(0, 1)
    ax.set_ylim(ymin, 0.5)


def plot_zoom(ax, state1, state2, ts):
    lw = 1
    x1 = np.arange(0.5/state1.shape[0], 1, 1/state1.shape[0])
    x2 = np.arange(0.5/state2.shape[0], 1, 1/state2.shape[0])
    # Plot interfaces of ts estimate and actual ts
    state2_inter = state2.reshape([200,2,200,2]).mean(axis=(1,3))
    ts_estimate = (state1 + state2_inter) / 2
    ax.contour(x1, x1, ts_estimate.T, colors='k', levels=[0], linewidths=lw)
    ax.contour(x2, x2, ts.T, colors='k', linestyles='--', levels=[0], linewidths=lw)
    # Plot interfaces of final states
    ax.contour(x1, x1, state1.T, colors=cz1, levels=[0], linewidths=lw)
    ax.contour(x2, x2, state2.T, colors=cz2, levels=[0], linewidths=lw)
    # Plot surface
    y0 = -zoom_region[1] / zoom_region[3]
    ax.axvspan(0, 1, ymax=y0, color=cs1)
    ax.axvspan(0.125, 0.375, ymax=y0, color=cs2)
    ax.axvspan(0.625, 0.875, ymax=y0, color=cs2)
    ax.axhline(0, c='k', lw=0.5, zorder=1)
    # Axes limits
    ax.set_aspect('equal')
    ax.set_xlim([zoom_region[0], zoom_region[0] + zoom_region[2]])
    ax.set_ylim([zoom_region[1], zoom_region[1] + zoom_region[3]])


def main():
    x11, x12, x21, x22, x31, x32, ts = load_data('data.json')

    fig, axes = fig_layout()
    plot_state(axes[0], x11)
    plot_state(axes[1], x12)
    plot_state(axes[2], x21)
    plot_state(axes[3], x22)
    plot_state(axes[4], x31)
    plot_state(axes[5], x32)
    plot_zoom(axes[6], x31, x32, ts)

    lt.savefig('../differentgrids.pdf')


if (__name__ == '__main__'):
    main()
