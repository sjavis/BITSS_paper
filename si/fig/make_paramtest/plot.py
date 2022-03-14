import copy
import json
import numpy as np
from matplotlib import pyplot as plt, cm
from scipy.ndimage import gaussian_filter
from pyutils import latexify as lt
# Get default style for SI
import sys; sys.path.insert(0, '..')
import style

subfigs = ['a', 'b']
systems = ['lj', 'cb']
levels = [[600, 1000, 2000],
          [57000, 60000, 65000]]
label_locs = [[(10, 0.01), (20, 0.003), (50,0.0003)],
              [(20, 0.01), (5.6, 0.13), (100, 0.2)]]

cmap = copy.copy(cm.get_cmap('viridis'))
cmap.set_bad('lightgrey')

with open('data.json', 'r') as f:
    data = json.load(f)
for i, system in enumerate(systems):
    d = data[system]
    shape = (len(np.unique(d['alpha'])), -1)
    alpha = np.reshape(d['alpha'], shape)
    beta = np.reshape(d['beta'], shape)
    fc = np.reshape(d['fc'], shape)
    
    fig = lt.figure(0.5)
    fig.text(0, 1, f'({subfigs[i]})', ha='left', va='top')
    ax = fig.add_axes((0.15, 0.17, 0.78, 0.81))
    plt.semilogx()
    plt.semilogy()

    # Colormap
    plt.pcolormesh(alpha, beta, fc, shading='nearest', cmap=cmap, vmax=np.nanpercentile(fc,90), ec='face', lw=0.1)
    plt.colorbar(label='function calls')

    # Contours
    filter1 = gaussian_filter(np.where(np.isnan(fc), 0., fc), 1, truncate=1)
    filter2 = gaussian_filter(np.where(np.isnan(fc), 0., 1.), 1, truncate=1)
    filtered = np.where(np.isnan(fc), np.nan, filter1/filter2)
    contour = plt.contour(alpha, beta, filtered, colors='w', levels=levels[i])
    plt.clabel(contour, fmt="%d", manual=label_locs[i])

    plt.plot([10], [0.1], marker='*', c='r', zorder=99)

    plt.xlabel(r'$\alpha$')
    plt.ylabel(r'$\beta$')
    plt.xticks([0.1, 1, 10, 100, 1000, 10000])
    plt.minorticks_off()
    lt.savefig(f'../paramtest-{subfigs[i]}.pdf')
