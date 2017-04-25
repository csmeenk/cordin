# Utility functions for reading & processing Cordin images

import struct
import numpy as py

def readraw(filename):
	"""readraw(filename)
		
		Read an image in binary .raw format.
	"""
	
	fid = open(filename, 'rb')
	rawdata = fid.read()
	fid.close()

	datalen=1920*1080
	rescale = 2.**14/2.**16
	fmt = '<' + str(datalen) + 'H'
	data = struct.unpack(fmt, rawdata)
	rdata = rescale*py.reshape(data,(1080,1920))
	
	# additional manipulation for even vs. odd frames. 
	# Frames 1-10, 31-40 are located on one side of the system.
	# Frames 11-30 are located on the opposite side
	
	# get the frame number
	framenum = int( filename.split('_')[1] )
	
	if framenum<11 or framenum>30:   # frame is from one bank
		if (framenum % 2):
			# frame is odd
			data_out = py.flipud(rdata)
		else:
			# frame is even
			data_out = py.fliplr(rdata)
	else: # frame is from the second side (11 <= framenum <= 30)
		if (framenum % 2):
			# frame is odd
			data_out = py.fliplr(rdata)
		else:
			# frame is even
			data_out = py.flipud(rdata)
	
	#data_out=rdata		
	return data_out
