#!/bin/bash

figures=('toy2d' 'speedtest' 'adaptivemesh' 'flatdiscontinuous')

for fig in ${figures[@]}; do
  echo "Plotting $fig"
  cd make_$fig
  python3 ./plot.py
  cd ..
done
