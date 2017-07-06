#! /bin/bash

root_dir=.
src_dir=${root_dir}/src
data_dir=${root_dir}/data
log_dir=${root_dir}/log


if [ ! -d $src_dir ]; then
	mkdir $src_dir
fi

if [ ! -d $data_dir ]; then
	mkdir $data_dir
fi

if [ ! -d $log_dir ]; then
	mkdir $log_dir
fi	

