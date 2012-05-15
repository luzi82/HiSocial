#!/bin/bash

pushd ../tool >> /dev/null
	./install.py || exit 1
popd >> /dev/null

PYTHONPATH=../core:../tool:../common nosetests *.py
