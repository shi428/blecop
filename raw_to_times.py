#!/usr/bin/python
import os
import struct
import numpy as np
import random
import os
import wavefile
import sys
import glob

def convert_mp4(fname, dest):
	
	abs_file_path = os.path.abspath(fname)
	name = os.path.basename(abs_file_path)
	name_without_extension = name.split(".")[0]
        abs_without_extension = abs_file_path.replace(".mp4", "")
	print(name)
	print(abs_file_path)

	print("Obtaining audio stream")
	os.system("ffmpeg -hide_banner -loglevel warning -i {fpath} -vn -acodec pcm_s16le -ar 44100 -ac 2 ./{out:}.wav".format(
			fpath=abs_file_path,
			out=name_without_extension
	))

	vols = np.array(
			wavefile.load("./{fname:}.wav".format(fname=name_without_extension))[1][0]
	)

	size = vols.size

	vol = min(
			[
					max([vols[random.randrange(size)] for j in range(100)]) for i in range(1000)
			]
	)

	# bootstrap to identify a rough speaking volume

	print("Identifying frames")
	gaps = []
	i = 0
	start = 0
	while i < size:
			while i < size and vols[i] >= vol:
					i += 1
			start = i

			while i < size and vols[i] < vol:
					i += 1
			if i - start >= 44100:
					gaps.append((start, i))	

	start = 0
	talks = []

	def timestamp(seconds):
		hours = int(seconds) // 3600
		seconds -= hours * 3600
		minutes = int(seconds) // 60
		seconds -= minutes * 60
		seconds = round(seconds, 3)
		return str(hours).zfill(2) + ":" + str(minutes).zfill(2) + ":" + "%06.3f" % seconds

	split_cmd = "ffmpeg -hide_banner -loglevel warning -ss {start} -i {name}.mp4 -t {length} -async 1 ./{filename}"

	fout = open("./files.txt", "w")
	print("EXTRACTING")
	c = 0
	for i in range(len(gaps)):
		if (gaps[i][0] / 44100.0 - start / 44100.0) > 2:
			print(start / 44100.0, timestamp(start / 44100.0))
			print(gaps[i][0]-start) / 44100.0, timestamp((gaps[i][0]-start) / 44100.0)
			os.system(split_cmd.format(start=timestamp(start / 44100.0), length=timestamp(gaps[i][0] / 44100.0 - start / 44100.0), filename="segment{}.mp4".format(c), name=abs_without_extension))
			fout.write("file segment{}.mp4\n".format(c))
			c += 1
		start = gaps[i][1]
	fout.close()

	print("COMBINING")

	os.system("ffmpeg -f concat -i ./files.txt -c copy {}".format(dest))
	os.system("rm ./segment*")
	os.system("rm ./files.txt")
	os.system("rm *.wav")
convert_mp4(sys.argv[1], sys.argv[2])
