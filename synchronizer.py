#!/usr/bin/env python3

import subprocess
import configparser
import json
import zipfile
from datetime import datetime
import os
import time

CFG_FILE="synchronizer.ini"
LAST_UPDATE_FILE=".lastupdate"

def readConfig():
    """
    Read config specified in CFG_FILE.
    """

    config = configparser.ConfigParser()
    config.read(CFG_FILE)

    return config

def checkLastUpdate(config):
    """
    Checks the last update of the files.

    Args:
        config - ConfigParser object

    Returns:
        bool - True if archive is newer than timestamp in .lastupdate file.
               False if archive is older than timestamp in .lastupdate file.
    """

    line = ""

    if os.path.isfile(LAST_UPDATE_FILE):
        with open(LAST_UPDATE_FILE,'r') as f:
            line = f.readline()
    else:
        print("File {0} doesn't exists. Creating it.".format(LAST_UPDATE_FILE))
        with open(LAST_UPDATE_FILE,'w') as f:
            f.write("")
        # Update in case the file is missing - first run
        return True

    archive_path = config.get("Archive","path")

    if not os.path.isfile(archive_path):
        print("ERROR: File {0} is not a file.".format(archive_path))
        return False

    if line:
        datetime.fromtimestamp(os.path.getmtime(archive_path))
        return True
    else:
        print("ERROR: File {0} is empty. Should contain time of last update.".format(LAST_UPDATE_FILE))
        return False

########### MAIN #################

if __name__ == "__main__":
    config = readConfig()
    print(datetime.fromtimestamp(os.path.getmtime(CFG_FILE)))
    print(datetime.now())

    if not config:
        print("ERROR: Configuration file {0} was not loaded".format(CFG_FILE))
        exit(1)

    checkLastUpdate(config)
