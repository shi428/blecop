import struct
import matplotlib.pyplot as plt


a = open("../sound", "rb").read()
sound = []
c = 0
for i in range(0, len(a), 4):
	if c % 1000000 == 0:
		print c	
	val = struct.unpack("f", a[i:i+4])
	sound.append(val)
	c += 1
print "START"
plt.plot(sound)
plt.show()
