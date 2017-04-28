# High Speed Imaging
Repository for image and video processing software used for annotating and analyzing high speed imaging data.

### cordin.py
Utility functions for reading & processing Cordin images.

### anlz_pulse.py
Script to analyze bright and dark regions from a series of high speed images and calculate the signal to noise ratio vs. time.

### timestamp_file.sh
Script to add time stamp values onto a .avi video. Usage: 
```bash
$ timestamp_file.sh filename.avi fps starttime
```

### timestamp_ims_sh.py
A script to insert timestamps into a set of images. The images must be numbered sequentially (im001.jpg, im002.jpg, ...). Usage:
```bash
$ timestamp_ims_sh.py filename fps tstart magnification
```
