

from sys import exit

class Feature:
    def __init__(self,featureType):
        self.featureType = featureType
	self.logicalAND = False
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
  	elif self.featureType == "JetVeto":
		cutString = "@jets_btagged.size() <SIGN> <THRESHOLD> " 
  	elif self.featureType == "PtInc":
		#MeV
		cutString = "Sum$(lep_momentum.Pt() <SIGN> <THRESHOLD>) >= 3"
  	elif self.featureType == "MET":
		#MeV
		cutString = "MET_final_Et <SIGN> <THRESHOLD>"
  	elif self.featureType == "NSFOS":
		cutString = "nSFOS <SIGN> <THRESHOLD>"
  	elif self.featureType == "NMu":
		cutString = "Sum$(lep_isMuon) <SIGN> <THRESHOLD>"
		#in 0 SFOS you have eem and mme (NMUONS == 1 or 2)
		#in 1 SFOS you also have eem and mme (NMUONS == 1 or 2)
		#in 2 SFOS you have eee and mmm (NMUONS == 0 or 3)
  	elif self.featureType == "Mt":
		cutString ="allLep_mt_STVF <SIGN> <THRESHOLD>"
		#self.parameters["Thresh"] = range(0,60*GeV,10*GeV)
		#self.parametersInclusive["Thresh"] = 0
  	elif self.featureType == "DPhi":
		cutString = "TMath::Abs(allLep_deltaPhiMET) <SIGN> <THRESHOLD>"
	else:
		print "Cut",self.featureType,"Not understood!"
		exit(2)
	"""
	#I need to think about how to do the Zveto stuff well, may want to take absoute value of difference with z mass
  	elif self.featureType == "ZVeto":
		#MeV
		#cutString ="Sum$(masses_SFOS > 91187.6 - <ZWindowDown> && masses_SFOS < 91187.6 + <ZWindowUp> )==0"
		cutString ="Sum$(masses_SFOS <SIGN> <THRESHOLD> )==0"
  	#elif self.featureType == "ZVetoSymm":
	#	cutString ="Sum$(masses_SFOS > 91187.6 - <ZWindow> && masses_SFOS < 91187.6 + <ZWindow> )==0"
	#	self.parameters["ZWindow"] = [15*GeV] 
	#	self.parametersInclusive["ZWindow"] = 0
  	elif self.featureType == "ZVeto_ElEl":
		#cutString = "((<1l2l>*(masses_ElEl[0] > 91187.6 - <ZWindow> && masses_ElEl[0] < 91187.6 + <ZWindow> ))+ (<1l3l>*(masses_ElEl[1] > 91187.6 - <ZWindow> && masses_ElEl[1] < 91187.6 + <ZWindow> ))+ (<2l3l>*(masses_ElEl[2] > 91187.6 - <ZWindow> && masses_ElEl[2] < 91187.6 + <ZWindow> )))==0"
		cutString = "((<1l2l>*(masses_ElEl[0] > 91187.6 - <ZWindow> && masses_ElEl[0] < 91187.6 + <ZWindow> ))+ (<1l3l>*(masses_ElEl[1] > 91187.6 - <ZWindow> && masses_ElEl[1] < 91187.6 + <ZWindow> ))+ (<2l3l>*(masses_ElEl[2] > 91187.6 - <ZWindow> && masses_ElEl[2] < 91187.6 + <ZWindow> )))==0"
		self.parameters["1l2l"] = [1]
		self.parameters["1l3l"] = [1]
		self.parameters["2l3l"] = [1]
		self.parametersInclusive["1l2l"] = 1
		self.parametersInclusive["1l3l"] = 1
		self.parametersInclusive["2l3l"] = 1
		self.parameters["ZWindow"] = [15*GeV] 
		self.parametersInclusive["ZWindow"] = 0
  	elif self.featureType == "ZVeto_MuMu":
		cutString = "((<1l2l>*(masses_MuMu[0] > 91187.6 - <ZWindow> && masses_MuMu[0] < 91187.6 + <ZWindow> ))+ (<1l3l>*(masses_MuMu[1] > 91187.6 - <ZWindow> && masses_MuMu[1] < 91187.6 + <ZWindow> ))+ (<2l3l>*(masses_MuMu[2] > 91187.6 - <ZWindow> && masses_MuMu[2] < 91187.6 + <ZWindow> )))==0"
		self.parameters["ZWindow"] = range(0,40*GeV,10*GeV)
		self.parameters["ZWindow"] = [15*GeV] #range(0,40*GeV,10*GeV)
		self.parametersInclusive["ZWindow"] = 0
		self.parameters["1l2l"] = [1]
		self.parameters["1l3l"] = [1]
		self.parameters["2l3l"] = [1]
		self.parametersInclusive["1l2l"] = 1
		self.parametersInclusive["1l3l"] = 1
		self.parametersInclusive["2l3l"] = 1
  	elif self.featureType == "ZVeto_ElMu":
		cutString = "((<1l2l>*(masses_ElMu[0] > 91187.6 - <ZWindow> && masses_ElMu[0] < 91187.6 + <ZWindow> ))+ (<1l3l>*(masses_ElMu[1] > 91187.6 - <ZWindow> && masses_ElMu[1] < 91187.6 + <ZWindow> ))+ (<2l3l>*(masses_ElMu[2] > 91187.6 - <ZWindow> && masses_ElMu[2] < 91187.6 + <ZWindow> )))==0"
		self.parameters["ZWindow"] = [15*GeV] 
		self.parametersInclusive["ZWindow"] = 0
		self.parameters["1l2l"] = [1]
		self.parameters["1l3l"] = [1]
		self.parameters["2l3l"] = [1]
		self.parametersInclusive["1l2l"] = 1
		self.parametersInclusive["1l3l"] = 1
		self.parametersInclusive["2l3l"] = 1

  	elif self.featureType == "Mass_ElEl":
		cutString = "(<All>*((<1l2l>*(masses_ElEl[0] < <Thresh> && masses_ElEl[0] >= 0 ))+ (<1l3l>*(masses_ElEl[1] < <Thresh> && masses_ElEl[1] >=0 ))+ (<2l3l>*(masses_ElEl[2] < <Thresh>  && masses_ElEl[2] >=0 ))))==0"
		self.parameters["1l2l"] = [1]
		self.parameters["1l3l"] = [1]
		self.parameters["2l3l"] = [1]
		self.parameters["All"] = [1]
		self.parametersInclusive["1l2l"] = 1
		self.parametersInclusive["1l3l"] = 1
		self.parametersInclusive["2l3l"] = 1
		self.parametersInclusive["All"] = 1
		self.parameters["Thresh"] = [15*GeV] 
		self.parametersInclusive["Thresh"] = 0
  	elif self.featureType == "Mass_MuMu":
		cutString = "(<All>*((<1l2l>*(masses_MuMu[0] < <Thresh> && masses_MuMu[0] >= 0 ))+ (<1l3l>*(masses_MuMu[1] < <Thresh> && masses_MuMu[1] >=0 ))+ (<2l3l>*(masses_MuMu[2] < <Thresh>  && masses_MuMu[2] >=0 ))))==0"
		self.parameters["Thresh"] = [15*GeV] #range(0,40*GeV,10*GeV)
		self.parametersInclusive["Thresh"] = 0
		self.parameters["1l2l"] = [1]
		self.parameters["1l3l"] = [1]
		self.parameters["2l3l"] = [1]
		self.parameters["All"] = [1]
		self.parametersInclusive["1l2l"] = 1
		self.parametersInclusive["1l3l"] = 1
		self.parametersInclusive["2l3l"] = 1
		self.parametersInclusive["All"] = 1
  	elif self.featureType == "Mass_ElMu":
		cutString = "(<All>*((<1l2l>*(masses_ElMu[0] < <Thresh> && masses_ElMu[0] >= 0 ))+ (<1l3l>*(masses_ElMu[1] < <Thresh> && masses_ElMu[1] >=0 ))+ (<2l3l>*(masses_ElMu[2] < <Thresh>  && masses_ElMu[2] >=0 ))))==0"
		self.parameters["Thresh"] = [15*GeV] 
		self.parametersInclusive["Thresh"] = 0
		self.parameters["1l2l"] = [1]
		self.parameters["1l3l"] = [1]
		self.parameters["2l3l"] = [1]
		self.parameters["All"] = [1]
		self.parametersInclusive["1l2l"] = 1
		self.parametersInclusive["1l3l"] = 1
		self.parametersInclusive["2l3l"] = 1
		self.parametersInclusive["All"] = 1
	"""

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

	print "feature",self.cutString

