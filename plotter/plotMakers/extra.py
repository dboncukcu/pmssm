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


pmssm.impact1D("deltaEW",legendStyle="rightBottom",drawConfig={"XaxisSetTitleOffset":1.2})
pmssm.quantile1D("deltaEW",xaxisDrawConfig={"1Dlogy":False},legendStyle="leftTop",drawConfig={"legendFillWhite" : False})
pmssm.survivalProbability1D("deltaEW",xaxisDrawConfig={"1Dlogy":False},drawConfig={"legendFillWhite" : False})

pmssm.quantile2D("mA:tanbeta",quantile=0.99)
pmssm.survivalProbability2D("mA:tanbeta",showLegend=True)


pmssm.impact1D("chi1pm_ctau",legendStyle="rightTop",xaxisDrawConfig={"logScale":True})
pmssm.impact1D("chi1pm_ctau",
               legendStyle="leftBottom",
               xaxisDrawConfig={"1Dlogy":True,"logScale":True},
               drawConfig={
                    "XaxisSetTitleOffset":1.35,
                    "YaxisSetTitleOffset":1.3,
                    "leftMargin":0.03,
                    "rightMargin":0.01,
                    "bottomMargin":0.07,
                    "leftBottom" : {"x1":0.18,"x2":0.59,"y1":0.21,"y2":0.36},
                    })
# pmssm.quantile1D("chi1pm_ctau",drawConfig={"yMaxOffsett":0.1},xaxisDrawConfig={"1Dlogy":False,"logScale":True})
# pmssm.survivalProbability1D(" ",xaxisDrawConfig={"1Dlogy":False,"logScale":True})


pmssm_chi20_ctau = PMSSM(config=c)
pmssm_chi20_ctau.c.global_settings["logEps"] = 1e-5

pmssm_chi20_ctau.c.drawConfig["impact1D"]["bottomMargin"] = 0.07
pmssm_chi20_ctau.c.drawConfig["impact1D"]["leftMargin"] = 0.03
pmssm_chi20_ctau.c.drawConfig["impact1D"]["rightMargin"] = 0.01
pmssm_chi20_ctau.c.drawConfig["impact1D"]["XaxisSetTitleOffset"] = 1.3
pmssm_chi20_ctau.c.drawConfig["impact1D"]["YaxisSetTitleOffset"] = 1.3
pmssm_chi20_ctau.c.drawConfig["impact1D"]["rightTop"] = {"x1":0.53,"x2":0.83,"y1":0.72,"y2":0.9}
pmssm_chi20_ctau.impact1D("chi20_ctau",legendStyle="rightTop",xaxisDrawConfig={"1Dlogy":True,"logScale":True})

pmssm_chi20_ctau.c.drawConfig["quantile1D"]["XaxisSetTitleOffset"] = 1.3
pmssm_chi20_ctau.c.drawConfig["quantile1D"]["bottomMargin"] = 0.07
pmssm_chi20_ctau.c.drawConfig["quantile1D"]["rightMargin"] = 0.01
pmssm_chi20_ctau.c.drawConfig["quantile1D"]["leftBottom"] = {"x1":0.19,"x2":0.42,"y1":0.22,"y2":0.41}
pmssm_chi20_ctau.c.drawConfig["quantile1D"]["yMaxOffsett"] = 0.1
pmssm_chi20_ctau.quantile1D("chi20_ctau",legendStyle="leftBottom",xaxisDrawConfig={"1Dlogy":False,"logScale":True})

pmssm_chi20_ctau.c.drawConfig["survival1D"]["leftMargin"] = 0.03
pmssm_chi20_ctau.c.drawConfig["survival1D"]["rightMargin"] = 0.01
pmssm_chi20_ctau.c.drawConfig["survival1D"]["bottomMargin"] = 0.07
pmssm_chi20_ctau.c.drawConfig["survival1D"]["XaxisSetTitleOffset"] = 1.3
pmssm_chi20_ctau.c.drawConfig["survival1D"]["YaxisSetTitleOffset"] = 1.2
pmssm_chi20_ctau.c.drawConfig["survival1D"]["rightBottom"] = {"x1":0.49,"x2":0.92,"y1":0.22,"y2":0.4}
pmssm_chi20_ctau.survivalProbability1D("chi20_ctau",xaxisDrawConfig={"1Dlogy":False,"logScale":True})

pmssm.relicDensity1D()



# # ### flip-book plots
# pmssm_flipbook = PMSSM(config=c)
# pmssm_flipbook.c.particleConfig["abs(chi10)"]["min"] = 0
# pmssm_flipbook.c.particleConfig["abs(chi10)"]["max"] = 2000
# pmssm_flipbook.c.particleConfig["abs(chi10)"]["Ndivisions"] = -505
# pmssm_flipbook.c.particleConfig["abs(chi1pm)-abs(chi10)"]["min"] = 0.02
# pmssm_flipbook.survivalProbability2D("abs(chi1pm)-abs(chi10):abs(chi10)", analysis="cms_sus_18_004",customName="_1")
# pmssm_flipbook.survivalProbability2D("abs(chi1pm)-abs(chi10):abs(chi10)", analysis="cms_sus_18_004,cms_sus_20_001",customName="_2")
# pmssm_flipbook.survivalProbability2D("abs(chi1pm)-abs(chi10):abs(chi10)", analysis="cms_sus_18_004,cms_sus_20_001,cms_sus_21_007,cms_sus_21_007_mb",customName="_3")
# pmssm_flipbook.survivalProbability2D("abs(chi1pm)-abs(chi10):abs(chi10)", analysis="cms_sus_18_004,cms_sus_20_001,cms_sus_21_007,cms_sus_21_007_mb,cms_sus_21_006",customName="_4")
# pmssm_flipbook.survivalProbability2D("abs(chi1pm)-abs(chi10):abs(chi10)", analysis="combined",customName="_5")
# pmssm_flipbook.survivalProbability2D(
#     "abs(chi1pm)-abs(chi10):abs(chi10)", 
#     analysis="combined",
#     moreconstraints=["Omegah2<=0.132"],
#     customName="_6")
# pmssm_flipbook.survivalProbability2D(
#     "abs(chi1pm)-abs(chi10):abs(chi10)", 
#     analysis="combined",
#     moreconstraints=["Omegah2<=0.132","dd_exclusion_pval>=0.05"],
#     customName="_7")
# pmssm_flipbook.survivalProbability2D(
#     "abs(chi1pm)-abs(chi10):abs(chi10)", 
#     analysis="combined",
#     moreconstraints=["Omegah2<=0.132","dd_exclusion_pval>=0.05","deltaEW<=500"],
#     customName="_8")