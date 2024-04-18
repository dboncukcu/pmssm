import sys
import shutil

sys.path.append("/Users/dorukhan/Desktop/cern/pmssm/")

from ROOT import *
from pmssm import PMSSM, particleDrawConfig_TeV
import config as pltconfig

particleName = "abs(chi1pm)"

root_file_path = "pmssmtree_11aug2023.root"
tree_name = "mcmc"
outdir =  pltconfig.plotsdir+particleName.replace("(","").replace(")","")
print(outdir)
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
print(pmssm_plotter.outdir)
print("impact1D for: ", particleName, "\n\n")
pmssm_plotter.impact1D(drawstring=particleName, canvasStyle=pltconfig.righttop)
impactPlots1DCanvasStyle = {
    "legend":pltconfig.rightbottom["legend"].copy()
}
impactPlots1DCanvasStyle["legend"]["x1"] = 0.58
impactPlots1DCanvasStyle["legend"]["x2"] = 0.78
pmssm_plotter.impact1D(drawstring=particleName, xaxisDrawConfig={"1Dlogy":True}, canvasStyle=impactPlots1DCanvasStyle)

print("quantile 1D for: ", particleName, "\n\n")
quantilePlots1DCanvasStyle = {
    "legend":pltconfig.righttop["legend"].copy()
}
quantilePlots1DCanvasStyle["legend"]["x1"] = 0.75
quantilePlots1DCanvasStyle["legend"]["x2"] = 0.85
pmssm_plotter.quantilePlots1D(drawstring=particleName, canvasStyle=pltconfig.rightbottom)
pmssm_plotter.quantilePlots1D(drawstring=particleName, xaxisDrawConfig={"1Dlogy":True}, canvasStyle=quantilePlots1DCanvasStyle)

print("survivalProbability1D for:",particleName, "\n\n")
survivalPlots1DCanvasStyle = {
    "legend":pltconfig.rightbottom["legend"].copy()
}
survivalPlots1DCanvasStyle["legend"]["x1"] = 0.58
survivalPlots1DCanvasStyle["legend"]["x2"] = 0.78
pmssm_plotter.survivalProbability1D(drawstring=particleName, canvasStyle=survivalPlots1DCanvasStyle)
pmssm_plotter.survivalProbability1D(drawstring=particleName, xaxisDrawConfig={"1Dlogy":True} ,canvasStyle=survivalPlots1DCanvasStyle)


for ypar in pltconfig.yaxisFor2D:
    if ypar == "abs(chi20-chi10)":
        quantilePlots2DCanvasStyle = {"legend":pltconfig.righttop["legend"].copy()}
        quantilePlots2DCanvasStyle["legend"]={"textColor":kWhite}
        quantilePlots2DCanvasStyle["legend"]["x1"] = 0.17
        survivalProbability2DCanvasStyle =  {"legend":pltconfig.lefttop["legend"].copy()}
        survivalProbability2DCanvasStyle["legend"]["x1"] = 0.35
        survivalProbability2DCanvasStyle["legend"]["x2"] = 0.81
        survivalProbability2DCanvasStyle["legend"]["y2"] = 0.33
        survivalProbability2DCanvasStyle["legend"]["y1"] = 0.15
    elif ypar == "abs(chi1pm)-abs(chi10)":
        quantilePlots2DCanvasStyle = {"legend":pltconfig.righttop["legend"].copy()}
        quantilePlots2DCanvasStyle["legend"]={"textColor":kBlack}
        quantilePlots2DCanvasStyle["legend"]["x1"] = 0.13
        survivalProbability2DCanvasStyle = {"legend":pltconfig.lefttop["legend"].copy()}
        survivalProbability2DCanvasStyle["legend"]["x1"] = 0.35
        survivalProbability2DCanvasStyle["legend"]["x2"] = 0.81
        survivalProbability2DCanvasStyle["legend"]["y2"] = 0.3
        survivalProbability2DCanvasStyle["legend"]["y1"] = 0.15
    
    print("survivalProbability2D for: ", ypar, particleName, "\n\n")
    if ypar != "abs(chi10)": 
        pmssm_plotter.survivalProbability2D(drawstring = ypar+":"+particleName,analysis=pltconfig.analysisName,contourSwitch=True, canvasStyle= survivalProbability2DCanvasStyle)
    else:
        pmssm_plotter.survivalProbability2D(drawstring = ypar+":"+particleName,analysis=pltconfig.analysisName,contourSwitch=True)
    print("0.5 quantile 2D for: ", ypar, particleName, "\n\n")
    if ypar != "abs(chi10)": 
        pmssm_plotter.quantilePlots2D(drawstring=ypar+":"+particleName,analysis=pltconfig.analysisName, quantile = 0.5, canvasStyle=quantilePlots2DCanvasStyle)
    else:
        pmssm_plotter.quantilePlots2D(drawstring=ypar+":"+particleName,analysis=pltconfig.analysisName, quantile = 0.5)
    print("0.75 quantile 2D for: ", ypar, particleName, "\n\n")
    if ypar != "abs(chi10)":
        pmssm_plotter.quantilePlots2D(drawstring=ypar+":"+particleName,analysis=pltconfig.analysisName, quantile = 0.75, canvasStyle=quantilePlots2DCanvasStyle)
    else:
        pmssm_plotter.quantilePlots2D(drawstring=ypar+":"+particleName,analysis=pltconfig.analysisName, quantile = 0.75)

    print("0.9 quantile 2D for: ", ypar, particleName, "\n\n")
    if ypar != "abs(chi10)":
        pmssm_plotter.quantilePlots2D(drawstring=ypar+":"+particleName,analysis=pltconfig.analysisName, quantile = 0.9, canvasStyle=quantilePlots2DCanvasStyle)
    else:
        pmssm_plotter.quantilePlots2D(drawstring=ypar+":"+particleName,analysis=pltconfig.analysisName, quantile = 0.9)
    print("0.99 quantile 2D for: ", ypar, particleName, "\n\n")
    if ypar != "abs(chi10)":
        pmssm_plotter.quantilePlots2D(drawstring=ypar+":"+particleName,analysis=pltconfig.analysisName, quantile = 0.99, canvasStyle=quantilePlots2DCanvasStyle)
    else:
        pmssm_plotter.quantilePlots2D(drawstring=ypar+":"+particleName,analysis=pltconfig.analysisName, quantile = 0.99)
