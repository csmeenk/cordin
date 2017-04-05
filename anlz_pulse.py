"""anlz_pulse.py
	
	Script to analyze bright and dark regions from a series of high speed images and calculate the signal to noise ratio vs. time.
	
	Output:
		Fig 1. bright signal and dark signal vs. time
		Fig 2. SNR vs. time

Christopher Smeenk
March 8, 2017
"""

import pylab as py

# filename format
fnametempate = 'Frame%03d_16bpp.tiff'
# frame rate
SpeedFPS=1937046.00

t = py.arange(40)/SpeedFPS

# initialize variables for reading in data
ims = []
# bright signal
S = []
Serr = []
# create a mask to filter a bright ROI in the measured images
Smask = py.zeros((1080,1920), dtype=bool)
Smask[500:550,950:1000] = True
# dark signal
D = []
Derr = []
# create a mask to filter a dark ROI in the measured images
Dmask = py.zeros((1080,1920), dtype=bool)
Dmask[50:100,1800:1850] = True

#
# -----------  read the data ----------------------
#
for fnum in range(1,41):
	theim = py.imread(fnametempate % fnum)
	ims.append(theim)
	
	# extract signal intensity & std
	S.append( theim[Smask].mean() )
	Serr.append( theim[Smask].std() )
	
	D.append( theim[Dmask].mean() )
	Derr.append( theim[Dmask].std() )
	
# change formatting of the variables to arrays
S = py.array(S)
Serr = py.array(Serr)
D =  py.array(D)
Derr = py.array(Derr)
# calculate signal to noise ratio
SNR = S/D
SNR_err = py.sqrt(1./D**2 * Serr**2 + S**2/D**4 * Derr**2)

#
# ---------- plot the output -------------------
#
py.figure()
# plot the bright signal
hn1=py.errorbar(t*1e6,S,yerr=Serr,marker='x',markersize=10,markeredgewidth=2,ls='None')
# plot the dark signal
hn2=py.errorbar(t*1e6,D,yerr=Derr,marker='o',markersize=10,markeredgewidth=2,ls='None')
py.xlabel('time [$\mu$s]')
py.ylabel('signal [arb.]')
py.title('2017-03-08  flashlamp pulse (%1.3g Mfps)' % (SpeedFPS/1e6))
py.legend((hn1[0],hn2[0]), ('bright signal','dark signal'), numpoints=1)

py.figure()
py.errorbar(t*1e6, SNR, marker='s',markersize=10,markeredgewidth=2,ls='None')
py.xlabel('time [$\mu$s]')
py.ylabel('Bright/dark signal []')
py.title('2017-03-08  flashlamp SNR (%1.3g Mfps)' % (SpeedFPS/1e6))
