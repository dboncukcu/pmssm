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
c.global_settings["outputPath"] = "../../output/survival1D"



pmssm = PMSSM(config=c)

pmssm.constraints.printAnalysisList()

pmssm.survivalProbability1D("abs(chi10)")
pmssm.survivalProbability1D("abs(chi1pm)")
pmssm.survivalProbability1D("abs(chi20)")
pmssm.survivalProbability1D("g")
pmssm.survivalProbability1D("t1")
pmssm.survivalProbability1D("lcsp")

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
