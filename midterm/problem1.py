import os, sys, scipy, numpy
from eface import *
from kmeans import Init2

def main( ):
  """"""
  return problem1( '/home/ulman/CSI709/csi709-image-processing/class6/parsed' )

def problem1( directory ):
  # load names of fiduciary point files
  fidnames = FidNames( directory )
  
  # load fiduciary points
  fids = FidFiles( fidnames )

  # load images
  mgs = Images( fidnames )

  # average each fiduciary point across all images
  fidavg = AverageFid( fids )
  center = calcCenter( fidavg )
  fidavg = fidavg - center

  # shift fids to center the origin between the nostril fiduciary points
  shiftFids( fids )
  # calculate dx/dy between each personal fiduciary point and the corresponding
  # average fiduciary point
  diffFids( fids, fidavg )

  # there are 20 unique people in the dataset, so use 20 clusters
  clust1, mmb = kMeansCluster( 20, array( fids ) )

  return clust1, mmb


def kMeansCluster( K, data ):
  """KMeans clustering driver modified from kmeans.py"""

  # randomly assign the data vectors to clusters
  clust1 = Init2( K, data )
  
  ok = 1
  while ok:
    # assign data vectors to clusters
    mmb = AssignMembership( clust1, data )

    # calculate the average of each cluster
    clust2 = ClusterAverage( mmb, data )
    
    diff = ( abs( clust1-clust2) ).sum()
    if diff==0:
      ok = 0
    
    print 'Difference', diff
    clust1 = clust2 + 0
  
  return clust1, mmb


# Decide which cluster each vector belongs to
def AssignMembership( clusts, data ):
    NC = len( clusts )
    mmb = []
    for i in range( NC ):
        mmb.append( [] )

    for i in range( len( data )):
        sc = zeros( NC )
        for j in range( NC ):
            sc[j] = DiffClust(clusts[j],data[i])
        mn = sc.argmin()
        mmb[mn].append( i )
    return mmb



# compare all of the vectors to a target: abs-subtraction
def DiffClust( clust1, clust2 ):
  """a metric for comparing a given target set of fiduciary points against
     a list of other sets of fiduciary points. Based on clustering.CompareVecs()
     in the class python function library"""
  # calculate the difference between the points in each cluster
  diffs = clust1 - clust2

  # calculate the length of each x,y difference vector
  distances = numpy.sqrt( ( diffs * diffs ).sum(1) )

  # sum the lengths of the difference vectors for each fiduciary point
  return distances.sum( 0 )



def ClusterAverage( mmb, data ):
  """ClusterAverage modified from kmeans.py to accept cluster
     averages consisting of 45 x,y fiduciary point pairs"""
  # number of clusters
  K = len( mmb )
  
  # dimensions of data vectors
  N = data[0].shape
  
  # return array containing an average fiduciary point set
  # for each cluster
  clusts = zeros( (K,N[0],N[1]), float )
  
  # calculate the average fiduciary point set for each cluster
  for i in range( K ):
    vecs = data[mmb[i]]
    clusts[i] = vecs.mean(0)
  
  return clusts

def diffFids( fids, fidavg ):
  """calculate the offset of each fiduciary point in fids from its corresponding
     fiduciary point in fidavg"""
  for i in xrange( len( fids ) ):
    fids[i] = fids[i] - fidavg

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
