import os, sys, random, scipy, numpy, Image, sophia, color
from scipy.signal import convolve2d
from scipy.ndimage.measurements import label
from scipy import zeros, ones
from random import randint

def main():
  """Search for a file called boatsmall.jpg on the python path and run countBoatsFile() on it."""
  return countBoatsFile( findfile( 'boatsmall.jpg' ) )

def countBoatsFile( fileName ):
  """Counts the number of boats in an input file."""
  return countBoats( Image.open( fileName ) )

def countBoats( image ):
  """Counts the number of boats in an input image."""

  # convert the image to a matrix and extract r,g,b color channels
  cube = sophia.Image2Cube( image )
  r,g,b = cube

  # convert to luv colorspace
  l,u,v = color.RGB2LUV( r,g,b )

  # build a mask which ignores the black areas at the edge of the image
  mask_black_border = ( l > 7000 )

  # there are two types of ships in the image: ships with shiny white
  # hulls, and one ship almost entirely covered with a green canopy
  # we build one mask for each class of ship

  # find areas of the image with very high lightness channel, these
  # correspond to the shiny paint on ship's hulls
  mask_shiny = ( l > 15200 )

  # find areas with light green coloring (using the u channel)
  mask_green_canopy = ( u < -300 ) * ( u > -4000 )

  # there are many small shiny areas along the pier
  # remove them by removing everything from the shiny mask
  # with less than 14 connected pixels
  mask = removeSmallBlobs( mask_shiny * mask_black_border, 14 )

  # blur the resulting mask using a custom kernel, then threshold
  # the result so we again have a 0/1 mask
  # this helps ensure that nearby shiny spots on ships are connected
  # into a single blob
  kernel = numpy.array([1., 1., 1., 1., 3., 1., 1., 1., 1.])
  kernel = kernel / numpy.sum( kernel )
  kernel = kernel.reshape( (3,3) )
  mask = convolve2d( mask, kernel, mode="same" ) > 0.06

  # add the green canopy mask to the shiny paint mask
  mask = mask | ( mask_green_canopy * mask_black_border )

  # use label() to find the connected sections of the mask
  labels, count = label( mask, structure=ones( (3,3) ) )
  
  # initialize some arrays to store output images
  mask_r = zeros( l.shape )
  mask_g = zeros( l.shape )
  mask_b = zeros( l.shape )

  # look through each labeled blob
  boatCount = 0
  for i in range( 1, count+1 ):
    # create a mask for the labeled blob
    single_mask = labels == i
    # ignore any remaining small blobs (less than 20 pixels)
    if ( scipy.sum( single_mask ) > 20 ):
      boatCount = boatCount + 1
      # assign a random color to each boat
      mask_r = mask_r + ( single_mask * randint( 0, 255 ) )
      mask_g = mask_g + ( single_mask * randint( 0, 255 ) )
      mask_b = mask_b + ( single_mask * randint( 0, 255 ) )

  # build two output images
  sophia.Cube2Image( r * (mask_r != 0), g * (mask_g != 0), b * (mask_b != 0) ).show()
  sophia.Cube2Image( mask_r, mask_g, mask_b ).show()

  # return the final boat count
  return boatCount

def removeSmallBlobs( matrix, max_size ):
  """removes (sets to 0) contiguous blobs smaller than max_size in the input matrix"""
  
  # create a new output matrix
  label_matrix = zeros( matrix.shape )

  # use label() to find the connected sections of the input matrix
  labels, count = label( matrix, structure=ones( (3,3) ) )

  # only include blobs of size larger than max_size in the output matrix
  for i in range( 1, count+1 ):
    single_mask = labels == i
    if ( scipy.sum( single_mask ) > max_size ):
      label_matrix = label_matrix + single_mask

  return label_matrix

# inspired by: http://dotnot.org/blog/archives/2004/03/06/find-a-file-in-pythons-path/
# I wanted a way to automatically find the named image file in the same way python finds imported modules (similar to searching for resources on the Java classpath)
def findfile( name ):
  for directory in sys.path:
    potential = os.path.join( directory, name )
    if os.path.isfile( potential ):
      return potential

if __name__ == "__main__":
  main() 
