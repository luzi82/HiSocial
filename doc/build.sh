#!/bin/bash

rm -rf output
mkdir output

mkdir -p output/admin
xmlto xhtml src/admin/home.xml -o output/admin

mkdir -p output/hack
xmlto xhtml src/hack/home.xml -o output/hack
