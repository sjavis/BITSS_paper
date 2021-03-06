#!/usr/bin/env python3
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mim
import networkx as nx
from pele.utils.disconnectivity_graph import DisconnectivityGraph

import pyutils.latexify as lt
# Get default style for paper
import sys; sys.path.insert(0, '..')
import style

# Flat data generated by energyLandscapes/bits_test/zeroeigen2d/view.py
# Discontinuous data from energyLandscapes/bits_test/discontinuous-lj7/network/dgraph/{min,ts}.data

def plot_flat(fig, hsize):
    ### Plot parameters
    ax_size = np.array([[0.15, 0.2, 0.83, 0.78],
                        [0.42, 0.25, 0.48, 0.38]])
    axin_bounds = np.array([[0.57, 0.725], [-2,-1.45]])
    axin_scale = 50

    y0 = 0.3
    dx = 2.5

    cpath = style.c1
    cmin = style.c2
    cts = style.c3
    ms = 5
    mec = 'k'
    lw = 1.2

    ax_size[:,1] = ax_size[:,1] * hsize[1] + hsize[0]
    ax_size[:,3] = ax_size[:,3] * hsize[1]
    dy = dx * ax_size[1,3] / ax_size[1,2]

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

    def make_potential():
        xlim = (-dx, dx)
        ylim = (y0-dy, y0+dy)
        x, y = np.mgrid[xlim[0]:xlim[1]:100j, ylim[0]:ylim[1]:100j]
        e = energy(x, y)

        fig = plt.figure(frameon=False, figsize=(xlim[1]-xlim[0], ylim[1]-ylim[0]))
        ax = fig.add_axes([0,0,1,1])
        plt.contourf(x, y, e, cmap='Greys_r', levels=10)
        ax.axis('off')
        plt.savefig(f'potential.png', dpi=600)
        plt.close(fig)

    def read_data():
        data = pd.read_csv('flat_path.csv')
        path = np.reshape([np.array(data['path1']),
                           np.array(data['path2'])], (2,-1,2))
        return path

    def make_axes():
        fig.text(0, hsize[0]+hsize[1], '(a)', ha='left', va='top')
        ax1 = fig.add_axes(ax_size[0])
        ax1.set_ylabel('Energy')
        ax1.set_xlabel('Normalised pathlength')
        ax2 = fig.add_axes(ax_size[1])
        ax2.set_xticks([])
        ax2.set_yticks([])
        # ax2.set_aspect('equal')
        return ax1, ax2

    def plot_path_energy(ax, path):
        path = np.concatenate((path[0], path[1,::-1]))
        e = energy(path[:,0], path[:,1])
        dist = np.cumsum(np.linalg.norm(np.diff(path, axis=0, prepend=[path[0]]), axis=1))
        dist = dist / np.max(dist)
        ax.plot(dist, e, c=cpath, lw=lw)
        ax.plot(dist[0] , e[0] , c=cmin, marker='o', ms=ms, mec=mec)
        ax.plot(dist[-1] , e[-1] , c=cmin, marker='o', ms=ms, mec=mec)
        ax.plot(dist[np.argmax(e)], np.max(e), c=cts , marker='o', ms=ms, mec=mec)

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
        axin.plot(dist[np.argmax(e)], np.max(e), c=cts , marker='o', ms=ms, mec=mec)
        axin.set_xlim(axin_bounds[0])
        axin.set_ylim(axin_ylim)
        axin.set_xticks([])
        axin.set_yticks([])
        axin.margins(0, 0.2)
        axin.text(0.98, 0.95, r'$\times\text{'+str(axin_scale)+r'}$',
                  ha='right', va='top', transform=axin.transAxes)
        box, _ = ax.indicate_inset_zoom(axin, edgecolor='k')#, alpha=1)
        box.set_visible(False)

        ax.text(0.4, -1.83, 'i', ha='center')
        ax.text(0.89, -1.95, 'iii', ha='center')
        axin.text(0.75, 0, 'ii', ha='center', va='bottom', transform=axin.transAxes)

    def plot_potential(ax):
        img = mim.imread('potential.png')
        ax.imshow(img, extent=(-dx, dx, y0-dy, y0+dy))
        ax.axvline(cut1-w, ls=':', c='k')
        ax.axvline(cut1, ls=':', c='k')
        ax.axvline(cut2, ls=':', c='k')
        ax.axvline(cut2+w, ls=':', c='k')
        ax.text(0.35, 0.29, 'i', ha='center', va='center', transform=ax.transAxes)
        ax.text(0.61, 0.55, 'ii', ha='center', va='center', transform=ax.transAxes)
        ax.text(0.78, 0.22, 'iii', ha='center', va='center', transform=ax.transAxes)

    def plot_path(ax, path):
        x1 = path[0]
        x2 = path[1]
        ax.plot(x1[:,0] , x1[:,1] , c=cpath, lw=lw)
        ax.plot(x2[:,0] , x2[:,1] , c=cpath, lw=lw)
        ax.plot(x1[0,0] , x1[0,1] , c=cmin, marker='o', ms=ms, mec=mec)
        ax.plot(x2[0,0] , x2[0,1] , c=cmin, marker='o', ms=ms, mec=mec)
        ax.plot(x1[-1,0], x1[-1,1], c=cts , marker='o', ms=ms, mec=mec)
        ax.plot(x2[-1,0], x2[-1,1], c=cts , marker='o', ms=ms, mec=mec)

    make_potential()
    path = read_data()
    ax1, ax2 = make_axes()
    plot_path_energy(ax1, path)
    plot_potential(ax2)
    plot_path(ax2, path)


def plot_discontinuous(fig, hsize):
    space1 = 0.1
    space2 = 0.2
    space2label = 0.03
    w1 = 0.3
    w2 = 0.4
    h1 = 0.9
    h2 = 0.7
    y2 = 0.2
    c1 = style.c1
    c2 = 'dimgrey'
    
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
        min_x = minima[[f'x{i}' for i in range(14)]].to_numpy()
        nodes = [Node(i, min_e[i], min_x[i]) for i in range(len(minima))]
        # TS
        e_ts = np.loadtxt(f'{potential}-ts.data', usecols=0)
        pairs = np.loadtxt(f'{potential}-ts.data', usecols=[3,4], dtype=int) - 1
        ts = [TS(nodes[pair[0]], nodes[pair[1]], e_ts[i]) for i, pair in enumerate(pairs)]
        return nodes, ts

    def make_axes():
        fig.text(0, hsize[0]+0.95*hsize[1], '(b)', ha='left', va='top')
        fig.text(w1+space1+space2label, hsize[0]+0.95*hsize[1], '(c)', ha='left', va='top')
        pot_ax = fig.add_axes([space1, hsize[0]+y2*hsize[1], w1, h2*hsize[1]])
        dg_ax = fig.add_axes([w1+space1+space2, hsize[0]+(1-h1)/2*hsize[1], w2, h1*hsize[1]])
        dg_ax.set_ylabel(r'Energy / $\epsilon$')
        dg_ax.set_ylim(-13, -10.5)
        return dg_ax, pot_ax
    
    def make_dgraph(nodes, ts):
        # Generate disconnectivity graph
        g = nx.Graph()
        g.add_nodes_from(nodes)
        for t in ts:
            g.add_edge(t.minimum1, t.minimum2, ts=t)
        dg = DisconnectivityGraph(g, Emax=-10.5, order_by_value=lambda m: -m.i)
        dg.calculate()
        return dg

    def offset_graph(dg, offset):
        def recursive_offset(tree):
            tree.data['x'] += offset
            for subtree in tree.get_branches():
                recursive_offset(subtree)
        recursive_offset(dg.tree_graph)
    
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
        ax.plot(x[x<=r0], y[x<=r0], c=c2)
        ax.plot(x[x>=r0], y[x>=r0], c=c1)
        ax.plot([r0,r0], [-1,0.9], ls='--', c=c1)
        ax.arrow(r0, 0.8, 0, arrow_len, ec='none', fc=c1, width=arrow_width, head_length=arrow_len, length_includes_head=True)
        ax.set_xlim(0.8, 2.6)
        ax.set_ylim(-1.3, 1.3)
        ax.set_xticks([1, 1.5, 2, 2.5])
        ax.set_xlabel(r'$r$ / $\sigma$', labelpad=xpad)
        ax.set_ylabel(r'$V(r)$ / $\epsilon$', labelpad=ypad)
        ax.minorticks_off()
    
    nodes1, ts1 = load_data('discont')
    nodes2, ts2 = load_data('lj')
    dg1 = make_dgraph(nodes1, ts1)
    dg2 = make_dgraph(nodes2, ts2)
    offset_graph(dg1, -0.04)
    offset_graph(dg2, 0.04)
    dg1.color_by_group([[0,1,2,3]], [c1])
    dg2.color_by_group([[0,1,2,3]], [c2])

    # Plot
    dg_ax, pot_ax = make_axes()
    dg2.plot(axes=dg_ax, linewidth=1)
    dg1.plot(axes=dg_ax, linewidth=1)
    dg_ax.tick_params(which='both', direction='in')

    # Plot clusters on dgraph
    ybot, ytop = dg_ax.get_ylim()
    dy = (ytop - ybot) / 4
    xpos, nodes = dg1.get_minima_layout()
    ypos = [n.energy for n in nodes]
    for i in range(len(xpos)):
        tmp_ax = dg_ax.inset_axes([xpos[i]-0.5, ypos[i]-dy, 1, dy], transform=dg_ax.transData)
        plot_cluster(nodes[i].x, tmp_ax)

    plot_potenial(pot_ax)


def main():
    h1 = 0.48
    h2 = 0.37
    h = h1 + h2

    fig = lt.figure(1, h)
    plot_flat(fig, [h2/h, h1/h])
    plot_discontinuous(fig, [0, h2/h])
    lt.savefig('../flatdiscontinuous.pdf')


if (__name__ == '__main__'):
    main()
