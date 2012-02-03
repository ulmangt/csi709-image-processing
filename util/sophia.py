# -*- coding: utf-8 -*-
# sophia.py  (Greek for knowledge)
# 13 Sept 2011
# J. M. Kinser

from numpy import arctan, arctan2, array, convolve, cos, fromstring
from numpy import indices, pi, ravel, sin, sqrt, uint8, zeros
from scipy.ndimage import map_coordinates
from scipy.signal import cspline2d
from scipy import fftpack 
import Image

## ###########  Image Conversion ############

# convert an array to an image
def a2i( indata ):
    mg = Image.new( 'L', indata.transpose().shape)
    mn = indata.min()
    a = indata - mn
    mx = a.max()
    a = a*256./mx
    mg.putdata( ravel(a))
    return mg

# convert an array to an image without scaling
def a2if( data ):
    mg = Image.new( 'L', transpose(data).shape)
    mg.putdata( ravel(data))
    return mg

# convert gray-scale image to an array
def i2a( mg ):
    mgt = mg.transpose(2).transpose(1)
    f = mgt.getdata()
    z = array(f)
    zz = z.reshape( mg.size ).transpose()
    return zz

def i2a( mg ):
    H,V = mg.size
    d = fromstring( mg.tostring(), uint8)
    d = d.reshape( (V,H) )
    return d

## ############### PLOTTING #############
def PlotSave( name, data ):
    # the number of rows
    if len(data.shape)>1:
        (nc,nr) = data.shape
    else :
    	nc = data.shape[0]
    	nr = 1
    fp = open( name, 'w')
    if nr > 1 :
        for i in range(0,nc):
            for j in range(0,nr):
                fp.write( str( data[i,j] ))
                fp.write(' ')
            fp.write('\n')
    else:
        for i in range(0,nc):
            fp.write( str(data[i]) )
            fp.write( '\n' )          
    fp.close()

def PlotRead( name ):
    fp = open( name, 'r' )
    a = fp.readline()
    b = a.split()
    N = len(b)	# horizontal dimension
    dalist = []
    dalist.append( b )
    ok=1
    while ok ==1:
        a=fp.readline()
        b=a.split()
        if len(b)>0:
            dalist.append( b )
        else:
            ok = 0
    M = len( dalist )
    # so far the data is in a list.  convert to an array
    data = zeros( (M,N), float )	# 'd'=Float
    for i in range(0,M):
        for j in range(0,N):
            data[i,j] = float( dalist[i][j] )
    fp.close()
    return data

## ### ###  Image Creations ### ###
def Circle( size, loc,rad):
    """Create a frame with a binary filled circle
    size is (v,h) of size of array
    loc is (v,h) of circle location
    rad is integer of radius"""
    b1,b2 = indices( size )
    b1,b2 = b1-loc[0], b2-loc[1]
    mask = b1*b1 + b2*b2
    mask = (mask <= rad*rad ).astype(int)
    return mask

def Wedge( vh, t1, t2 ):
    """in degrees"""
    ans = zeros( vh )
    ndx = indices( vh ).astype(float)
    ndx[0] = ndx[0] - vh[0]/2
    ndx[1] = ndx[1] - vh[1]/2
    # watch out for divide by zero
    mask = ndx[0] == 0
    ndx[0] = (1-mask)*ndx[0] + mask*1e-10
    # compute the angles
    ans = arctan( ndx[1] / ndx[0] )
    # mask off the angle
    ans = ans + pi/2    # scales from 0 to pi
    mask = ans >= t1/180.*pi 
    mask2 = ans < t2/180.*pi 
    mask = (mask * mask2).astype(int)
    return mask

## ### ###  MEtrics ### ###

def Distance( p1, p2 ):
    a = p1-p2
    return sqrt( (a**2).sum() )

# For images with localized regions: use scipy labels and ...
# scipy.ndimage.measurements.standard_deviation
# scipy.ndimage.measurements.variance
def LocalStdDev( data, radius ):
    N = pi * radius**2 # number of points
    x = cspline2d( data, 30*radius )
    dev = (data - x)**2
    V,H = data.shape
    a = Circle( (V,H), (V/2,H/2), radius )
    dev = Correlate( dev, a ).real
    dev = sqrt( dev/N )
    return dev

## ### ###  Geometric transformations ### ###

def RPolar( data, pxy ):
    """Radius Polar Transormation"""
    ndx = indices( data.shape )
    v,h = data.shape
    a = ndx[1].astype(float)
    a = a / h * 2 *pi
    x = ndx[0] * cos(a)
    y = ndx[0] * sin(a)
    ndx[0] = x.astype(int) + pxy[0]
    ndx[1] = y.astype(int) + pxy[1]
    answ = map_coordinates( data, ndx )
    return answ


def IRPolar( rpdata, pxy ):
    """Inverse Radius Polar Transormation"""
    ndx = indices( rpdata.shape )
    ndx[0] -= pxy[0]
    ndx[1] -= pxy[1]
    v,h = rpdata.shape
    r = sqrt( ndx[0]**2 + ndx[1]**2 )
    theta = arctan2( -ndx[1], -ndx[0] )/2/pi*h
    ndx[0] = r.astype(int)
    ndx[1] = theta.astype(int) +h/2 
    ndx[1][pxy[0]:,pxy[1]] -=1
    answ = map_coordinates( rpdata, ndx )
    return answ

def Barrel ( data, bend, cvh ):
    """Barrel (bend>1) and Pincushion (0<bend<1)"""
    cv,ch = cvh
    a = indices(data.shape)
    V,H = data.shape
    a[0],a[1] = cv-a[0],a[1]-ch
    r = sqrt( a[0]*a[0] + a[1]*a[1] )
    t = arctan2( a[0], a[1] )
    r = (r ** bend)/(cv**(bend-1))
    x = r* cos( t );     y = r* sin( t )
    x = x + ch;     y = cv - y
    coords = array([y.astype(int),x.astype(int)])
    z = map_coordinates( data, coords )
    return z

## ### ###  Correlations ### ###

def Swap( mat ):
    #performs a quadrant swap
    V,H = mat.shape
    V2, H2 = V/2 ,H/2
    ans = zeros( (V,H), mat.dtype )
    ans[:V2, :H2] = mat[-V2:,-H2:] + 0
    ans[:V2, -H2:] = mat[-V2:,:H2] + 0
    ans[-V2:, :H2] = mat[:V2,-H2:] + 0
    ans[-V2:, -H2:] = mat[:V2,:H2] + 0
    return ans

def Correlate( A, B, sw=0 ):
    # performs Fourier space correlation
    # switch: 0 assumes, A, B, and C are in object space
    # switch: 1 is A and B in F space.  C in object space
    n = len( A.shape )
    if sw==0 and n==1:
        a = fftpack.fft(A)
        b = fftpack.fft(B)
        c = a * b.conjugate( )
        C = fftpack.ifft( c );
        C = Swap(C);
    if sw==0 and n==2:
        a = fftpack.fft2( A) 
        b = fftpack.fft2(B)
        c = a * b.conjugate( )
        C = fftpack.ifft2( c )
        C = Swap(C)
    if sw==1 and n==2:
        c = A * B.conjugate( )
        C = fftpack.ifft2( c )
        C = Swap(C)
    return C

# ### ### ### ### ### ###  Geometry
def FindCircleCenter( p1, p2, p3 ):
    # given three points on the circle, find the center
    # lines: l1 = line(p1,p2), l2 = line(p2,p3)
    # convert to array
    if type(p1)==type((1,1)):
        #it's a tuple - not an array
        p1,p2,p3 = array(p1),array(p2),array(p3)
    # find midpoints of l1 and l2
    p1,p2,p3 = p1.astype(float),p2.astype(float), p3.astype(float)
    dl1 = (p1+p2)/2.
    dl2 = (p2+p3)/2.
    # find slopes for l1 and l2
    if p2[0]==p1[0]: 
        ml1 = 999999.
    else:
        ml1 = (p2[1]-p1[1]) / (p2[0]-p1[0])
    if p2[0]==p3[0]: 
        ml2 = 999999.
    else:
        ml2 = (p3[1]-p2[1]) / (p3[0]-p2[0])
    # find slopes for bisectors b1 and b2.  They bisect l1 and l2
    if ml1 !=0: mb1 = -1./ml1
    else: mb1 = 999999.
    if ml2 !=0: mb2 = -1./ml2
    else: mb2 = 999999.
    # find intercepts of b1 and b2
    b1 = dl1[1] - mb1 * dl1[0]
    b2 = dl2[1] - mb2 * dl2[0]
    # find point where b1 and b2 intersect
    x = (b2-b1)/(mb1-mb2)
    y = mb1 * x + b1
    return x,y
