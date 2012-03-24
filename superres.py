import os, sys, scipy, numpy, Image, sophia

def main():
  print "main"

def dummyZoom( img ):
  """Simply copy each pixel of the low resolution image into
     its four corresponding high resolution image pixels"""

  # low resolution matrix
  low_mat = sophia.i2a( img.convert( 'L' ) )

  # make four copies of each low resolution pixel
  return low_mat.repeat( 2, axis=0 ).repeat( 2, axis= 1 );


# inspired by: http://dotnot.org/blog/archives/2004/03/06/find-a-file-in-pythons-path/
# I wanted a way to automatically find the named image file in the same way python finds imported modules (similar to seaching for resources on the Java classpath)
def findFile( name ):
  for directory in sys.path:
    potential = os.path.join( directory, name )
    if os.path.isfile( potential ):
      return potential

if __name__ == "__main__":
  main()
