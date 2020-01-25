import struct
import numpy as np
import IPython
import random
import os
import wavefile
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import sys

def wav_to_floats(filename):
	w = wavefile.load(filename)
	return w[1][0]

signal = wav_to_floats("../penis.wav")
"""
a = open("../sound", "rb").read()
sound = []
c = 0
for i in range(0, len(a), 4):
	if c % 1000000 == 0:
		print c
	val = struct.unpack("f", a[i:i+4])
	sound.append(val)
	c += 1
"""

a = np.array(signal)

# bootstrap to identify a rough speaking volume

y = []
for i in range(1000):
	x = []
	for j in range(100):
		x.append(a[random.randrange(a.size)])
	y.append(max(x))
vol = min(y)

print "START"
gaps = []
i = 0
while i < len(a):
	while i < len(a) and a[i] >= vol: #skip talking frames
		i += 1
	start = i # start of empty
	while i < len(a) and a[i] < vol: #empty range
		i += 1
	if i - start >= 44100:
		gaps.append((start, i)) #stop!
	i += 1
print len(gaps)

"""
with open("indices", "w") as f:
	for i in gaps:
		s = str(i) + "\n"
		f.write(s)
"""
print "START EXTRACT"

ffmpeg_extract_subclip("../penis.mp4", float(gaps[0][0] / 44100.0), float(gaps[0][1] / 44100.0) , targetname="gaplol.mp4")

IPython.embed()
