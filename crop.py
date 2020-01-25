#!/usr/bin/env python 
import imageio
imageio.plugins.ffmpeg.download()
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import sys
if __name__ == "__main__":
    ffmpeg_extract_subclip(sys.argv[1], float(sys.argv[2]), float(sys.argv[3]) , targetname=None)
