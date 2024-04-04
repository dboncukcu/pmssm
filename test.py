from ROOT import *
from pmssm import PMSSM, particleDrawConfig_TeV

root_file_path = "pmssmtree_11aug2023.root"
tree_name = "mcmc"
outdir = "plots_sun"

root_file = TFile(root_file_path) # type: ignore
intree = root_file.Get(tree_name)

pmssm_plotter = PMSSM(
    intree = intree, 
    outdir = outdir,
    particleDrawConfig= particleDrawConfig_TeV,
    canvasStyle= {
        "energy" : "",
        "extraText" : "Preliminary",
        "lumi" : "",
        "analysisName" : "Combined",
    }
    )

pmssm_plotter.impact(
    drawstring="b1",
    name="buttom",
)

pmssm_plotter.impact(
    drawstring="g",
    name="gluon",
)

pmssm_plotter.survivalProbability2D(
    drawstring = "abs(chi10):g",
    name = "gluino_chi10_higgsino_RDPlanck",
    moreconstraints = []
    )