import os, sys, scipy, numpy, Image, sophia, color, eigenimage

def main():
  0;

def generateEigenImagesDirectory( directory ):
  l = splitImages( directory )
  return generateEigenImagesColor( l )

# how do I generate the color eigenimages?
# combine 3 eigenimages from three channels?
# use only 1 and set the other channels to all 0s?

def generateEigenImagesColor( imageList ):
  emgs1, evls1 = eigenimage.EigenImages( numpy.array( imageList[0] ) )
  emgs2, evls2 = eigenimage.EigenImages( numpy.array( imageList[1] ) )
  emgs3, evls3 = eigenimage.EigenImages( numpy.array( imageList[2] ) )

  return (evls1, evls2, evls3), (emgs1, emgs2, emgs3 );

def sortEigenImages( evls, emgs ):
  evls1, evls2, evls3 = evls
  emgs1, emgs2, emgs3 = emgs

  evlsmax = max( list(evls1), list(evls2), list(evls3) )
  sorted_l = sorted( zip( evlsmax, evls1, evls2, evls3, emgs1, emgs2, emgs3 ) )
  sorted_l.reverse( )
  evlsmax, evls1, evls2, evls3, emgs1, emgs2, emgs3 = zip( *sorted_l )

  return (evls1, evls2, evls3), (emgs1, emgs2, emgs3 )

def generateEigenImages( imageList ):
  emgs, evls = eigenimage.EigenImages( numpy.array( imageList[0] ) )

  sorted_l = sorted( zip( evls, emgs ) )
  sorted_l.reverse()
  sorted_evls, sorted_emgs = zip( *sorted_l )

  return sorted_evls, sorted_emgs, imageList;

def splitImages( directory, n=64, m=64 ):
  """Given a directory containing images, returns a list of smaller n by m sub-images"""
  l1 = []
  l2 = []
  l3 = []

  for f in os.listdir( directory ):
    print "Processing: ", f
    try:
      image = Image.open( os.path.join( directory, f ) )
    except IOError:
      print "Trouble opening image: ", f
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
  y,u,v = color.RGB2YUV( r, g, b )

  # get the x and y size of the image
  sizeX = image.size[0]
  sizeY = image.size[1]

  # x and y pixel index counters
  xi = 0
  yi = 0

  # generate a Kaiser Mask
  mask = sophia.KaiserMask( (n,m), (n/2,m/2), -20, numpy.sqrt( (n/2)**2+(m/2)**2 ) )

  while ( xi < sizeX - n ):
    yi = 0
    while ( yi < sizeY - m ):

      # generate sub matrix
      c1, c2, c3 = subImage( y, u, v, xi, yi, n, m )

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

def subImage( c1, c2, c3, xi, yi, n=64, m=64 ):
  """
Given three matrices c1, c2, c3 representing an image, selects a portion
of the image starting at pixel (x,y) of size n by m."""
  
  s1 = c1[yi:yi+m,xi:xi+n]
  s2 = c2[yi:yi+m,xi:xi+n]
  s3 = c3[yi:yi+m,xi:xi+n]

  return ( s1, s2, s3 )

def YUV2RGB(y,u,v):
  r = 1.0*y + 0.0*u + 1.13983*v
  g = 1.0*y - 0.39465*u + -0.58060*v
  b = 1.0*y + 2.03211*u + 0.0*v
  return r,g,b

def displaySubImages( emgs, evls, row, col, n=64, m=64 ):

  c1 = numpy.zeros( ( row * n , col * m ) );
  c2 = numpy.zeros( ( row * n , col * m ) );
  c3 = numpy.zeros( ( row * n , col * m ) );

  index = 0
  for r in range( row ):
    for c in range( col ):

      #ya = emgs[0][index] * numpy.sqrt( evls[0][index] )
      #ua = emgs[1][index] * numpy.sqrt( evls[1][index] )
      #va = emgs[2][index] * numpy.sqrt( evls[2][index] )

      ya = emgs[0][index]
      ua = emgs[1][index]
      va = emgs[2][index]

      ra,ga,ba = YUV2RGB( ya, ua, va )

      c1[r*n:(r+1)*n,c*m:(c+1)*m] = normalize( ra )
      c2[r*n:(r+1)*n,c*m:(c+1)*m] = normalize( ga )
      c3[r*n:(r+1)*n,c*m:(c+1)*m] = normalize( ba )

      index += 1

  imr = sophia.a2if( c1 )
  img = sophia.a2if( c2 )
  imb = sophia.a2if( c3 )

  Image.merge( 'RGB', ( imr, img,  imb ) ).show()

def normalize( indata ):
  mn = indata.min()
  a = indata - mn
  mx = a.max()
  a = a*256./mx
  return a;

def displaySubImage( l, i ):
  """
A debugging function. Given a list of sub-images produced by splitImage and
an index into the list, displays the sub-image"""
  # why can the eigenimage values be interpreted directly as yuv values?
  # am I still getting very small eigenimage component values?
  r, g, b = YUV2RGB( l[0][i], l[1][i], l[2][i] )
  Image.merge( 'RGB', ( sophia.a2i(r), sophia.a2i(g), sophia.a2i(b) ) ).show()

if __name__ == "__main__":
  main() 

