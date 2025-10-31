#!/bin/bash

# Usage: ./release.sh <version>

if [ -z "$1" ]; then
    echo "Please provide a version number"
    exit 1
fi

VERSION=$1

# Run tests
./run_tests.sh

if [ $? -ne 0 ]; then
    echo "Tests failed. Aborting release."
    exit 1
fi

# Update version in values.yaml
sed -i '' "s/tag: .*/tag: \"$VERSION\"/" canary-demo/values.yaml

# Commit changes
git add canary-demo/values.yaml
git commit -m "Release version $VERSION"
git tag "v$VERSION"

# Push changes
git push origin main
git push origin "v$VERSION"

# Update Helm release
helm upgrade canary-demo ./canary-demo -n canary-demo --set image.tag=$VERSION
