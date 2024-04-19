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
    canvasStyle = pltconfig.generalProperties,
    friendAnalysis=[{"treeName":"cms_sus_20_001","path":"/Users/dorukhan/Desktop/cern/pmssm/sus_20_001_likelihood.root"}],
    )


deltaM = ["abs(chi1pm)-abs(chi10)","abs(chi20-chi10)","g-abs(chi10)","t1-abs(chi10)","b1-abs(chi10)","lcsp-abs(chi10)"]
for ypar in deltaM:
    
    survivalProbability2DCanvasStyle2 = pltconfig.righttop.copy()
    survivalProbability2DCanvasStyle2["legend"]["legendNColumns"] = 1


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
        canvasStyle= survivalProbability2DCanvasStyle if ypar != "abs(chi1pm)-abs(chi10)" else survivalProbability2DCanvasStyle2,
        yaxisDrawConfig={"nbin":50},
        )
    
    
    pmssm_plotter.survivalProbability2D(
        drawstring = ypar+":"+particleName,
        analysis="cms_sus_20_001",
        contourSwitch=True, 
        canvasStyle= survivalProbability2DCanvasStyle if ypar != "abs(chi1pm)-abs(chi10)" else survivalProbability2DCanvasStyle2,
        yaxisDrawConfig={"nbin":50},
        )
    
    # quantilePlots2DStyle = {
    #     "legend" : {
    #         "textColor":kWhite
    #     }
    # }

    # pmssm_plotter.quantilePlots2D(drawstring=ypar+":"+particleName,analysis=pltconfig.analysisName, quantile = 0.5,yaxisDrawConfig={"nbin":50},canvasStyle = quantilePlots2DStyle)
    # pmssm_plotter.quantilePlots2D(drawstring=ypar+":"+particleName,analysis=pltconfig.analysisName, quantile = 0.75,yaxisDrawConfig={"nbin":50},canvasStyle = quantilePlots2DStyle)
    # pmssm_plotter.quantilePlots2D(drawstring=ypar+":"+particleName,analysis=pltconfig.analysisName, quantile = 0.9,yaxisDrawConfig={"nbin":50},canvasStyle = quantilePlots2DStyle)
    # pmssm_plotter.quantilePlots2D(drawstring=ypar+":"+particleName,analysis=pltconfig.analysisName, quantile = 0.99,yaxisDrawConfig={"nbin":50},canvasStyle = quantilePlots2DStyle)