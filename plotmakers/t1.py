import sys
import shutil

sys.path.append("/Users/dorukhan/Desktop/cern/pmssm/")

from ROOT import *
from pmssm import PMSSM, particleDrawConfig_TeV
import config as pltconfig

particleName = "t1"

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

print("quantile 1D for: ", particleName, "\n\n")
pmssm_plotter.quantilePlots1D(drawstring=particleName, canvasStyle= pltconfig.rightbottom)

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
