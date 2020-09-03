#!/usr/bin/env python3

import json
import requests
import sys
from datetime import datetime
from influxdb import InfluxDBClient


def get_data(token):
    headers = {'Authorization': 'Bearer ' + token,
               'content-type': 'application/json'}

    url = 'https://api.tibber.com/v1-beta/gql'

    data = {'query': "{viewer {homes {currentSubscription {priceInfo { today { startsAt total } }}}}}"}
    data = json.dumps(data)
    try:
        resp = requests.post(url, data, headers=headers, verify=True).json()
        data = []
        for point in resp['data']['viewer']['homes'][0]['currentSubscription']['priceInfo']['today']:
            data.append({
                'measurement': 'spot_price',
                'tags': {
                    'date': point['startsAt'].split('T')[0],
                    'id': point['startsAt']
                },

                'time': point['startsAt'],
                'fields': {
                    'date': point['startsAt'].split('T')[0],
                    'price': point['total']
                }
            })

    except:
        print ('Something went wrong')
        sys.exit(1)
    return data


def update_influx(influx_host, influx_port, influx_db, influx_user, influx_pass, token):
    client = InfluxDBClient(host=influx_host, port=int(influx_port), username=influx_user, password=influx_pass)
    client.switch_database(influx_db)

    today = datetime.today().strftime("%Y-%m-%d")
    bind_params = {'today': today}

    cached = client.query('select "price" FROM "tibberData"."autogen"."spot_price" WHERE "date" = $today GROUP BY "date";', bind_params=bind_params)
    if not cached:
        client.write_points(get_data(token), database='tibberData', time_precision=None, batch_size=10000, protocol='json')


if __name__ == '__main__':
    if len(sys.argv) < 7:
        sys.exit(1)
    else:
        update_influx(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[1])
