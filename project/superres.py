import os, sys, scipy, numpy, Image, sophia, operator
from numpy import sum, sqrt, zeros, array

def main():
  # load a small section of the boat image
  mat_low = loadImage( 'boatsmall.jpg', (100,150,125,175) ).astype(float)

  # perform nearest neighbor and bilinear interpolation
  # to zoom the image x2
  mat_nn = nearestNeighborZoom( mat_low )
  mat_bi = bilinearZoom( mat_low )

  # show the results
  sophia.a2i( mat_nn ).show()
  sophia.a2i( mat_bi ).show()

  # look for patches of the image similar to the given
  # patch at (100,100,120,120)
  d = scorePatches( mat_low, (0,0,20,20) )
  # create a 5 by 5 grid of the most similar 25 patches
  mat_patch = displayPatches( mat_low, d, 5, 5 )
  sophia.a2if( mat_patch ).show() 

def main2():
  # load a small section of the boat image
  mat_low = loadImage( 'boatsmall.jpg', (100,150,125,175) ).astype(float)

  low_val, high_val = patchSimilarityZoom( mat_low )

  high_mat = numpy.linalg.lstsq( high, low )

  width, height = mat_low.shape

  sophia.a2i( high_mat[0].reshape( width*2, height*2 ) ).show()

  return high_mat, low_val, high_val

def loadImage( path, crop=None ):
  """
  Loads the image at the provided path, crops it, and returns a matrix
  representation of the image converted to grayscale.
  """
  if crop:
    return sophia.i2a( Image.open( findFile( path ) ).crop( crop ).convert( 'L' ) )
  else:
    return sophia.i2a( Image.open( findFile( path ) ).convert( 'L' ) )

def nearestNeighborZoom( mat ):
  """
  Zooms image 2x.
  Simply copy each pixel of the low resolution image
  into its four corresponding high resolution image pixels.
  """

  # make four copies of each low resolution pixel
  return mat.repeat( 2, axis=0 ).repeat( 2, axis= 1 );

def bilinearZoom( mat ):
  """
  Zooms image 2x.
  Each high resolution image pixel g(n1,n2) = A0 + A1*n1 + A2*n2 + A3*n1*n2
  The coefficients are a linear function of the surrounding four image values 
  See: Bovik, Alan C. Handbook of Image and Video Processing. 2nd ed. Amsterdam: Elsevier Academic, 2005. 35-37. Print.
  Also See: http://en.wikipedia.org/wiki/Bilinear_interpolation
  """

  mat = nearestNeighborZoom( mat )
  high_mat = zeros( mat.shape )

  for x in xrange( 1, mat.shape[0]-1 ):
    for y in xrange( 1, mat.shape[1]-1 ):

      # name the indices of the four surrounding pixels
      # in the same manner as Bovik in Handbook of Image and Video Processing
      n10 = x
      n20 = y-1

      n11 = x
      n21 = y+1  

      n12 = x-1
      n22 = y 

      n13 = x+1
      n23 = y+1

      # build and solve the linear system
      A = array( [[ 1, n10, n20, n10*n20 ],
                        [ 1, n11, n21, n11*n21 ],
                        [ 1, n12, n22, n12*n22 ],
                        [ 1, n13, n23, n13*n23 ]] )

      b = array( [ mat[n10,n20], mat[n11,n21], mat[n12,n22], mat[n13,n23] ] ) 

      try:

        coef = numpy.linalg.solve( A, b )
        high_mat[x,y] = coef[0] + coef[1]*x + coef[2]*y + coef[3]*x*y
 
      except numpy.linalg.linalg.LinAlgError as err:
 
        print 'Singular Matrix: ', A

  return high_mat


def patchSimilarityZoom( mat, size=5, k=9 ):
  """
  Zooms image 2x.
  Utilizes patch similarity within the single image. For each 5x5 subsection of the image,
  similar patches in other parts of the image are searched for. Those patches are then
  treated as if they are all independent images of the initial patch and are used to
  reconstruct a high resolution version of the original patch. This process is repeated
  across the entire image.
  See: Daniel Glasner, Shai Bagon, and Michal Irani. Super-resolution from a Single Image.
       http://www.wisdom.weizmann.ac.il/~vision/SingleImageSR.html
  """

  # get the width and height of the high and low resolution image
  width = mat.shape[1]
  height = mat.shape[0]
  low_size = width * height

  high_width = width*2;
  high_height = height*2
  high_size = high_width * high_height

  # build the linear constraint matrices
  # create an array of low resolution pixel intensities
  low_val = numpy.zeros( low_size*k, float )
  # create a matrix for the high resolution constraints
  # one column for each pixel in the high resolution image
  # and one row for each constraint
  high_val = numpy.zeros( (low_size*k , high_size) , float )

  # loop over pixels in the low resolution image
  index = 0
  for x in xrange( 0, width ):
    print 'row:', x, '/', width
    for y in xrange( 0, height ):

      # create a square gaussian kernel
      # multiple by 2 because the kernel acts
      # on the pixels of the high resolution image
      kernel = createGaussianKernel( x*2, y*2, width*2, height*2, size*2 )

      # calculate the patch bounds (watching for edge conditions)
      target_patch = getPatchFromCoords( x, y, width, height, size )

      # find similar patches
      d = scorePatches( mat, target_patch )  

      # add constraints for the first k similar patches
      for p in d[0:k]:
        patch, weight = p
        x1,y1,x2,y2 = patch
        # stick the kernel into the appropriate place in the matrix
        # (given my the patch p) then ravel the matrix into a
        # 1d constraint vector and add it to the other constraints
        constraint = numpy.zeros( ( high_width, high_height ), float )
        constraint[x1*2:x2*2,y1*2:y2*2] = kernel
        high_val[index] = constraint.ravel( )
        low_val[index] = mat[y,x]
        index = index + 1

  return low_val, high_val

# size must be odd here (a size in the low rez image)
def getPatchFromCoords( x, y, width, height, size ):
  """
  Given a pixel position, the width and height of the image, and the size
  of the desired patch, returns a tuple with the upper left and lower right
  pixel coordinates (inclusive) of the patch.
  """
  x1 = max( 0, x-size/2 )
  y1 = max( 0, y-size/2 )
  x2 = min( width, x+size/2+1 )
  y2 = min( height, y+size/2+1 )
  return ( x1, y1, x2, y2 )

# size must be even here (a size in the high rez image
# which is double the low res, so if the low rez size
# is odd this should be even)
def createGaussianKernel( x, y, width, height, size ):
  # create a 5x5 gaussian kernel approximation
  # adapted from: http://scipy-lectures.github.com/intro/numpy/numpy.html
  # with x values ranging from -4 to 4
  kernelx = numpy.linspace( -4, 4, size )
  kernel = numpy.exp( -0.1*kernelx**2 )
  # treat the 1d kernel as a column vector times a row vector
  # resulting in a 2d kernel matrix
  kernel = kernel[:,numpy.newaxis] * kernel[numpy.newaxis,:]

  # if we are near the edge of the image, we only need a section of the kernel
  x1 = max( 0, size/2-x-1 )
  y1 = max( 0, size/2-y-1 )
  x2 = min( size, size/2+width-x-1 )
  y2 = min( size, size/2+height-y-1 )
  kernel = kernel[x1:x2,y1:y2]

  # normalize the kernel
  kernel = kernel / numpy.sum( kernel )

  return kernel

def displayPatch( mat, patch ):
  """Display a rectangular subsection of the given image matrix."""
  sophia.a2i( mat[ patch[1]:patch[3], patch[0]:patch[2] ] ).show()

def displayPatches( mat, d, rows, cols ):
  """
  Given an image matrix, a dictionary produced by scorePatches(), and a number of rows and columns.
  Returns a larg image matrix with the best rows*cols patches from d tiled in the image.
  """

  first = d[0]
  width = first[0][2] - first[0][0]
  height = first[0][3] - first[0][1]

  img = zeros( ( cols * width, rows * height ) )

  count = 0
  for x in xrange( cols ):
    for y in xrange( rows ):
      patch = d[count][0]
      img[ x*width:(x+1)*width , y*height:(y+1)*height ] = mat[ patch[1]:patch[3], patch[0]:patch[2] ] 
      count = count + 1

  return img

def scorePatches( mat, patch ):
  """
  Given an image matrix and a four-tuple representing the upper left and lower right corners of a
  sub-section of the image.
  Score all similarly sized sections of the image for their similarity to the given patch and return
  a list of the patch coordinates sorted by similarity score.
  """

  # get the width and height of the search patch
  patch_width = patch[2] - patch[0]
  patch_height = patch[3] - patch[1]

  # get the width and height of the overall image
  image_width = mat.shape[1]
  image_height = mat.shape[0]

  # create a dictionary of patches and their scores
  d = {}

  # iterate through each pixel in the image, creating a candidate patch
  # using that pixel as its upper left corner and score that candidate
  # against the target patch
  for x in xrange( image_width - patch_width ):
    #print x , '/' , image_width - patch_width
    for y in xrange( image_height - patch_height ):
      candidate_patch = (x, y, x+patch_width, y+patch_height)
      score = scorePatch( mat, patch, candidate_patch )
      d[candidate_patch] = score

  return sorted(d.iteritems(), key=operator.itemgetter(1))



def scorePatch( mat, target_patch, candidate_patch ): 
  """
  Given an image matrix and two patches (cropped sections of the image matrix which must be the same size).
  Computes the similarity between the two patches where similarity is defined as the sum of the squared
  differences between pixel intensities of corresponding pixels in the patches.
  """

  tx1,ty1,tx2,ty2 = target_patch
  cx1,cy1,cx2,cy2 = candidate_patch

  # get the width and height of the search patch
  patch_width = tx2 - tx1
  patch_height = ty2 - ty1

  score = 0
  
  target_mat = mat[ty1:ty2,tx1:tx2]
  candidate_mat = mat[cy1:cy2,cx1:cx2]

  return sqrt( sum( ( target_mat - candidate_mat )**2 ) )



# inspired by: http://dotnot.org/blog/archives/2004/03/06/find-a-file-in-pythons-path/
# I wanted a way to automatically find the named image file in the same way python finds imported modules (similar to seaching for resources on the Java classpath)
def findFile( name ):
  for directory in sys.path:
    potential = os.path.join( directory, name )
    if os.path.isfile( potential ):
      return potential

if __name__ == "__main__":
  main()
