#!/bin/bash
tag=$1
diri="../1_data/MDV/NU/${tag}/20211126/"
file=$(ls ${diri}*.mdv)
RadName='TEAM-R'
layer='all'
date > run.log
for f in $file
do
	./run_plot_mdv.sh $f $RadName DZ $layer
	# ./run_plot_mdv.sh $f $RadName VE $layer
	./run_plot_mdv.sh $f $RadName VR $layer
done
