#! /bin/bash

./setup.sh

root_dir=.
src_dir=${root_dir}/src
data_dir=${root_dir}/data
mdl_dir=${root_dir}/mdl

if [ $1 = debug ]; then
	host=127.0.0.1
	port=5000
	python3 ${src_dir}/server.py -m $1 -n $host -p $port
elif [ $1 = deploy ]; then
	host=0.0.0.0
	port=5000
	python3 ${src_dir}/server.py -m $1
elif [ $1 = clean ]; then
	# remove file
	echo 'remove file'
	rm -rf ${data_dir}/*.json
	rm -rf ${mdl_dir}/*
	rm -rf src/__pycache__/ 
fi
