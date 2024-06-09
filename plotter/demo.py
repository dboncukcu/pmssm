from ROOT import  *

from PlotterConfig import PlotterConfig
from Plotter import PMSSM

c = PlotterConfig()
c.global_settings["outputFileFormat"] = "pdf"

root_dict = [
    {"treeName": "mcmc", "filePath" : "/eos/user/d/dboncukc/rootFiles/pmssmtree_11aug2023.root "},
    {"treeName": "cms_sus_20_001",  "filePath" :"/eos/user/d/dboncukc/rootFiles/sus_20_001_likelihood.root"}
]

pmssm = PMSSM(root_dict,config=c)

pmssm.constraints.printAnalysisList()

pmssm.impact1D("g")

pmssm.impact1D("t1",legendStyle="leftTop")

pmssm.impact1D("t1",analysis="combined simplified",legendStyle="leftTop")

for analysis in pmssm.constraints.getAnalysisList():
    pmssm.impact1D("t1",analysis=analysis,legendStyle="leftTop")