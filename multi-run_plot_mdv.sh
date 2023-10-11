#!/bin/bash
diri='{RadarDataPath}'
file=$(ls ${diri}*.mdv)
RadName='{RadarName}'
layer='{SpecificHeight}'
date > run.log
for f in $file
do
	./run_plot_mdv.sh $f $RadName DZ $layer
	./run_plot_mdv.sh $f $RadName VE $layer
done
