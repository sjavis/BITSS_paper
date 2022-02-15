#!/usr/bin/env python3
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import networkx as nx
from pele.utils.disconnectivity_graph import DisconnectivityGraph

import pyutils.latexify as lt
# Get default style for paper
import sys; sys.path.insert(0, '..')
import style

c1 = style.c1
c2 = 'k'

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


def load_data(potential):
    # minima
    minima = pd.read_csv(f'{potential}-min.data')
    min_e = np.array(minima['energy'])
    min_x = minima[[f'x{i}' for i in range(ndof)]].to_numpy()
    nodes = [Node(i, min_e[i], min_x[i]) for i in range(len(minima))]
    # TS
    e_ts = np.loadtxt(f'{potential}-ts.data', usecols=0)
    pairs = np.loadtxt(f'{potential}-ts.data', usecols=[3,4], dtype=int) - 1
    ts = [TS(nodes[pair[0]], nodes[pair[1]], e_ts[i]) for i, pair in enumerate(pairs)]
    return nodes, ts


def make_dgraph(nodes, ts):
    # Generate disconnectivity graph
    g = nx.Graph()
    g.add_nodes_from(nodes)
    for t in ts:
        g.add_edge(t.minimum1, t.minimum2, ts=t)
    dg = DisconnectivityGraph(g, Emax=-10.5, order_by_value=lambda m: -m.i)
    dg.calculate()
    return dg


def plot_clusters(dg, nodes):
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

    ax = plt.gca()
    ybot, ytop = ax.get_ylim()
    dy = (ytop - ybot) / 4
    xpos, nodes = dg.get_minima_layout()
    ypos = [n.energy for n in nodes]
    for i in range(len(xpos)):
        tmp_ax = ax.inset_axes([xpos[i]-0.5, ypos[i]-dy, 1, dy], transform=ax.transData)
        plot_cluster(nodes[i].x, tmp_ax)
    ax.set_xlim(np.min(xpos)-0.5, np.max(xpos)+0.5)


def offset_graph(dg, offset):
    def recursive_offset(tree):
        tree.data['x'] += offset
        for subtree in tree.get_branches():
            recursive_offset(subtree)
    recursive_offset(dg.tree_graph)


def main():
    nodes1, ts1 = load_data('lj')
    nodes2, ts2 = load_data('discont')
    dg1 = make_dgraph(nodes1, ts1)
    dg2 = make_dgraph(nodes2, ts2)
    offset_graph(dg1, -0.03)
    offset_graph(dg2, 0.03)
    dg1.color_by_group([[0,1,2,3]], [c1])
    dg2.color_by_group([[0,1,2,3]], [c2])

    w = 0.4
    h = 0.8
    x0 = 0.2
    w1 = 1 - 0.1/w
    h1 = 0.9

    # Plot
    fig = lt.figure(w, h)
    ax = fig.add_axes([0.99-w1, (1-h1)/2, w1, h1])
    dg1.plot(axes=ax, linewidth=1)
    dg2.plot(axes=ax, linewidth=1)
    plot_clusters(dg1, nodes1)
    ax.legend([Line2D([0],[0],c=c1,lw=1), Line2D([0],[0],c=c2,lw=1)], ['Lennard-Jones', 'Discontinuous'], loc='lower left')
    ax.set_ylabel(r'Energy / $\epsilon$')
    ax.set_ylim(-13, -10.5)

    # plt.tight_layout()
    lt.savefig('../clusterdgraphs.pdf')


if (__name__ == "__main__"):
    main()
