
#include "TMath.h"


bool getLogBins(int nbins,double *bins,double xmin,double xmax){

  if ( xmin <= 0 ) return false;
  if (xmax <= xmin) return false;
  if ( nbins <= 0 ) return false;
  double fac = TMath::Power(xmax/xmin, 1.0/double(nbins));
  double x = xmin;
  for (int ibin = 0;ibin<nbins+1;ibin++){
	bins[ibin] = x;
	x *= fac;	
  }
  return true;

}
