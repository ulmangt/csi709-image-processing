
import numpy
import math

def imblend( orig, swap ):
  w,h = orig[0].shape

  nr = numpy.zeros( (w,h) )
  ng = numpy.zeros( (w,h) )

  nb = numpy.zeros( (w,h) )

  for x in range( w ):
    print x
    for y in range( h ):
      b = blend( x, y, w, h )
      nr[x,y] = b * orig[0][x,y] + ( 1.0-b ) * swap[0][x,y]
      ng[x,y] = b * orig[1][x,y] + ( 1.0-b ) * swap[1][x,y]
      nb[x,y] = b * orig[2][x,y] + ( 1.0-b ) * swap[2][x,y]

  return (nr, ng, nb)
  

def blend( x,y,w,h ):
  r = math.sqrt( w**2 + h**2 ) / 2.0
  d = math.sqrt( (x -w/2.0)**2 + ( y - h/2.0)**2 )
  return min( 1.0, max( 0.0, d / r ) )


def dist( x,y,w,h ):
  return math.sqrt( (x -w/2.0)**2 + ( y - h/2.0)**2 )



