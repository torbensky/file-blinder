#!/usr/bin/env python

import sys
import os
import glob
import re
import string
import random
import shutil
import argparse

def appendToBlindCSV(imagesDir, line):
    filename = os.path.join(imagesDir, 'blind.csv')

    if os.path.exists(filename):
        append_write = 'a' # append if already exists
    else:
        append_write = 'w' # make a new file if not

    blindCSV = open(filename,append_write)
    blindCSV.write(line)
    blindCSV.close()

def generateBlindId(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def groupImagesByPrefix(images):
    groups = {}
    for image in images:        
        groupName = '_'.join(image.split('_')[:-1])
        if groupName in groups:
            groups[groupName].append(image)
        else:
            groups[groupName] = [image]
    return groups

def blindPrefixGroupedImages(imagesDir, extension):
    allImages = glob.glob(os.path.join(imagesDir, "*.%s" % extension))
    groups = groupImagesByPrefix(allImages)
    for group in groups:
        blindId = generateBlindId()
        os.mkdir(os.path.join(imagesDir, blindId))
        for imageFile in groups[group]:
            # the "discriminator" is the non-unique part of the filename
            # We need this to create the new, blinded file. We only blind the grouped part because that is where the identifying info is.
            # The last part of the file name is just the type of image and does not identify the individual.
            discriminator = imageFile.split('_')[-1]
            shutil.copyfile(imageFile, os.path.join(imagesDir, blindId, "%s_%s" % (blindId,discriminator)))
            appendToBlindCSV(imagesDir, "%s,%s\n" % (imageFile,blindId))

def blindAllImages(imagesDir, extension):
    for imageFile in glob.glob(os.path.join(imagesDir, "*.%s" % extension)):
        blindId = generateBlindId()
        os.mkdir(os.path.join(imagesDir, blindId))
        shutil.copyfile(imageFile, os.path.join(imagesDir, blindId, "%s.%s" % (blindId,extension)))
        appendToBlindCSV(imagesDir, "%s,%s\n" % (imageFile,blindId))

parser = argparse.ArgumentParser(description='Blind a directory of images')
parser.add_argument('input_dir', type=str, help='The path to a directory of images you want blinded')
parser.add_argument('type', type=str, choices=['all-images-in-dir', 'group-by-prefix'], help='The type of blinding to use')
parser.add_argument('--fileType', type=str, dest='file_type', default="tif",
                    help='The type of image file to blind (default: "tif")')

args = parser.parse_args()

if args.type == 'all-images-in-dir':
    print "Blinding all '.%s' images in directory %s..." % (args.file_type, args.input_dir)
    blindAllImages(args.input_dir, args.file_type)
elif args.type == 'group-by-prefix':
    print "Blinding groups of '.%s' images in directory %s..." % (args.file_type, args.input_dir)
    blindPrefixGroupedImages(args.input_dir, args.file_type)
else:
    print "Error: unrecognized 'type' argument - doing nothing :'("