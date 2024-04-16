import sys
import shutil

sys.path.append("/Users/denizgungordu/Desktop/pmssm")

from ROOT import *
from pmssm import PMSSM, particleDrawConfig_TeV
import config as pltconfig

particleName = "abs(chi20-chi10)"

root_file_path = "pmssmtree_11aug2023.root"
tree_name = "mcmc"
outdir =  pltconfig.plotsdir+particleName.replace("(","").replace(")","").replace("-","")
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
survivalPlots1DCanvasStyle = {
    "legend":pltconfig.rightbottom["legend"].copy()
}
survivalPlots1DCanvasStyle["legend"]["x1"] = 0.58
survivalPlots1DCanvasStyle["legend"]["x2"] = 0.78

quantilePlots1DCanvasStyle = {
    "legend":pltconfig.rightbottom["legend"].copy()
}
quantilePlots1DCanvasStyle["legend"]["x1"] = 0.70
quantilePlots1DCanvasStyle["legend"]["x2"] = 0.90


print("quantile 1D for: ", particleName, "\n\n")
pmssm_plotter.quantilePlots1D(drawstring=particleName)

print("survivalProbability1D for:",particleName, "\n\n")
pmssm_plotter.survivalProbability1D(drawstring=particleName, canvasStyle=survivalPlots1DCanvasStyle)


 