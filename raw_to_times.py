import struct
import numpy as np
#import IPython
import random
import os
import wavefile
import sys
import glob


name = sys.argv[1].split(".")[0]

convcmd = "ffmpeg -i ../{} ../{}.mpeg".format(sys.argv[1], name)

wavcmd = "ffmpeg -i ../{} -vn -acodec pcm_s16le -ar 44100 -ac 2 ../{}.wav".format(sys.argv[1], name)

print convcmd
exit()
os.system(convcmd)
os.system(wavcmd)

def wav_to_floats(filename):
	w = wavefile.load(filename)
	return w[1][0]

signal = wav_to_floats("../{}.wav".format(name))

a = np.array(signal)

# bootstrap to identify a rough speaking volume

for i in range(1):
    y = []
    for i in range(1000):
	x = []
	for j in range(100):
	    x.append(a[random.randrange(a.size)])
	y.append(max(x))
    vol = min(y)
    print(vol)

#exit()

print "START"
gaps = []
i = 0
#while i < len(a):
#	while i < len(a) and a[i] >= vol: #skip talking frames
#		i += 1
#	start = i # start of empty
#	while i < len(a) and a[i] < vol: #empty range
#		i += 1
#	if i - start >= 44100:
#		gaps.append((start, i)) #stop!
for i,x in np.ndenumerate(a):
    if a[i] >= vol:
        continue
    start = i
    if a[i] < vol:
        continue
    if i - start >= 44100:
        gaps.append(start + 22050, i - 22050)
print(gaps)
exit()


start = 0

talks = []

def timestamp(seconds):
	hours = int(seconds) // 3600
	seconds -= hours * 3600
	minutes = int(seconds) // 60
	seconds -= minutes * 60
	seconds = round(seconds, 3)
	return str(hours).zfill(2) + ":" + str(minutes).zfill(2) + ":" + "%06.3f" % seconds

cmd = "ffmpeg -ss {start} -i ../{name}.mpeg -t {length} -vcodec copy -acodec copy ../{filename}"

fout = open("../files.txt", "w")
print "EXTRACTING"
c = 0
for i in range(len(gaps)):
	if (gaps[i][0] / 44100.0 - start / 44100.0) > 2:
		print start / 44100.0, timestamp(start / 44100.0)
		# print gaps[i][0] / 44100.0, timestamp(gaps[i][0] / 44100.0)
		print (gaps[i][0]-start) / 44100.0, timestamp((gaps[i][0]-start) / 44100.0)
		os.system(cmd.format(start=timestamp(start / 44100.0), length=timestamp(gaps[i][0] / 44100.0 - start / 44100.0), filename="segment{}.mpeg".format(c), name=name))
		fout.write("file segment{}.mpeg\n".format(c))
		c += 1
	start = gaps[i][1]

fout.close()
print "COMBINING"

os.system("ffmpeg -f concat -i ../files.txt -c copy -fflags +genpts ../merged.mpeg")
print "DELETING"
os.system("rm ../segment*")
