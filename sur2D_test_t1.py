from ROOT import *
import os,sys
import argparse
import numpy as np
from array import array



from utils.plots import get_SP_plot_2D,get_prior_CI,get_posterior_CI
from plotter import Plotter



def createSurvivalPlotPalette():
    custompalette = []
    cols = TColor.GetNumberOfColors()# This gets the colors of the Palette currently set in ROOT
    #This part sets bins with a survival probability of zero (less than second entry of sprobcontours list to be exact) to Black color. Bins with a survival probability of exactly 1 (greater than second last entry of sprobcontours list) to Grey.
    for i in range(cols):
        if i<19: # The exact i was found by trial and error. Sorry.
            col = kBlack
        # elif i > 253:
        #     col = kGray
        else:
            col = TColor.GetColorPalette(i) # This part keeps the color from the currently set palette
            
        custompalette.append(col)
    custompalette = np.intc(custompalette)
    return custompalette
ColPal = createSurvivalPlotPalette()
Plotter.setPalette(ColPal)


infile = TFile("pmssmtree_11aug2023.root")
intree = infile.Get("mcmc")
intree.AddFriend("cms_sus_20_001",TFile("sus_20_001_likelihood.root"))


hist = get_SP_plot_2D(
    intree,
    "combined",
    "lcsp_chi10",
    "m(LCSP) [TeV]",
    100,0,7000,
    "m(#tilde{#chi}^{0}_{1}) [TeV]",
    50,0,1000,
    False,False,
    "abs(chi10):t1"
    )


prior_data =  get_prior_CI(
    intree, 
    hname =  "t1_chi10_priorcontours",
    xbins = 100, 
    xlow = 0, 
    xup = 7000, 
    ybins = 50, 
    ylow = 0, 
    yup = 1000, 
    _logx = False, 
    _logy =False, 
    drawstring = "abs(chi10):t1",
    moreconstraints= [])

posterior_data = get_posterior_CI(
    intree, 
    analysis = "combined", 
    hname = "t1_chi10_posteriorcontours", 
    xbins = 100, 
    xlow = 0, 
    xup = 7000, 
    ybins = 50, 
    ylow = 0, 
    yup = 1000,
    _logx = False, 
    _logy =False, 
    drawstring = "abs(chi10):t1",
    moreconstraints = [])


p = Plotter(canvasSettings={
    "xmin": 0,
    "xmax": 7,
    "ymin": 0,
    "ymax": 1,
    "nameXaxis": "m(#tilde{t}_{1}) [TeV]",
    "nameYaxis": "m(#tilde{#chi}^{0}_{1}) [TeV]",
    "canvName": "test2",
    "extraSpace": 0.04,
    "iPos": 0,
    "is3D": True,
})
p.tuning(tuning={"ZaxisSetMaxDigits":3},hist=hist)
p.tuning(tuning={"ZaxisSetTitleOffset":1.28},hist=hist)
p.tuning(tuning={"YaxisSetTitleOffset":1.25})
p.tuning(tuning={"XaxisSetTitleOffset":1})
# p.tuning(tuning={"XaxisSetMaxDigits":2})
p.tuning(tuning={"SetBottomMargin":0.02})

hist.GetZaxis().SetTitle("Survival Probability")
p.scaleXaxis(hist,1000)
p.scaleYaxis(hist,1000)
p.Draw2D(hist,"colz")

for ix,interval in enumerate(prior_data):
    for cont in prior_data[interval]:
        p.scaleGraphXaxis(cont,1000)
        p.scaleGraphYaxis(cont,1000)
        # p.Draw(cont,"same")
        cont.Draw("same")
for ix,interval in enumerate(posterior_data):
    for cont in posterior_data[interval]:
        p.scaleGraphXaxis(cont,1000)
        p.scaleGraphYaxis(cont,1000)
        # p.Draw(cont,"same")
        cont.Draw("same")
        

leftTop = {"x1":0.18,"x2":0.52,"y1":0.8,"y2":0.9}
rightTop = {"x1":0.48,"x2":0.82,"y1":0.8,"y2":0.9}
rightBottom = {"x1":0.48,"x2":0.82,"y1":0.18,"y2":0.28}
leftBottom = {"x1":0.18,"x2":0.52,"y1":0.18,"y2":0.28}

p.createLegend(**rightTop,header="COMBINED",columns=2)
# p.fillWhiteLegend()

for ix,interval in enumerate(prior_data):
    if interval in prior_data.keys() and len(prior_data[interval])>0:
        p.addEntryToLegend(prior_data[interval][0],str(int(100*(interval)))+"%  prior CI","l",)
    if interval in posterior_data.keys() and len(posterior_data[interval])>0:
        p.addEntryToLegend(posterior_data[interval][0],str(int(100*(interval)))+"% posterior CI","l",)


p.SaveAs("test_t1.png",redraw=True)
