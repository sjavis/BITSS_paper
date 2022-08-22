#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import json

##### Choose results to visualise
n = 200
grid = (n,n+1)

##### Read in the coordinates
nodes = np.reshape(np.loadtxt("sw_nodestate"), grid)
ndof = nodes.size
with open('states.json', 'r') as f:
    data = json.load(f)
    data = [np.reshape(data['sw_m1'], grid),
            np.reshape(data['sw_ts'], grid),
            np.reshape(data['sw_m2'], grid)]

##### Surface contact angles
ca = np.reshape(np.loadtxt("sw_contactangles"), grid)
ca = np.ma.masked_where(nodes!=-1, ca)
surface = ca[:,[0]]
surface_x, surface_y = np.mgrid[-0.5:surface.size, -(grid[1]-1)/20:1:(grid[1]-1)/20]

##### Contour plot levels
limits = np.array([np.min([np.nanmin(data[i][:,1:])+0.1 for i in range(len(data))]),
                   np.max([np.nanmax(data[i][:,1:]) for i in range(len(data))])])
if (limits[0] == limits[1]): limits += [-1e-6, 1e-6]
levels = np.linspace(limits[0], limits[1], 7)

##### Visualise
for i, state in enumerate(data):
    fig = plt.figure(figsize=(5,3))
    ax = plt.axes((0.01,0.01,0.98,0.98))
    plt.axis('off')
    ax.set_aspect('equal')

    plt.contourf(state.T, cmap='Blues', levels=levels)
    plt.pcolormesh(surface_x, surface_y, surface, cmap='Greys_r', vmax=140, zorder=2)

    plt.ylim((surface_y[0,0], n*2/5))
    ax.axhline(surface_y[0,0], c='k')
    ax.axhline(surface_y[0,1], c='k')

    plt.savefig(f'c{i}.png')
