#!/usr/bin/env bash

current_file_content=$1
handled_result=$(cat $current_file_content | sed "s/\"//g")
pytest $handled_result
