# sw-pkg-utility
Small utility (Python, 7-Zip) created to speed up software delivery to stakeholders. Reduced 15 minute process to 1 minute.

### PURPOSE:
Automate creation of TSW archives.  Number of maintained TSW
archives is rapidly growing and otherwise must be manually created, taking
additional time.

### DESCRIPTION:
For each tsp file in the current directory, copy it and any
other software files to a working directory.  Archive this working
directory using 7-Zip LZMA compression, AES-256 encryption.  Copy the
resulting archive back out to the base directory and scrub the working
directory from the file system.

### REQUIREMENTS:
Python 3+, 7-Zip 9.20

### RUN INSTRUCTIONS:
Copy this script file into the directory that you wish to
archive.  Run from command line using "python .\bundle.py".

### DATE:
06/27/2016

### AUTHOR:
Eric Schnipke
