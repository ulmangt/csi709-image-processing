import os, sys, scipy, numpy, Image, sophia

def main():
  print "main"

def nearestNeighborZoom( img ):
  """
  Zooms image 2x.
  Simply copy each pixel of the low resolution image
  into its four corresponding high resolution image pixels.
  """

  # low resolution matrix
  low_mat = sophia.i2a( img.convert( 'L' ) )

  # make four copies of each low resolution pixel
  return low_mat.repeat( 2, axis=0 ).repeat( 2, axis= 1 );

def bilinearZoom( img ):
  """
  Zooms image 2x.
  Each high resolution image pixel g(n1,n2) = A0 + A1*n1 + A2*n2 + A3*n1*n2
  The coefficients are a linear function of the surrounding four image values 
  See: Bovik, Alan C. Handbook of Image and Video Processing. 2nd ed. Amsterdam: Elsevier Academic, 2005. 35-37. Print.
  """

  mat = nearestNeighborZoom( img )

  high_mat = numpy.copy( mat )

  for x in xrange( 1, mat.shape[0]-1 ):
    for y in xrange( 1, mat.shape[1]-1 ):

      # name the indices of the four surrounding pixels
      # in the same manner as Bovik in Handbook of Image and Video Processing
      n10 = x-1
      n20 = y

      n11 = x
      n21 = y-1  

      n12 = x
      n22 = y+1  

      n13 = x+1
      n23 = y 

      # build and solve the linear system
      A = numpy.array( [[ 1, n10, n20, n10*n20 ],
                        [ 1, n11, n21, n11*n21 ],
                        [ 1, n12, n22, n12*n22 ],
                        [ 1, n13, n23, n13*n23 ]] )

      y = numpy.array( [ mat[n10,n20], mat[n11,n21], mat[n12,n22], mat[n13,n23] ] ) 

      try:
        coef = numpy.linalg.solve( A, y )
        high_mat[x,y] = coef[0] + coef[1]*x + coef[2]*y + coef[3]*x*y
      except numpy.linalg.linalg.LinAlgError as err:
        print 'Singular Matrix: ', A

  return high_mat

# inspired by: http://dotnot.org/blog/archives/2004/03/06/find-a-file-in-pythons-path/
# I wanted a way to automatically find the named image file in the same way python finds imported modules (similar to seaching for resources on the Java classpath)
def findFile( name ):
  for directory in sys.path:
    potential = os.path.join( directory, name )
    if os.path.isfile( potential ):
      return potential

if __name__ == "__main__":
  main()
