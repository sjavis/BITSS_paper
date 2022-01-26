#!/usr/bin/env python3
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.tri as mtri
import json
import pyutils.latexify as lt
# Get default style for paper
import sys; sys.path.insert(0, '..')
import style

# Figure parameters
ar = 0.5
w1 = 0.24
h1 = 0.9
w2 = 0.2
h2 = 0.4
w3 = 0.025
h3 = 0.65
h4 = 0.13
wspace1 = 0.02
wspace3 = 0.08
hspace4 = 0.04

region = [-30, 30, -30, 30]
indicator_region = [185, 455, 140, 140]

# Plot parameters
cmap = 'RdBu_r'
lw = 0.1
lalpha = 0.3


def set_region(tri, disp):
    def in_region(x, y):
        return (x>region[0]) & (x<region[1]) & (y>region[2]) & (y<region[3])
    node_mask = ~in_region(tri.x, tri.y)
    tri_mask = np.all(node_mask[tri.triangles], axis=1)
    tri.set_mask(tri_mask)
    # disp_mask = np.full(disp.shape, True)
    # disp_mask[:,tri.triangles[~tri_mask]] = False


def load_data(data_file):
    with open(data_file) as f:
        data = json.load(f)
    disp1 = data['d1']
    disp2 = data['d2']
    disp3 = data['d3']
    tri1 = mtri.Triangulation(data['x1'], data['y1'], data['t1'])
    tri2 = mtri.Triangulation(data['x2'], data['y2'], data['t2'])
    tri3 = mtri.Triangulation(data['x3'], data['y3'], data['t3'])
    set_region(tri1, disp1)
    set_region(tri2, disp2)
    set_region(tri3, disp3)
    return tri1, disp1, tri2, disp2, tri3, disp3


def create_axes():
    wspace2 = (1 - w1 - 3*w2 - w3 - wspace1 - wspace3) / 2
    hspace2 = (1 - h4 - 2*h2)
    hspace3 = (1 - h4 - h3) / 2
    xax1 = w1 + wspace1
    xax2 = xax1 + w2 + wspace2
    xax3 = xax2 + w2 + wspace2
    yax1 = 1 - h2
    yax2 = h4 + hspace4

    fig = lt.figure(1, ar)
    fig.text(0,  1, '(a)', ha='left', va='top')

    ax1   = fig.add_axes((   0,   (1-h1)/2,             w1, h1))
    ax211 = fig.add_axes((xax1, yax1, w2, h2))
    ax212 = fig.add_axes((xax1, yax2, w2, h2))
    ax221 = fig.add_axes((xax2, yax1, w2, h2))
    ax222 = fig.add_axes((xax2, yax2, w2, h2))
    ax231 = fig.add_axes((xax3, yax1, w2, h2))
    ax232 = fig.add_axes((xax3, yax2, w2, h2))
    ax3   = fig.add_axes((1-w3, yax2+hspace3, w3*0.95, h3))
    ax4   = fig.add_axes((xax1, hspace4, 3*w2+2*wspace2, h4))
    axes = [ax1, ax211, ax212, ax221, ax222, ax231, ax232, ax3, ax4]

    ax1.axis('off')
    ax4.axis('off')
    for ax in axes[1:7]:
        ax.set_xticks([])
        ax.set_yticks([])

    # Zoom indicator
    ax1.indicate_inset(bounds=indicator_region, inset_ax=ax211, ec='k')

    # State labels
    fig.text(xax1, yax1+h2/2, 'State 1', rotation='vertical', ha='right', va='center')
    fig.text(xax1, yax2+h2/2, 'State 2', rotation='vertical', ha='right', va='center')

    # Arrow
    ax4.set_aspect('equal')
    ax4.arrow(0, 0, 1, 0, width=0.015, color='k')
    fig.text(xax1+1.5*w2+wspace2,  0, 'BITSS trajectory', ha='center', va='bottom')
    return fig, axes


def plot_cylinder(ax):
    img = mpl.image.imread('cylinder.png')
    halfwidth = int(0.5 * img.shape[0] * ax.bbox.width / ax.bbox.height)
    center = int(img.shape[1] / 2) + 40
    ax.imshow(img[::-1,center-halfwidth:center+halfwidth+1], origin='lower')


def plot_region(ax, tri, disp, state=None, vmax=None):
    if (vmax is None): vmax = np.max(np.abs(disp))
    if (state is not None): disp = disp[state]
    cnt = ax.tricontourf(tri, disp, cmap=cmap, vmin=-vmax, vmax=vmax)
    ax.triplot(tri, 'k-', lw=lw, alpha=lalpha)
    ax.set_xlim(region[:2])
    ax.set_ylim(region[2:])

    for c in cnt.collections:
        c.set_edgecolor("face")


def plot_colorbar(ax, vmax):
    mpl.colorbar.ColorbarBase(ax, cmap=plt.get_cmap(cmap), norm=mpl.colors.Normalize(vmin=-vmax, vmax=vmax))
    ax.yaxis.set_ticks_position('left')


def main():
    tri1, disp1, tri2, disp2, tri3, disp3 = load_data('data.json')
    vmax = 0.4 * np.max([np.max(np.abs(d)) for d in [disp1, disp2, disp3]])

    fig, axes = create_axes()
    plot_cylinder(axes[0])
    plot_region(axes[1], tri1, disp1, 0, vmax)
    plot_region(axes[2], tri1, disp1, 1, vmax)
    plot_region(axes[3], tri2, disp2, 0, vmax)
    plot_region(axes[4], tri2, disp2, 1, vmax)
    plot_region(axes[5], tri3, disp3, 0, vmax)
    plot_region(axes[6], tri3, disp3, 1, vmax)
    plot_colorbar(axes[7], vmax)

    lt.savefig('../changingmesh', dpi=500)


if (__name__ == "__main__"):
    main()
