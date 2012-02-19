import os, sys, scipy, numpy, Image, sophia, color, eigenimage

def generateEigenImages( directory ):
  l = splitImages( directory )

  emgs, evls = eigenimage.EigenImages( numpy.array( l[0] ) )
  sorted_l = sorted( zip( evls, emgs ) )
  sorted_l.reverse()
  sorted_emgs, sorted_evls = zip( *sorted_l )

  return sorted_evls, sorted_emgs, l;

def splitImages( directory, n=64, m=64 ):
  """Given a directory containing images, returns a list of smaller n by m sub-images"""
  l1 = []
  l2 = []
  l3 = []

  for f in os.listdir( directory ):
    print "Processing: ", f
    image = Image.open( os.path.join( directory, f ) )
    l = splitImage( image, n, m )
    l1.extend( l[0] )
    l2.extend( l[1] )
    l3.extend( l[2] )

  return ( l1, l2, l3 )

def splitImage( image, n=64, m=64 ):
  """
Given a single image, splits the image into smaller n by m non-overlapping
sub-images and returns a list of the sub-images. If the size of the input
image is not an even multiple of n or m, some parts of the image will not
be used."""

  # create a list for the sub-images
  l1 = []
  l2 = []
  l3 = []

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

      l1.append( c1 )
      l2.append( c2 )
      l3.append( c3 )

      yi += m
    xi += n

  return ( l1, l2, l3 )


def displaySubImage( l, i ):
  """
A debugging function. Given a list of sub-images produced by splitImage and
an index into the list, displays the sub-image"""
  r, g, b = color.HSV2RGB( l[0][i], l[1][i], l[2][i] )
  Image.merge( 'RGB', ( sophia.a2i(r), sophia.a2i(g), sophia.a2i(b) ) ).show()

def displaySubImageRGB( l, i ):
  """
A debugging function. Given a list of sub-images produced by splitImage and
an index into the list, displays the sub-image"""
  Image.merge( 'RGB', ( sophia.a2i(l[0][i]), sophia.a2i(l[1][i]), sophia.a2i(l[2][i]) ) ).show()

def subImage( c1, c2, c3, xi, yi, n=64, m=64 ):
  """
Given three matrices c1, c2, c3 representing an image, selects a portion
of the image starting at pixel (x,y) of size n by m."""
  
  s1 = c1[yi:yi+m,xi:xi+n]
  s2 = c2[yi:yi+m,xi:xi+n]
  s3 = c3[yi:yi+m,xi:xi+n]

  return ( s1, s2, s3 )

