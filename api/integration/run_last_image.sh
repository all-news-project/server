#!/bin/sh

image_id=$(cat image_id.txt)

# Getting IP Address
ip_address=$(ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1' | awk '{print $2}' | sed -n 2p)
echo "IP address: '$ip_address'"

docker run --network host -e CONNECTION_STRING="mongodb://$ip_address:27017/" -p 5000:5000 "$image_id"
