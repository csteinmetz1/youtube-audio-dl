from __future__ import print_function
import os
import sys
import subprocess
import re
import string
import pafy

# place list of YouTube video URLs to donwload in a .txt file

def getAudio(youTubeURL):
    audio = pafy.new(youTubeURL)
    audioStream = audio.getbestaudio(preftype="m4a", ftypestrict=True)
    pattern = re.compile('[\W_]+', re.UNICODE)
    filename = audio.title.encode('utf-8').replace(" ", "_").strip('\n') # remove whitespace & newlines
    filename = pattern.sub('_', filename) # remove non-alphanumeric chars - these cause problems with locating the file
    print('Downloading ', filename)
    audioOutput = audioStream.download(filepath="./downloads/" + filename + ".m4a")
    return filename

def convertAudio(m4aAudio):
    """ Convert m4a audio file to mp3 using ffmpeg """
    ffmpeg_call = """ffmpeg -i \"./downloads/%s.m4a\" \"./downloads/%s.mp3\"""" %(m4aAudio, m4aAudio)
    subprocess.call(ffmpeg_call, shell=True)
    os.remove("./downloads/" + m4aAudio + ".m4a")

def main(filename):
    with open("youTubeURLs.txt", "r") as youTubeURLs:
        # iterate through each URL in the file
        for youTubeURL in youTubeURLs.read().split():
            m4aAudio = getAudio(youTubeURL) # get audio stream from YT and filename
            convertAudio(m4aAudio) # convert to mp3

if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        main(filename)
    else:
        print("Usage: python pyYTaudio.py path_to_file")