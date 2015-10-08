from math import pow,log10

def getLogBins(nbins,xmin,xmax):
  if ( xmin <= 0 ): return 0
  if  xmax <= xmin : return 0
  if ( nbins <= 0 ): return 0
  bins =[]
  fac = pow(float(xmax)/float(xmin), 1.0/float(nbins))
  x = xmin
  for ibin in range(nbins+1):
	bins.append(x)
	x *= fac;	
  return bins

def convertLogFractionToPhysical(fracvalue,fracmin,fracmax,physmin,physmax):
    rate = log10(physmax/physmin)/(fracmax-fracmin)
    offset = log10(physmax) - rate*fracmax
    physvalue = pow(10,rate*fracvalue+offset)
    return physvalue

def convertLinearFractionToPhysical(fracvalue,fracmin,fracmax,physmin,physmax):
    rate = (physmax-physmin)/(fracmax-fracmin)
    offset = physmax - rate*fracmax
    physvalue = rate*fracvalue+offset
    return physvalue

def getLinearBins(nbins,xmin,xmax):
    
    if ( nbins <= 0 ): return 0
    if  xmax <= xmin : return 0
    bins = []
    step = float(xmax-xmin)/float(nbins)
    for binnum in range(0,nbins+1):
        bins.append(xmin+step*binnum)
    return bins

