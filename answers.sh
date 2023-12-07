#!/bin/bash

for dir in $(find . -type d -name 'dec_*' | sort -V); do
    find "$dir" -maxdepth 1 -name "*.py" -type f -o -name "*.go" -type f | while read file; do
        if [[ $file == *.py ]]; then
            python3 "$file"
        elif [[ $file == *.go ]]; then
            go run "$file"
        fi
    done
done
