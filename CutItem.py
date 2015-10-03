
import wx
class CutItem:
    def __init__(self,name,imageName):
    	self.name = name
	self.imageName = imageName
	self.image = wx.Image(item.imageName, wx.BITMAP_TYPE_ANY)
	self.imageControl = None
        self.xmin = -1
        self.xmax = -1
        self.nbins = 0
	#from looking at an image
	#the first gives the end point of the left margin
	#as a fraction of the total width
	self.fractionBinStart = 52./326.
	#and this gives the start point of the right margin
	#as a fraction of the total width
	self.fractionBinEnd = 307./326.
	self.fractionTopStart =  6/311.
	self.fractionBottomEnd =  204/311.
	self.cuts=[]
	#self.fractionBottom = 
    def update(self):
	self.bitmap = wx.BitmapFromImage(image)
	self.imageControl = wx.StaticBitmap(self, wx.ID_ANY, self.bitmap)
    def getLowBinEdge(self,xvalue, getInXCoordinates=False):
    	#xvalue should be the fraction along the total width of the image

	position = self.fractionBinStart
	step = (self.fractionBinEnd - self.fractionBinStart)/self.nbins
	binnum = -1
	while True: #position < self.fractionBinEnd:
	    print "position",position
	    if xvalue < position:
	        break
	    position += step
	    binnum+=1
	
	if binnum < 0  or binnum > self.nbins-1: 
		print "Couldn't get cut value for input",xvalue
		return None
	binEdge = self.xmin + (self.xmax - self.xmin)*binnum/self.nbins
	if getInXCoordinates:
		return position - step
		
	return binEdge
    def addCut(self,xvalue,threshold,isGreaterThan):
    	#if not > then it is <
	#xvalue should be the fraction along the image
    	self.cuts.append([xvalue,threshold,isGreaterThan])
	
        
    


