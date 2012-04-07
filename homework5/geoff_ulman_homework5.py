import os, sys, scipy, numpy, Image, sophia, color

def main():
  findBoats( "boatsmall.jpg", 18, "boat", "png" )
  return

def findBoats( image_name, num_train, prefix_train, extension_train ):
  image = sophia.i2a( Image.open( findfile( image_name ) ).convert( 'L' ) ) 
  boats = loadBoats( num, prefix, extension )
  

def loadBoats( num, prefix, extension ):
  boats = []
  
  for i in xrange( num ):
    name = prefix + str(i) + "." + extension
    mat = sophia.i2a( Image.open( findfile( name ) ).convert( 'L' ) ) 
    boats.append( mat )
  
  return boats


# inspired by: http://dotnot.org/blog/archives/2004/03/06/find-a-file-in-pythons-path/
# I wanted a way to automatically find the named image file in the same way python finds imported modules (similar to seaching for resources on the Java classpath)
def findfile( name ):
  for directory in sys.path:
    potential = os.path.join( directory, name )
    if os.path.isfile( potential ):
      return potential

if __name__ == "__main__":
  main()
