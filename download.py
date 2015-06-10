#!/usr/bin/env python

# download.py: download literally everything from S3: all buckets, all files
# use with caution

from boto.s3.connection import S3Connection
from cloudfile.config import config
from cloudfile.util import gen_md5
from os import makedirs, mkdir, remove
from os.path import dirname, isdir, isfile, join, normpath
from re import match

conn = S3Connection(config.get('secrets', 'AWS_ACCESS_KEY'),
                    config.get('secrets', 'AWS_SECRET_KEY'))
buckets = conn.get_all_buckets()

local_path = config.get('paths', 'LOCAL')

for b in buckets:
    print('bucket {}'.format(b.name))
    b_path = normpath(join(local_path, b.name))

    for f in b.list():
        k = b.get_key(f)
        m = match(r'<Key[^,]+,([^>]+)>', str(k.name))
        k_name = m.group(1).decode('utf-8')
        if k_name[-1] == '/': # skip empty directory keys
            print('\tskipping directory key {}'.format(k_name.encode('utf-8')))
            continue
        f_path = normpath(join(b_path, k_name))
        f_base = dirname(f_path)
        if not isdir(f_base):
            makedirs(f_base)
        if isfile(f_path): # NOTE: assumes all downloaded files have been checksummed
            print('\tskipping {} (downloaded)'.format(k_name.encode('utf-8')))
        else:
            print('\tdownloading {}'.format(k_name.encode('utf-8')))
            k.get_contents_to_filename(f_path)
            if gen_md5(f_path) == k.md5:
                print('\tchecksum match: {}'.format(k.md5))
            else:
                print('\tERROR: checksum mismatch for {}'.format(f_path))
                remove(f_path)
