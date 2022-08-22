#!/usr/bin/env python3

import numpy as np
from matplotlib import pyplot as plt
import json

sigma = 1
n_particle = 7
rad = 1.12*sigma/2
col = 'C0'


### Load data
with open('states.json', 'r') as f:
    data = json.load(f)
lj = np.array([np.array(data['lj_m1']).reshape((-1,2)),
               np.array(data['lj_ts']).reshape((-1,2)),
               np.array(data['lj_m2']).reshape((-1,2))])
lj[0,:,0] -= lj[0,5,0]
lj[1,:,0] -= lj[1,5,0]
lj[2,:,0] -= lj[2,5,0]
lj[0,:,1] -= lj[0,5,1]
lj[1,:,1] -= lj[1,5,1]
lj[2,:,1] -= lj[2,5,1]
width = np.max(lj[:,:,0])+rad - (np.min(lj[:,:,0])-rad)
height = np.max(lj[:,:,1])+rad - (np.min(lj[:,:,1])-rad)

# Rearrange
lj = lj[:,[5,2,3,4,0,6,1]]


### Plot
for i_state in np.arange(0, len(lj)):
    plt.figure(figsize=(5,5))
    plt.axes((0,0,1,1))
    for i_part in range(n_particle):
        circle = plt.Circle(lj[i_state,i_part], rad, alpha=1, fc=col, ec='none', lw=3)
        plt.text(lj[i_state,i_part,0], lj[i_state,i_part,1], i_part, ha='center', va='center_baseline', size=60)
        plt.gca().add_artist(circle)

    xlim = (np.max(lj[i_state,:,0]) + np.min(lj[i_state,:,0]))/2 + np.array([-width/2, width/2])
    ylim = (np.max(lj[i_state,:,1]) + np.min(lj[i_state,:,1]))/2 + np.array([-height/2, height/2])
    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.gca().axis('off')
    plt.gca().set_aspect('equal')
    plt.savefig(f'a{i_state}.png')
