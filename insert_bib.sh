#!/bin/bash

start_tag='% start bib'
end_tag='% end bib'

BBLFILE="${1%.tex}.bbl"
if [ ! -f "$1" ]; then
  echo "File not found"
  exit 1
elif [ ! -f "$BBLFILE" ]; then
  echo "BBL file does not exist. Run bibtex on file."
  exit 1
fi

# Remove commented lines
sed -i "/^%/d" $BBLFILE

# Delete between two tags
sed -i "/${start_tag}/,/${end_tag}/{//!d}" $1

# Paste bibliography between two tags
sed -i "/${start_tag}/r $BBLFILE" $1
