import sys
import shutil

sys.path.append("/Users/dorukhan/Desktop/cern/pmssm/")

from ROOT import *
from pmssm import PMSSM, particleDrawConfig_TeV
import config as pltconfig

particleName = "g"

root_file_path = "pmssmtree_11aug2023.root"
tree_name = "mcmc"
outdir = pltconfig.plotsdir+particleName

if pltconfig.refreshDir:
    shutil.rmtree(outdir, ignore_errors=True)



root_file = TFile(root_file_path) # type: ignore
intree = root_file.Get(tree_name)

pmssm_plotter = PMSSM(
    intree = intree, 
    outdir = outdir,
    particleDrawConfig= particleDrawConfig_TeV,
    canvasStyle = pltconfig.generalProperties
    )

print("impact1D for: ", particleName, "\n\n")
pmssm_plotter.impact1D(drawstring=particleName)

impactPlots1DCanvasStyle = {
    "legend":pltconfig.rightbottom["legend"].copy()
}
impactPlots1DCanvasStyle["legend"]["x1"] = 0.58
impactPlots1DCanvasStyle["legend"]["x2"] = 0.78
pmssm_plotter.impact1D(drawstring=particleName, xaxisDrawConfig={"1Dlogy":True},canvasStyle=impactPlots1DCanvasStyle)

survivalPlots1DCanvasStyle = {
    "legend":pltconfig.rightbottom["legend"].copy()
}
survivalPlots1DCanvasStyle["legend"]["x1"] = 0.58
survivalPlots1DCanvasStyle["legend"]["x2"] = 0.78

quantilePlots1DCanvasStyle = {
    "legend":pltconfig.righttop["legend"].copy()
}
quantilePlots1DCanvasStyle["legend"]["x1"] = 0.75
quantilePlots1DCanvasStyle["legend"]["x2"] = 0.85


print("quantile 1D for: ", particleName, "\n\n")
pmssm_plotter.quantilePlots1D(drawstring=particleName, canvasStyle=pltconfig.rightbottom)
pmssm_plotter.quantilePlots1D(drawstring=particleName, xaxisDrawConfig={"1Dlogy":True}, canvasStyle=quantilePlots1DCanvasStyle)

print("survivalProbability1D for:",particleName, "\n\n")
pmssm_plotter.survivalProbability1D(drawstring=particleName, canvasStyle=survivalPlots1DCanvasStyle)
pmssm_plotter.survivalProbability1D(drawstring=particleName, xaxisDrawConfig={"1Dlogy":True} ,canvasStyle=survivalPlots1DCanvasStyle)

for ypar in pltconfig.yaxisFor2D:
    print("survivalProbability2D for: ", ypar, particleName, "\n\n")
    if ypar != "abs(chi10)":
        pmssm_plotter.survivalProbability2D(drawstring = ypar+":"+particleName,analysis=pltconfig.analysisName,contourSwitch=True, canvasStyle={"legend" :{"textColor":kWhite}})
    else:
        pmssm_plotter.survivalProbability2D(drawstring = ypar+":"+particleName,analysis=pltconfig.analysisName,contourSwitch=True)
    print("0.5 quantile 2D for: ", ypar, particleName, "\n\n")
    if ypar != "abs(chi10)":
        pmssm_plotter.quantilePlots2D(drawstring=ypar+":"+particleName,analysis=pltconfig.analysisName, quantile = 0.5, canvasStyle={"legend" :{"textColor":kWhite}})
    else:
        pmssm_plotter.quantilePlots2D(drawstring=ypar+":"+particleName,analysis=pltconfig.analysisName, quantile = 0.5)
    print("0.75 quantile 2D for: ", ypar, particleName, "\n\n")
    if ypar != "abs(chi10)":
        pmssm_plotter.quantilePlots2D(drawstring=ypar+":"+particleName,analysis=pltconfig.analysisName, quantile = 0.75, canvasStyle={"legend" :{"textColor":kWhite}})
    else:
        pmssm_plotter.quantilePlots2D(drawstring=ypar+":"+particleName,analysis=pltconfig.analysisName, quantile = 0.75)

    print("0.9 quantile 2D for: ", ypar, particleName, "\n\n")
    if ypar != "abs(chi10)":
        pmssm_plotter.quantilePlots2D(drawstring=ypar+":"+particleName,analysis=pltconfig.analysisName, quantile = 0.9, canvasStyle={"legend" :{"textColor":kWhite}})
    else:
        pmssm_plotter.quantilePlots2D(drawstring=ypar+":"+particleName,analysis=pltconfig.analysisName, quantile = 0.9)
    print("0.99 quantile 2D for: ", ypar, particleName, "\n\n")
    if ypar != "abs(chi10)":
        pmssm_plotter.quantilePlots2D(drawstring=ypar+":"+particleName,analysis=pltconfig.analysisName, quantile = 0.99, canvasStyle={"legend" :{"textColor":kWhite}})
    else:
        pmssm_plotter.quantilePlots2D(drawstring=ypar+":"+particleName,analysis=pltconfig.analysisName, quantile = 0.99)

import sys
import shutil

sys.path.append("/Users/dorukhan/Desktop/cern/pmssm/")

from ROOT import *
from pmssm import PMSSM, particleDrawConfig_TeV
import config as pltconfig

particleName = "g"

root_file_path = "pmssmtree_11aug2023.root"
tree_name = "mcmc"
outdir = pltconfig.plotsdir+particleName

if pltconfig.refreshDir:
    shutil.rmtree(outdir, ignore_errors=True)



root_file = TFile(root_file_path) # type: ignore
intree = root_file.Get(tree_name)

pmssm_plotter = PMSSM(
    intree = intree, 
    outdir = outdir,
    particleDrawConfig= particleDrawConfig_TeV,
    canvasStyle = pltconfig.generalProperties
    )

print("impact1D for: ", particleName, "\n\n")
pmssm_plotter.impact1D(drawstring=particleName)

impactPlots1DCanvasStyle = {
    "legend":pltconfig.rightbottom["legend"].copy()
}
impactPlots1DCanvasStyle["legend"]["x1"] = 0.58
impactPlots1DCanvasStyle["legend"]["x2"] = 0.78
pmssm_plotter.impact1D(drawstring=particleName, xaxisDrawConfig={"1Dlogy":True},canvasStyle=impactPlots1DCanvasStyle)

survivalPlots1DCanvasStyle = {
    "legend":pltconfig.rightbottom["legend"].copy()
}
survivalPlots1DCanvasStyle["legend"]["x1"] = 0.58
survivalPlots1DCanvasStyle["legend"]["x2"] = 0.78

quantilePlots1DCanvasStyle = {
    "legend":pltconfig.righttop["legend"].copy()
}
quantilePlots1DCanvasStyle["legend"]["x1"] = 0.75
quantilePlots1DCanvasStyle["legend"]["x2"] = 0.85


print("quantile 1D for: ", particleName, "\n\n")
pmssm_plotter.quantilePlots1D(drawstring=particleName, canvasStyle=pltconfig.rightbottom)
pmssm_plotter.quantilePlots1D(drawstring=particleName, xaxisDrawConfig={"1Dlogy":True}, canvasStyle=quantilePlots1DCanvasStyle)

print("survivalProbability1D for:",particleName, "\n\n")
pmssm_plotter.survivalProbability1D(drawstring=particleName, canvasStyle=survivalPlots1DCanvasStyle)
pmssm_plotter.survivalProbability1D(drawstring=particleName, xaxisDrawConfig={"1Dlogy":True} ,canvasStyle=survivalPlots1DCanvasStyle)


deltaMParticle = "abs(g-chi10)"
for ypar in pltconfig.yaxisFor2D:
    print("survivalProbability2D for: ", ypar, deltaMParticle, "\n\n")
    
    canvasStyle2D = {
            "legend":pltconfig.leftbottom["legend"].copy()
        }
    canvasStyle2D["legend"]["legendNColumns"] = 1
    
    
    
    
    if ypar != "abs(chi10)":
        pmssm_plotter.survivalProbability2D(drawstring = ypar+":"+deltaMParticle,analysis=pltconfig.analysisName,contourSwitch=True, canvasStyle=canvasStyle2D)
    else:
        pmssm_plotter.survivalProbability2D(drawstring = ypar+":"+deltaMParticle,analysis=pltconfig.analysisName,contourSwitch=True)
    print("0.5 quantile 2D for: ", ypar, deltaMParticle, "\n\n")
    if ypar != "abs(chi10)":
        pmssm_plotter.quantilePlots2D(drawstring=ypar+":"+deltaMParticle,analysis=pltconfig.analysisName, quantile = 0.5, canvasStyle=canvasStyle2D)
    else:
        pmssm_plotter.quantilePlots2D(drawstring=ypar+":"+deltaMParticle,analysis=pltconfig.analysisName, quantile = 0.5)
    print("0.75 quantile 2D for: ", ypar, deltaMParticle, "\n\n")
    if ypar != "abs(chi10)":
        pmssm_plotter.quantilePlots2D(drawstring=ypar+":"+deltaMParticle,analysis=pltconfig.analysisName, quantile = 0.75, canvasStyle=canvasStyle2D)
    else:
        pmssm_plotter.quantilePlots2D(drawstring=ypar+":"+deltaMParticle,analysis=pltconfig.analysisName, quantile = 0.75)

    print("0.9 quantile 2D for: ", ypar, deltaMParticle, "\n\n")
    if ypar != "abs(chi10)":
        pmssm_plotter.quantilePlots2D(drawstring=ypar+":"+deltaMParticle,analysis=pltconfig.analysisName, quantile = 0.9, canvasStyle=canvasStyle2D)
    else:
        pmssm_plotter.quantilePlots2D(drawstring=ypar+":"+deltaMParticle,analysis=pltconfig.analysisName, quantile = 0.9)
    print("0.99 quantile 2D for: ", ypar, deltaMParticle, "\n\n")
    if ypar != "abs(chi10)":
        pmssm_plotter.quantilePlots2D(drawstring=ypar+":"+deltaMParticle,analysis=pltconfig.analysisName, quantile = 0.99, canvasStyle=canvasStyle2D)
    else:
        pmssm_plotter.quantilePlots2D(drawstring=ypar+":"+deltaMParticle,analysis=pltconfig.analysisName, quantile = 0.99)
