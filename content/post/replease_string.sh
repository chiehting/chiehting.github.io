#!/bin/bash

path=${1:-.}
pre="categories: "

files=$(find $path -type f|grep -v $0)

IFS=$'\n'
for file in $files
do
  for string in $(cat ${file} | grep ${pre})
  do
    newString="$pre[$(echo ${string/$pre/} | tr -s ' ' ',')]"
    sed -i '' "s/$string/$newString/g" $file
  done
done

