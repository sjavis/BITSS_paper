#!/usr/bin/env python3
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from pele.utils.disconnectivity_graph import DisconnectivityGraph

import pyutils.latexify as lt
# Get default style for paper
import sys; sys.path.insert(0, '..')
import style

ndof = 14

class Node:
    def __init__(self, i, e, x):
        self.i = i
        self.energy = e
        self.x = x
    def __hash__(self):
        return self.i
    def __str__(self):
        return 'Node '+str(self.i)
    def __eq__(self, other):
        return hash(self) == hash(other)
    def __lt__(self, other):
        return hash(self) < hash(other)

class TS:
    def __init__(self, min1, min2, e):
        self.minimum1 = min1
        self.minimum2 = min2
        self.energy = e
    def __hash__(self):
        return hash(self.minimum1) ^ hash(self.minimum2)
    def __str__(self):
        return 'TS '+str(self.i)
    def __eq__(self, other):
        return hash(self) == hash(other)
    def __lt__(self, other):
        return hash(self) < hash(other)


def load_data():
    # minima
    minima = pd.read_csv('min.data')
    min_e = np.array(minima['energy'])
    min_x = minima[[f'x{i}' for i in range(ndof)]].to_numpy()
    nodes = [Node(i, min_e[i], min_x[i]) for i in range(len(minima))]
    # TS
    e_ts = np.loadtxt('ts.data', usecols=0)
    pairs = np.loadtxt('ts.data', usecols=[3,4], dtype=int) - 1
    ts = [TS(nodes[pair[0]], nodes[pair[1]], e_ts[i]) for i, pair in enumerate(pairs)]
    return nodes, ts


def make_dgraph(nodes, ts):
    # Generate disconnectivity graph
    g = nx.Graph()
    g.add_nodes_from(nodes)
    for t in ts:
        g.add_edge(t.minimum1, t.minimum2, ts=t)
    dg = DisconnectivityGraph(g, Emax=-10.5)
    dg.calculate()
    return dg


def plot_cluster(x, ax):
    rad = 1.1225 / 2
    # ax.set_xlim(np.min(x[0::2])-rad*1.1, np.max(x[0::2])+rad*1.1)
    # ax.set_ylim(np.min(x[1::2])-rad*1.1, np.max(x[1::2])+rad*1.1)
    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-2.5, 2.5)
    ax.set_axis_off()
    ax.set_aspect('equal')
    for xy in np.reshape(x, (-1,2)):
        ax.add_patch(plt.Circle(xy, rad, fill=False))


def plot_potenial(ax):
    c = style.c1
    xpad = 0#-2
    ypad = 0
    arrow_len = 0.3
    arrow_width = 0.05
    def lj(r):
        return 4*(1/r**12 - 1/r**6)
    r0 = 2**(1/6)
    x = np.linspace(0.9, 2.5, 100)
    y = lj(x)
    ax.plot(x[x<=r0], y[x<=r0], c='grey')
    ax.plot(x[x>=r0], y[x>=r0], c=c)
    ax.plot([r0,r0], [-1,0.9], ls='--', c=c)
    ax.arrow(r0, 0.8, 0, arrow_len, ec='none', fc=c, width=arrow_width, head_length=arrow_len, length_includes_head=True)
    ax.set_xlim(0.8, 2.6)
    ax.set_ylim(-1.3, 1.3)
    ax.set_xticks([1, 1.5, 2, 2.5])
    ax.set_xlabel(r'$r$ / $\sigma$', labelpad=xpad)
    ax.set_ylabel(r'$V(r)$ / $\epsilon$', labelpad=ypad)
    ax.minorticks_off()


def main():
    nodes, ts = load_data()
    dg = make_dgraph(nodes, ts)

    space1 = 0.2
    space2 = 0.1
    w1 = 0.4
    w2 = 0.25
    h1 = 0.9
    h2 = 0.7
    y2 = 0.2

    # Plot
    fig = lt.figure(1, 0.4)#, facecolor='grey')
    ax = fig.add_axes([space1, (1-h1)/2, w1, h1])
    fig.text(0, 0.95, '(b)', ha='left', va='top')
    fig.text(w1+space1, 0.95, '(c)', ha='left', va='top')
    dg.plot(axes=ax, linewidth=1)
    ax.set_ylabel(r'Energy / $\epsilon$')
    ax.set_ylim(-13, -10.5)

    # Show minima
    ybot, ytop = ax.get_ylim()
    dy = (ytop - ybot) / 4
    xpos, nodes = dg.get_minima_layout()
    ypos = [n.energy for n in nodes]
    for i in range(len(xpos)):
        tmp_ax = ax.inset_axes([xpos[i]-0.5, ypos[i]-dy, 1, dy], transform=ax.transData)
        plot_cluster(nodes[i].x, tmp_ax)

    # Show potential
    # pot_ax = ax.inset_axes([0.17, 0.03, 0.3, 0.3])
    pot_ax = fig.add_axes([w1+space1+space2, y2, w2, h2])
    plot_potenial(pot_ax)

    # plt.tight_layout()
    lt.savefig('../discontinuous')
    # plt.show()


if (__name__ == "__main__"):
    main()
