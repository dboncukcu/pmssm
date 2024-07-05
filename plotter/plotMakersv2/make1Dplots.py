import os
import sys
current_file_path = os.path.abspath(__file__)
parent_directory = os.path.dirname(os.path.dirname(current_file_path))
sys.path.append(parent_directory)


from ROOT import  *

from PlotterConfig import PlotterConfig
from Plotter import PMSSM


## IMPACT 1D

c_impact = PlotterConfig()
c_impact.global_settings["outputPath"] = "../../output/impact1D"
pmssm_impact = PMSSM(config=c_impact)

pmssm_impact.constraints.printAnalysisList()


pmssm_impact.impact1D("tau1")
pmssm_impact.impact1D("abs(chi10)",legendStyle="rightTop")
pmssm_impact.impact1D("abs(chi1pm)")
pmssm_impact.impact1D("abs(chi2pm)",legendStyle="leftTop")
pmssm_impact.impact1D("abs(chi20)")
pmssm_impact.impact1D("abs(chi30)",legendStyle="leftTop")
pmssm_impact.impact1D("abs(chi40)",legendStyle="leftTop")
pmssm_impact.impact1D("t1",legendStyle="leftTop")
pmssm_impact.impact1D("b1")
pmssm_impact.impact1D("lcsp",legendStyle="rightTop")
pmssm_impact.impact1D("Mq1")
pmssm_impact.impact1D("Md1")
pmssm_impact.impact1D("Ml1")
pmssm_impact.impact1D("g")
del pmssm_impact


## QUANTILE 1D


c_quantile = PlotterConfig()
c_quantile.global_settings["outputPath"] = "../../output/quantile1D"
pmssm_quantile = PMSSM(config=c_quantile)

pmssm_quantile.constraints.printAnalysisList()


pmssm_quantile.quantile1D_with_sigmaVariations("tau1", xaxisDrawConfig={"bins":100})
pmssm_quantile.quantile1D_with_sigmaVariations("abs(chi10)", xaxisDrawConfig={"bins":100})
pmssm_quantile.quantile1D_with_sigmaVariations("abs(chi1pm)", xaxisDrawConfig={"bins":100})
pmssm_quantile.quantile1D_with_sigmaVariations("abs(chi2pm)", xaxisDrawConfig={"bins":100})
pmssm_quantile.quantile1D_with_sigmaVariations("abs(chi20)", xaxisDrawConfig={"bins":100})
pmssm_quantile.quantile1D_with_sigmaVariations("abs(chi30)",legendStyle="rightTop", xaxisDrawConfig={"bins":100})
pmssm_quantile.quantile1D_with_sigmaVariations("abs(chi40)", xaxisDrawConfig={"bins":100})
pmssm_quantile.quantile1D_with_sigmaVariations("t1", xaxisDrawConfig={"bins":100})
pmssm_quantile.quantile1D_with_sigmaVariations("b1", xaxisDrawConfig={"bins":100})
pmssm_quantile.quantile1D_with_sigmaVariations("lcsp", xaxisDrawConfig={"bins":100})
pmssm_quantile.quantile1D_with_sigmaVariations("g", xaxisDrawConfig={"bins":100})
pmssm_quantile.quantile1D_with_sigmaVariations("Mq1", xaxisDrawConfig={"bins":100})
pmssm_quantile.quantile1D_with_sigmaVariations("Md1", xaxisDrawConfig={"bins":100})
pmssm_quantile.quantile1D_with_sigmaVariations("Ml1", xaxisDrawConfig={"bins":100})

del pmssm_quantile
# ## SURVIVAL 1D


c_survival = PlotterConfig()
c_survival.global_settings["outputPath"] = "../../output/survival1D"
pmssm_survival = PMSSM(config=c_survival)

pmssm_survival.constraints.printAnalysisList()


pmssm_survival.survivalProbability1D("tau1")
pmssm_survival.survivalProbability1D("abs(chi10)")
pmssm_survival.survivalProbability1D("abs(chi1pm)")
pmssm_survival.survivalProbability1D("abs(chi2pm)")
pmssm_survival.survivalProbability1D("abs(chi20)")
pmssm_survival.survivalProbability1D("abs(chi30)")
pmssm_survival.survivalProbability1D("abs(chi40)")
pmssm_survival.survivalProbability1D("t1")
pmssm_survival.survivalProbability1D("b1")
pmssm_survival.survivalProbability1D("lcsp")
pmssm_survival.survivalProbability1D("g")
pmssm_survival.survivalProbability1D("Mq1")
pmssm_survival.survivalProbability1D("Md1")
pmssm_survival.survivalProbability1D("Ml1")

del pmssm_survival
