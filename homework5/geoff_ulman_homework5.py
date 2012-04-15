import os, sys, scipy, numpy, Image, sophia, color, fpf
from scipy.fftpack import fft2, ifft2
from scipy.signal import convolve2d
from scipy.ndimage.measurements import label
from scipy import zeros, ones

def main_allboats( fp=0 ):
  """
  Train to detect all 18 boat images and provide two clutter images which are
  trained against (images of the shiny peaks on the docks).
  """
  boats = loadImages( 18, "boat_images/boat", "png" )
  clutter = loadImages( 2, "boat_images/clutter", "png" )
  return findBoats( fp, "boat_images/boatsmall.jpg", boats, clutter )


def main_missingboat( fp=0 ):
  """
  Train to detect 16 of the boat images and train against the two large
  boat images on the southern portion of the dock.
  """
  boats = loadImages( 16, "boat_images/boat", "png" )
  clutter = [ loadMatrix( "boat_images/boat16.png" ), loadMatrix( "boat_images/boat17.png" ) ]
  return findBoats( fp, "boat_images/boatsmall.jpg", boats, clutter )


def findBoats( fp, image_name, boats, clutter ):

  # load the full boats image
  full_image = loadMatrix( image_name )
  
  # get the dimensions of the boat image
  rows = full_image.shape[0]
  cols = full_image.shape[1]

  # combine the boats ( constraint=1 )
  # and the clutter ( constraint=0 ) images 
  images = []
  images.extend( boats )
  images.extend( clutter )

  # construct a matrix with one rwo for each image
  mat_images = numpy.zeros( ( len( images ), rows * cols ), complex )
  centered_images = []

  # loop through each image, centering it in a frame the
  # size of the originial boats image
  # then perform a 2d fft and place the raveled image
  # into a row of the matrix
  for i,image in enumerate( images ):
    centered_image = sophia.Plop( image, rows, cols )
    centered_images.append( centered_image )
    if fp == 0:
      mat_images[i,:] = centered_image.ravel( )
    else:
      mat_images[i,:] = fft2( centered_image ).ravel( )

  # build the constraint vector
  constraint = numpy.append( numpy.ones( len( boats ) ), numpy.zeros( len( clutter ) ) )

  # use FPF to build the fractional power filter which will
  # be correlated with the original image
  if fp == 0:
    filt = fpf.FPF( mat_images, constraint, fp ).reshape( full_image.shape )
  else:
    filt = ifft2( fpf.FPF( mat_images, constraint, fp ).reshape( full_image.shape ) )

  # perform the correlation
  corr = sophia.Correlate( full_image, filt )

  # show the resulting image
  sophia.a2i( corr.real ).show()

  return filt, corr, centered_images

def countPeaks( corr, thresh ):
  """
  Count the peaks in the correlation matrix for the given threshold.
  The threshold is applied, then the resulting peaks are blurred
  so that nearby peaks are connected. label() is then used to count
  contiguous regions.
  """
  peaks = ( corr > thresh ) * buildBorderMask( )
  peaks = blurMask( peaks, 5 )
  sophia.a2i( peaks ).show( )
  labels, count = label( peaks, structure=ones( (3,3) ) )
  print "Boats:", count

def loadImages( num, prefix, extension ):
  """Load a series of images with similar names and extensions."""

  boats = []
  
  for i in xrange( num ):
    name = prefix + str(i) + "." + extension
    mat = loadMatrix( name )
    boats.append( mat )
  
  return boats

def loadMatrix( name ):
  """
  Load a single image, converting it to black and white, converting
  its data type to float, and scaling it to 0 to 1
  """
  image = Image.open( findfile( name ) ).convert( 'L' )
  return sophia.i2a( image ).astype( float ) / 255

def buildBorderMask( name="boat_images/boatsmall.jpg" ):
  """
  Mask the area around the edge of the dock so that spurrious
  detections do not show up there.
  """
  return 1.0 - blurMask( loadMatrix( name ) < 0.01, 30 )

def blurMask( mask, amount ):
  """
  Blurs the provided mask, expanding 1.0 cells
  into adjacent 0.0 cells.
  """
  kernel = numpy.ones(amount*amount,float)
  kernel = kernel / numpy.sum( kernel )
  kernel = kernel.reshape( (amount,amount) )
  return convolve2d( mask, kernel, mode="same" ) != 0.0;

# inspired by: http://dotnot.org/blog/archives/2004/03/06/find-a-file-in-pythons-path/
# I wanted a way to automatically find the named image file in the same way python finds imported modules (similar to seaching for resources on the Java classpath)
def findfile( name ):
  for directory in sys.path:
    potential = os.path.join( directory, name )
    if os.path.isfile( potential ):
      return potential

if __name__ == "__main__":
  main_allboats()
