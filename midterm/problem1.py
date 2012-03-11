import os, sys, scipy, numpy, eigenimage
from eface import *
from kmeans import Init2, Split
from random import shuffle

def main( ):
  """"""
  return problem1( '/home/ulman/CSI709/csi709-image-processing/class6/parsed', '/home/ulman/CSI709/csi709-image-processing/midterm/warps' )

def problem1( data_directory, warp_directory, load_warps=True ):
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

  # get names for the individuals
  name_map, name_list = getPersonMapping( fidnames )
  
  if ( load_warps ):
    # load precalculated warped images
    wmgs = LoadWarps( warp_directory )
  else:
    # warp the images to conform to the average fiduciary points
    wmgs = WarpAll( fidavg, mgs, fids )

    print 'done warps'    

    SaveWarps( wmgs, warp_directory )

    # calculate eigen images from the warped images
    emgs, evals, mgavg = GoEigen( wmgs )

    print 'done eigen'

  return clust1, mmb

def substitudeIndicesForNames( mmb, name_list ):
  """given the output of kMeansCluster(), returns an array with person names
     substituted for the data indices
     [0,2,10] might become ['mrjo0','mrjo0','mrcz0'] for example"""
  mmb_name = []
  for mmbi in mmb:
    mmbi_name = []
    for i in mmbi:
      mmbi_name.append( name_list[i] )
    mmb_name.append( mmbi_name )

  return mmb_name

def getPersonMapping( fidnames ):
  """modified from eface.py, takes a list of fidname files and create a mapping
     from data index to person name, also returns a list where each index contains
     the name of the person associated with the fiduciary points at that index"""
  # get individual names
  people_map = {}
  people_list = [None]*len(fidnames)
  for g in GetNames( fidnames ):
    people_map[g] = []
  for i in range( len( fidnames )):
    f = fidnames[i]
    loc2 = f.rfind( '/')
    loc1 = f.rfind( '/', 0, loc2-1 )
    me = f[loc1+1 : loc2]
    people_map[me].append( i )
    people_list[i] = me
  return ( people_map, people_list )

def kMeansCluster( K, data ):
  """KMeans clustering driver modified from kmeans.py"""

  # randomly assign the data vectors to clusters
  clust1 = Init2( K, data )
  
  for i in range( 3 ):

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
  
    # make some random cluster adjustments to make sure
    # we don't settle into a local maxima
    mmb = ReorderClusters( mmb )
    clust1 = ClusterAverage( mmb, data ) + 0

  return clust1, mmb


def ReorderClusters( mmb ):
  # make 10 random group swaps
  i = 10
  while ( i > 0 ):
    i1 = 0
    i2 = 0

    # the groups must not be the same
    while ( i1 == i2 ):
      i1 = random.randint(0, len(mmb)-1)
      i2 = random.randint(0, len(mmb)-1)

    # one of the groups must be large
    if ( len( mmb[i1] ) < 5 and len( mmb[i2] ) < 5 ):
      continue

    # split the groups
    mmbi11, mmbi12 = Split( mmb[i1] )
    mmbi21, mmbi22 = Split( mmb[i2] )

    # swap values as long as neither new cluster would be left empty
    if ( len( mmbi11 ) + len( mmbi21 ) != 0 and len( mmbi12 ) + len( mmbi22 ) != 0 ):
      mmbi11.extend( mmbi21 )
      mmbi12.extend( mmbi22 )
      mmb[i1] = list( mmbi11 )
      mmb[i2] = list( mmbi12 )
      i = i - 1

  return mmb

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
