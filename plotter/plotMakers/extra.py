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
c.global_settings["outputPath"] = "../../output/extra"

c.global_settings["logEps"] = 1e-8

pmssm = PMSSM(config=c)

pmssm.constraints.printAnalysisList()

pmssm.impact1D("deltaEW",legendStyle="rightBottom",drawConfig={"XaxisSetTitleOffset":1.2})
pmssm.quantile1D("deltaEW",xaxisDrawConfig={"1Dlogy":False},legendStyle="leftTop")
pmssm.survivalProbability1D("deltaEW",xaxisDrawConfig={"1Dlogy":False},drawConfig={"legendFillWhite" : False})

# pmssm.impact1D("t1",analysis="cms_sus_20_001")
# pmssm.impact1D("lcsp",analysis="cms_sus_20_001")
# pmssm.impact1D("g",analysis="cms_sus_20_001")
# pmssm.quantile2D("abs(chi20)-abs(chi10):abs(chi10)",quantile=0.99,analysis="cms_sus_20_001")


# for analyis in pmssm.constraints.getAnalysisList():
#     pmssm.survivalProbability2D("abs(chi1pm)-abs(chi10):abs(chi10)",analysis=analyis)
#     pmssm.quantile2D("t1-abs(chi10):abs(chi10)",quantile=0.99,analysis=analyis)


# pmssm.quantile2D("abs(chi1pm)-abs(chi10):abs(chi10)",quantile=0.99)
# pmssm.quantile2D("abs(chi20)-abs(chi10):abs(chi10)",quantile=0.99)
# pmssm.quantile2D("g-abs(chi10):abs(chi10)",quantile=0.99)
# pmssm.quantile2D("t1-abs(chi10):abs(chi10)",quantile=0.99)
# pmssm.quantile2D("b1-abs(chi10):abs(chi10)",quantile=0.99)
# pmssm.quantile2D("lcsp-abs(chi10):abs(chi10)",quantile=0.99)

# pmssm.survivalProbability2D("abs(chi20)-abs(chi10):abs(chi10)",showLegend=True,legendStyle="rightBottom")
# pmssm.survivalProbability2D("abs(chi1pm)-abs(chi10):abs(chi10)")
# pmssm.survivalProbability2D("g-abs(chi10):abs(chi10)")
# pmssm.survivalProbability2D("t1-abs(chi10):abs(chi10)")
# pmssm.survivalProbability2D("b1-abs(chi10):abs(chi10)")
# pmssm.survivalProbability2D("lcsp-abs(chi10):abs(chi10)")