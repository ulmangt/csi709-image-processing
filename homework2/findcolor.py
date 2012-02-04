import os, sys, scipy, numpy, Image, sophia

def findcolor( image, color, tolerance ):
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

  # create masks for all three channels
  rmask = mask( ra, color[0], tolerance )
  gmask = mask( ga, color[1], tolerance )
  bmask = mask( ba, color[2], tolerance )

  # create an overall mask of pixels which meet each channel mask
  overall_mask = rmask * gmask * bmask

  # apply the mask to the r,g,b channels of the image
  ra_masked = ra * overall_mask
  ga_masked = ga * overall_mask
  ba_masked = ba * overall_mask

  # create images from the three masked channels
  ri_masked = sophia.a2if( ra_masked )
  gi_masked = sophia.a2if( ga_masked )
  bi_masked = sophia.a2if( ba_masked )

  # combine the masked channels into a single RGB image
  final_image = Image.merge( 'RGB', ( ri_masked, gi_masked, bi_masked ) )

  return final_image

# return a mask array containing True for values of array within tolerance
# of the given value and false otherwise
def mask( array, value, tolerance ):
  array_low  = ( array > float(value - tolerance) )
  array_high = ( array < float(value + tolerance) )
  return array_low * array_high
 
