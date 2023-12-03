#!/bin/bash

find . -name "*.py" -type f | while read file; do
    python3 "$file"
done
