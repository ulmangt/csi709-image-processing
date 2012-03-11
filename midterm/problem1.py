import os, sys, scipy, numpy, warp
from eface import *

def main( ):
  """"""
  problem1( '/home/ulman/CSI709/csi709-image-processing/class6/parsed' )

def problem1( directory ):
  # load names of fiduciary point files
  fidnames = FidNames( directory )
  
  # load fiduciary points
  fids = FidFiles( fidnames )

  # load images
  mgs = Images( fidnames )

  # average each fiduciary point across all images
  fidavg = AverageFid( fids )

def shiftFids( fids ):
  """shift all the fiduciary points so that the origin falls on the point
     directly between the two nostril fiduciary points"""
  for i in xrange( len( fids ) ):
    center = calcCenter( fids[i] )
    fids[i] = fids[i] - center

def calcCenter( fid ):
  """calculate the average of the two nostril fiduciary points, we define
     this value as the center of the fiduciary point grid"""
  #fiduciary points at index 14 and 15 are the left and right nostrils
  return fid[14:16].mean(0)

if __name__ == "__main__":
  main() 
