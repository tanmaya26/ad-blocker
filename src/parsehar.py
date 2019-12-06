"""Reads a har file from the filesystem, converts to CSV, then dumps to
stdout.
"""
import argparse
import json
import csv
from urlparse import urlparse


def main(harfile_path):
    """Reads a har file from the filesystem, converts to CSV, then dumps to
    stdout.
    """
    harfile = open(harfile_path)
    harfile_json = json.loads(harfile.read())
    i = 0
    with open(harfile_path[:-3] + '.csv', 'w') as f:
        csv_file = csv.writer(f)
        csv_file.writerow(['id', 'url', 'hostname', 'size (bytes)',
            'size (kilobytes)', 'mimetype'])

        for entry in harfile_json['log']['entries']:
            i = i + 1
            url = entry['request']['url']
            urlparts = urlparse(entry['request']['url'])
            size_bytes = entry['response']['bodySize']
            size_kilobytes = float(entry['response']['bodySize'])/1024
            mimetype = 'unknown'
            if 'mimeType' in entry['response']['content']:
                mimetype = entry['response']['content']['mimeType']

            csv_file.writerow([i, url, urlparts.hostname, size_bytes,
                size_kilobytes, mimetype])

if __name__ == '__main__':
    argparser = argparse.ArgumentParser(
        prog='parsehar',
        description='Parse .har files into comma separated values (csv).')
    argparser.add_argument('harfile', type=str, nargs=1,
                        help='path to harfile to be processed.')
    args = argparser.parse_args()

    main(args.harfile[0])