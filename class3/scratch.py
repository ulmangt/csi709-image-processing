import os, sys, scipy, numpy, Image, sophia, color

def main():
  findcolor( findfile( '20120129a.jpg' ) ).show()

def findcolor( image, query=(110,110), tolerance=30, mode=1 ):
  """
Given an image (or a file path pointing to an image file) and a size three tuple representing an RGB color returns a new image with all pixels not near the given color masked in black.
mode = 1 returns a black and white mask, mode = 0 returns the mask applied to the original image."""
 
  # if image is a string, load the image it points to, otherwise
  # assume that it already is an image
  if isinstance( image, str ):
    image = Image.open( image )

  # ensure that the call to split() will work
  image = image.convert( 'RGB' )
 
  ra,ga,ba = sophia.Mg2Cube( image )

  y,cb,cr = color.RGB2YCbCr( ra, ga, ba )

  # create masks for all three channels
  cbmask = mask( cb, query[0], tolerance )
  crmask = mask( cr, query[1], tolerance )

  # create an overall mask of pixels which meet each channel mask
  overall_mask = cbmask * crmask

  # apply the mask to the r,g,b channels of the image
  y_masked = y * overall_mask
  cb_masked = cb * overall_mask
  cr_masked = cr * overall_mask

  # combine the masked channels into a single RGB image
  if mode:
    final_image = sophia.a2if( overall_mask * 255 )
  else:
    # create images from the three masked channels
    yi_masked = sophia.a2if( y_masked )
    cbi_masked = sophia.a2if( cb_masked )
    cri_masked = sophia.a2if( cr_masked )
    final_image = Image.merge( 'RGB', ( ri_masked, gi_masked, bi_masked ) )

  return final_image

# return a mask array containing True for values of array within tolerance
# of the given value and false otherwise
def mask( array, value, tolerance ):
  array_low  = ( array > float(value - tolerance) )
  array_high = ( array < float(value + tolerance) )
  return array_low * array_high

# inspired by: http://dotnot.org/blog/archives/2004/03/06/find-a-file-in-pythons-path/
# I wanted a way to automatically find the named image file in the same way python finds imported modules (similar to seaching for resources on the Java classpath)
def findfile( name ):
  for directory in sys.path:
    potential = os.path.join( directory, name )
    if os.path.isfile( potential ):
      return potential

if __name__ == "__main__":
  main() 
