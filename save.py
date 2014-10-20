
import os
import win32api
import argparse
import platform
import gzip

OUTPUT_FILE_EXT = '.mic'  # MIgration Checker
ENCODING = 'UTF-8'

description_string = 'Save the file system information so it can be checked later by check.py.'
epilog = 'Author: James Abel (j@abel.co).  This source code is kept at ' \
         'https://github.com/latusrepo/migration_checker .'
parser = argparse.ArgumentParser(description=description_string, epilog=epilog)
parser.add_argument('-v', '--verbose', action='store_true', help='Verbose.')
parser.add_argument('-o', '--output', help='Output folder.')
parser.add_argument('-p', '--path', required=True, help='Path to the root of the file system to be checked.')

args = parser.parse_args()

output_file_path = platform.node() + OUTPUT_FILE_EXT + '.gz'
if args.output:
    output_file_path = os.path.join(args.output, output_file_path)

if args.verbose:
    print('path', args.path)
    print('output', output_file_path)

count = 0
with gzip.open(output_file_path, 'w') as output_file:
    for root, dirs, files in os.walk(args.path):
        for name in files:
            full_path = os.path.abspath(os.path.join(root, name))
            output_file.write(bytes(full_path, ENCODING))
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

if args.verbose:
    print(count, 'files')

