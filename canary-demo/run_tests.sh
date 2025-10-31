#!/bin/bash

# Install test dependencies
pip install requests

# Run tests
python -m unittest tests/test_app.py

# Check if tests passed
if [ $? -eq 0 ]; then
    echo "Tests passed. Proceeding with deployment."
    exit 0
else
    echo "Tests failed. Aborting deployment."
    exit 1
fi
