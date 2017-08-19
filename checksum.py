#!/usr/bin/python3
import os
import sys
import hashlib

folder = sys.argv[1]
curdir = os.path.abspath('.')

def make_sha_of(data):
    return hashlib.sha256(data).hexdigest()

def make_shas(dirname):
    filename = 'checksums.txt'
    checksums = []
    os.chdir(dirname)
    for file in [x for x in os.listdir(dirname) if os.path.isfile(x)]:
        with open(file, 'rb') as f:
            checksums.append((file, make_sha_of(f.read())))

    with open(filename, 'w') as f:
        for file, sha in checksums:
            f.write('{}:{}\n'.format(file, sha))

for root, dirs, files in os.walk(curdir):
    make_shas(root)
    os.chdir(curdir)
