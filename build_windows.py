from distutils.core import setup # Need this to handle modules
import py2exe

# We have to import all modules used in our program
from pytube import YouTube
import tkinter as tk
from tkinter import ttk
from tkinter.ttk import *
import os 
import urllib.request
from tkinter import *
import PIL.Image
import PIL.ImageTk
import time
from tkinter.constants import *
from tkinter import messagebox
import datetime;

# Call setup function 
setup(
    options = {'py2exe': {'bundle_files': 1, 'compressed': True}},
    windows=['.\src\ytdwnld.py'], # indicate that we're dealing with an app with a graphical UI 
    zipfile = None,
    ) 