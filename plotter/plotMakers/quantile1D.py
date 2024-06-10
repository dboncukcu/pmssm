import os
import sys
current_file_path = os.path.abspath(__file__)
parent_directory = os.path.dirname(os.path.dirname(current_file_path))
sys.path.append(parent_directory)


from ROOT import  *

from PlotterConfig import PlotterConfig
from Plotter import PMSSM

c = PlotterConfig()
c.global_settings["outputFileFormat"] = "pdf"
c.global_settings["outputPath"] = "../../output/quantile1D"

root_dict = [
    {"treeName": "mcmc", "filePath" : "/eos/user/d/dboncukc/rootFiles/pmssmtree_11aug2023.root "},
    {"treeName": "cms_sus_20_001",  "filePath" :"/eos/user/d/dboncukc/rootFiles/sus_20_001_likelihood.root"}
]

pmssm = PMSSM(root_dict,config=c)

pmssm.constraints.printAnalysisList()

pmssm.quantile1D("abs(chi10)",drawConfig={"yMaxOffsett": 0.65},legendStyle="rightTop")
pmssm.quantile1D("abs(chi1pm)",legendStyle="rightBottom")
pmssm.quantile1D("abs(chi20)",drawConfig={"yMaxOffsett": 0.035},legendStyle="rightBottom")
pmssm.quantile1D("g",drawConfig={"yMaxOffsett": 0.65},legendStyle="leftTop")
pmssm.quantile1D("t1",drawConfig={"yMaxOffsett": 0.65},legendStyle="rightTop")
pmssm.quantile1D("lcsp",drawConfig={"yMaxOffsett": 0.2})
pmssm.quantile1D("b1")

#pmssm.impact1D("g")
#pmssm.impact1D("abs(chi10)",drawConfig={"yMaxOffsett": 0.0035},legendStyle="rightTop")
#pmssm.impact1D("abs(chi10)")
#pmssm.impact1D("abs(chi20)")
#pmssm.impact1D("abs(chi1pm)",drawConfig={"yMaxOffsett": 0.0035},legendStyle="rightTop")
#pmssm.impact1D("lcsp",drawConfig={"yMaxOffsett": 0.0035},legendStyle="rightTop")
#pmssm.impact1D("t1",drawConfig={"yMaxOffsett": 0.001},legendStyle="leftTop")



# pmssm.impact1D("t1",legendStyle="leftTop")





# pmssm.impact1D("t1",analysis="combined simplified",legendStyle="leftTop")

# for analysis in pmssm.constraints.getAnalysisList():
#     pmssm.impact1D("t1",analysis=analysis,legendStyle="leftTop")
