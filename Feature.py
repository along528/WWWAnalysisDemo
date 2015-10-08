

from sys import exit

class Feature:
    def __init__(self,featureType):
        self.featureType = featureType
	self.logicalAND = False
	self.onAllLeptons = False
	self.cutOnMass = False
	self.requiresSum = False
	self.scaleThreshold = 1.
	self.cuts = []
	self.cutString = ""
	self.Configure()
    def Reset(self):
    	self.cuts = []
	self.cutString = ""
	#self.logicalAND = False
    def HasCuts(self):
    	if self.cutString!="": return True
	return False
    def Print(self):
	print "Configured Feature",self.featureType,"for cuts:"
	print "\t",self.cutString
        #for cut in self.cuts: print "\t",cut
    def Configure(self,cut=None,direction=None):
        #configure with defaults
	sign = None
	if direction!=None:
	    if direction>0: sign = ">="
	    elif direction<0: sign = "<"
	    else:
	    	print "Warning! direction not understood. not configuring"
		return
	threshold = None
	if cut!=None: threshold = str(cut)
	    	
	cutString = ""
  	if self.featureType == "nbjets":
		cutString = "btagEff85 <SIGN> <THRESHOLD>"  
		self.onAllLeptons = False
		self.cutOnMass = False
  	elif self.featureType == "njets":
		cutString = "@jets_btagged.size() <SIGN> <THRESHOLD> " 
		self.onAllLeptons = False
		self.cutOnMass = False
  	elif self.featureType == "pt":
		#cutString = "Sum$(lep_pt <SIGN> <THRESHOLD>) >= 3"
		cutString = "lep_pt <SIGN> <THRESHOLD>"
		self.onAllLeptons = True
		self.cutOnMass = False
		self.scaleThreshold = 1000.
  	elif self.featureType == "phi":
		#cutString = "Sum$(lep_phi <SIGN> <THRESHOLD>) >= 3"
		cutString = "lep_phi <SIGN> <THRESHOLD>"
		self.onAllLeptons = True
		self.cutOnMass = False
  	elif self.featureType == "eta":
		#cutString = "Sum$(lep_eta <SIGN> <THRESHOLD>) >= 3"
		cutString = "lep_eta <SIGN> <THRESHOLD>"
		self.onAllLeptons = True
		self.cutOnMass = False
  	elif self.featureType == "charge":
		#cutString = "Sum$(lep_charge <SIGN> <THRESHOLD>) >= 3"
		cutString = "lep_charge <SIGN> <THRESHOLD>"
		self.onAllLeptons = True
		self.cutOnMass = False
  	elif self.featureType == "masselel":
		#cutString = "Sum$(masses_ElEl <SIGN> <THRESHOLD>) >= 3"
		cutString = "masses_ElEl <SIGN> <THRESHOLD>"
		self.onAllLeptons = False
		self.cutOnMass = True
		self.scaleThreshold = 1000.
  	elif self.featureType == "masselmu":
		#cutString = "Sum$(masses_ElMu <SIGN> <THRESHOLD>) >= 3"
		cutString = "masses_ElMu <SIGN> <THRESHOLD>"
		self.onAllLeptons = False
		self.cutOnMass = True
		self.scaleThreshold = 1000.
  	elif self.featureType == "massmumu":
		#cutString = "Sum$(masses_MuMu <SIGN> <THRESHOLD>) >= 3"
		cutString = "masses_MuMu <SIGN> <THRESHOLD>"
		self.onAllLeptons = False
		self.cutOnMass = True
		self.scaleThreshold = 1000.
  	elif self.featureType == "masssfos":
		#cutString = "Sum$(masses_SFOS <SIGN> <THRESHOLD>) >= 3"
		cutString = "masses_SFOS <SIGN> <THRESHOLD>"
		self.onAllLeptons = False
		self.cutOnMass = True
		self.scaleThreshold = 1000.
  	elif self.featureType == "met":
		cutString = "MET_final_Et <SIGN> <THRESHOLD>"
		self.onAllLeptons = False
		self.cutOnMass = False
		self.scaleThreshold = 1000.
  	elif self.featureType == "metphi":
		cutString = "MET_final_phi <SIGN> <THRESHOLD>"
		self.onAllLeptons = False
		self.cutOnMass = False
  	elif self.featureType == "metsumet":
		cutString = "MET_final_sumEt <SIGN> <THRESHOLD>"
		self.onAllLeptons = False
		self.cutOnMass = False
		self.scaleThreshold = 1000.
  	elif self.featureType == "nsfos":
		cutString = "nSFOS <SIGN> <THRESHOLD>"
		self.onAllLeptons = False
		self.cutOnMass = False
  	elif self.featureType == "nmuons":
		#in 0 SFOS you have eem and mme (NMUONS == 1 or 2)
		#in 1 SFOS you also have eem and mme (NMUONS == 1 or 2)
		#in 2 SFOS you have eee and mmm (NMUONS == 0 or 3)
		cutString = "Sum$(lep_isMuon) <SIGN> <THRESHOLD>"
		self.onAllLeptons = False
		self.cutOnMass = False
  	elif self.featureType == "mt":
		cutString ="allLep_mt <SIGN> <THRESHOLD>"
		self.onAllLeptons = False
		self.cutOnMass = False
		self.scaleThreshold = 1000.
  	elif self.featureType == "deltaphi":
		cutString = "allLep_deltaPhiMET <SIGN> <THRESHOLD>"
		self.onAllLeptons = False
		self.cutOnMass = False
	else:
		print "Cut",self.featureType,"Not understood!"
		exit(2)

	self.cutString = ""
	logicalAND = self.logicalAND
	if threshold==None or sign==None: return
	if self.cutOnMass:
		'''
		The way the mass veto works, we must do something special.
		Instead of asking that there are values of the mass within some range,
		we actually want that there are no values of the mass outside this range.
		this means we want to flip the signs and the logic
		'''
		if sign==">=": sign="<"
		else: sign=">="
		logicalAND = not self.logicalAND
	cutString = cutString.replace("<SIGN>",sign)
	cutString = cutString.replace("<THRESHOLD>",str(float(threshold)*self.scaleThreshold))
	self.cuts.append(cutString)

	if len(self.cuts)>0:
		self.cutString = self.cuts[0]
	if len(self.cuts)>1:
		self.cutString+= " %s " % ("&&" if logicalAND else "||")
		self.cutString+= self.cuts[1]
	if self.onAllLeptons:
		self.cutString = "Sum$("+self.cutString+") >=3"
	elif self.cutOnMass:
		self.cutString = "Sum$("+self.cutString+") ==0"


