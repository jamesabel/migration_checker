
import os
import win32api
import argparse
import platform
import gzip
import subprocess

WALK_FILE_EXT = '.mic'  # MIgration Checker
DIR_FILE_EXT = '.txt'  # just a text file
ENCODING = 'UTF-8'

description_string = 'Save the file system information so it can be checked later by check.py.'
epilog = 'Author: James Abel (j@abel.co).  This source code is kept at ' \
         'https://github.com/latusrepo/migration_checker .'
parser = argparse.ArgumentParser(description=description_string, epilog=epilog)
parser.add_argument('-v', '--verbose', action='store_true', help='Verbose.')
parser.add_argument('-o', '--output', help='Output folder.')
parser.add_argument('-p', '--path', required=True, help='Path to the root of the file system to be checked.')

args = parser.parse_args()

output_file_path = platform.node() + WALK_FILE_EXT + '.gz'
if args.output:
    output_file_path = os.path.join(args.output, output_file_path)

if args.verbose:
    print('path', args.path)
    print('output', output_file_path)

count = 0
total_size = 0
with gzip.open(output_file_path, 'w') as output_file:
    for root, dirs, files in os.walk(args.path):
        for name in files:
            full_path = os.path.abspath(os.path.join(root, name))
            output_file.write(bytes(full_path, ENCODING))
            size = 0
            try:
                size = os.path.getsize(full_path)
                output_file.write(bytes(',', ENCODING))
                output_file.write(bytes(str(size), ENCODING))
            except:
                if args.verbose:
                    print('could not get size', full_path)
            try:
                file_attrib = win32api.GetFileAttributes(full_path)
                output_file.write(bytes(',', ENCODING))
                output_file.write(bytes(str(file_attrib), ENCODING))  # windows
            except:
                if args.verbose:
                    print('could not get attributes', full_path)
            output_file.write(bytes(os.linesep, ENCODING))
            count += 1
            total_size += size

if args.verbose:
    print(count, 'files')
    print(total_size, 'bytes')

# now, do a dir in the OS to get the files

def do_dir(special = None):
    output_file_path = platform.node()
    if special:
        output_file_path += '_' + special
    output_file_path += DIR_FILE_EXT
    if args.output:
        output_file_path = os.path.join(args.output, output_file_path)
    output_file_path = os.path.abspath(output_file_path)
    cmd = ['dir', '/s']
    if special:
        cmd.append('/' + special)
    if args.verbose:
        print(args.path, cmd, output_file_path)
    with open(output_file_path, 'w') as f:
        sp = subprocess.Popen(cmd, cwd=args.path, shell=True, stdout=f)
        sp.wait()

do_dir()  # regular
do_dir('AH')  # hidden
do_dir('AS')  # system

if args.verbose:
    print('done')
