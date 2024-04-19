import sys
import shutil

sys.path.append("/Users/denizgungordu/Desktop/pmssm/")

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
    friendAnalysis=[{"treeName":"cms_sus_20_001","path":"/Users/denizgungordu/Desktop/pmssm/sus_20_001_likelihood.root"}],
    )


deltaM = ["abs(chi1pm)-abs(chi10)","abs(chi20-chi10)","g-abs(chi10)","t1-abs(chi10)","b1-abs(chi10)","lcsp-abs(chi10)"]
for ypar in deltaM:
    

    print("survivalProbability2D for: ", ypar, particleName, "\n\n")
    survivalProbability2DCanvasStyle = {
        "legend":pltconfig.righttop["legend"].copy()
    }
    #survivalProbability2DCanvasStyle["legend"]={"textColor":kWhite}
    survivalProbability2DCanvasStyle["legend"]["x1"] = 0.52
    survivalProbability2DCanvasStyle["legend"]["x2"] = 0.95
    survivalProbability2DCanvasStyle["legend"]["legendNColumns"] = 1


    pmssm_plotter.survivalProbability2D(
        drawstring = ypar+":"+particleName,
        analysis="combined",
        contourSwitch=True, 
        canvasStyle= survivalProbability2DCanvasStyle,
        yaxisDrawConfig={"nbin":50},
        )
    
    # pmssm_plotter.survivalProbability2D(
    #     drawstring = ypar+":"+particleName,
    #     analysis="combined_with_cms_sus_20_001",
    #     contourSwitch=True, 
    #     canvasStyle= survivalProbability2DCanvasStyle,
    #     yaxisDrawConfig={"nbin":50},
    #     )
    
    # pmssm_plotter.survivalProbability2D(
    #     drawstring = ypar+":"+particleName,
    #     analysis="cms_sus_20_001",
    #     contourSwitch=True, 
    #     canvasStyle= survivalProbability2DCanvasStyle,
    #     yaxisDrawConfig={"nbin":50},
    #     )
    
    # quantilePlots2DStyle = {
    #     "legend" : {
    #         "textColor":kWhite
    #     }
    # }

    # pmssm_plotter.quantilePlots2D(drawstring=ypar+":"+particleName,analysis=pltconfig.analysisName, quantile = 0.5,yaxisDrawConfig={"nbin":50},canvasStyle = quantilePlots2DStyle)
    # pmssm_plotter.quantilePlots2D(drawstring=ypar+":"+particleName,analysis=pltconfig.analysisName, quantile = 0.75,yaxisDrawConfig={"nbin":50},canvasStyle = quantilePlots2DStyle)
    # pmssm_plotter.quantilePlots2D(drawstring=ypar+":"+particleName,analysis=pltconfig.analysisName, quantile = 0.9,yaxisDrawConfig={"nbin":50},canvasStyle = quantilePlots2DStyle)
    # pmssm_plotter.quantilePlots2D(drawstring=ypar+":"+particleName,analysis=pltconfig.analysisName, quantile = 0.99,yaxisDrawConfig={"nbin":50},canvasStyle = quantilePlots2DStyle)