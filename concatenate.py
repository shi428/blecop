#!/usr/bin/env python
#concatenates mp4 files
import glob
import os
import imageio
from moviepy.video.io.ffmpeg_tools import *
#def concatenate(filename="output.mp4"):
 
if __name__ == "__main__":
    videos = glob.glob("*.mp4")
    with open("files.txt", "w") as fout:
        for i in videos:
            fout.write('file '+i+"\n")
    print videos
    os.system("ffmpeg -f concat -i files.txt -c copy -fflags +genpts merged.mp4")
#    concatenate()
