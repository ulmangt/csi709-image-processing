import Image;
from sophia import a2i, i2a;

def Glance( fname1, fname2 ):
  i1 = Image.open( fname1 );
  i2 = Image.open( fname2 );

  i1 = i1.convert( 'RGB' );
  i2 = i2.convert( 'RGB' );

  r,g,b = i1.split()
  rd1 = sophia.i2a(r)
  gd1 = sophia.i2a(g)
  bd1 = sophia.i2a(b)

  r,g,b = i2.split()
  rd2 = sophia.i2a(r)
  gd2 = sophia.i2a(g)
  bd2 = sophia.i2a(b)

  mg2 = Image.merge('RGB', (a2i(abs(rd1-rd2)),a2i(abs(gd1-gd2)),a2i(abs(bd1-bd2))) )

  return mg2;
