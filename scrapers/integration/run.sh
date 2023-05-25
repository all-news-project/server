#!/bin/bash

# Read the environment variables from the env file
source env

# Store the current environment variables in a temporary file
env > temp-env

# Run the Python file
python run.py

# Remove the environment variables
while IFS= read -r line; do
    if [[ $line != *"_="* ]]; then
        unset "${line%%=*}"
    fi
done < temp-env

rm temp-env