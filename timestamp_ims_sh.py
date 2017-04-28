#!/usr/bin/python
# -*- coding: utf-8 -*-
"""timestamp_ims_sh.py

	A script to insert timestamps into a set of images. The images must be numbered sequentially (im001.jpg, im002.jpg, ...). This script is intended to run from the command line e.g.:
	$ timestamp_ims_sh.py filename fps tstart magnification
	
	To extract the images from an avi file use:
	$ mplayer inputfile.avi -vo jpeg:subdirs=outputdir -ao null

	
	Optionally write the images to an .avi movie using:
	$ mencoder "mf://tstamp/*_tstamp.jpg" -mf fps=10 -o tstamp/newanim.avi -ovc lavc -lavcopts vcodec=msmpeg4v2

"""

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import glob, os, sys

class TextLabel():
	def __init__(self, p=(0,0), c=255, size=70):
		self.position = p # (x,y)
		self.color = c  # (r,g,b) or integer for grayscale images
		self.font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", size)
	
	def set_color(self, thecolor):
		self.color = thecolor
	
	def set_fontsize(self, sz):
		self.font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", sz)
		
def draw_timestamp(theimage, time, text):
	
	draw = ImageDraw.Draw(theimage)
	# draw.text((x, y),"Sample Text",(r,g,b))
	if tstep > 5e-3:
		# write in seconds
		draw.text(text.position,'t=%.1f s' % time,text.color,font=text.font)
	elif tstep > 1e-4:
		# write in milliseconds
		draw.text(text.position,'t=%.1f ms' % (time*1e3), text.color,font=text.font)
	else:
		# write in microseconds
		draw.text(text.position,'t=%.1f us' % (time*1e6), text.color,font=text.font)


def draw_scale_bar(theimage, mag, text):
	"""draw_scale_bar(theimage, mag)
	
	Draw a scale bar using a length calibration stored in SCALE.
	"""
	# determine the type of image (RGB vs. monochrome)
	if len( theimage.getbands() ) > 1:
		# RGB - ispeed
		thescale = SCALE['ispeed'][mag]  # um/pixel
		line_start = 1050
	else:
		# monochrome - cordin
		thescale = SCALE['cordin'][mag]  # um/pixel
		line_start = 1600
	
	draw = ImageDraw.Draw(theimage)
	
	# draw a line 35 um long
	line_length = 35./thescale   # pixels
	line_end = line_start + line_length
	
	draw.line([(line_start,20), (line_end,20)], fill=text.color, width=5)
	draw.text((line_start,45), '35 um', text.color, font=text.font)
	

# --------- User define the following parameters --------- #

if len(sys.argv) != 5:
	print "Error in " + __file__
	sys.exit("Insufficient number of arguments.")

# leading characters on the file names
filename = sys.argv[1]
file_ext = os.path.splitext(filename)

# time settings
fps = float(sys.argv[2])
tstart = float(sys.argv[3])   # time of the first frame

# magnification (=20,60, or 120)
M = int(sys.argv[4])

# set the font
thefont = TextLabel()
# font = ImageFont.truetype(<font-file>, <font-size>)
#font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", fontsize)

# ----------- End user defined parameters ---------------- #

# scale calibration vs. objective magnification
SCALE = {'ispeed':{20:1.085, 60:0.343, 120:0.18}, 'cordin':{20:0.63, 60:0.205, 120:0.100} }

savedir = "tstamp"
try:
	os.mkdir(savedir)
except OSError:
	pass
tstep = 1./fps
t = 0. + tstart  # initialize the time

if file_ext[0] == '*':
	filelist = glob.glob(filename)
else:
	filelist = glob.glob(file_ext[0] + '*' + file_ext[1])
filelist.sort()


for fname in filelist:
	img = Image.open(fname)
	
	# check if image is an RGB image
	if len( img.getbands() ) > 1 and thefont.color.__class__ == int:
		# expand text color definition
		#text_color = tuple( [grey_text_color]*3 )
		initial_color = 0 + thefont.color
		thefont.set_color( (255,255,255) )#tuple( [initial_color]*3 )
		
	# add the time stamp
	draw_timestamp(img, t, thefont)
	# add the scale bar
	draw_scale_bar(img, M, thefont)
	
	# update the time
	t += tstep
	
	# revised filename
	old_fname = os.path.splitext(fname)
	new_fname = old_fname[0] + '_tstamp' + old_fname[1]
	img.save( os.path.join(savedir,new_fname) )
