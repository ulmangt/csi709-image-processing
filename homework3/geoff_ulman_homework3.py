import os, sys, scipy, numpy, Image, sophia, color

def splitImages( imageList, n, m ):
  """Given a list of images, returns a list of smaller n by m sub-images"""
  return

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
  #h,s,v = color.RGB2HSV( r, g, b )

  # get the x and y size of the image
  sizeX = image.size[0]
  sizeY = image.size[1]

  # x and y pixel index counters
  xi = 0
  yi = 0

  # generate a Kaiser Mask
  mask = sophia.KaiserMask( (n,m), (n/2,m/2), 0, max(n,m)/2 )

  while ( xi < sizeX - n ):
    yi = 0
    while ( yi < sizeY - m ):

      # generate sub matrix
      c1, c2, c3 = subImage( r,g,b, xi, yi, n, m )

      # apply mask
      c1 = c1 * mask
      c2 = c2 * mask
      c3 = c3 * mask

      l.append( (c1,c2,c3) )

      yi += m
    xi += n

  return l


def displaySubImage( l, i ):
  """
A debugging function. Given a list of sub-images produced by splitImage and
an index into the list, displays the sub-image"""
  h,s,v = l[i]
  r, g, b = color.HSV2RGB( h, s, v )
  Image.merge( 'RGB', ( sophia.a2i(r), sophia.a2i(g), sophia.a2i(b) ) ).show()

def displaySubImageRGB( l, i ):
  """
A debugging function. Given a list of sub-images produced by splitImage and
an index into the list, displays the sub-image"""
  r,g,b = l[i]
  Image.merge( 'RGB', ( sophia.a2i(r), sophia.a2i(g), sophia.a2i(b) ) ).show()

def subImage( c1, c2, c3, xi, yi, n=64, m=64 ):
  """
Given three matrices c1, c2, c3 representing an image, selects a portion
of the image starting at pixel (x,y) of size n by m."""
  
  s1 = c1[yi:yi+m,xi:xi+n]
  s2 = c2[yi:yi+m,xi:xi+n]
  s3 = c3[yi:yi+m,xi:xi+n]

  return ( s1, s2, s3 )

