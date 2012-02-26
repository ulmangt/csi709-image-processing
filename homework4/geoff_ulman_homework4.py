import os, sys, scipy, numpy, Image, sophia, color

def main():
  """Search for a file called car.png on the python path and run bumpFilterFile() on it."""
  bumpFilterFile( findfile( 'car.png' ) ).show()

def bumpFilterFile( filePath ):
  """Given the path to a file, open the file as an image and run bumpFilterImage() on it."""
  image = Image.open( filePath )
  return bumpFilterImage( image )


def bumpFilterImage( image ):
  """Given an image, detect edges in the image. Then, darken the pixels in the image which
     fall on those edges. Finally, also darken pixels to one side of the edge and lighten
     pixels on the other side, creating a bump-like effect."""
  
  # convert the input image to greyscale
  image_bw = image.convert( 'L' )
  # convert the greyscale image to a matrix
  matrix = sophia.i2a( image_bw )
  # find edges in the greyscale image using a simple shift and subtract gradient calculation
  edges = edgeDetectMatrix( matrix )
  # convert the original RGB image to a cube
  cube = sophia.Image2Cube( image )

  # adjust the color image three times based on the edge matrix
  cube = shiftAdjust( cube, edges, 4, (0,0) );
  cube = shiftAdjust( cube, edges, 3, (1,1) );
  cube = shiftAdjust( cube, edges, -2, (-1,-1) );

  # convert the cube back into a color image
  r_i = sophia.a2if( cube[0] )
  g_i = sophia.a2if( cube[1] )
  b_i = sophia.a2if( cube[2] )
  image_p = Image.merge( 'RGB', ( r_i, g_i, b_i ) );

  return image_p

def shiftAdjust( inputCube, mask, multiplier, shift ):
  """Given a cube from sophia.Image2Cube, a matrix of the same size, a scalar multipler,
     and an x/y shift tuple, return a new cube with the mask applied to the inputCube,
     possibly shifted and scaled by the multiplier."""

  # shift the mask
  mask_s = shiftMatrix( mask, shift )

  # apply the shifted mask to each channel of the inputCube
  c_0 = inputCube[0] - numpy.abs( mask_s ) * multiplier
  c_1 = inputCube[1]  - numpy.abs( mask_s ) * multiplier
  c_2 = inputCube[2] - numpy.abs( mask_s ) * multiplier

  # return a new cube
  return ( c_0, c_1, c_2 )

def shiftMatrix( matrix, shift ):
  """A simple wraper function around numpy.roll() which allows shifting
     in two dimensions simultaneously."""
  matrix_p = numpy.roll( matrix, shift[0], axis=0 )
  matrix_p = numpy.roll( matrix_p, shift[1], axis=1 )
  return matrix_p

def edgeDetectMatrix( matrix ):
  """Apply a simple shift and subtract gradient detection algorithm on a matrix."""
  
  # interpret the matrix as type float
  matrix = matrix.astype( float )

  # get the shape of the matrix
  w, h = matrix.shape

  # construct a new matrix which will contain the edge detections
  matrix_p = numpy.zeros( (w, h) )

  # perform the shift and subtract and return the results
  matrix_diff =  matrix[:-1,:-1] - matrix[1:,1:]
  matrix_p[1:,1:] = matrix_diff
  return matrix_p

# inspired by: http://dotnot.org/blog/archives/2004/03/06/find-a-file-in-pythons-path/
# I wanted a way to automatically find the named image file in the same way python finds imported modules (similar to seaching for resources on the Java classpath)
def findfile( name ):
  for directory in sys.path:
    potential = os.path.join( directory, name )
    if os.path.isfile( potential ):
      return potential

if __name__ == "__main__":
  main() 
