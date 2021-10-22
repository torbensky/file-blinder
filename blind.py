#!/usr/bin/env python

import os
import glob
import string
import random
import shutil
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askdirectory
from tkinter.messagebox import askyesno

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

def getApplicableFiles(filesDir, extension):
    allFiles = glob.glob(os.path.join(filesDir, "*.%s" % extension))
    return allFiles

def blindPrefixGroupedFiles(filesDir, extension):
    allFiles = getApplicableFiles(filesDir, extension)
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
    for blindFile in getApplicableFiles(filesDir, extension):
        actualExtension = os.path.splitext(blindFile)[1]
        blindId = generateBlindId()
        os.mkdir(os.path.join(filesDir, blindId))
        shutil.copyfile(blindFile, os.path.join(filesDir, blindId, "%s%s" % (blindId,actualExtension)))
        appendToBlindCSV(filesDir, "%s,%s\n" % (os.path.basename(blindFile),blindId))

input_dir = os.getcwd()

MODES = [
    'all-files-in-dir',
    'group-by-prefix',
]

def updateAffectedFiles():
    file_type = fileTypeCombo.get() or "*"
    if file_type == "All file types":
        file_type = "*"   
    affected_files = getApplicableFiles(input_dir, file_type)
    affected_files_list.delete(0,tk.END)
    for file_name in affected_files:
        affected_files_list.insert(tk.END, file_name)
    

def pick_file():
    global input_dir
    input_dir = askdirectory(initialdir=input_dir)
    print('input_dir', input_dir)
    input_dir_label.configure(text=input_dir)
    if input_dir != "":
        files = os.listdir(input_dir)
        FileTypes = ['All file types']
        for file_name in files:
            parts = file_name.split(".")
            if len(parts) == 1:
                continue
            ext = parts[-1]
            if not ext in FileTypes:
                FileTypes.append(ext)
        fileTypeCombo.configure(values=FileTypes)
        fileTypeCombo.current(0)
        run_button["state"] = "normal"
        updateAffectedFiles()
    else:
        run_button["state"] = "disabled"

def handleFileTypeChange(event):
    updateAffectedFiles()


def handleRun():
    mode = modeCombo.get()
    file_type = fileTypeCombo.get() or "*"
    if file_type == "All file types":
        file_type = "*"    

    files_affected = len(getApplicableFiles(input_dir, file_type))

    if file_type == "*":
        prompt = "This will blind all files in directory %s\n\n" % (input_dir)
    else:
        prompt = "This will blind all '.%s' files in directory %s\n\n" % (file_type, input_dir)
    prompt = "%s%s files will be blinded" % (prompt, files_affected)
    prompt = "%s\n\nDo you want to continue?" % prompt

    answer = askyesno(title='Confirmation',
    message=prompt)
    if not answer:
        return

    if mode == MODES[0]:
        blindAllFiles(input_dir, file_type)
    elif mode == MODES[1]:
        blindPrefixGroupedFiles(input_dir, file_type)

BG_PRIMARY = '#EDDEA4'
FG_PRIMARY = '#0FA3B1'

current_mode = 0

app = tk.Tk()
app.configure(bg=BG_PRIMARY)

gui_style = ttk.Style()
# gui_style.configure('My.TButton', foreground = '#334353')
gui_style.configure('My.TFrame', background=BG_PRIMARY)

frm = ttk.Frame(app, padding=20, style="My.TFrame")
frm.grid()

row_idx = 0

# MODE
modeLabel = tk.Label(frm,
                    text = "1. Type of blinding mode",
                    bg = BG_PRIMARY)
modeLabel.grid(column=0, row=row_idx, sticky="w")
modeCombo = ttk.Combobox(frm, 
                        values=MODES,
                        state="readonly",
                        style="My.TCombobox")
modeCombo.grid(column=1, row=row_idx)
row_idx +=1
modeCombo.current(0)

# FILE PICKER
label = tk.Label(frm,
                    text = "2. Input directory with the files",
                    wraplength=200,
                    bg = BG_PRIMARY)
label.grid(column=0, row=row_idx, sticky="w")
pick_file_button = tk.Button(frm, text="Pick Input Directory", bg=FG_PRIMARY, command=pick_file)
pick_file_button.grid(column=1, row=row_idx, sticky="nesw", pady=(20,0))
row_idx +=1
input_dir_label = tk.Label(frm,
                    text = '',
                    bg = BG_PRIMARY)
input_dir_label.grid(column=0, columnspan=2, row=row_idx, sticky="e",pady=(0,20))
row_idx += 1

# FILE TYPE
label = tk.Label(frm,
                    text = "3. Type of files you want blinded",
                    wraplength=200,
                    bg = BG_PRIMARY)
label.grid(column=0, row=row_idx, sticky="w")
fileTypeCombo = ttk.Combobox(frm, 
                            values=[])
fileTypeCombo.grid(column=1, row=row_idx)
fileTypeCombo.bind("<<ComboboxSelected>>", handleFileTypeChange)
row_idx +=1

# AFFECTED FILES
# label.grid(column=0, row=row_idx, sticky="w")
# row_idx += 1
affected_files_list = tk.Listbox(frm, width=0, height=6)
affected_files_list.grid(column=0, columnspan=2, row=row_idx, sticky="e")
row_idx += 1

# RUN
run_button = tk.Button(frm, text="Run", bg=FG_PRIMARY, command=handleRun)
run_button.grid(column=0, columnspan=2, row=row_idx, sticky="nesw", pady=(20,0))
row_idx +=1
run_button["state"] = "disabled"

frm.mainloop()

# parser = argparse.ArgumentParser(description='Blind a directory of files')
# parser.add_argument('input_dir', type=str, help='The path to a directory of files you want blinded')
# parser.add_argument('type', type=str, choices=['all-images-in-dir', 'all-files-in-dir', 'group-by-prefix'], help='The type of blinding to use')
# parser.add_argument('--fileType', type=str, dest='file_type', default="",
#                     help='The type of file to blind (default: any type of file)')

# args = parser.parse_args()

