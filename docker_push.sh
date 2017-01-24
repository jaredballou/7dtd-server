#!/bin/bash

./docker_build.sh

docker tag jballou/7dtd-server:latest jballou/7dtd-server:latest
docker push jballou/7dtd-server:latest
