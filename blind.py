#!/usr/bin/env python

import os
import glob
import string
import random
import shutil
import argparse

def appendToBlindCSV(filesDir, line):
    filename = os.path.join(filesDir, 'blind.csv')

    if os.path.exists(filename):
        append_write = 'a' # append if already exists
    else:
        append_write = 'w' # make a new file if not

    blindCSV = open(filename,append_write)
    blindCSV.write(line)
    blindCSV.close()

def generateBlindId(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def groupFilesByPrefix(files):
    groups = {}
    for file in files:
        parts = file.split('_')
        # files without a '_' in the name are ignored
        if len(parts) > 1:
            groupName = '_'.join(file.split('_')[:-1])
            if groupName in groups:
                groups[groupName].append(file)
            else:
                groups[groupName] = [file]
    return groups

def blindPrefixGroupedFiles(filesDir, extension):
    allFiles = glob.glob(os.path.join(filesDir, "*.%s" % extension))
    groups = groupFilesByPrefix(allFiles)
    for group in groups:
        blindId = generateBlindId()
        os.mkdir(os.path.join(filesDir, blindId))
        for blindFile in groups[group]:
            # the "discriminator" is the non-unique part of the filename
            # We need this to create the new, blinded file. We only blind the grouped part because that is where the identifying info is.
            # The last part of the file name is just the type of file and does not identify the individual.
            discriminator = blindFile.split('_')[-1]
            shutil.copyfile(blindFile, os.path.join(filesDir, blindId, "%s_%s" % (blindId,discriminator)))
            appendToBlindCSV(filesDir, "%s,%s\n" % (os.path.basename(blindFile),blindId))

def blindAllFiles(filesDir, extension):
    for blindFile in glob.glob(os.path.join(filesDir, "*.%s" % extension)):
        actualExtension = os.path.splitext(blindFile)[1]
        blindId = generateBlindId()
        os.mkdir(os.path.join(filesDir, blindId))
        shutil.copyfile(blindFile, os.path.join(filesDir, blindId, "%s.%s" % (blindId,actualExtension)))
        appendToBlindCSV(filesDir, "%s,%s\n" % (os.path.basename(blindFile),blindId))

parser = argparse.ArgumentParser(description='Blind a directory of files')
parser.add_argument('input_dir', type=str, help='The path to a directory of files you want blinded')
parser.add_argument('type', type=str, choices=['all-images-in-dir', 'all-files-in-dir', 'group-by-prefix'], help='The type of blinding to use')
parser.add_argument('--fileType', type=str, dest='file_type', default="",
                    help='The type of file to blind (default: any type of file)')

args = parser.parse_args()

if args.type == 'all-images-in-dir' or args.type == 'all-files-in-dir':
    if args.file_type == "":
        print "Blinding all files in directory %s..." % (args.input_dir)
    else:
        print "Blinding all '.%s' files in directory %s..." % (args.file_type, args.input_dir)
        
    blindAllFiles(args.input_dir, args.file_type or "*")
elif args.type == 'group-by-prefix':
    print "Blinding groups of files in directory %s..." % (args.input_dir)
    blindPrefixGroupedFiles(args.input_dir, args.file_type or "*")
else:
    print "Error: unrecognized 'type' argument - doing nothing :'("