from __future__ import print_function
import os
import sys
import subprocess
import re
import string
import pafy

##################################################################
## NOTE:                                                        ##
## Place list of YouTube video URLs to donwload in a .txt file  ##
## (ensure the URLs are newline delimited)                      ##
## if no ouput directory is specified current directory is used ##
##################################################################

def get_audio(youTubeURL, dl_dir):
    """ Use pafy to download m4a audio stream """
    audio = pafy.new(youTubeURL)
    audio_stream = audio.getbestaudio(preftype="m4a", ftypestrict=True)
    pattern = re.compile('[\W_]+', re.UNICODE)
    filename = audio.title.encode('utf-8').replace(" ", "_").strip('\n') # remove whitespace & newlines
    filename = pattern.sub('_', filename) # remove non-alphanumeric chars - these cause problems with locating the file
    print('Downloading ', filename)
    filepath = os.path.join(dl_dir, filename + ".m4a")
    audio_output = audio_stream.download(filepath=filepath)
    return filename

def convert_audio(m4a_audio, dl_dir):
    """ Convert m4a audio file to mp3 using ffmpeg """
     ########### FIX THIS ###########
    ffmpeg_call = """ffmpeg -i \"%s/%s.m4a\" \"%s/%s.mp3\"""" %(dl_dir, m4aAudio, dl_dir, m4aAudio)
    subprocess.call(ffmpeg_call, shell=True)
    os.remove(os.path.join(dl_dir, m4aAudio + ".m4a"))

def normalize_audio(audio, dl_dir):
    m4a_path = os.path.join(dl_dir, audio + ".m4a")
    mp3_path = os.path.join(dl_dir, audio + ".mp3")
    ffmpeg_normalize_call = """ffmpeg-normalize --threshold 0 --force \"%s\" --format mp3""" %(m4a_path)
    print("Normalizing audio stream. Wait...\n")
    subprocess.call(ffmpeg_normalize_call, shell=True)
    os.remove(m4a_path)

def normalize_audio_manual(mp3_audio, dl_dir):
    """ *Unused function*

    Uses only ffmpeg to read peak value and normalize.
    This requires capturing the output of the volume detect
    function and parsing it for max_volume and then by performing
    the peak maximization with another ffmpeg call. Would prefer 
    not to need the ffmpeg-normalize lib as a dependancy.    

    """
    mp3_path = os.path.join(dl_dir, mp3_audio + ".mp3")
    ffmpeg_call = """ffmpeg -i %s -af \"volumedetect\" -vn -sn -dn -f null /dev/null""" %(mp3_path)
    audio_analysis = subprocess.check_output(ffmpeg_call, stderr=subprocess.STDOUT, shell=True)
    max_volume = audio_analysis.find("max_volume")
    max_volume_db = audio_analysis[max_volume+13:max_volume+16]
    ffmpeg_call = """ffmpeg -i \"%s\" -af \"volume=%sdB\" -c:v copy -c:a libmp3lame -q:a 1 \"%s\"""" %(mp3_path, max_volume_db, mp3_path)
    subprocess.call(ffmpeg_call, shell=True)

def main(filename, dl_dir):
    with open(filename, "r") as youTubeURLs:
        # iterate through each URL in the file
        num_videos = 0
        for youTubeURL in youTubeURLs.read().split():
            normalize_audio(get_audio(youTubeURL, dl_dir), dl_dir) # peak normalize the stream (lectures tend to be quiet)
            num_videos += 1
        print("Donwloaded and converted %d video(s)" %(num_videos))

if __name__ == "__main__":
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        dl_dir = os.getcwd()
        main(filename, dl_dir)
    elif len(sys.argv) == 3:
        filename = sys.argv[1]
        dl_dir = sys.argv[2]
        main(filename, dl_dir)
        
    else:
        print("Usage: python pyYTaudio.py path_to_txt_file path_to_save_dir")