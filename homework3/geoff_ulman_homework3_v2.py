import os, sys, scipy, numpy, Image, sophia, color, eigenimage

def generateEigenImagesDirectory( directory ):
  l = splitImages( directory )
  return generateEigenImages( l )

def generateEigenImages( imageList ):
  emgs, evls = eigenimage.EigenImages( numpy.array( imageList ) )

  sorted_l = sorted( zip( evls, emgs ) )
  sorted_l.reverse()
  sorted_evls, sorted_emgs = zip( *sorted_l )

  return sorted_emgs, sorted_evls

def splitImages( directory, n=64, m=64 ):
  """Given a directory containing images, returns a list of smaller n by m sub-images"""
  l = []

  for f in os.listdir( directory ):
    print "Processing: ", f
    try:
      image = Image.open( os.path.join( directory, f ) )
    except IOError:
      print "Trouble opening image: ", f
    l.extend( splitImage( image, n, m ) )

  return l

def splitImage( image, n=64, m=64 ):
  """
Given a single image, splits the image into smaller n by m non-overlapping
sub-images and returns a list of the sub-images. If the size of the input
image is not an even multiple of n or m, some parts of the image will not
be used."""

  # create a list for the sub-images
  l = []

  # convert the image to matricies
  r,g,b = sophia.Image2Cube( image )

  # convert the r, g, b matrices to y, u, v colorspace
  h,s,v = color.RGB2HSV( r, g, b )

  # get the x and y size of the image
  sizeX = image.size[0]
  sizeY = image.size[1]

  # x and y pixel index counters
  xi = 0
  yi = 0

  # generate a Kaiser Mask
  mask = sophia.KaiserMask( (n,m), (n/2,m/2), 0, int( max(n,m) * 0.7 ) )

  while ( xi < sizeX - n ):
    yi = 0
    while ( yi < sizeY - m ):

      # generate sub matrix
      c1, c2, c3 = subImage( h, s, v, xi, yi, n, m )

      # apply mask
      c1 = c1 * mask
      c2 = c2 * mask
      c3 = c3 * mask

      c = numpy.zeros((n,3*m))

      # color.RGB2HSV() return h as int on 0 to 255
      c[:,0:m] = c1 / 255.;
      c[:,m:2*m] = c2;
      c[:,2*m:3*m] = c3;

      l.append( c )

      yi += m
    xi += n

  return l


def displaySubImage( emgs, i, n=64, m=64 ):
  """
A debugging function. Given a list of sub-images produced by splitImage and
an index into the list, displays the sub-image"""

  h = emgs[i][:,0:m]
  s = emgs[i][:,m:m*2]
  v = emgs[i][:,m*2:m*3]

  imh = sophia.a2i( h )
  ims = sophia.a2i( s )
  imv = sophia.a2i( v )

  imh.show()
  ims.show()
  imv.show()

  r, g, b = color.HSV2RGB( h, s, v )

  imr = sophia.a2i( r )
  img = sophia.a2i( g )
  imb = sophia.a2i( b )

  #Image.merge( 'RGB', ( imr, img, imb ) ).show()


def subImage( c1, c2, c3, xi, yi, n=64, m=64 ):
  """
Given three matrices c1, c2, c3 representing an image, selects a portion
of the image starting at pixel (x,y) of size n by m."""
  
  s1 = c1[yi:yi+m,xi:xi+n]
  s2 = c2[yi:yi+m,xi:xi+n]
  s3 = c3[yi:yi+m,xi:xi+n]

  return ( s1, s2, s3 )

  return emgs, evls;
