#!/usr/bin/python3
import os
import sys
import hashlib

folder = sys.argv[1]
curdir = os.path.abspath('.')

def make_md5s(dirname):
    filename = 'checksums.txt'
    checksums = []
    os.chdir(dirname)
    for file in [x for x in os.listdir(dirname) if os.path.isfile(x)]:
        with open(file, 'rb') as f:
            checksums.append((file, hashlib.md5(f.read()).hexdigest()))

    with open(filename, 'w') as f:
        for file, md5 in checksums:
            f.write('{}:{}\n'.format(file, md5))

for root, dirs, files in os.walk(curdir):
    make_md5s(root)
    os.chdir(curdir)
