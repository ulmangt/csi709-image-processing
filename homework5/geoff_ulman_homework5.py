import os, sys, scipy, numpy, Image, sophia, color, fpf
from scipy.fftpack import fft2, ifft2

def main():
  return findBoats( "boatsmall.jpg", 0, 18, "boat", "png" )

def findBoats( image_name, fp, num_train, prefix_train, extension_train ):
  full_image = loadMatrix( image_name )
  boats = loadBoats( num_train, prefix_train, extension_train )
  
  rows = full_image.shape[0]
  cols = full_image.shape[1]

  mat_boats = numpy.zeros( ( num_train, rows * cols ) )
  centered_boats = []
  for i,boat in enumerate( boats ):
    centered_boat = sophia.Plop( boat, rows, cols )
    centered_boats.append( centered_boat )
    mat_boats[i,:] = fft2( centered_boat ).ravel( )

  constraint = numpy.ones( num_train )

  filt = ifft2( fpf.FPF( mat_boats, constraint, fp ).reshape( full_image.shape ) )

  corr = sophia.Correlate( full_image, filt )

  return filt, corr, centered_boats

def loadBoats( num, prefix, extension ):
  boats = []
  
  for i in xrange( num ):
    name = prefix + str(i) + "." + extension
    mat = loadMatrix( name )
    boats.append( mat )
  
  return boats

def loadMatrix( name ):
  image = Image.open( findfile( name ) ).convert( 'L' )
  return sophia.i2a( image ).astype( float ) / 255

# inspired by: http://dotnot.org/blog/archives/2004/03/06/find-a-file-in-pythons-path/
# I wanted a way to automatically find the named image file in the same way python finds imported modules (similar to seaching for resources on the Java classpath)
def findfile( name ):
  for directory in sys.path:
    potential = os.path.join( directory, name )
    if os.path.isfile( potential ):
      return potential

if __name__ == "__main__":
  main()
