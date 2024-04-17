import sys
import shutil

sys.path.append("/Users/dorukhan/Desktop/cern/pmssm/")

from ROOT import *
from pmssm import PMSSM, particleDrawConfig_TeV
import config as pltconfig

particleName = "abs(chi10)"

root_file_path = "pmssmtree_11aug2023.root"
tree_name = "mcmc"
outdir =  pltconfig.plotsdir+"DeltaMasses/"
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


deltaM = ["abs(chi1pm-chi10)","abs(chi20-chi10)","g-abs(chi10)","t1-abs(chi10)","b1-abs(chi10)","lcsp-abs(chi10)"]
for ypar in deltaM:
    
    quantilePlots2DCanvasStyle = pltconfig.righttop.copy()
    quantilePlots2DCanvasStyle["legend"]={"textColor":kWhite}
    quantilePlots2DCanvasStyle["legend"]["x1"] = 0.15
    quantilePlots2DCanvasStyle["legend"]["x2"] = 0.15


    print("survivalProbability2D for: ", ypar, particleName, "\n\n")
    survivalProbability2DCanvasStyle = pltconfig.rightbottom.copy()
    #survivalProbability2DCanvasStyle["legend"]={"textColor":kWhite}
    survivalProbability2DCanvasStyle["legend"]["x1"] = 0.52
    survivalProbability2DCanvasStyle["legend"]["x2"] = 0.93
    survivalProbability2DCanvasStyle["legend"]["y2"] = 0.40
    survivalProbability2DCanvasStyle["legend"]["y1"] = 0.15
    survivalProbability2DCanvasStyle["legend"]["legendNColumns"] = 1


    pmssm_plotter.survivalProbability2D(
        drawstring = ypar+":"+particleName,
        analysis=pltconfig.analysisName,
        contourSwitch=True, 
        canvasStyle= survivalProbability2DCanvasStyle,
        yaxisDrawConfig={"nbin":50},
        )
