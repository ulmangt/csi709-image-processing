import os, sys
os.chdir( '/home/ulman/CSI709/csi709-image-processing/' )
sys.path.append( 'lib' )
import scipy, numpy, Image, sophia

sys.path.append( 'homework3' )
import geoff_ulman_homework3

evls, emgs = geoff_ulman_homework3.generateEigenImagesDirectory( '/home/ulman/CSI709/csi709-image-processing/test-smaller' )

