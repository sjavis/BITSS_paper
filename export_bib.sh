#!/bin/bash

AUXFILE="${1%.tex}.aux"
if [ ! -f "$1" ]; then
  echo "File not found"
  exit 1
elif [ ! -f "$AUXFILE" ]; then
  echo "AUX file does not exist. Run bibtex on file."
  exit 1
fi

bibexport -ns $AUXFILE
# Remove empty lines, abstract, url, etc
sed -i '/^\s*$/d' bibexport.bib
remove_fields=('abstract' 'url' 'issn' 'isbn' 'annote' 'month')
for field in "${remove_fields[@]}"; do
  sed -i "/^\s*$field =.*},$/d" bibexport.bib
  sed -i "/^\s*$field =\s*{/,/},$/d" bibexport.bib
done
