#!/bin/bash

py_figs=('toy2d' 'speedtest' 'adaptivemesh' 'flatdiscontinuous')
tex_figs=('BAHschematic')

for fig in ${py_figs[@]}; do
  echo "Plotting $fig"
  cd make_$fig
  python3 ./plot.py
  cd ..
done

for fig in ${tex_figs[@]}; do
  echo "Plotting $fig"
  pdflatex -interaction=nonstopmode -file-line-error -jobname=$fig make_$fig/plot.tex | \
    grep -v "[0-9]*/[0-9]*/[0-9]*/[0-9]*:[0-9]*:[0-9]*" | \
    grep ".*:[0-9]*:\|Warning\|Overfull" --color=always
  rm $fig.aux
  rm $fig.log
done
