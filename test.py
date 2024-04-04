from ROOT import *
from pmssm import PMSSM, particleDrawConfig_TeV
import os
import shutil



root_file_path = "pmssmtree_11aug2023.root"
tree_name = "mcmc"
outdir = "plots_sun"

if os.path.exists(outdir):
    shutil.rmtree(outdir)

root_file = TFile(root_file_path) # type: ignore
intree = root_file.Get(tree_name)

pmssm_plotter = PMSSM(
    intree = intree, 
    outdir = outdir,
    particleDrawConfig= particleDrawConfig_TeV,
    canvasStyle= {
        "energy" : "13",
        "extraText" : "Preliminary",
        "lumi" : "",
        "analysisName" : "",
    }
    )

# pmssm_plotter.impact(
#     drawstring="b1",
#     name="buttom",
# )

# pmssm_plotter.impact(
#     drawstring="g",
#     name="gluon",
# )

# pmssm_plotter.survivalProbability2D(
#     drawstring = "abs(chi10):g",
#     name = "gluino_chi10_higgsino_RDPlanck",
#     moreconstraints = []
#     )


pmssm_plotter.survivalProbability2D(
    drawstring = "abs(chi10):g",
    name = "gluino_chi10_higgsino_RDPlanck_contour",
    moreconstraints = [],
    contourSwitch = True
    )

pmssm_plotter.quantilePlots1D(
    drawstring = "g",
    name = "gluino",
    moreconstraints = [],
    canvasStyle= {
        "offset" : {
            "ymax" : 0
        }
    }
    )

pmssm_plotter.quantilePlots1D(
    drawstring = "b1",
    name = "bottom",
    moreconstraints = []
    )