import os, sys, scipy, numpy, math, operator
from eface import *
from numpy import cov, dot
from kmeans import Init2, Split

def main( ):
  """"""
  return recognition_system( '/home/ulman/CSI709/csi709-image-processing/class6/parsed' )

def recognition_system( data_directory ):
  # load names of fiduciary point files
  fidnames = FidNames( data_directory )
  
  # load fiduciary points
  fids = FidFiles( fidnames )

  # average each fiduciary point across all images
  fidavg = AverageFid( fids )
  center = calcCenter( fidavg )
  fidavg = fidavg - center

  # shift fids to center the origin between the nostril fiduciary points
  shiftFids( fids )
  # calculate dx/dy between each personal fiduciary point and the corresponding
  # average fiduciary point
  diffFids( fids, fidavg )

  print '\n\nRunning K-Means Clustering...\n'

  # there are 20 unique people in the dataset, so use 20 clusters
  clust1, mmb = kMeansCluster( 20, array( fids ) )

  # get names for the individuals and turn the kmeans cluster output
  # from indices into person identifiers
  name_map, name_list = getPersonMapping( fidnames )
  mmb_names = substitudeIndicesForNames( mmb, name_list )
  # get the names of the people in the data set
  gnames = GetNames( fidnames )

  print '\n\nCalculating Gini Index of Clusters...\n'

  # calculate the gini index for each cluster (a sense of the purity
  # of each cluster)
  for names in mmb_names:
    gini = calculateGiniIndex( names )
    print 'Cluster: ', names, 'Gini Index: ', gini
 
  # calculate some sizes then reshape the centered dx/dy fiduciary point data
  # into a 2D matrix with a column vector of data (size 90) for each person
  num_people = len( fids )
  data_per_person = reduce(operator.mul, fids[0].shape )
  fids_pca_in = numpy.array( fids ).reshape( ( num_people, data_per_person ) )

  # calculate the bias in the input data  
  fids_pca_mean = fids_pca_in.mean( 0 )

  print '\n\nPerforming Leave-One-Out Cross Validation...\n'

  print 'Predicted Class, True Class, Distance To Neighbor'

  # perform leave-one-out cross-validation on the recognition system
  # create 84 (num_people) different PCA spaces, each using 83 of the
  # data points, and use it to attempt to classify the remaining data point
  correct_count = 0
  for i in range( num_people ):
    fids_pca_in_minus_one = numpy.delete( fids_pca_in, i, 0 )
    name_list_minus_one = list(name_list)
    name_list_minus_one.pop( i )

    # transform the fiduciary points into a 3 dimensional PCA space which we can plot
    cffs, vecs = PCA( fids_pca_in_minus_one, 3 )

    # transform the unknown point into pca space
    unk_point = fidToPcaSpace( fids_pca_in[i], vecs )
  
    # use the known points to classify the unknown point
    dist, unk_class = classify( unk_point, cffs, name_list_minus_one )

    # get the true classification of the 'unknown' point
    true_class = name_list[i]

    # count how many we get right
    if unk_class == true_class :
      correct_count += 1
      print 'CORRECT:', unk_class, true_class, dist
    else:
      print 'WRONG:', unk_class, true_class, dist


  # calculate and print the estimate error of the classification system
  error = 1 - float( correct_count ) / float( num_people )

  print '\nClassification Error:', error

  # use the routine from the class resource eface.py to generate a gnuplot command
  # commented out since it generates lots of files
  #plot_command = PlotPeople( cffs, fidnames, gnames )



def classify( unknown, known_list, name_list ):
  """given an unknown point in PCA space and a list of known points in PCA space
     (identified by the correpsonding entries in name_list), use a simple
     nearest neighbor classifier to classify the unknown point"""
 
  closestDist = None
  closestName = None

  for i, name in enumerate( name_list ) :

   # calculate the euclidian distance between the unknown and known point
    dist = numpy.linalg.norm( unknown - known_list[i] )
  
    # search through the points, looking for the closest
    if closestDist == None or dist < closestDist:
      closestDist = dist
      closestName = name

  # return the classification of the closest known point we found
  # this is our classification of the unknown point
  return closestDist, closestName



def fidToPcaSpace( fid, vecs ):
  """given a set of fiduciary points and a set of vectors defining a PCA space
     transforms the given fiduciary points into the PCA space"""

  # allocate an array to return the result in
  result = zeros( len( vecs ) )

  # iterate over the eigenvectors, dotting each with the ficuciary point data vector
  for i, vec in enumerate( vecs ):
    result[i] = dot( fid, vec )

  # return the result
  return result



# pca.py
# modified from class materials, chapter 8 Principal Component Analysis
def PCA( indata, D=2 ):
  """given fiduciary points from multiple faces, construct a PCA space
     with D dimensions and project the fiduciary points into the new space"""

  # center the data (remove bias)
  a = indata - indata.mean(0)

  # calculate covariance
  cv = cov( a.transpose() )

  # calculate eigenvectors and eigenvalues
  evl, evc = numpy.linalg.eig( cv )

  # map the input data intp the new eigenvalue space 
  V,H = indata.shape
  cffs = zeros( (V,D) )
  ag = abs(evl).argsort( )
  ag = ag[::-1]
  me = ag[:D]
  for i in range( V ):
    k = 0
    for j in me:
      cffs[i,k] = (indata[i] * evc[:,j]).sum()
      k += 1
  vecs = evc[:,me].transpose()

  return cffs, vecs



def calculateGiniIndex( names ):
  """calculate the gini index for the given cluster, a measure
     of the purity of the cluster.
     a gini index of 0 indicates the cluster consists of only
     data from a single person."""

  # create a dictionary containing the number of times each name appears in the list
  d = dict((i,names.count(i)) for i in names)

  # if there is only one or zero items, the gini index is 0
  if ( len( d ) < 2 ):
    return 0.0

  size = len( names )
  accum = 0

  # perform gini index calculation
  for k,v in d.iteritems():
    p = float( v ) / float( size )
    accum += p * ( 1 - p )

  return accum



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



# eface.py
# modified from class materials
def getPersonMapping( fidnames ):
  """takes a list of fidname files and create a mapping
     from data index to person name, also returns a list where each index contains
     the name of the person associated with the fiduciary points at that index"""
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



# kmeans.py
# modified from class materials
def kMeansCluster( K, data ):
  """KMeans clustering driver"""

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



# kmeans.py
# modified from class materials
def AssignMembership( clusts, data ):
  """Decide which cluster each vector belongs to"""
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



# kmeans.py
# modified from class materials
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



# kmeans.py
# modified from class materials
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

