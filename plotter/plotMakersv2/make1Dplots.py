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
pmssm_impact.impact1D("abs(chi20)")
pmssm_impact.impact1D("t1",legendStyle="leftTop")
pmssm_impact.impact1D("b1")
pmssm_impact.impact1D("lcsp",legendStyle="rightTop")
pmssm_impact.impact1D("g")

## QUANTILE 1D


c_quantile = PlotterConfig()
c_quantile.global_settings["outputPath"] = "../../output/quantile1D"
pmssm_quantile = PMSSM(config=c_quantile)

pmssm_quantile.constraints.printAnalysisList()


pmssm_quantile.quantile1D("tau1",legendStyle="leftTop")
pmssm_quantile.quantile1D("abs(chi10)")
pmssm_quantile.quantile1D("abs(chi1pm)")
pmssm_quantile.quantile1D("abs(chi20)")
pmssm_quantile.quantile1D("t1")
pmssm_quantile.quantile1D("b1")
pmssm_quantile.quantile1D("lcsp")
pmssm_quantile.quantile1D("g")
