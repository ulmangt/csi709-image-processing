def convert( convert_pixel, c1, c2, c3 ):
  """
Given convert_pixel, a function that takes three color component values
and outputs a tuple of three color component values, and three numyp
arrays of color component values, outputs a tuple of three new color
component values."""
  x = c1.shape[0]
  y = c1.shape[1]

  c1_prime = numpy.zeros( (x,y) )
  c2_prime = numpy.zeros( (x,y) )
  c3_prime = numpy.zeros( (x,y) )

  for xi in xrange(x):
    for yi in xrange(y):
      c1_value = c1[xi,yi]
      c2_value = c2[xi,yi]
      c3_value = c3[xi,yi]

      if c1_value > 1: c1_value /= 255.0
      if c2_value > 1: c2_value /= 255.0
      if c3_value > 1: c3_value /= 255.0

      c1_prime[xi,yi],c2_prime[xi,yi],c3_prime[xi,yi] = convert_pixel( c1_value, c2_value, c3_value )

  return (c1_prime,c2_prime,c3_prime)
