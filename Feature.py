

from sys import exit

class Feature:
    def __init__(self,featureType):
        self.featureType = featureType
	self.logicalAND = False
	self.onAllLeptons = False
	self.requiresSum = False
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
  	if self.featureType == "BJetVeto":
		cutString = "btagEff85 <SIGN> <THRESHOLD>"  
		self.onAllLeptons = False
  	elif self.featureType == "JetVeto":
		cutString = "@jets_btagged.size() <SIGN> <THRESHOLD> " 
		self.onAllLeptons = False
  	elif self.featureType == "PtInc":
		#cutString = "Sum$(lep_pt <SIGN> <THRESHOLD>) >= 3"
		cutString = "lep_pt <SIGN> <THRESHOLD>"
		self.onAllLeptons = True
  	elif self.featureType == "Phi":
		#cutString = "Sum$(lep_phi <SIGN> <THRESHOLD>) >= 3"
		cutString = "lep_phi <SIGN> <THRESHOLD>"
		self.onAllLeptons = True
  	elif self.featureType == "Eta":
		#cutString = "Sum$(lep_eta <SIGN> <THRESHOLD>) >= 3"
		cutString = "lep_eta <SIGN> <THRESHOLD>"
		self.onAllLeptons = True
  	elif self.featureType == "Charge":
		#cutString = "Sum$(lep_charge <SIGN> <THRESHOLD>) >= 3"
		cutString = "lep_charge <SIGN> <THRESHOLD>"
		self.onAllLeptons = True
  	elif self.featureType == "MassElEl":
		#cutString = "Sum$(masses_ElEl <SIGN> <THRESHOLD>) >= 3"
		cutString = "masses_ElEl <SIGN> <THRESHOLD>"
		self.onAllLeptons = True
  	elif self.featureType == "MassElMu":
		#cutString = "Sum$(masses_ElMu <SIGN> <THRESHOLD>) >= 3"
		cutString = "masses_ElMu <SIGN> <THRESHOLD>"
		self.onAllLeptons = True
  	elif self.featureType == "MassMuMu":
		#cutString = "Sum$(masses_MuMu <SIGN> <THRESHOLD>) >= 3"
		cutString = "masses_MuMu <SIGN> <THRESHOLD>"
		self.onAllLeptons = True
  	elif self.featureType == "MassSFOS":
		#cutString = "Sum$(masses_SFOS <SIGN> <THRESHOLD>) >= 3"
		cutString = "masses_SFOS <SIGN> <THRESHOLD>"
		self.onAllLeptons = True
  	elif self.featureType == "MET":
		cutString = "MET_final_Et <SIGN> <THRESHOLD>"
		self.onAllLeptons = False
  	elif self.featureType == "METPhi":
		cutString = "MET_final_phi <SIGN> <THRESHOLD>"
		self.onAllLeptons = False
  	elif self.featureType == "METSumEt":
		cutString = "MET_final_sumEt <SIGN> <THRESHOLD>"
		self.onAllLeptons = False
  	elif self.featureType == "NSFOS":
		cutString = "nSFOS <SIGN> <THRESHOLD>"
		self.onAllLeptons = False
  	elif self.featureType == "NMu":
		#in 0 SFOS you have eem and mme (NMUONS == 1 or 2)
		#in 1 SFOS you also have eem and mme (NMUONS == 1 or 2)
		#in 2 SFOS you have eee and mmm (NMUONS == 0 or 3)
		cutString = "Sum$(lep_isMuon) <SIGN> <THRESHOLD>"
		self.onAllLeptons = False
  	elif self.featureType == "Mt":
		cutString ="allLep_mt <SIGN> <THRESHOLD>"
		self.onAllLeptons = False
  	elif self.featureType == "DPhi":
		cutString = "allLep_deltaPhiMET <SIGN> <THRESHOLD>"
		self.onAllLeptons = False
	else:
		print "Cut",self.featureType,"Not understood!"
		exit(2)

	self.cutString = ""
	if threshold==None or sign==None: return
	cutString = cutString.replace("<SIGN>",sign)
	cutString = cutString.replace("<THRESHOLD>",threshold)
	self.cuts.append(cutString)

	if len(self.cuts)>0:
		self.cutString = self.cuts[0]
	if len(self.cuts)>1:
		self.cutString+= " %s " % ("&&" if self.logicalAND else "||")
		self.cutString+= self.cuts[1]
	if self.onAllLeptons:
		self.cutString = "Sum$("+self.cutString+") >=3"


