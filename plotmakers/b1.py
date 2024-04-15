import sys
import shutil

sys.path.append("/Users/dorukhan/Desktop/cern/pmssm/")

from ROOT import *
from pmssm import PMSSM, particleDrawConfig_TeV
import config as pltconfig

particleName = "b1"

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
pmssm_plotter.impact1D(drawstring=particleName, canvasStyle=pltconfig.righttop)

print("quantile 1D for: ", particleName, "\n\n")
pmssm_plotter.quantilePlots1D(drawstring=particleName, canvasStyle=pltconfig.rightbottom)

for ypar in pltconfig.yaxisFor2D:
    
    quantilePlots2DCanvasStyle = pltconfig.righttop.copy()
    quantilePlots2DCanvasStyle["legend"] = {"textColor":kWhite}
    
    print("survivalProbability2D for: ", ypar, particleName, "\n\n")
    if ypar != "abs(chi10)":
        
        
        survivalProbability2DCanvasStyle = pltconfig.righttop.copy()
        survivalProbability2DCanvasStyle["legend"]["x1"] = 0.3
        survivalProbability2DCanvasStyle["legend"]["y2"] = 0.8
        survivalProbability2DCanvasStyle["legend"]["y1"] = 0.7

        pmssm_plotter.survivalProbability2D(drawstring = ypar+":"+particleName,analysis=pltconfig.analysisName,contourSwitch=True, canvasStyle=survivalProbability2DCanvasStyle)
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
