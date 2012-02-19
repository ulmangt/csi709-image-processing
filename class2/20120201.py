Python 2.7.1+ (r271:86832, Apr 11 2011, 18:05:24) 
[GCC 4.5.2] on linux2
Type "copyright", "credits" or "license()" for more information.
==== No Subprocess ====
>>> 309*229*3
212283
>>> 212/13.
16.307692307692307
>>> import os
>>> os.chdir('/media/8E80DA7580DA636F/science/courses/ImageProc')
>>> import Image
>>> mg = Image.open( 'egypt.jpg')
>>> mg.size
(309, 229)
>>> mg.mode
'RGB'
>>> mg.show()
>>> mg.show()
>>> mg2 = mg.rotate( 20 )
>>> mg2.show()
>>> mg2 = mg.rotate( 20 , expand=1)
>>> mg2.show()
>>> 
>>> 
>>> import Image
>>> mg = Image.open( 'egypt.jpg')
>>> mg.mode
'RGB'
>>> mg.size
(309, 229)
>>> 
>>> dir( mg )
['_Image__transformer', '__doc__', '__getattr__', '__init__', '__module__', '__repr__', '_copy', '_dump', '_expand', '_getexif', '_makeself', '_new', '_open', 'app', 'applist', 'bits', 'category', 'convert', 'copy', 'crop', 'decoderconfig', 'decodermaxblock', 'draft', 'filename', 'filter', 'format', 'format_description', 'fp', 'fromstring', 'getbands', 'getbbox', 'getcolors', 'getdata', 'getextrema', 'getim', 'getpalette', 'getpixel', 'getprojection', 'histogram', 'huffman_ac', 'huffman_dc', 'icclist', 'im', 'info', 'layer', 'layers', 'load', 'load_djpeg', 'load_end', 'load_prepare', 'mode', 'offset', 'palette', 'paste', 'point', 'putalpha', 'putdata', 'putpalette', 'putpixel', 'quantization', 'quantize', 'readonly', 'resize', 'rotate', 'save', 'seek', 'show', 'size', 'split', 'tell', 'thumbnail', 'tile', 'tobitmap', 'tostring', 'transform', 'transpose', 'verify']
>>> 
>>> 
>>> r,g,b = mg.split()
Traceback (most recent call last):
  File "<pyshell#24>", line 1, in <module>
    r,g,b = mg.split()
  File "/usr/lib/python2.7/dist-packages/PIL/Image.py", line 1497, in split
    if self.im.bands == 1:
AttributeError: 'NoneType' object has no attribute 'bands'
>>> mg = mg.convert('RGB' )
>>> r,g,b = mg.split()
>>> r.show()
>>> g.show()
>>> g.show()
>>> b.show()
>>> mg2 = Image.merge( 'RGB', (r,g,b) )
>>> mg2.show()
>>> mg2 = Image.merge( 'RGB', (g,r,b) )
>>> mg2.show()
>>> Image.merge( 'RGB', (g,r,b) ).show()
>>> 
>>> 
>>> 
>>> 
>>> # second glance
>>> mg1 = Image.open( 'SecondGlance/20120129a.jpg')
>>> mg2 = Image.open('SecondGlance/20120129b.jpg')
>>> r,g,b = mg1.split()
Traceback (most recent call last):
  File "<pyshell#43>", line 1, in <module>
    r,g,b = mg1.split()
  File "/usr/lib/python2.7/dist-packages/PIL/Image.py", line 1497, in split
    if self.im.bands == 1:
AttributeError: 'NoneType' object has no attribute 'bands'
>>> mg1 = mg1.convert('RGB' )
>>> r,g,b = mg1.split()
>>> import sophia
Traceback (most recent call last):
  File "<pyshell#46>", line 1, in <module>
    import sophia
ImportError: No module named sophia
>>> import sys
>>> sys.path.append('pysrc')
>>> import sophia
>>> rdata = sophia.i2a( r )
>>> rdata.shape
(524, 785)
>>> r1data = sophia.i2a( r )
>>> g1data = sophia.i2a( g )
>>> b1data = sophia.i2a( b )
>>> r,g,b = mg2.split()
Traceback (most recent call last):
  File "<pyshell#55>", line 1, in <module>
    r,g,b = mg2.split()
  File "/usr/lib/python2.7/dist-packages/PIL/Image.py", line 1497, in split
    if self.im.bands == 1:
AttributeError: 'NoneType' object has no attribute 'bands'
>>> mg2 = mg2.convert('RGB')
>>> r,g,b = mg2.split()
>>> r2data = sophia.i2a( r )
>>> g2data = sophia.i2a( g )
>>> b2data = sophia.i2a( b )
>>> 
>>> 
>>> os.getcwd()
'/media/8E80DA7580DA636F/science/courses/ImageProc'
>>> os.chdir('..')
KeyboardInterrupt
>>> rd= abs( r1data + r2data )
>>> rd= abs( r1data + g2data )
KeyboardInterrupt
>>> rd= abs( r1data - r2data )
>>> gd= abs( g1data - g2data )
>>> bd= abs( b1data - b2data )
>>> rdmg = sophia.a2i( rd )
>>> rdmg.show()
>>> rdmg = sophia.a2i( rd )
KeyboardInterrupt
>>> gdmg = sophia.a2i( gd )
>>> bdmg = sophia.a2i( bd )
>>> 
>>> 
>>> mg3= Image.merge( 'RGB', (rdmg, gdmg, bdmg) )
>>> mg3.show()
>>> mask = mg3.convert('L')
>>> mask = sophia.i2a( mask )
>>> mask = mask > 0.1
>>> sophia.a2i( mask ).show()
>>> mask = mask*0.5 + 0.5
>>> answ = rdata * mask
>>> sophia.a2i( answ ).show()
>>> 
>>> import secondglance as sg
Traceback (most recent call last):
  File "<pyshell#84>", line 1, in <module>
    import secondglance as sg
ImportError: No module named secondglance
>>> import glance
>>> mg3 = glance.Glance( 'SecondGlance/20120129a.jpg', 'SecondGlance/20120129b.jpg')
Traceback (most recent call last):
  File "<pyshell#86>", line 1, in <module>
    mg3 = glance.Glance( 'SecondGlance/20120129a.jpg', 'SecondGlance/20120129b.jpg')
  File "pysrc/glance.py", line 30, in Glance
    mg3= Image.merge( 'RGB', (rdmg, gdmg, bdmg) )
NameError: global name 'rdmg' is not defined
>>> reload( glance )
<module 'glance' from 'pysrc/glance.py'>
>>> mg3 = glance.Glance( 'SecondGlance/20120129a.jpg', 'SecondGlance/20120129b.jpg')
>>> mg3.show()
>>> reload( glance )
<module 'glance' from 'pysrc/glance.py'>
>>> mg3 = glance.Glance( 'SecondGlance/20120129a.jpg', 'SecondGlance/20120129b.jpg')
>>> show
Traceback (most recent call last):
  File "<pyshell#92>", line 1, in <module>
    show
NameError: name 'show' is not defined
>>> mg3.show()
>>> reload( glance.sophia )
<module 'sophia' from 'pysrc/sophia.py'>
>>> 
>>> 
>>> 
[DEBUG ON]
>>> mg3 = glance.Glance( 'SecondGlance/20120129a.jpg', 'SecondGlance/20120129b.jpg')
[DEBUG ON]
>>> 
[DEBUG OFF]
>>> import dance
Traceback (most recent call last):
  File "<pyshell#96>", line 1, in <module>
    import dance
ImportError: No module named dance
>>> import dancer
Traceback (most recent call last):
  File "<pyshell#97>", line 1, in <module>
    import dancer
ImportError: No module named dancer
>>> sys.path.append('/media/8E80DA7580DA636F/science/basil')
>>> import dancer
>>> q = dancer.Dancer('/media/8E80DA7580DA636F/science/basil')
Traceback (most recent call last):
  File "<pyshell#100>", line 1, in <module>
    q = dancer.Dancer('/media/8E80DA7580DA636F/science/basil')
  File "/media/8E80DA7580DA636F/science/basil/dancer.py", line 17, in __init__
    self.mg = [ Image.open( JPY + 'wet_floorboard.jpg')]
  File "/usr/lib/python2.7/dist-packages/PIL/Image.py", line 1952, in open
    fp = __builtin__.open(fp, "rb")
IOError: [Errno 2] No such file or directory: '/media/8E80DA7580DA636F/science/basilwet_floorboard.jpg'
>>> 
