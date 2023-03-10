from moviepy.editor import *
import os
import glob


def MP4ToMP3(mp4, mp3):
    FILETOCONVERT = AudioFileClip(mp4)
    FILETOCONVERT.write_audiofile(mp3)
    FILETOCONVERT.close()

base_path = "/home/superx/Documents/scripts"

os.chdir(base_path+"/mp4")
for file in glob.glob("*.mp4"):
    print(file)
    name = os.path.splitext(file)[0]
    AUDIO_FILE_PATH = base_path+"/mp3/"+name+".mp3"
    MP4ToMP3(file, AUDIO_FILE_PATH)
