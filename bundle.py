###############################################################################
# PURPOSE:  Automate creation of TSW archives.  Number of maintained TSW
# archives is rapidly growing and otherwise must be manually created, taking
# additional time.
#
# DESCRIPTION:  For each tsp file in the current directory, copy it and any
# other software files to a working directory.  Archive this working
# directory using 7-Zip LZMA compression, AES-256 encryption.  Copy the
# resulting archive back out to the base directory and scrub the working
# directory from the file system.
#
# REQUIREMENTS:  Python 3+, 7-Zip 9.20
#
# RUN INSTRUCTIONS:  Copy this script file into the directory that you wish to
# archive.  Run from command line using "python .\cpg_bundle.py".
#
# DATE:  06/27/2016
#
# AUTHOR:  Eric Schnipke
###############################################################################

# Import required packages
import os
import sys
from glob import glob
import shutil
import subprocess


###############################################################################
# 7-Zip Execution Parameters
###############################################################################
apps = {'7z': 'C:\\Program Files\\7-Zip\\7z.exe'}  # 7-Zip install path
commands = {'add': 'a'}
switches = {'AES-256 key': '-p{DELETED}',
            'content visibility': '-mhe',  # Hide contents until unlocked
            'multi-threading': '-mmt=2',  # 2 cores
            'compression level': '-mx=5',  # Normal
            }


###############################################################################
# File Object: Provides convenience methods for concatenating file
# names/extensions and file cleanup.
###############################################################################
class File(object):
    def __init__(self, name, extension, clean=False):
        self._name = name
        self._extension = extension
        self._filename = self._name + '.' + self._extension

        # clean, if necessary
        if clean and self.exists:
            self.remove()

    @property
    def name(self):
        # Get the file name
        return self._name

    @property
    def extension(self):
        # Get the file extension
        return self._extension

    @property
    def filename(self):
        # Get the file name + extension
        return self._filename

    @property
    def exists(self):
        # Get whether file exists in cwd
        return os.path.isfile(self._filename)

    def remove(self):
        # Remove the file if it exists
        if self.exists:
            print('Removing pre-existing file ' + self._filename)
            os.remove(self._filename)


###############################################################################
# Miscellaneous utility functions
###############################################################################
def get_model_name(file_to_search):
    # Get model name by searching file for 'Model' field
    for line in file_to_search:
        if 'Model=' in line:
            return line[len('Model='):-1]  # get model name


def create_dir(name, clean=False):
    # Create new directory
    if os.path.isdir(name) and clean:
        shutil.rmtree(name)  # clean, if necessary
        print('Removing pre-existing directory ' + name)
    os.mkdir(name)
    return name


###############################################################################
# Start of execution
###############################################################################
if __name__ == '__main__':
    print('------------------------------------------------------------------')
    print('>> RUNNING SCRIPT ' + sys.argv[0])
    print('------------------------------------------------------------------')

    base_dir = os.getcwd()

    all_tsp_files = glob('*.tsp')
    for tsp_file in all_tsp_files:
        #######################################################################
        # Use current tsp file 'model' field as archive name.
        #######################################################################
        with open(tsp_file, 'r') as f:
            archive_file = File(name=get_model_name(f),
                                extension='TSW',
                                clean=True)
            f.close()

        #######################################################################
        # Create working dir using file name of current tsp file.
        #######################################################################
        tsp_file_name = tsp_file.split('.')[0]
        working_dir = create_dir(tsp_file_name, clean=True)

        #######################################################################
        # Copy current tsp file (only) and any files without exluded extensions
        # to working dir.
        #######################################################################
        all_files = glob('*.*')
        for file in all_files:
            file_ext = os.path.basename(file).split('.')[1].lower()
            excluded = ['tsp', 'py', 'tsw']
            if (file == tsp_file) or (file_ext not in excluded):
                shutil.copy(file, working_dir)

        #######################################################################
        # Archive working dir using 7-Zip LZMA compression, AES-256 encryption.
        #######################################################################
        # enter working dir
        os.chdir(working_dir)
        # archive using 7-Zip
        subprocess.call([apps.get('7z'),
                         commands.get('add'),
                         switches.get('AES-256 key'),
                         switches.get('content visibility'),
                         switches.get('multi-threading'),
                         switches.get('compression level'),
                         archive_file.filename  # output file
                         ])
        # copy archive out of working dir
        shutil.copy(archive_file.filename, base_dir)

        #######################################################################
        # Exit to base dir and clean up working dir.
        #######################################################################
        os.chdir(base_dir)
        shutil.rmtree(working_dir)
