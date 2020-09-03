#!/bin/bash

while getopts t:h:p:d:u:k: option
do
case "${option}"
in
t) TOKEN=${OPTARG};;
h) INFLUXDB_HOST=${OPTARG};;
p) INFLUXDB_PORT=${OPTARG};;
d) INFLUXDB_DB=${OPTARG};;
u) INFLUXDB_USER=${OPTARG};;
k) INFLUXDB_PASS=${OPTARG};;
esac
done

python3 /config/www/config/python_modules/get_tibber_data.py $TOKEN $INFLUXDB_HOST $INFLUXDB_PORT $INFLUXDB_DB $INFLUXDB_USER $INFLUXDB_PASS