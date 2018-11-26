#!/usr/bin/env python2
"""
Logpuzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Google's Python Class
http://code.google.com/edu/languages/google-python-class/

Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"

"""

import os
import re
import sys
import urllib
import argparse


def read_urls(filename):
    """Returns a list of the puzzle urls from the given log file,
    extracting the hostname from the filename itself.
    Screens out duplicate urls and returns the urls sorted into
    increasing order."""
    # +++your code here+++
    head, _, tail = filename.partition("_")
    filename_re = re.compile(r'GET\s/(\S*puzzle\S*)\s')
    with open(filename, 'rt') as f_obj:
        f_contents = f_obj.read()
        matches = filename_re.findall(f_contents)
    return [os.path.join('http://', tail, match) for match in matches]


def download_images(img_urls, dest_dir):
    """Given the urls already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory
    with an img tag to show each local image file.
    Creates the directory if necessary.
    """
    # +++your code here+++
    if dest_dir not in os.listdir(os.getcwd()):
        os.mkdir(dest_dir)
    img_num = 0
    for img_url in img_urls:
        filename, _ = urllib.urlretrieve(img_url)
        imagename_match = re.search(r'\W(\w+)\.jpg$', img_url)
        imagename = imagename_match.group(1)
        with open(filename, 'rb') as f_obj:
            # with open(os.path.join(os.getcwd(), dest_dir, 'img'
                                #    + str(img_num).zfill(2) + '.img'), 'wb') as target:
            with open(os.path.join(os.getcwd(), dest_dir, imagename + '.jpg'), 'wb') as target:
                target.write(f_obj.read())
            img_num += 1
    with open(os.path.join(os.getcwd(), dest_dir, 'index.html'), 'wt') as target:
        target.write("<html>\n<style>img{margin:0}</style>\n<body>\n")
        for filename in sorted(os.listdir(os.path.join(os.getcwd(), dest_dir)), key=str.lower):
            if 'index' not in filename:
                target.write("<img src=\"{}\">".format(filename))
        target.write("</html>\n</body>")


def create_parser():
    """Create an argument parser object"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--todir',  help='destination directory for downloaded images')
    parser.add_argument('logfile', help='apache logfile to extract urls from')

    return parser


def main(args):
    """Parse args, scan for urls, get images from urls"""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    img_urls = read_urls(parsed_args.logfile)

    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])
