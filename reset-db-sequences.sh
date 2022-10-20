#!/bin/bash

# Skript to fix the PostgreSQL database auto incrementin indexes
# after import.
# The reset.sql file should be in the same directory, as the script

if [ $# -ne 1 ]; then
    echo Give database URI as argument
    exit 1
fi

psql $1 -Atq -f reset.sql -o temp && psql $1 -f temp && rm temp
