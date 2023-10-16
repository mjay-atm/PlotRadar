#!/bin/bash
file=$(ls ../1_data/UF_TR/5_PSS/uf_*)
for f in $file
do
    python demo_qc.py $f
done
