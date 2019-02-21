#!/usr/bin/env python3
"""
    Purpose:
        Helper Library for interacting with directories in an environment.
"""

# Python Library Imports
import os
import sys
import logging
import shutil
from zipfile import ZipFile, ZIP_DEFLATED

# Local Library Import
from data_structures import dict_helpers


###
# Directory Helpers
###


def create_directories(
    directory_structure, base_dir=".", overwrite=False, permissions=0O755
):
    """
    Purpose:
        Make directories matching the hierarchy passed in directory_structure.
        If overwrite is set to False, existing directories will be kept.
    Args:
        directory_structure (Dictionary of Dictionariess): Dictionariess
            detailing the hierarchy of directories to create
        base_dir (String): Path to the location where the directories will be
            created
        overwrite (Boolean): Whether or not to overwrite the directory if
            initializing a method/attack that already exists
    Returns:
        N/A
    """
    logging.info(
        f"Creating directories in {base_dir} (overwrite = {overwrite}: "
        "{directory_structure}"
    )

    paths = dict_helpers.flatten_dict_keys(directory_structure, only_leaves=True)
    full_paths = [f"{base_dir}/{path}" for path in paths]
    paths_that_exist, paths_that_dont_exist = check_directories_exist(full_paths)

    if not overwrite and paths_that_exist:
        error_msg =\
            f"Directories already exist and overwrite set to false, "\
            "Failing: {paths_that_exist}"
        logging.error(error_msg)
        raise Exception(error_msg)

    for path in paths_that_exist:
        logging.info(f"Removing Path {path} and all of its files")
        shutil.rmtree(path, ignore_errors=True)
    for path in full_paths:
        logging.info(f"Creating Path {path}")
        os.makedirs(path, permissions)


def check_directories_exist(paths):
    """
    Purpose:
        Takes in a list of directories and returns which ones do and do not exist
    Args:
        paths (List of Strings): List of directories to check for the
            existance of on the operating system. these should be full paths or
            relative paths to the current process execution
    Returns:
        paths_that_exist (List of Strings): Directories that do exist in the OS
        paths_that_dont_exist (List of Strings): Directories that do not exist in
            the OS
    """

    paths_that_exist = [path for path in paths if os.path.isdir(path)]
    paths_that_dont_exist = [path for path in paths if not os.path.isdir(path)]

    return paths_that_exist, paths_that_dont_exist


def zip_directory(dir_to_zip, zip_filename=None, overwrite=False):
    """
    Purpose:
        Takes in a directory on the OS and will create a .zip archive of the directory.
        Will use the name of the directory for zippping if one is not specified
    Args:
        dir_to_zip (String): Path to the dir that will be zipped
        zip_filename (String): Filename of the resulting .zip file
        overwrite (Boolean): Whether or not to overwrite the zipfile if it alread exists
    Returns:
        N/A
    """

    if not zip_filename:
        zip_filename = "{0}.zip".format(dir_to_zip.split("/")[-1])

    if not os.path.isdir(dir_to_zip):
        error_msg = "Directory doesn't exist, cannot zip nothing"
        logging.error(error_msg)
        raise Exception(error_msg)
    elif not overwrite and os.path.isfile(zip_filename):
        error_msg = "ZipFile already exists, and overwrite set to False, Failing"
        logging.error(error_msg)
        raise Exception(error_msg)

    with ZipFile(zip_filename, 'w', ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(dir_to_zip):
            for file in files:
                zipf.write(os.path.join(root, file))
