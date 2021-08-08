#!/usr/bin/env python3

import argparse
import json

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

ELASTICSEARCH_HOSTS = ['192.168.56.12']

QUERIES = [
    {'name': 'syslog', 'search': Search(index='syslog-*')},
    {'name': 'winlogbeat', 'search': Search(index='winlogbeat-*')}]


def main():
    args = parse_args()
    download_logs(args.start, args.end, args.suffix)


def parse_args():
    parser = argparse.ArgumentParser(description='Download logs')
    parser.add_argument('start', help='start time')
    parser.add_argument('end', help='end time')
    parser.add_argument('suffix', help='suffix for filename')
    return parser.parse_args()


def download_logs(start, end, suffix):
    client = Elasticsearch(ELASTICSEARCH_HOSTS)
    for query in QUERIES:
        filename = query['name'] + '_' + str(suffix) + '.jsonl'
        print('Writing ' + filename + '...')
        with open(filename, 'w') as f:
            for hit in query['search'].using(client).filter(
                    'range', **{'@timestamp': {'gte': start, 'lt': end}}).scan():
                f.write(json.dumps(hit.to_dict(), sort_keys=True) + '\n')


if __name__ == '__main__':
    main()
