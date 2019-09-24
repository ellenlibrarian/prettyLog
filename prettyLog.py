# This script reads in a Voyager import log and extracts IDs for duplicate bibs, as well as IDs for bibs, MFHDs, and items added. It then exports this information to a text file and cleans up the temporary file created as part of the script's functioning.
# I wrote this to quickly find all duplicates within an import log files since those need to be addressed after the import. I added the functionality to grab the other IDs because it would be useful if something went terribly awry and I needed to delete them all.

# Modules required: re, os

def findDuplicates():
  duplicates = []
  fh = open(fname)
  fout = open("temp.txt", "w")
  # read through file, extract the line after the line starting with BibID & rank and write to temp file
  with fh as f:
    lines = f.readlines()
    n_lines = len(lines)
    for i, line in enumerate (lines) :
      line = line.rstrip()
      if line.startswith("	BibID & rank") and \
          n_lines > i + 2 and lines[i + 2].startswith("") :
          duplicates.append(lines[i+1])
    fout.write(str(duplicates))

def cleanFile():
    fh = open("temp.txt", 'r')
    fout = open("importReport.txt", 'w')
    # read through temp.txt and extract only the bib id from the information within
    data = fh.read()
    ids = re.findall(r'[0-9]+\s', data)
    fout.write("Duplicate bibs:" + "\n")
    #print(bibs)
    for id in ids:
        fout.write(id + '\n')

def extractBibsAdded():
    fh = open(fname)
    fout = open("importReport.txt", "a")
    fout.write("\n" + "Bibs added:" + "\n")
    # read through log file and extract added bib ids
    for line in fh :
        line = line.rstrip()
        if not line.startswith("	Adding Bib") :
            continue
        line = re.findall(r'[0-9]+',line)
        for id in line:
            fout.write(id + "\n")

def extractMFHDsAdded():
    fh = open(fname)
    fout = open("importReport.txt", "a")
    fout.write("\n" + "MFHDs added:" + "\n")
    # read through log file and extract added MFHD ids
    for line in fh :
        line = line.rstrip()
        if not line.startswith("MFHD_ID ") :
            continue
        line = re.findall(r'[0-9]+',line)
        for id in line:
            fout.write(id + "\n")

def extractItemsAdded():
    fh = open(fname)
    fout = open("importReport.txt", "a")
    fout.write("\n" + "Items added:" + "\n")
    # read through the log file and extract added item IDs
    for line in fh :
        line = line.rstrip()
        if not line.startswith("ITEM_ID ") :
            continue
        line = re.findall(r'[0-9]+',line)
        for id in line:
            fout.write(id + "\n")

def deleteTempFile():
    import os
    # delete temp.txt since it is no longer needed
    os.remove("temp.txt")

import re # importing this here because multiple functions need it
fname = input("Enter file name: ")
print("Report will be in importReport.txt.")
findDuplicates()
cleanFile()
extractBibsAdded()
extractMFHDsAdded()
extractItemsAdded()
deleteTempFile()
