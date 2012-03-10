import os, sys, random, scipy, numpy, Image, sophia, color
from scipy.signal import convolve2d
from scipy.ndimage.measurements import label
from scipy import zeros, ones
from random import randint

def main():
  """Search for a file called boatsmall.jpg on the python path and run countBoatsFile() on it."""
  countBoatsFile( findfile( 'boatsmall.jpg' ) )

def countBoatsFile( fileName ):
  """Counts the number of boats in an input file."""
  countBoats( Image.open( fileName ) )

def countBoats( image ):
  """Counts the number of boats in an input image."""
  cube = sophia.Image2Cube( image )
  l,u,v = color.RGB2LUV( cube[0], cube[1], cube[2] )

  mask_black_border = ( l > 7000 )
  mask_upper_right = createMaskCorner( l.shape )

  mask_shiny = ( l > 15200 )
  #kernel = ones( (3,3) ) / 9.
  #mask_shiny = convolve2d( mask_shiny, kernel, mode="same" ) > 0.35

  mask_green_cannopy = ( u < -100 )
  mask_red_cannopy = ( u > 2700 )
  mask_black_cannopy = ( l > 10000 ) * ( l < 11000 )

  mask_ship = mask_shiny | mask_green_cannopy # | mask_red_cannopy # | mask_black_cannopy
  mask_ignore = mask_black_border * mask_upper_right

  mask = mask_ship * mask_ignore

  labels, count = label( mask, structure=ones( (3,3) ) )
  
  label_mask_r = zeros( l.shape )
  label_mask_g = zeros( l.shape )
  label_mask_b = zeros( l.shape )

  boatCount = 0
  for i in range( 1, count+1 ):
    single_mask = labels == i
    if ( scipy.sum( single_mask ) > 20 ):
      boatCount = boatCount + 1
      label_mask_r = label_mask_r + ( single_mask * randint( 0, 255 ) )
      label_mask_g = label_mask_g + ( single_mask * randint( 0, 255 ) )
      label_mask_b = label_mask_b + ( single_mask * randint( 0, 255 ) )

  sophia.a2i( mask ).show()
  sophia.a2i( mask_shiny ).show()
  sophia.a2i( mask_black_cannopy ).show()

  sophia.Cube2Image( label_mask_r, label_mask_g, label_mask_b ).show()

  print boatCount, count

def createMaskCorner( shape ):
  slope = ( 125. - 0 ) / ( 350. - 250. )
  rangex = xrange( shape[1] )
  rangey = xrange( shape[0] )
  return numpy.array( [ [ slope * (x - 250 ) < y for x in rangex] for y in rangey] )

def randomColorPalette( colors ):
  palette = [ 0, 0, 0 ]
  return palette.extend( [ random.randint( 0, 255 ) for i in range( colors * 3 ) ] )

# inspired by: http://dotnot.org/blog/archives/2004/03/06/find-a-file-in-pythons-path/
# I wanted a way to automatically find the named image file in the same way python finds imported modules (similar to seaching for resources on the Java classpath)
def findfile( name ):
  for directory in sys.path:
    potential = os.path.join( directory, name )
    if os.path.isfile( potential ):
      return potential

if __name__ == "__main__":
  main() 
