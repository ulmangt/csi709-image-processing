def kmeans( vecs, gamma ):
  """a k-means clustering algorithm based on clustering.CheapClustering()
     in the class python function library"""
  # vecs: array of data vectors
  # gamma: threshold.  Below this is a match
  clusters = [ ]  # collect the clusters here.
  ok = 1
  work = list(vecs) # copy of data that can be destroyed
  while ok:
    target = work.pop( 0 )
    # score for all remaining vecs in work
    scores = CompareVecs(target, work )
    # threshold vectors
    nz = nonzero( less( scores, gamma) )[0][::-1]
    group = []
    group.append( target )
    # add vectors to group
    for i in nz:
      group.append( work.pop( i ) )
      clusters.append( group )
      if len( work )==1:
        clusters.append( [work.pop(0)])
      if len(work)==0:
        ok = 0
  return clusters


# compare all of the vectors to a target: abs-subtraction
def CompareVecs( target, vecs ):
  """a metric for comparing a given target set of fiduciary points against
     a list of other sets of fiduciary points. Based on clustering.CompareVecs()
     in the class python function library"""
  # number of vectors
  N = len( vecs )

  # calculate the difference between each vector and the target
  diffs = abs( target - vecs )

  # calculate the length of each x,y difference vector
  distances = numpy.sqrt( ( diffs * diffs ).sum(2) )

  # sum the lengths of the difference vectors for each fiduciary point
  total_distance = distances.sum(1)
  return scores



# compare all of the vectors to a target: abs-subtraction
def DiffClust( clust1, clust2 ):
  """a metric for comparing a given target set of fiduciary points against
     a list of other sets of fiduciary points. Based on clustering.CompareVecs()
     in the class python function library"""
  # calculate the difference between the points in each cluster
  diffs = clust1 - clust2

  # calculate the length of each x,y difference vector
  distances = numpy.sqrt( ( diffs * diffs ).sum(2) )

  # sum the lengths of the difference vectors for each fiduciary point
  total_distance = distances.sum(1)
  return scores

