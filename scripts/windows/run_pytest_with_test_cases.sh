#!/usr/bin/env bash

current_file_content=$1
handled_result=$(cat $current_file_content | sed "s/\"//g")
echo $handled_result
echo "Start to run pytest ..."
pytest $handled_result
echo "Run pytest done."
