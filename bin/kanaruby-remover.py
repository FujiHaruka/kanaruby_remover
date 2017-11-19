#!/usr/bin/env python
import sys
import os
import argparse
import cv2
import logging


package_path = os.path.dirname(os.path.abspath(__file__)) + "/../kanaruby_remover"
sys.path.append(package_path)

from remover import remove_rubies

parser = argparse.ArgumentParser(description='Remove kana rubies')

parser.add_argument('src', type=str, help='Source image path')
parser.add_argument('dest', type=str, help="Destination image path")
parser.add_argument('--log', type=str, help="Log level", default="INFO")

args = parser.parse_args()
src = args.src
dest = args.dest
loglevel = args.log

logging.basicConfig(level=getattr(logging, loglevel))

# Main
image = cv2.imread(src)
dest_image = remove_rubies(image)
if not os.path.exists(os.path.dirname(dest)):
    os.mkdir(os.path.dirname(dest))
cv2.imwrite(dest, dest_image)
