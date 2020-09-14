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

def getDraqIds(imagesDir):
    ids = []
    for draqFile in glob.glob(os.path.join(imagesDir, "*Draq5*.tif")):
        match = re.match(r'.*?Draq5_(.*?).tif', draqFile)
        ids.append(match.group(1))
    return ids

def blindOligDraqImages(imagesDir):
    appendToBlindCSV(imagesDir,'Draq5 File Source,Olig File Source,Original ID,Blind ID\n')
    ids = getDraqIds(imagesDir)
    print "Blinding %d image pairs..." % len(ids)
    for id in ids:
        blindId = generateBlindId()
        oligFile = os.path.join(imagesDir, "Olig2_" + id + ".tif")
        draqFile = os.path.join(imagesDir, "Olig2_Draq5_" + id + ".tif")
        #print "\t%s -> %s" % (id, blindId)

        os.mkdir(os.path.join(imagesDir, blindId))
        shutil.copyfile(oligFile, os.path.join(imagesDir, blindId, "Olig2.tif"))
        shutil.copyfile(draqFile, os.path.join(imagesDir, blindId, "Olig2_Draq5.tif"))

        appendToBlindCSV(imagesDir, "%s,%s,%s,%s\n" % (draqFile,oligFile,id,blindId))
    print "All done!"

def blindAllImages(imagesDir, extension):
    for imageFile in glob.glob(os.path.join(imagesDir, "*.%s" % extension)):
        blindId = generateBlindId()
        os.mkdir(os.path.join(imagesDir, blindId))
        shutil.copyfile(imageFile, os.path.join(imagesDir, blindId, "%s.%s" % (blindId,extension)))
        appendToBlindCSV(imagesDir, "%s,%s\n" % (imageFile,blindId))

parser = argparse.ArgumentParser(description='Blind a directory of images')
parser.add_argument('input_dir', type=str, help='The path to a directory of images you want blinded')
parser.add_argument('type', type=str, choices=['olig2-draq5-pairs', 'all-images-in-dir'], help='The type of blinding to use')
parser.add_argument('--fileType', type=str, dest='file_type', default="tif",
                    help='The type of image file to blind (default: "tif")')

args = parser.parse_args()

if args.type == 'olig2-draq5-pairs':
    print "Blinding Olig2 Draq5 image pairs..."
    blindOligDraqImages(args.input_dir)
elif args.type == 'all-images-in-dir':
    print "Blinding all images in directory %s..." % args.input_dir
    blindAllImages(args.input_dir, args.file_type)
else:
    print "Error: unrecognized 'type' argument - doing nothing :'("