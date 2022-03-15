#!/bin/bash

start_tag='%% start bib'
mid_tag='%% mid bib'
end_tag='%% end bib'

BBLFILE="${1%.tex}.bbl"
AUXFILE="${1%.tex}.aux"
if [ ! -f "$1" ]; then
  echo "Error: File not found."
  exit 1
fi

# Use bibtex to generate aux file
sed -i "/$start_tag/,/$mid_tag/ {//b; /$start_tag/b; s/^%\s*//}" $1 # Uncomment
sed -i "/$mid_tag/,/$end_tag/ {//b; /$mid_tag/b; /^%/b; s/^/% /}" $1 # Comment
latex -interaction=batchmode "$1" > /dev/null 2>&1
sed -i "/$start_tag/,/$mid_tag/ {//b; /$start_tag/b; s/^/% /}" $1 # Comment
sed -i "/$mid_tag/,/$end_tag/ {//b; /$mid_tag/b; s/^%\s*//}" $1 # Uncomment
if [ ! -f "$AUXFILE" ]; then
  echo "Error: Failure generating aux file."
  exit 1
fi

# Generate bbl file
bibtex -terse "$AUXFILE"
if [ ! -f "$BBLFILE" ]; then
  echo "Error: Failure generating bbl file."
  exit 1
fi
sed -i "/^%/d" $BBLFILE

# Paste bibliography into tex file
sed -i "/${mid_tag}/,/${end_tag}/{//!d}" $1
sed -i "/${mid_tag}/r $BBLFILE" $1
