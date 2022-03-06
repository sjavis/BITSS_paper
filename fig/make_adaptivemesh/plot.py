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

def plot_cb(fig, y0, htot):
    # Figure parameters
    w1 = 0.24
    h1 = 0.45
    w2 = 0.2
    h2 = 0.2
    w3 = 0.025
    h3 = 0.325
    h4 = 0.05
    wspace1 = 0.02
    wspace3 = 0.08
    hspace2 = 0.03
    hspace4 = 0.04
    zoom_region = [-30, 30, -30, 30]
    indicator_region = [185, 455, 140, 140]

    # Plot parameters
    cmap = 'RdBu_r'
    lw = 0.1
    lalpha = 0.3

    h = (1 - y0) * htot
    hspace1 = (h - h1) / 2
    hspace3 = (h - h4 - h3) / 2
    wspace2 = (1 - w1 - 3*w2 - w3 - wspace1 - wspace3) / 2

    def load_data(data_file):
        def set_region(tri, disp):
            def in_region(x, y):
                return (x>zoom_region[0]) & (x<zoom_region[1]) & (y>zoom_region[2]) & (y<zoom_region[3])
            node_mask = ~in_region(tri.x, tri.y)
            tri_mask = np.all(node_mask[tri.triangles], axis=1)
            tri.set_mask(tri_mask)
            # disp_mask = np.full(disp.shape, True)
            # disp_mask[:,tri.triangles[~tri_mask]] = False
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

    def create_axes(fig, y0):
        xax1 = w1 + wspace1
        xax2 = xax1 + w2 + wspace2
        xax3 = xax2 + w2 + wspace2
        yax1 = y0 + hspace1/htot
        yax21 = 1 - h2/htot
        yax22 = y0 + (h4 + hspace4) / htot
        yax3 = yax22 + hspace3/htot
        yax4 = y0 + hspace4/htot

        ax1   = fig.add_axes((0, yax1, w1, h1/htot))
        ax211 = fig.add_axes((xax1, yax21, w2, h2/htot))
        ax212 = fig.add_axes((xax1, yax22, w2, h2/htot))
        ax221 = fig.add_axes((xax2, yax21, w2, h2/htot))
        ax222 = fig.add_axes((xax2, yax22, w2, h2/htot))
        ax231 = fig.add_axes((xax3, yax21, w2, h2/htot))
        ax232 = fig.add_axes((xax3, yax22, w2, h2/htot))
        ax3   = fig.add_axes((1-w3, yax3, w3*0.95, h3/htot))
        ax4   = fig.add_axes((xax1, yax4, 3*w2+2*wspace2, h4/htot))
        axes = [ax1, ax211, ax212, ax221, ax222, ax231, ax232, ax3, ax4]

        ax1.axis('off')
        ax4.axis('off')
        for ax in axes[1:7]:
            ax.set_xticks([])
            ax.set_yticks([])

        # Zoom indicator
        ax1.indicate_inset(bounds=indicator_region, inset_ax=ax211, ec='k')

        # State labels
        fig.text(xax1, yax21+h2/2, 'State 1', rotation='vertical', ha='right', va='center')
        fig.text(xax1, yax22+h2/2, 'State 2', rotation='vertical', ha='right', va='center')

        # Arrow
        ax4.set_aspect('equal')
        ax4.arrow(0, 0, 1, 0, width=0.015, color='k')
        fig.text(xax1+1.5*w2+wspace2,  y0+0.4*hspace4/htot, 'BITSS trajectory', ha='center', va='bottom')
        return axes

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
        ax.set_xlim(zoom_region[:2])
        ax.set_ylim(zoom_region[2:])

        for c in cnt.collections:
            c.set_edgecolor("face")

    def plot_colorbar(ax, vmax):
        mpl.colorbar.ColorbarBase(ax, cmap=plt.get_cmap(cmap), norm=mpl.colors.Normalize(vmin=-vmax, vmax=vmax))
        ax.yaxis.set_ticks_position('left')

    tri1, disp1, tri2, disp2, tri3, disp3 = load_data('cb_data.json')
    vmax = 0.4 * np.max([np.max(np.abs(d)) for d in [disp1, disp2, disp3]])
    axes = create_axes(fig, y0)
    plot_cylinder(axes[0])
    plot_region(axes[1], tri1, disp1, 0, vmax)
    plot_region(axes[2], tri1, disp1, 1, vmax)
    plot_region(axes[3], tri2, disp2, 0, vmax)
    plot_region(axes[4], tri2, disp2, 1, vmax)
    plot_region(axes[5], tri3, disp3, 0, vmax)
    plot_region(axes[6], tri3, disp3, 1, vmax)
    plot_colorbar(axes[7], vmax)


def plot_sw(fig, y1, htot):
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

    def create_axes(fig, y1):
        # Parameters
        h2 = w1 * zoom_region[3] / zoom_region[2]
        w3 = 3*w1 + 2*ws1
        xa = ws0
        xb = xa + w1 + ws1
        xc = xb + w1 + ws1
        xd = 0.999 - w2
        ya = (h3 + hs3) / htot
        yb = y1 - h1/htot
        yc = ya + 0.5*(y1 - ya - h2/htot)
        # Axes
        ax11 = fig.add_axes([xa, yb, w1, h1/htot])
        ax12 = fig.add_axes([xa, ya, w1, h1/htot])
        ax13 = fig.add_axes([xb, yb, w1, h1/htot])
        ax14 = fig.add_axes([xb, ya, w1, h1/htot])
        ax15 = fig.add_axes([xc, yb, w1, h1/htot])
        ax16 = fig.add_axes([xc, ya, w1, h1/htot])
        ax2 = fig.add_axes([xd, yc, w2, h2/htot])
        ax3 = fig.add_axes([xa, 0, w3, h3/htot])
        axes = [ax11, ax12, ax13, ax14, ax15, ax16, ax2, ax3]
        for ax in axes[:-1]:
            ax.set_xticks([])
            ax.set_yticks([])
        ax3.axis('off')
        # Zoom indicator
        ind_lw = 0.8
        ax15_trans = fig.add_axes([xc, yb, w1, h1/htot], sharex=ax15, sharey=ax15, fc='none')
        params = {'bounds':zoom_region, 'inset_ax':ax2, 'alpha':1, 'lw':ind_lw, 'zorder':99}
        _, conn1 = ax15_trans.indicate_inset(**params, edgecolor=cz1)
        _, conn2 = ax16.indicate_inset(**params, edgecolor=cz2)
        [line.set(lw=ind_lw) for line in conn1]
        [line.set(lw=ind_lw) for line in conn2]
        # State labels
        fig.text(xa, yb+h1/htot/2, 'State 1', rotation='vertical', ha='right', va='center')
        fig.text(xa, ya+h1/htot/2, 'State 2', rotation='vertical', ha='right', va='center')
        # Arrow
        ax3.set_aspect('equal')
        ax3.arrow(0, 0, 1, 0, width=0.015, color='k')
        # fig.text(xa+0.5*w3,  0, 'BITSS trajectory', ha='center', va='bottom')
        return axes

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

    x11, x12, x21, x22, x31, x32, ts = load_data('sw_data.json')
    axes = create_axes(fig, y1)
    plot_state(axes[0], x11)
    plot_state(axes[1], x12)
    plot_state(axes[2], x21)
    plot_state(axes[3], x22)
    plot_state(axes[4], x31)
    plot_state(axes[5], x32)
    plot_zoom(axes[6], x31, x32, ts)

def main():
    h1 = 0.5
    h2 = 0.34
    h = h1 + h2

    fig = lt.figure(1, h)
    fig.text(0,  1, '(a)', ha='left', va='top')
    fig.text(0,  h2/h, '(b)', ha='left', va='top')

    plot_cb(fig, h2/h, h)
    plot_sw(fig, h2/h, h)

    lt.savefig('../adaptivemesh.pdf', dpi=500)


if (__name__ == "__main__"):
    main()
