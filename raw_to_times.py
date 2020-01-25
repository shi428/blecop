import struct
import numpy
import IPython
import random

a = open("sound", "rb").read()
sound = []
c = 0
for i in range(0, len(a), 4):
	if c % 1000000 == 0:
		print c
	val = struct.unpack("f", a[i:i+4])
	sound.append(val)
	c += 1

a = numpy.array(a)

# bootstrap to identify a rough speaking volume

y = []
for i in range(1000):
	x = []
	for i in range(100):
		x.append(a[random.randrange(a.size)])
	y.append(max(x))
vol = min(y)

indices = []

for i, x in np.nditer(a):
	if x > vol:
		indices.append(i)

curr = 0
start = 0
times = []
for i in indices:
	if i == curr + 1:
		pass
	else:
		times.append((start, curr))
		start = curr
	curr += 1

with open("indices", "w") as f:
	for i in times:
		s = str(times[0]) + str(times[1]) + "\n"
		f.write(s)

IPython.embed()
