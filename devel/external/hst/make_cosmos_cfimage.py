# Copyright (c) 2012-2022 by the GalSim developers team on GitHub
# https://github.com/GalSim-developers
#
# This file is part of GalSim: The modular galaxy image simulation toolkit.
# https://github.com/GalSim-developers/GalSim
#
# GalSim is free software: redistribution and use in source and binary forms,
# with or without modification, are permitted provided that the following
# conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions, and the disclaimer given in the accompanying LICENSE
#    file.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions, and the disclaimer given in the documentation
#    and/or other materials provided with the distribution.
#
"""@file make_cosmos_cfimage.py Makes a high SNR estimate of noise correlation function in F814W
COSMOS science stacks.

Uses a pickled list of cutout images from empty regions of noise from unrotated coadds in the COSMOS
F814W data, stored in the file NOISEIMFILE (see below).  The noise images were cut from the images:

acs_I_095921+0228_unrot_sci_20.fits
acs_I_100210+0246_unrot_sci_20.fits
acs_I_100236+0209_unrot_sci_20.fits
acs_I_100249+0209_unrot_sci_20.fits
acs_I_100303+0152_unrot_sci_20.fits

provided by Alexie Leauthaud.

This list consistes of 92 NumPy arrays of various sizes and shapes, all containing no discernable
objects, visually selected from the science data.

The pickled list of objects is stored at the GREAT3 Dropbox account as it is ~90MB in size, in a
non-public folder.  This folder will be happily shared with anyone who is interested, however, so
please just email barnaby.t.p.rowe@gmail.com to request sharing.

The output of stacking and averaging the correlation function from the 92 individual noise fields is
saved to CFIMFILE (see below), and some illustrative plots in linear and log space are generated in
PNG format.
"""

import os
import cPickle
import numpy as np
import galsim

# Subtract off the mean for each field explicitly (bg subtraction never perfect)?
# There does seem to be a consistent positive bg around giving a constant CF of 2.4e-7 (~2% of peak)
# that we might want to remove.  See the Pull Request #366 on GalSim's Github site.
SUBTRACT_MEAN=True

NOISEIMFILE = "acs_I_unrot_sci_20_noisearrays.pkl"  # Input pickled list filename
if SUBTRACT_MEAN:
    CFIMFILE = "acs_I_unrot_sci_20_cf_subtracted.fits" # Output image of the correlation function
else:
    CFIMFILE = "acs_I_unrot_sci_20_cf_unsubtracted.fits" # Output image of the correlation function
CFPLOTFILE = "acs_I_unrot_sci_20_cf.png"            # Plot (linear) of the output CF 
CFLOGPLOTFILE = "acs_I_unrot_sci_20_log10cf.png"    # Plot (log) of the output CF
NPIX = 81                                           # Make an image of the final correlation
                                                    # function that is NPIX by NPIX

if not os.path.isfile(CFIMFILE): # If the CFIMFILE already exists skip straight through to the plots
    # Read in the pickled images
    noiseims = cPickle.load(open(NOISEIMFILE, 'rb'))
    # Loop through the images and sum the correlation functions
    hst_ncf = None
    bd = galsim.BaseDeviate(12345) # Seed is basically unimportant here
    for noiseim in noiseims:
        noiseim = noiseim.astype(np.float64)
        if hst_ncf is None:
            # Initialize the HST noise correlation function using the first image
            hst_ncf = galsim.CorrelatedNoise(
                bd, galsim.ImageViewD(noiseim), correct_periodicity=True,
                subtract_mean=SUBTRACT_MEAN)
        else:
            hst_ncf += galsim.CorrelatedNoise(
                bd, galsim.ImageViewD(noiseim), correct_periodicity=True,
                subtract_mean=SUBTRACT_MEAN)
    hst_ncf /= float(len(noiseims))
    # Draw and plot an output image of the resulting correlation function
    cfimage = galsim.ImageD(NPIX, NPIX)
    hst_ncf.draw(cfimage, dx=1.)
    # Save this to the output filename specified in the script header
    cfimage.write(CFIMFILE)
else:
    cfimage = galsim.fits.read(CFIMFILE)

# Then make nice plots
import matplotlib.pyplot as plt
plt.clf()
plt.pcolor(cfimage.array, vmin=0.)
plt.axis((0, NPIX, 0, NPIX))
plt.colorbar()
plt.set_cmap('hot')
plt.title(r'COSMOS F814W-unrotated-sci noise correlation function')
plt.savefig(CFPLOTFILE)
plt.show()
plt.clf()
plt.pcolor(np.log10(cfimage.array + 1.e-7))
plt.axis((0, NPIX, 0, NPIX))
plt.colorbar()
plt.set_cmap('hot')
plt.title('log10 COSMOS F814W-unrotated-sci noise correlation function')
plt.savefig(CFLOGPLOTFILE)
plt.show()        
