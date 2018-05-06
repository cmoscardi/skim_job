#!/bin/bash

for f in `ls data`; do
  python gen_skim.py data/$f data/SKIM_$f;
done
