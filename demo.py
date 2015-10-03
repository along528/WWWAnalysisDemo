import wx
from CutItem import CutItem
import math

items = []
nsfos = CutItem("nsfos","SFOSSignalRegions.png")
nsfos.xmin = 0
nsfos.xmax = 3
nsfos.nbins = 3
items.append(nsfos)
items.append(nsfos)
items.append(nsfos)
items.append(nsfos)
items.append(nsfos)
items.append(nsfos)

#class ExamplePanel(wx.Panel):
#    def __init__(self, parent):
#        wx.Panel.__init__(self, parent)
class ExamplePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
	self.parent = parent
	self.foundItem = -1

	self.reInitBuffer = False
        # create some sizers
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
	self.hgap = 2
	self.vgap = 2
	self.xlen = 2
	self.ylen = 3
        self.grid = wx.GridSizer(rows = self.xlen, cols=self.ylen,hgap=self.hgap, vgap=self.vgap)
        self.hSizer = wx.BoxSizer(wx.HORIZONTAL)

        #self.quote = wx.StaticText(self, label="Your quote: ")
	self.images = []
	for item in items:
		self.images.append( wx.Image(item.imageName, wx.BITMAP_TYPE_ANY))



	
	#self.imageCtrl1 = wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(img)) #self.image1))
	#self.imageCtrl2 = wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(img)) #self.image1))
	#self.imageCtrl3 = wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(img)) #self.image1))
	#self.imageCtrl4 = wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(img)) #self.image1))


	self.imageControls = []
	self.bitmaps = []
	print "parent",parent.GetSize()
	for image in self.images:
	    print "image",image.GetSize()
	    self.bitmaps.append(wx.BitmapFromImage(image))
	    self.imageControls.append(wx.StaticBitmap(self, wx.ID_ANY, self.bitmaps[len(self.bitmaps)-1]))
	
	index = 0
	for xpos in range(0,self.xlen):
	    for ypos in range(0,self.ylen):
                self.grid.Add(self.imageControls[index],0,wx.ALIGN_RIGHT) #,0) #,wx.ALIGN_RIGHT) #, pos=(xpos,ypos)) #,span=(2,2))
		index+=1
	
	self.Bind(wx.EVT_SIZE, self.onSize)
        self.Bind(wx.EVT_IDLE, self.onIdle)
        self.Bind(wx.EVT_LEFT_DOWN, self.onLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.onLeftUp)
        self.Bind(wx.EVT_MOTION, self.onMotion)
	
	self.ResizeFrame()


        # A multiline TextCtrl - This is here to show how the events work in this program, don't pay too much attention to it
        #self.logger = wx.TextCtrl(self, size=(200,300), style=wx.TE_MULTILINE | wx.TE_READONLY)

        # A button
        self.button =wx.Button(self, label="Select")
        self.Bind(wx.EVT_BUTTON, self.OnClick,self.button)
        self.clearButton =wx.Button(self, label="Clear")
        self.Bind(wx.EVT_BUTTON, self.onClear,self.clearButton)
	#self.grid.Add(self.button,(3,1))

	"""
        # the edit control - one line version.
        self.lblname = wx.StaticText(self, label="Your name :")
        grid.Add(self.lblname, pos=(1,0))
        self.editname = wx.TextCtrl(self, value="Enter here your name", size=(140,-1))
        grid.Add(self.editname, pos=(1,1))
        self.Bind(wx.EVT_TEXT, self.EvtText, self.editname)
        self.Bind(wx.EVT_CHAR, self.EvtChar, self.editname)

        # the combobox Control
        self.sampleList = ['friends', 'advertising', 'web search', 'Yellow Pages']
        self.lblhear = wx.StaticText(self, label="How did you hear from us ?")
        grid.Add(self.lblhear, pos=(3,0))
        self.edithear = wx.ComboBox(self, size=(95, -1), choices=self.sampleList, style=wx.CB_DROPDOWN)
        grid.Add(self.edithear, pos=(3,1))
        self.Bind(wx.EVT_COMBOBOX, self.EvtComboBox, self.edithear)
        self.Bind(wx.EVT_TEXT, self.EvtText,self.edithear)

        # add a spacer to the sizer
        grid.Add((10, 40), pos=(2,0))

        # Checkbox
        self.insure = wx.CheckBox(self, label="Do you want Insured Shipment ?")
        grid.Add(self.insure, pos=(4,0), span=(1,2), flag=wx.BOTTOM, border=5)
        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox, self.insure)

        # Radio Boxes
        radioList = ['blue', 'red', 'yellow', 'orange', 'green', 'purple', 'navy blue', 'black', 'gray']
        rb = wx.RadioBox(self, label="What color would you like ?", pos=(20, 210), choices=radioList,  majorDimension=3,
                         style=wx.RA_SPECIFY_COLS)
        grid.Add(rb, pos=(5,0), span=(1,2))
        self.Bind(wx.EVT_RADIOBOX, self.EvtRadioBox, rb)
	"""


        #hSizer.Add(self.logger)
        #mainSizer.Add(self.imageCtrl1, 0, wx.ALL, 5)
        #mainSizer.Add(self.imageCtrl2, 0, wx.ALL, 5)
	#self.hSizer.Add(self.grid,0,wx.ALL,5)
	self.hSizer.Add(self.button,0,wx.CENTER)
	self.hSizer.Add(self.clearButton,0,wx.CENTER)
        self.mainSizer.Add(self.grid, 0) #,wx.ALL|wx.EXPAND, 5)
        self.mainSizer.Add(self.hSizer,0,wx.CENTER) #, 0, wx.RIGHT)
        self.SetSizerAndFit(self.mainSizer)
    def onMotion(self,event):
    	if not event.LeftIsDown():
		event.Skip(True)
		return 
	
        if not self.HasCapture(): self.CaptureMouse()
	currentPosition = event.GetPositionTuple()
	self.computeCut(event,self.startPosition,currentPosition)
	
    def onLeftDown(self, event):
        ''' Called when the left mouse button is pressed. '''
        if not self.HasCapture(): self.CaptureMouse()
        self.startPosition = event.GetPositionTuple()
	print "start",self.startPosition
	self.drawnArrows = False
	self.drawnLines = False
	self.change = False
	self.arrowLeft = False
	self.computeCut(event,self.startPosition)

    def onLeftUp(self, event):
        ''' Called when the left mouse button is released. '''
        if self.HasCapture():
            self.endPosition = event.GetPositionTuple()
	    print "stop",self.endPosition
	    self.ReleaseMouse()
	    self.computeCut(event,self.startPosition,self.endPosition)
	    if not self.drawnArrows:
	    	self.Clear()
	    self.change = False
	    self.drawnArrows = False
	    self.arrowLeft = False
    
    
    def computeCut(self,event,startPosition,endPosition = None): #,endPosition):
    	for i in range(0,6):
	    position = self.grid.GetItem(i).GetPosition()
	    size = self.grid.GetItem(i).GetSize()
	    xmin = position[0]
	    xmax = xmin + size[0]
	    ymin = position[1]
	    ymax = ymin + size[1]
	    if startPosition[0] > xmin and startPosition[0] < xmax and startPosition[1] > ymin and startPosition[1] < ymax: 
	        self.foundItem = i
		break
	print "Found:",i
	val = 0
	xvalue = float(startPosition[val]-position[val])/float(size[val])
	lowBinEdge = items[i].getLowBinEdge(xvalue)
	binEdgeXValue= items[i].getLowBinEdge(xvalue,getInXCoordinates=True)
	dc = wx.MemoryDC(self.bitmaps[i])
	dc.SetPen(wx.Pen(wx.RED, 1))

	topLinePosition = (ymax-ymin)*items[i].fractionTopStart #+ ymin
	bottomLinePosition = (ymax-ymin)*items[i].fractionBottomEnd #+ ymin
	#dc.DrawLines(( (startPosition[0]-position[0],topLinePosition ),(startPosition[0]-position[0],bottomLinePosition) ))
	#x1 = binEdgeXValue*size[0]
	x1 = xvalue*size[0]
	y1 = topLinePosition 
	#x2 = binEdgeXValue*size[0]
	x2 = xvalue*size[0]
	y2 = bottomLinePosition
	delta = 0
	print items[i].fractionBinEnd
	histRightEdge = (items[i].fractionBinEnd*size[0]) #+position[0])
	histLeftEdge   = items[i].fractionBinStart*size[0]
	dc.DrawLine(x1,y1 ,x2,y2)
	#if not self.drawnLines: self.change = True
	#else: self.change = False
	self.drawnLines = True
	if endPosition!=None:
			mouseDelta = 10
			if endPosition[0] > startPosition[0]+mouseDelta:
				arrowX1 = x1
				arrowY1 = (y1+y2)/2
				arrowX2 = histRightEdge-delta
				arrowY2 = (y1+y2)/2
				dc.DrawLine(arrowX1,arrowY1 ,arrowX2,arrowY2)

				featherLength = 20
				featherAngle = math.pi/4
				arrowFeatherX1 = arrowX2
				arrowFeatherY1 = arrowY2
				arrowFeatherX2 = arrowX2 - featherLength*math.cos(featherAngle)
				arrowFeatherY2 = arrowY2 - featherLength*math.sin(featherAngle)
				dc.DrawLine(arrowFeatherX1,arrowFeatherY1 ,arrowFeatherX2,arrowFeatherY2)
				arrowFeatherY2 = arrowY2 + featherLength*math.sin(featherAngle)
				dc.DrawLine(arrowFeatherX1,arrowFeatherY1 ,arrowFeatherX2,arrowFeatherY2)
				if not self.drawnArrows:
					self.drawnArrows = True
					self.change = True
				elif self.arrowLeft:
					self.change = True
				else:
					self.change = False
				self.arrowLeft = False
			elif endPosition[0] < startPosition[0]-mouseDelta:
				arrowX1 = x1
				arrowY1 = (y1+y2)/2
				arrowX2 = histLeftEdge+delta
				arrowY2 = (y1+y2)/2
				dc.DrawLine(arrowX1,arrowY1 ,arrowX2,arrowY2)

				featherLength = 20
				featherAngle = math.pi/4
				arrowFeatherX1 = arrowX2
				arrowFeatherY1 = arrowY2
				arrowFeatherX2 = arrowX2 + featherLength*math.cos(featherAngle)
				arrowFeatherY2 = arrowY2 - featherLength*math.sin(featherAngle)
				dc.DrawLine(arrowFeatherX1,arrowFeatherY1 ,arrowFeatherX2,arrowFeatherY2)
				arrowFeatherY2 = arrowY2 + featherLength*math.sin(featherAngle)
				dc.DrawLine(arrowFeatherX1,arrowFeatherY1 ,arrowFeatherX2,arrowFeatherY2)
				if not self.drawnArrows:
					self.drawnArrows = True
					self.change = True
				elif not self.arrowLeft:
					self.change = True
				else:
					self.change = False
				self.arrowLeft = True
        if self.change:
		self.Clear()
	dc.SelectObject(wx.NullBitmap)
	self.imageControls[i].SetBitmap(self.bitmaps[i])  
	#else:
	#    	self.bitmaps[i] = wx.BitmapFromImage(self.images[i])
	#	self.imageControls[i].SetBitmap(self.bitmaps[i])  
		
	"""
	print "bin edge",lowBinEdge
	if startPosition[0] < endPosition[0]: 
		print "> cut"
	elif startPosition[0] > endPosition[0]: 
		print "< cut"
	else:
		print "Specify cut direction"
	"""

	#((83, 375), (83, 42), (120, 42), (120,375), (83,375)))

	    	

    	
    	
    def onClear(self,event):
    	self.ClearAll()
    def ClearAll(self):
    	for i in range(len(items)): self.Clear(i)


    def Clear(self,i=-1):
    		if i < 0: i  = self.foundItem
		if i < 0: return
		self.bitmaps[i] = wx.BitmapFromImage(self.images[i])
		self.imageControls[i].SetBitmap(self.bitmaps[i])  
    def ResizeFrame(self):
	frameSize =  self.parent.GetClientSize()
	availableXSpace = frameSize[1]/self.xlen - self.vgap*(self.xlen+1)
	availableYSpace = frameSize[0]/self.ylen - self.hgap*(self.ylen+1)
	print availableXSpace
	print availableYSpace
	self.images =[]
	self.bitmaps = []
        for index,item in enumerate(items):
	    image = wx.Image(item.imageName, wx.BITMAP_TYPE_ANY)
	    self.ResizeImage(image,(availableXSpace,availableYSpace))
	    self.images.append(image)
	    self.bitmaps.append(wx.BitmapFromImage(image))
	    self.imageControls[index].SetBitmap(self.bitmaps[len(self.bitmaps)-1])

	#assume images are all of the same size
	newSize = image.GetSize()
	newFrameSize = (newSize[0]*self.ylen + self.hgap*(self.ylen+1), newSize[1]*self.xlen + self.vgap*(self.xlen+1)) #+30)
	newvgap = (frameSize[1] - newSize[1]*self.xlen )/(self.xlen+1)
	newhgap = (frameSize[0] - newSize[0]*self.ylen )/(self.ylen+1)
	print "newgap",newvgap,newhgap
	self.grid.SetHGap(newhgap)
	self.grid.SetVGap(newvgap)

	print "new frame size",newFrameSize
	#self.parent.SetSize(newFrameSize)
	#self.grid.RecalcSizes()
        self.SetSizerAndFit(self.mainSizer)



    def ResizeImage(self,image,availableSpace):
    	currentSize = image.GetSize()
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
	return image.Rescale(newSize[0],newSize[1],quality=wx.IMAGE_QUALITY_BICUBIC )
	
    def onIdle(self, event):
        ''' Called when the window is resized. We set a flag so the idle
            handler will resize the buffer. '''

    def onSize(self, event):
        ''' If the size was changed then resize the bitmap used for double
            buffering to match the window size.  We do it in Idle time so
            there is only one refresh after resizing is done, not lots while
            it is happening. '''
	self.ResizeFrame()
	self.reInitBuffer = False
	event.Skip(True)
	#if not self.HasCapture(): self.CaptureMouse()


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
#frame = wx.Frame(None ,style=wx.DEFAULT_FRAME_STYLE)
#frame.SetInitialSize((2000,2000))
panel = ExamplePanel(frame)
frame.Show()
app.MainLoop()


