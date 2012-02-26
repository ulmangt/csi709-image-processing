
def edgeDetectCube( cube ):
  """Given a cube from sophia.Image2Cube, """
  r, g, b = cube
  w, h = r.shape
  r_p = edgeDetectMatrix( r )
  g_p = edgeDetectMatrix( g )
  b_p = edgeDetectMatrix( b )
  return ( r_p, g_p, b_p )
