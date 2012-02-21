#!/bin/bash

# A script to clean all .pyc in project
# Eclipse sometimes does not know how to clean

for f in `find . | grep ".pyc$"` ; do
	rm $f
done

