#!/usr/bin/env python
import sys
import os
import argparse
import cv2

package_path = os.path.dirname(os.path.abspath(__file__)) + "/../kanaruby_remover"
sys.path.append(package_path)

from remover import remove_rubies

parser = argparse.ArgumentParser(description='Remove kana rubies')

parser.add_argument('src', type=str, help='Source image path')
parser.add_argument('dest', type=str, help="Destination image path")

args = parser.parse_args()
src = args.src
dest = args.dest

# Main
image = cv2.imread(src)
dest_image = remove_rubies(image)
cv2.imwrite(dest, dest_image)
