#!/bin/bash


for file in *.c *.js *.py
do

    if head -n 1 "$file" | grep -qE '^(#|//)'
    then
        echo "Комментарий найден в файле $file"
    else
        echo "Комментарий не найден в файле $file"
    fi
done
