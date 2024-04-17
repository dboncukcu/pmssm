import sys
import shutil

sys.path.append("/Users/dorukhan/Desktop/cern/pmssm/")

from ROOT import *
from pmssm import PMSSM, particleDrawConfig_TeV
import config as pltconfig

particleName = "abs(chipm)-abs(chi10)"

root_file_path = "pmssmtree_11aug2023.root"
tree_name = "mcmc"
outdir =  pltconfig.plotsdir+"__"+particleName.replace("(","").replace(")","").replace("-","")
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

quantilePlots1DCanvasStyle = {
    "legend":pltconfig.righttop["legend"].copy()
}
quantilePlots1DCanvasStyle["legend"]["x1"] = 0.75
quantilePlots1DCanvasStyle["legend"]["x2"] = 0.85
quantilePlots1DCanvasStyle["offset"] = {
    "ymax" : 5.5,
}

print("quantile 1D for: ", particleName, "\n\n")
pmssm_plotter.quantilePlots1D(drawstring=particleName)
pmssm_plotter.quantilePlots1D(drawstring=particleName, xaxisDrawConfig={"1Dlogy":True}, canvasStyle=quantilePlots1DCanvasStyle)
