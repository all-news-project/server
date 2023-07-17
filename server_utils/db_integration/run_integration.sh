#!/bin/sh

# Get version as tag
version=$(cat ../../version.txt)
mongodb_container_name="mongodb-container:$version"
ehco "Container name: $mongodb_container_name"

mongodb_image_name="mongodb-image:$version"
echo "Image name: $mongodb_image_name"

# Build mongodb image
docker build -t my-mongodb .

# Run mongodb image
docker run -d -p 27017:27017 -v /var/lib/mongodb:/data/db --name "$mongodb_container_name" "$mongodb_image_name"
