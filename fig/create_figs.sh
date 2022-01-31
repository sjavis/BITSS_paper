#!/bin/bash

figures=('toy2d' 'speedtest' 'changingmesh' 'differentgrids' 'zeroeigen' 'discontinuous')

for fig in ${figures[@]}; do
  echo "Plotting $fig"
  cd make_$fig
  python3 ./plot.py
  cd ..
done
