import wx
from FeatureImage import FeatureImage
from CutPanel import CutPanel
from os import system
import math


app = wx.App(False)
frame = wx.Frame(None,size=(1100,700)) 

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
panel = CutPanel(frame,images)
frame.Show()
app.MainLoop()


