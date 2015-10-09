import wx
from FeatureImage import FeatureImage
from os import system
import math


#class ExamplePanel(wx.Panel):
#    def __init__(self, parent):
#        wx.Panel.__init__(self, parent)
class ExamplePanel(wx.Panel):
    def __init__(self, parent,images):
        wx.Panel.__init__(self, parent)
	self.parent = parent
	self.images = images
	self.foundItem = None
	self.clearMode = False
	self.blinded = True
	self.logY = True


	#Create Sizers for organizing materials in frame
	self.reInitBuffer = False
        # create some sizers
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
	self.hgap = 2
	self.vgap = 2
	self.SetGridShape()
        self.grid = wx.GridSizer(rows = self.nrows, cols=self.ncols,hgap=self.hgap, vgap=self.vgap)
        self.vSizer = wx.BoxSizer(wx.VERTICAL)
        self.hSizerLegend = wx.BoxSizer(wx.HORIZONTAL)
        self.hSizerRadio = wx.BoxSizer(wx.HORIZONTAL)
        self.hSizerButtons = wx.BoxSizer(wx.HORIZONTAL)

	#Build Grid of Plots
	for index,image in enumerate(self.images):
                self.grid.Add(image.imageControl,0,wx.ALIGN_RIGHT) 
		image.SetGridSizer(self.grid,index)
	self.ResizeFrame()
	
	#Set Bindings
	#self.Bind(wx.EVT_SIZE, self.onSize)
        self.Bind(wx.EVT_LEFT_DOWN, self.onLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.onLeftUp)
        self.Bind(wx.EVT_MOTION, self.onMotion)
	


	self.signalRectangleImage = wx.Image("input/images/SignalRectangle.png", wx.BITMAP_TYPE_ANY)
	scale = .3
        rectangleSize= self.signalRectangleImage.GetSize()
	self.signalRectangleImage.Rescale(scale*rectangleSize[0],scale*rectangleSize[1],quality=wx.IMAGE_QUALITY_BICUBIC )
	self.signalRectangleBitmap = wx.BitmapFromImage(self.signalRectangleImage)
	self.signalRectangleImageControl = wx.StaticBitmap(self, wx.ID_ANY, self.signalRectangleBitmap)

	self.bgRectangleImage = wx.Image("input/images/BGRectangle.png", wx.BITMAP_TYPE_ANY)
        rectangleSize= self.bgRectangleImage.GetSize()
	self.bgRectangleImage.Rescale(scale*rectangleSize[0],scale*rectangleSize[1],quality=wx.IMAGE_QUALITY_BICUBIC )
	self.bgRectangleBitmap = wx.BitmapFromImage(self.bgRectangleImage)
	self.bgRectangleImageControl = wx.StaticBitmap(self, wx.ID_ANY, self.bgRectangleBitmap)

	self.signalTxt = wx.StaticText(self,label="Signal",style=wx.ALIGN_CENTRE)
	self.bgTxt = wx.StaticText(self,label="Background",style=wx.ALIGN_CENTRE)

        #Build Buttons
        #self.button =wx.Button(self, label="Select")
        #self.Bind(wx.EVT_BUTTON, self.OnClick,self.button)
        self.clearButton =wx.Button(self, label="Clear")
        self.Bind(wx.EVT_BUTTON, self.onClear,self.clearButton)
        self.clearAllButton =wx.Button(self, label="Clear All")
        self.Bind(wx.EVT_BUTTON, self.onClearAll,self.clearAllButton)
        self.printButton =wx.Button(self, label="Print")
        self.Bind(wx.EVT_BUTTON, self.onPrint,self.printButton)
        self.runButton =wx.Button(self, label="Run")
        self.Bind(wx.EVT_BUTTON, self.onRun,self.runButton)
        self.resetButton =wx.Button(self, label="Reset")
        self.Bind(wx.EVT_BUTTON, self.onReset,self.resetButton)
        self.resizeButton =wx.Button(self, label="Resize")
        self.Bind(wx.EVT_BUTTON, self.onSize,self.resizeButton)

	radioList = ['Yes','No']
	self.blindingRadioBox = wx.RadioBox(self,label="Blinded?",choices=radioList,style=wx.RA_SPECIFY_COLS,majorDimension=2)
	self.Bind(wx.EVT_RADIOBOX,self.onBlind,self.blindingRadioBox)
	radioList = ['Yes','No']
	self.logyRadioBox = wx.RadioBox(self,label="Log Y-axis?",choices=radioList,style=wx.RA_SPECIFY_COLS,majorDimension=2)
	self.Bind(wx.EVT_RADIOBOX,self.onLogY,self.logyRadioBox)


	#Apply Sizers
	#self.hSizer.Add(self.button,0,wx.CENTER)
	self.hSizerLegend.Add(self.signalTxt,0,wx.CENTER)
	self.hSizerLegend.Add(self.signalRectangleImageControl ,0,wx.CENTER)
	self.hSizerLegend.Add(self.bgTxt,0,wx.CENTER)
	self.hSizerLegend.Add(self.bgRectangleImageControl ,0,wx.CENTER)
	self.hSizerRadio.Add(self.blindingRadioBox,0,wx.CENTER)
	self.hSizerRadio.Add(self.logyRadioBox,0,wx.CENTER)
	self.hSizerButtons.Add(self.resetButton,0,wx.CENTER)
	self.hSizerButtons.Add(self.resizeButton,0,wx.CENTER)
	self.hSizerButtons.Add(self.clearButton,0,wx.CENTER)
	self.hSizerButtons.Add(self.clearAllButton,0,wx.CENTER)
	self.hSizerButtons.Add(self.printButton,0,wx.CENTER)
	self.hSizerButtons.Add(self.runButton,0,wx.CENTER)
	self.vSizer.Add(self.hSizerRadio,0,wx.CENTER)
	self.vSizer.Add(self.hSizerButtons,0,wx.CENTER)
        self.mainSizer.Add(self.hSizerLegend, 0,wx.CENTER) 
        self.mainSizer.Add(self.grid, 0) 
        self.mainSizer.Add(self.vSizer,0,wx.CENTER) 
        self.SetSizerAndFit(self.mainSizer)
    def onLeftDown(self, event):
        '''Here we check if we are clicking on a plot and if so
	draw a line indicating where the threshold in the plot
	would be.  The threshold is temporarily stored.
	If we are not clicking on the appropriate region
	then nothing happens'''


        if not self.HasCapture(): self.CaptureMouse()
	#Figure out where we are clicking
        self.startPosition = event.GetPositionTuple()
	#Determine which figure this corresponds to
    	for image in self.images:
	    if image.IsInPosition(self.startPosition):
	        self.foundItem = image
		break
	#if we are clicking on a figure then proceed
	if self.foundItem:
	    if self.clearMode:
	        self.foundItem.Clear()
	    else:
	        #calculate the threshold this corresponds to 
	        #for the particular figure
	        self.foundItem.ComputeCutThreshold(self.startPosition)
	        #clear the drawing and put a line there
	        self.foundItem.Reset()
	        self.foundItem.DrawThreshold(self.startPosition)

    def SetGridShape(self):
    	nImages = len(self.images)
	if nImages==1:
	    self.nrows = 1
	    self.ncols = 1
	elif nImages==2:
	    self.nrows = 1
	    self.ncols = 2
	elif nImages==3:
	    self.nrows = 1
	    self.ncols = 3
	elif nImages==4:
	    self.nrows = 2
	    self.ncols = 2
	elif nImages==5 or nImages==6:
	    self.nrows = 2
	    self.ncols = 3
	elif nImages==7 or nImages==8:
	    self.nrows = 2
	    self.ncols = 4
	else:
	    print "Pick fewer features"
	    exit(2)
    def onBlind(self,event):
        if event.GetInt()==0: self.blinded = True
	else: self.blinded=False
	self.UpdatePlots()
	#Necessary to keep arrows on new plots
	for image in self.images: image.Reset()
    def onReset(self,event):
	for image in self.images:
	    image.SetImageNames(useInput=True)
	self.UpdatePlots()
	self.ClearAll()
	#Necessary to keep arrows on new plots
	for image in self.images: image.Reset()
    def onLogY(self,event):
        if event.GetInt()==0: self.logY = True
	else: self.logY=False
	self.UpdatePlots()
	#Necessary to keep arrows on new plots
	for image in self.images: image.Reset()
    def UpdatePlots(self):
        for image in self.images:
	    image.ChangeImage(self.blinded,self.logY)
	self.ResizeFrame()
    def onMotion(self,event):
    	'''While holding down the left button
	we try to determine the direction that the cut
	shold cut. An arrow is drawn temporarily indicating
	the direction which tracs the direction of the mouse'''
    	if not event.LeftIsDown():
		event.Skip(True)
		return 
	if self.clearMode: return
        if not self.HasCapture(): self.CaptureMouse()
	currentPosition = event.GetPositionTuple()
	#if we already found an image from the left down
	#event then proceed
	if self.foundItem:
	    #temporarily save the current direction
	    #and check to see if there is any update in the direction
	    #from a possible previous onMotion event.
	    oldCutDirection = self.foundItem.GetCutDirection()
	    newCutDirection = self.foundItem.ComputeCutDirection(self.startPosition,currentPosition)
	    if oldCutDirection!= newCutDirection:
	        #if there is an update to the direction
		#then we clear the plot and redraw both the cut threshold and the arrow
	    	self.foundItem.Reset()
		self.foundItem.DrawThreshold(self.startPosition)
	    	self.foundItem.DrawArrow(self.startPosition,currentPosition)
	event.Skip(True)
	
    def onLeftUp(self, event):
        '''Upon releasing the mouse, we check to see
	if we properly established a threshold and direction,
	if so that information should be saved and the image
	is kept. If not, the inputs and drawings are thrown away.
	'''
	if self.clearMode: 
		self.clearMode = False
		return
        if self.HasCapture():
            self.endPosition = event.GetPositionTuple()
	    self.ReleaseMouse()
	    #if not self.drawnArrows:
	    #	self.Clear()
    	    if self.foundItem: 
	    	if self.foundItem.cutDirection==0:
	        	self.foundItem.Reset()
		elif self.foundItem.GetNCuts()==2:
			self.foundItem.cutDirection=0
	        	self.foundItem.Reset()
		else:
			self.foundItem.Save()
			self.foundItem.Reset()
		self.foundItem.cutDirection=0
	self.foundItem = None
    def onPrint(self,event):
    	print "**********Recorded Cut Values********"
        for image in self.images:
	    print "Item",image.index,image.name,":"
	    index=0
	    for cut,direction in image.CutThresholdsAndDirections:
	    	
		if index>0:  
			if image.feature.logicalAND: print "\tAND"
			else: print "\tOR"
	        print "\t%s %3.2f" % ((">" if direction>0 else "<"),float(cut))
		index+=1
    def onRun(self,event):
        print "Running..."
	ofile = open('output/cuts.txt','w')
	for image in self.images:
	    image.ProcessCuts()
	    if image.feature.HasCuts():
	        ofile.write(image.feature.cutString+"\n")
	ofile.close()
	#I may want to make this pre-compiled
	system("root -q -b -l src/RunCuts.cxx")
	system("root -q -b -l src/WriteHistograms.cxx")
	system("root -q -b -l src/Draw.cxx")
	for image in self.images:
	    image.SetImageNames(useInput=False)
	self.UpdatePlots()
	#Necessary to keep arrows on new plots
	for image in self.images: image.Reset()
	print "Done!"

    def onClear(self,event):
    	self.clearMode = True
    def onClearAll(self,event):
    	self.ClearAll()
    def ClearAll(self):
    	for i in range(len(self.images)): self.Clear(i)
    def Clear(self,i=-1):
    	if i < 0: i  = self.foundItem
	if i < 0: return
	self.images[i].Clear()
    def ResizeFrame(self):
    	print "size"
	frameSize =  self.parent.GetClientSize()
	availableYSpace = frameSize[1]/self.nrows - self.vgap*(self.nrows+1) - 50
	availableXSpace = frameSize[0]/self.ncols - self.hgap*(self.ncols+1)
	for image in self.images:
	    #image = wx.Image(image.imageName, wx.BITMAP_TYPE_ANY)
	    image.Reset(True)
	    image.ResizeImage((availableYSpace,availableXSpace))
	#assume images are all of the same size
	newSize = self.images[0].image.GetSize()
	newFrameSize = (newSize[0]*self.ncols + self.hgap*(self.ncols+1), 
			newSize[1]*self.nrows + self.vgap*(self.nrows+1)) 
	newvgap = (frameSize[1] - newSize[1]*self.nrows )/(self.nrows+1)
	newhgap = (frameSize[0] - newSize[0]*self.ncols )/(self.ncols+1)
	self.grid.SetHGap(newhgap)
	self.grid.SetVGap(newvgap)
        self.SetSizerAndFit(self.mainSizer)

    def onSize(self, event):
	self.ResizeFrame()
	event.Skip(True)
    def EvtRadioBox(self, event):
        self.logger.AppendText('EvtRadioBox: %d\n' % event.GetInt())
    def EvtComboBox(self, event):
        self.logger.AppendText('EvtComboBox: %s\n' % event.GetString())
    def OnClick(self,event):
        if self.HasCapture(): self.ReleaseMouse()
        else : self.CaptureMouse()
    def EvtText(self, event):
        self.logger.AppendText('EvtText: %s\n' % event.GetString())
    def EvtChar(self, event):
        self.logger.AppendText('EvtChar: %d\n' % event.GetKeyCode())
        event.Skip()
    def EvtCheckBox(self, event):
        self.logger.AppendText('EvtCheckBox: %d\n' % event.Checked())
app = wx.App(False)
frame = wx.Frame(None,size=(1100,700)) #,style=wx.MAXIMIZE)

images = []
images.append(FeatureImage("nsfos",frame,cutAtBinEdge=True))
images.append(FeatureImage("pt",frame,cutAtBinEdge=False))
images.append(FeatureImage("met",frame,cutAtBinEdge=False))
images.append(FeatureImage("nbjets",frame,cutAtBinEdge=True))
images.append(FeatureImage("njets",frame,cutAtBinEdge=True))
images.append(FeatureImage("masselel",frame,cutAtBinEdge=False))
#images.append(FeatureImage("masssfos",frame,cutAtBinEdge=False))
images.append(FeatureImage("deltaphi",frame,cutAtBinEdge=False))
images.append(FeatureImage("nmuons",frame,cutAtBinEdge=True))
#images.append(FeatureImage("nsfos","output/plots/unblinded/logY/nsfos.png",frame))
#images.append(FeatureImage("NSFOS","input/SFOSSignalRegions.png",frame,xmin=0,xmax=3,nbins=3))
panel = ExamplePanel(frame,images)
frame.Show()
app.MainLoop()


