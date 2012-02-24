  #imh.show()
  #ims.show()
  #imv.show()

  #r, g, b = color.HSV2RGB( h, s, v )

  #imr = sophia.a2i( r )
  #img = sophia.a2i( g )
  #imb = sophia.a2i( b )

  #Image.merge( 'RGB', ( imr, img, imb ) ).show()


def displaySubImagesHSV( emgs, row, col, n=64, m=64 ):

  c1 = numpy.zeros( ( row * n , col * m ) );
  c2 = numpy.zeros( ( row * n , col * m ) );
  c3 = numpy.zeros( ( row * n , col * m ) );

  index = 0
  for r in range( row ):
    for c in range( col ):
      image = normalize( emgs[index] )

      

      c1[r*n:(r+1)*n,c*m:(c+1)*m] = image[:,0:m]
      c2[r*n:(r+1)*n,c*m:(c+1)*m] = image[:,m:m*2]
      c3[r*n:(r+1)*n,c*m:(c+1)*m] = image[:,m*2:m*3]

      index += 1

  ic1 = sophia.a2if( c1 )
  ic2 = sophia.a2if( c2 )
  ic3 = sophia.a2if( c3 )

  Image.merge( 'RGB', ( ic1, ic2, ic3 ) ).show()

def displaySubImageHSV( emgs, i, n=64, m=64 ):
  """
A debugging function. Given a list of sub-images produced by splitImage and
an index into the list, displays the sub-image"""

  h = normalize( emgs[i][:,0:m], 360.0 )
  s = normalize( emgs[i][:,m:m*2], 1.0 )
  v = normalize( emgs[i][:,m*2:m*3], 1.0 )

  r, g, b = color.HSV2RGB( h, s, v )

  imr = sophia.a2i( r )
  img = sophia.a2i( g )
  imb = sophia.a2i( b )

  Image.merge( 'RGB', ( imr, img, imb ) ).show()


emgs, evls = geoff_ulman_homework3_v2.generateEigenImagesDirectory( '/home/ulman/CSI709/csi709-image-processing/homework3/test', 99999999 )

