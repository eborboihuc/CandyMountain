#!/usr/bin/env python2
# Import libraries
from os import remove as remove
from os import system as execute
from os import name as system

def getFullscreen():
    # Open file
    f = open("settings.txt", "r+")
    fl = list(f)

    # Check if fullscreen is True or False
    if fl[0] == "fullscreen=True\n":
        return True
    elif fl[0] == "fullscreen=False\n":
        return False

    # Close the file
    f.close()

def changeFullscreen():
    # Open file
    f = open("settings.txt", "r+")
    fl = list(f)

    # Check if fullscreen is True or False
    if fl[0] == "fullscreen=True\n":
        fs = True
    elif fl[0] == "fullscreen=False\n":
        fs = False

    # Close the file
    f.close()

    # Remove the file
    remove("settings.txt")

    # Make a new file
    if system == "nt":
        execute("type NUL > settings.txt")
    elif system == "posix":
        execute("touch settings.txt")
    nf = open("settings.txt", "r+")

    # Change fullscreen
    if fs:
        nf.write("fullscreen=False\n")
    elif not fs:
        nf.write("fullscreen=True\n")

    # Close the new file
    nf.close()
