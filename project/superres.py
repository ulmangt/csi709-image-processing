import os, sys, scipy, numpy, Image, sophia, operator

def main():
  # load a small section of the boat image
  mat_low = loadImage( 'boatsmall.jpg', (100,100,200,200) ).astype(float)

  # perform nearest neighbor and bilinear interpolation
  # to zoom the image x2
  mat_nn = nearestNeighborZoom( mat_low )
  mat_bi = bilinearZoom( mat_low )

  # show the results
  sophia.a2i( mat_nn ).show()
  sophia.a2i( mat_bi ).show()

  # look for patches of the image similar to the given
  # patch at (100,100,120,120)
  d = scorePatches( mat_low, (0,79,20,99) )

  # create a 5 by 5 grid of the most similar 25 patches
  mat_patch = displayPatches( mat_low, d, 5, 5 )
  sophia.a2if( mat_patch ).show() 

  return d

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

  #high_mat = numpy.copy( mat )
  high_mat = numpy.zeros( mat.shape )

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
      A = numpy.array( [[ 1, n10, n20, n10*n20 ],
                        [ 1, n11, n21, n11*n21 ],
                        [ 1, n12, n22, n12*n22 ],
                        [ 1, n13, n23, n13*n23 ]] )

      b = numpy.array( [ mat[n10,n20], mat[n11,n21], mat[n12,n22], mat[n13,n23] ] ) 

      try:
        coef = numpy.linalg.solve( A, b )
        high_mat[x,y] = coef[0] + coef[1]*x + coef[2]*y + coef[3]*x*y
      except numpy.linalg.linalg.LinAlgError as err:
        print 'Singular Matrix: ', A

  return high_mat

def displayPatch( mat, patch ):
  sophia.a2i( mat[ patch[1]:patch[3], patch[0]:patch[2] ] ).show()

def displayPatches( mat, d, rows, cols ):
  """
  Given an image matrix, a dictionary produced by scorePatches(), and a number of rows and columns.
  Returns a larg image matrix with the best rows*cols patches from d tiled in the image.
  """

  first = d[0]
  width = first[0][2] - first[0][0]
  height = first[0][3] - first[0][1]

  img = numpy.zeros( ( cols * width, rows * height ) )

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
    print x , '/' , image_width - patch_width
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

  # get the width and height of the search patch
  patch_width = target_patch[2] - target_patch[0]
  patch_height = target_patch[3] - target_patch[1]

  score = 0
  
  for x in xrange( patch_width ):
    for y in xrange( patch_height ):
      target_pixel = mat[target_patch[1]+y,target_patch[0]+x]
      candidate_pixel = mat[candidate_patch[1]+y,candidate_patch[0]+x]
      #print target_pixel, candidate_pixel, ( target_pixel - candidate_pixel )
      score = score + (target_pixel-candidate_pixel)**2

  return numpy.sqrt( score )

# inspired by: http://dotnot.org/blog/archives/2004/03/06/find-a-file-in-pythons-path/
# I wanted a way to automatically find the named image file in the same way python finds imported modules (similar to seaching for resources on the Java classpath)
def findFile( name ):
  for directory in sys.path:
    potential = os.path.join( directory, name )
    if os.path.isfile( potential ):
      return potential

if __name__ == "__main__":
  main()
