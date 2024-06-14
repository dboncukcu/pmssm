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



pmssm = PMSSM(config=c)

pmssm.constraints.printAnalysisList()

""" 
DeltaEW = impact1D, quantile1D, survival1D
m(A) vs tan(beta) = quantile2D, survival2D
ctau (chargino) = impact1D, quantile1D, survival1D
ctau(2nd neutralino chi20) = impact1D, quantile1D, survival1D
relic density = special type
relic density vs dm(chi1pm, chi10) = ultra special type 
"""


# pmssm.impact1D("deltaEW")
# pmssm.quantile1D("deltaEW")
# pmssm.survivalProbability1D("deltaEW")

# pmssm.quantile2D("mA:tanbeta",quantile=0.99)
# pmssm.survivalProbability2D("mA:tanbeta",showLegend=True)


# pmssm.impact1D("chi1pm_ctau",legendStyle="rightTop")
# pmssm.impact1D("chi1pm_ctau",legendStyle="rightTop",xaxisDrawConfig={"1Dlogy":True})
# pmssm.quantile1D("chi1pm_ctau",drawConfig={"yMaxOffsett":0.1})
# pmssm.survivalProbability1D("chi1pm_ctau")

# pmssm.impact1D("chi20_ctau",legendStyle="rightTop")
pmssm.impact1D("chi20_ctau",legendStyle="leftTop",xaxisDrawConfig={"1Dlogy":True},drawConfig={"leftMargin":0.03,"YaxisSetTitleOffset":1.2,"rightMargin":0.09})
pmssm.quantile1D("chi20_ctau",drawConfig={"yMaxOffsett":0.1},legendStyle="leftTop")
pmssm.survivalProbability1D("chi20_ctau")