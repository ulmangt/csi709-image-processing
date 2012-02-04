import os, sys, scipy, numpy, Image, sophia

def findcolor( image, color ):
  """Given an image (or a file path pointing to an image file) and a size three tuple representing an RGB color returns a new image with all pixels not near the given color masked in black."""
 
  # if image is a string, load the image it points to, otherwise
  # assume that it already is an image
  if isinstance( image, str ):
    image = Image.open( image )

  # ensure that the call to split() will work
  image = image.convert( 'RGB' )
 
  # split the image into RGB channels
  r,g,b = image.split( )

  # convert greyscale images into arrays
  ra = sophia.i2a( r )
  ga = sophia.i2a( g )
  ba = sophia.i2a( b )

