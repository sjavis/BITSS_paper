#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import pyutils.latexify as lt

lt.update_width(246) # Double column: 510 pt, single column: 246 pt
plt.rc('font', size=9)
plt.rc('axes', labelsize=9)

##### Choose results to visualise
resolutions = [[200], [400], [200], [200, 400]]
data_files = ['200-ts', '400-ts', '200-400-ts', '200-400-bits']

limits = np.array([np.min([np.min(np.loadtxt(file))+0.1 for file in data_files]),
                   np.max([np.max(np.loadtxt(file))     for file in data_files])])
levels = np.linspace(limits[0], limits[1], 7)

interfaces = []

fig = lt.figure(0.5, 0.9)
ax = [plt.axes((0.01, 0.01, 0.98, 0.485)),
      plt.axes((0.01, 0.505, 0.98, 0.485))]

for i_f, file in enumerate(data_files):
    states = np.loadtxt(file)
    for res in resolutions[i_f]:
        # Get data
        grid = (res, res+1)
        ndof = grid[0]*grid[1]
        state = states[:ndof].reshape(grid)[:,1:]
        states = states[ndof:]
        ca = np.reshape(np.loadtxt(f'{res}-contact_angles'), grid)
        surface = ca[:,[0]]
        surface_x, surface_y = np.mgrid[-0.5:surface.size, -(grid[1]-1)/20:1:(grid[1]-1)/20]

        # Get interfaces
        if (i_f <= 2):
            c = plt.contour(state.T, levels=[0], alpha=0)
            interfaces.append(c.collections[0].get_paths()[0].vertices / res)

        # Plot final BITSS states
        if (i_f > 2):
            i = 0 if (res == 200) else 1
            plt.sca(ax[i])

            plt.xticks([])
            plt.yticks([])
            ax[i].set_aspect('equal')
            plt.contourf(state.T, cmap='Blues', levels=levels)

            plt.pcolormesh(surface_x, surface_y, surface, cmap='Greys_r', zorder=2)
            ax[i].axhline(0, c='k', lw=0.5)
            plt.ylim((surface_y[0,0], res/2))

            # Show grid
            plt.autoscale(False)
            for i in np.arange(50, state.shape[0], 50):
                plt.plot([i, i], [0, state.shape[1]], 'k-', lw=0.5, zorder=1)
            for i in np.arange(50, state.shape[1], 50):
                plt.plot([0, state.shape[0]], [i, i], 'k-', lw=0.5, zorder=1)

lt.savefig('../differentgrids-a', dpi=300)


### Plot interfaces
fig = lt.figure(0.5, 0.9)
ax = plt.axes((0.01, 0.01, 0.98, 0.98))
ax.set_aspect('equal')
ax.set_xticks([])
ax.set_yticks([])

axins = ax.inset_axes((0.3, -0.05, 0.12, 0.36), transform=ax.transData)
axins.set_xlim(0.6, 0.63)
axins.set_ylim(-0.005, 0.045)
axins.set_aspect('equal')
axins.set_xticks([])
axins.set_yticks([])
_, indicator_lines = ax.indicate_inset_zoom(axins, alpha=1, ec="k", label='')
indicator_lines[0].set_visible(True)
indicator_lines[1].set_visible(False)
indicator_lines[2].set_visible(False)
indicator_lines[3].set_visible(True)

labels = [200, 400, 'Both']
for i, interface in enumerate(interfaces):
    ax.plot(interface[:,0], interface[:,1], label=labels[i])
    axins.plot(interface[:,0], interface[:,1])

ca = np.reshape(np.loadtxt(f'400-contact_angles'), (400,401))
surface = ca[:,[0]]
surface_x, surface_y = np.mgrid[-0.5:surface.size, -(grid[1]-1)/40:1:(grid[1]-1)/40]
surface_x = surface_x / 400
ax.pcolormesh(surface_x, surface_y, surface, cmap='Greys_r', zorder=2)
ax.axhline(0, c='k', lw=1)
axins.pcolormesh(surface_x, surface_y, surface, cmap='Greys_r', zorder=2)
axins.axhline(0, c='k', lw=1)

ax.set_xlim(0.1, 0.65)
ax.set_ylim(-0.04, 0.45)
ax.legend(loc='upper right')
lt.savefig('../differentgrids-b', dpi=300)
