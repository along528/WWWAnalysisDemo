
import wx
import math
class CutItem:
    def __init__(self,name,imageName,frame,xmin=-1,xmax=-1,nbins=0):
    	self.name = name
	self.imageName = imageName
	self.image = wx.Image(self.imageName, wx.BITMAP_TYPE_ANY)
	self.bitmap = wx.BitmapFromImage(self.image)
	self.frame = frame
	self.imageControl = wx.StaticBitmap(self.frame, wx.ID_ANY, self.bitmap)
        self.xmin = xmin
        self.xmax = xmax
        self.nbins = nbins
	self.gridSizer = None
	self.cutDirection = 0
	self.index = -1
	self.dc = None
	self.doCutAtBinEdge = False
	self.tmpLines = []
	self.savedLines = []
	self.CutThresholdsAndDirections = []


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
    def CutAtBinEdge(self,switch=False):
    	self.doCutAtBinEdge = switch
    def SetGridSizer(self,grid,index):
    	#this allows the item to access informtion about itself in the gridSizer that holds it
    	self.gridSizer = grid
	self.index = index
    def IsInPosition(self,position):
    	if not self.gridSizer: 
		print "Error! Item not aware of grid position"
		return False
	xRange = self.GetXRange()
	yRange = self.GetYRange()
        imagePosition = self.GetPosition()
	imageSize = self.GetSize()
	if position[0] > xRange[0] and \
	   position[0] < xRange[1] and \
	   position[1] > yRange[0] and \
	   position[1] < yRange[1]: 
		return True
	return False
    def GetMousePosition(self,position,physical=False):
	positionFraction = float(position[0]-self.GetPosition()[0])/float(self.GetSize()[0])
	positionPhysical = (self.xmax-self.xmin)*(positionFraction-self.fractionBinStart)/(self.fractionBinEnd-self.fractionBinStart)
        if self.doCutAtBinEdge:
	    positionFraction = self.getLowBinEdge(positionFraction,True)
	    positionPhysical = self.getLowBinEdge(positionFraction)
	print "posblah",positionFraction,positionPhysical
	if physical: return positionPhysical
	return positionFraction
    def Save(self):
    	for line in self.tmpLines:
	   self.savedLines.append(line)
	self.CutThresholdsAndDirections.append([self.positionPhysical,self.cutDirection])
    def Clear(self):
    	self.savedLines = []
	self.CutThresholdsAndDirections = []
	self.Reset()
    def ComputeCutThreshold(self,position):
	self.positionFraction = self.GetMousePosition(position)
	self.positionPhysical = self.GetMousePosition(position,physical=True)
    def DrawLines(self,*args):
	dc = wx.MemoryDC(self.bitmap)
	dc.SetPen(wx.Pen(wx.RED, 1))
	print "args",args
	for line in args:
		x1,y1 = line[0]
		x2,y2 = line[1]
		dc.DrawLine(x1,y1 ,x2,y2)
	dc.SelectObject(wx.NullBitmap)
	self.imageControl.SetBitmap(self.bitmap)  
        
    def DrawThreshold(self,position):
	ymin,ymax = self.GetYRange()
	topLinePosition = (ymax-ymin)*self.fractionTopStart #+ ymin
	bottomLinePosition = (ymax-ymin)*self.fractionBottomEnd #+ ymin
	xfrac = self.GetMousePosition(position)
	x1 = xfrac*self.GetSize()[0]
	y1 = topLinePosition 
	x2 = xfrac*self.GetSize()[0]
	y2 = bottomLinePosition
	if xfrac < self.fractionBinStart or xfrac > self.fractionBinEnd: return
	line1 = ((x1,y1),(x2,y2))
	self.tmpLines.append(line1)
	self.DrawLines(line1)
    def DrawArrow(self,startPosition,currentPosition,featherLength=20,featherAngle=math.pi/4):
        direction = self.ComputeCutDirection(startPosition,currentPosition)
	if direction==0: return 
	ymin,ymax = self.GetYRange()
	topLinePosition = (ymax-ymin)*self.fractionTopStart #+ ymin
	bottomLinePosition = (ymax-ymin)*self.fractionBottomEnd #+ ymin
	xfrac = self.GetMousePosition(startPosition)
	x1 = xfrac*self.GetSize()[0]
	y1 = topLinePosition 
	x2 = xfrac*self.GetSize()[0]
	y2 = bottomLinePosition
	arrowX1 = x1
	arrowY1 = (y1+y2)/2
	arrowY2 = (y1+y2)/2
	if direction>0:
		arrowX2 = self.GetHistEdgeRight()
	elif direction<0:
		arrowX2 = self.GetHistEdgeLeft()
	else:
		print "Error! Problem drawing arrow"
		return
	lines = ()
	line1=((arrowX1,arrowY1),(arrowX2,arrowY2))
	self.tmpLines.append(line1)
	arrowFeatherX1 = arrowX2
	arrowFeatherY1 = arrowY2
	arrowFeatherX2 = arrowX2 - float(direction)*featherLength*math.cos(featherAngle)
	arrowFeatherY2 = arrowY2 - featherLength*math.sin(featherAngle)
	feather1=((arrowFeatherX1,arrowFeatherY1),(arrowFeatherX2,arrowFeatherY2))
	self.tmpLines.append(feather1)
	arrowFeatherY2 = arrowY2 + featherLength*math.sin(featherAngle)
	feather2=((arrowFeatherX1,arrowFeatherY1),(arrowFeatherX2,arrowFeatherY2))
	self.tmpLines.append(feather2)
	self.DrawLines(line1,feather1,feather2)

    def ComputeCutDirection(self,startPosition,currentPosition):
	mouseDelta = 10
	if currentPosition[0] > startPosition[0]+mouseDelta:
	    self.cutDirection = 1
	elif currentPosition[0] < startPosition[0]-mouseDelta:
	    self.cutDirection = -1
	else:
	    self.cutDirection = 0

	print "Cut direction is",self.cutDirection
	return self.cutDirection

    def GetXRange(self):
        imagePosition = self.GetPosition()
	imageSize = self.GetSize()
	xmin = imagePosition[0]
	xmax = xmin + imageSize[0]
	return (xmin,xmax)
    def GetYRange(self):
        imagePosition = self.GetPosition()
	imageSize = self.GetSize()
	ymin = imagePosition[1]
	ymax = ymin + imageSize[1]
	return (ymin,ymax)
    def Reset(self,full=False):
        self.tmpLines = []
	if full: self.image = wx.Image(self.imageName, wx.BITMAP_TYPE_ANY)
	self.bitmap = wx.BitmapFromImage(self.image)
	self.imageControl.SetBitmap(self.bitmap)  
	for line in self.savedLines:
	    self.DrawLines(line)
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
    def GetPosition(self):
    	if self.gridSizer!=None and self.index >=0:
	    return self.gridSizer.GetItem(self.index).GetPosition()
	return None
    def GetSize(self):
    	if self.gridSizer!=None and self.index >=0:
	    return self.gridSizer.GetItem(self.index).GetSize()
	return None

    def GetHistEdgeRight(self):
    	if self.gridSizer!=None and self.index >=0:
	    return self.fractionBinEnd*self.GetSize()[0]
	return None
    def GetHistEdgeLeft(self):
    	if self.gridSizer!=None and self.index >=0:
	    return self.fractionBinStart*self.GetSize()[0]
	return None
    def addCut(self,xvalue,threshold,isGreaterThan):
    	#if not > then it is <
	#xvalue should be the fraction along the image
    	self.cuts.append([xvalue,threshold,isGreaterThan])
	
    def ResizeImage(self,availableSpace):
    	currentSize = self.image.GetSize()
	#preserve aspect ratio
	aspectRatio = float(currentSize[1])/float(currentSize[0])

	#first try setting available x space
	newSize1 = (availableSpace[0],aspectRatio*availableSpace[0])
	newSize2 = (availableSpace[1]/aspectRatio,availableSpace[1])
	print newSize1
	print newSize2
	newSize = None
	if not newSize1[0] > availableSpace[0] and not newSize1[1] > availableSpace[1]: 
		newSize = newSize1
	elif not newSize2[0] > availableSpace[0] and not newSize2[1] > availableSpace[1]: 
		newSize = newSize2
	else:
		print "ERROR: couldn't resize into space",availableSpace
		return False
	print "newsize",newSize
	self.image.Rescale(newSize[0],newSize[1],quality=wx.IMAGE_QUALITY_BICUBIC )
	self.bitmap = wx.BitmapFromImage(self.image)
	self.imageControl.SetBitmap(self.bitmap)  
        
    


