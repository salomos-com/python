#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Function to update version in setup.py
update_version() {
    sed -i "s/version=\".*\"/version=\"$1\"/" setup.py
}

# Prompt for new version
echo "Current version: $(grep version setup.py | cut -d'"' -f2)"
read -p "Enter new version number: " NEW_VERSION

# Update version in setup.py
update_version $NEW_VERSION

# Run tests
echo "Running tests..."
python -m unittest discover tests

# Clean up old builds
echo "Cleaning up old builds..."
rm -rf build dist *.egg-info

# Build the package
echo "Building the package..."
python setup.py sdist bdist_wheel

# Check the package
echo "Checking the package..."
twine check dist/*

# Prompt for confirmation before uploading
read -p "Do you want to upload the package to PyPI? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "Uploading to PyPI..."
    twine upload dist/*
else
    echo "Upload cancelled."
fi

echo "Script completed."
