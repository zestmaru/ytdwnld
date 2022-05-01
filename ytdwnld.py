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

# Init GUI
root = tk.Tk()
root.title("ytdwnld") # Ttile
root.geometry('800x800') # Window size

# Apply the grid layout
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)

# Init tabs
tabControl = ttk.Notebook(root)
tab1 = ttk.Frame(tabControl) # Main tab
tab2 = ttk.Frame(tabControl) # About tab
tab3 = ttk.Frame(tabControl) # Debug tab

tabControl.add(tab1, text ='Download')
tabControl.add(tab2, text ='About')
tabControl.add(tab3, text ='Debug')

# Show Tabs
tabControl.pack(expand = 1, fill ="both")

# TextBox Creation
inputText = tk.Text(tab1,
                   height = 1,
                   width = 100)

# Placing the inputText at
# the middle of the root window
# relx and rely should be properly
# set to position the label on
# root window
inputText.place(anchor = 'w')

# Show inputText
inputText.pack()


def downloadButton(target):

    ''' 
    Function to download video or audio by accepting param string 'target' 
    
    :param target: 'video' or 'audio'
    :return: void
    '''

    # Get user string from inputText
    input = inputText.get(1.0, "end-1c")

    yt = YouTube(input) # Init pytube

    # Get video info into string
    videoInfo = "Title: {} \n\n Number of views: {} \n\n Length of video: {} seconds \n\n Description: {} \n\n".format(yt.title, 
                                                                                    yt.views, yt.length, yt.description)

    # Update videoInfoLabel on every new yt link
    videoInfoLabel.config(text = videoInfo)

    # Get video thumbnail url
    imageUrl = yt.thumbnail_url

    # Download thumbnail
    urllib.request.urlretrieve(
                        imageUrl,
                        "thumbnail.png")

    # Open this image with pillow library
    im = PIL.Image.open("thumbnail.png")

    # Set thumbnail x, y
    im.thumbnail((400, 400))

    # ??? PhotoImage from pillow library
    photo = PIL.ImageTk.PhotoImage(im)

    # Update imageLabel on every new yt link with new photo
    imageLabel.config(image = photo)

    # ??? Strange reference
    imageLabel.image = photo

    time.sleep(2) # Hold the horses

    # ct stores current time
    # used for debug
    ct = datetime.datetime.now()

    if target == 'video':

        # Remove video if exists
        videoName=yt.title+".mp4"
        if os.path.exists(videoName):
            os.remove(videoName)

        # Pass streams info into debug tab
        streams = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution')
        streamsInfo = "[{}] [VIDEO:: {}]\nStreams info: {}\n\n".format(ct, yt.title, streams)
        debugInfoTextBox.insert(tk.END, streamsInfo)

        # Download highest quality video
        downloadStream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution')[-1]
        downloadInfo = "[{}] [VIDEO:: {}]\nDOWNLOADING STREAM: {}\n\n".format(ct, yt.title, downloadStream)
        debugInfoTextBox.insert(tk.END, downloadInfo)
        return yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution')[-1].download()

    elif target == 'audio':

        # If video exists then just copy it and rename to mp3 instead of download...
        videoName=yt.title+".mp4"
        if os.path.exists(videoName):
            os.remove(videoName)

        # Remove audio if exists
        audioName=yt.title+".mp3"
        if os.path.exists(audioName):
            os.remove(audioName)

        # Pass streams info into debug tab
        streams = yt.streams.filter(only_audio=True)
        streamsInfo = "[{}] [AUDIO:: {}]\nStreams info: {}\n\n".format(ct, yt.title, streams)
        debugInfoTextBox.insert(tk.END, streamsInfo)
        
        # Download audio
        downloadStream = yt.streams.get_audio_only()
        downloadInfo = "[{}] [AUDIO:: {}]\nDOWNLOADING STREAM: {}\n\n".format(ct, yt.title, downloadStream)
        debugInfoTextBox.insert(tk.END, downloadInfo)

        yt.streams.get_audio_only().download()

        # Rename mp4 to mp3
        os.rename(yt.title+".mp4", yt.title+".mp3")
        
def onClosing():

    '''
    Show warning modal window if user trying to close app

    :return: void
    '''

    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        # Delete thumbnail image if exists
        if os.path.exists("thumbnail.png"):
            os.remove("thumbnail.png")
        # Destroy GUI
        root.destroy()

# Hack things
def audio():
    downloadButton("audio")
def video():
    downloadButton("video")

# downloadVideoButton init
downloadVideoButton = tk.Button(tab1,
                        text = "Download video", 
                        command = video)
downloadVideoButton.place(anchor = 'w')
downloadVideoButton.pack()

# downloadAudioButton init
downloadAudioButton = tk.Button(tab1,
                        text = "Download audio", 
                        command = audio)
downloadAudioButton.place(anchor = 'e')
downloadAudioButton.pack()  

# Image init
imageLabel = Label(tab1)
imageLabel.pack()

# Video info init
videoInfoLabel = tk.Label(tab1, text = "")
videoInfoLabel.pack()

# TODO: PROGRESS BAR
# bar= Progressbar(tab1, length=300)
# bar.pack(pady=20)

# Init About text 
aboutLabel = ttk.Label(tab2,
          text ="ytdwnld\n\nVersion 1.0.0r0~xxxxx").grid(column = 0,
                                    row = 0, 
                                    padx = 30,
                                    pady = 30)


# Init debug info
debugInfoTextBox = tk.Text(tab3,
                   height = 100,
                   width = 100)
debugInfoTextBox.pack()

# Create a scrollbar widget and set it's command to the text widget
scrollbar = ttk.Scrollbar(root, orient='vertical', command=debugInfoTextBox.yview)

# Communicate back to the scrollbar
debugInfoTextBox['yscrollcommand'] = scrollbar.set





# == footer ==
# Execute onClosing 
root.protocol("WM_DELETE_WINDOW", onClosing)

# Execute Tkinter
root.mainloop()