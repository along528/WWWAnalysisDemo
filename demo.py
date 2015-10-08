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


	#Create Sizers for organizing materials in frame
	self.reInitBuffer = False
        # create some sizers
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
	self.hgap = 2
	self.vgap = 2
	self.nrows = 2
	self.ncols = 3
        self.grid = wx.GridSizer(rows = self.nrows, cols=self.ncols,hgap=self.hgap, vgap=self.vgap)
        self.hSizer = wx.BoxSizer(wx.HORIZONTAL)

	#Build Grid of Plots
	for index,image in enumerate(self.images):
                self.grid.Add(image.imageControl,0,wx.ALIGN_RIGHT) 
		image.SetGridSizer(self.grid,index)
	
	#Set Bindings
	self.Bind(wx.EVT_SIZE, self.onSize)
        #self.Bind(wx.EVT_IDLE, self.onIdle)
        self.Bind(wx.EVT_LEFT_DOWN, self.onLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.onLeftUp)
        self.Bind(wx.EVT_MOTION, self.onMotion)
	

	self.ResizeFrame()

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



	#Apply Sizers
	#self.hSizer.Add(self.button,0,wx.CENTER)
	self.hSizer.Add(self.clearButton,0,wx.CENTER)
	self.hSizer.Add(self.clearAllButton,0,wx.CENTER)
	self.hSizer.Add(self.printButton,0,wx.CENTER)
	self.hSizer.Add(self.runButton,0,wx.CENTER)
        self.mainSizer.Add(self.grid, 0) 
        self.mainSizer.Add(self.hSizer,0,wx.CENTER) 
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
	system("root -q -b -l RunCuts.cxx")
	system("root -q -b -l WriteHistograms.cxx")
	system("root -q -b -l Draw.cxx")
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
	frameSize =  self.parent.GetClientSize()
	availableYSpace = frameSize[1]/self.nrows - self.vgap*(self.nrows+1)
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
	self.reInitBuffer = False
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
frame = wx.Frame(None,size=(800,560)) #,style=wx.MAXIMIZE)

images = []
images.append(FeatureImage("nsfos",frame,cutAtBinEdge=True))
images.append(FeatureImage("pt",frame,cutAtBinEdge=False))
images.append(FeatureImage("met",frame,cutAtBinEdge=False))
images.append(FeatureImage("nbjets",frame,cutAtBinEdge=True))
images.append(FeatureImage("njets",frame,cutAtBinEdge=True))
images.append(FeatureImage("masselel",frame,cutAtBinEdge=True))
#images.append(FeatureImage("nsfos","output/plots/unblinded/logY/nsfos.png",frame))
#images.append(FeatureImage("NSFOS","input/SFOSSignalRegions.png",frame,xmin=0,xmax=3,nbins=3))
panel = ExamplePanel(frame,images)
frame.Show()
app.MainLoop()


