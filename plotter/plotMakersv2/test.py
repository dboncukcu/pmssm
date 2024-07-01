import os
import sys
current_file_path = os.path.abspath(__file__)
parent_directory = os.path.dirname(os.path.dirname(current_file_path))
sys.path.append(parent_directory)


from ROOT import  *

from PlotterConfig import PlotterConfig
from Plotter import PMSSM



## QUANTILE 1D


c_quantile = PlotterConfig()
c_quantile.global_settings["outputPath"] = "../../output/quantile1D_with_sigmaVariations"
pmssm_quantile = PMSSM(config=c_quantile)

pmssm_quantile.constraints.printAnalysisList()


pmssm_quantile.quantile1D_with_sigmaVariations("tau1")
pmssm_quantile.quantile1D_with_sigmaVariations("abs(chi10)")
pmssm_quantile.quantile1D_with_sigmaVariations("abs(chi1pm)")
pmssm_quantile.quantile1D_with_sigmaVariations("abs(chi2pm)")
pmssm_quantile.quantile1D_with_sigmaVariations("abs(chi20)")
pmssm_quantile.quantile1D_with_sigmaVariations("abs(chi30)",legendStyle="rightTop")
pmssm_quantile.quantile1D_with_sigmaVariations("abs(chi40)")
pmssm_quantile.quantile1D_with_sigmaVariations("t1")
pmssm_quantile.quantile1D_with_sigmaVariations("b1")
pmssm_quantile.quantile1D_with_sigmaVariations("lcsp")
pmssm_quantile.quantile1D_with_sigmaVariations("g")
pmssm_quantile.quantile1D_with_sigmaVariations("Mq1")
pmssm_quantile.quantile1D_with_sigmaVariations("Md1")
pmssm_quantile.quantile1D_with_sigmaVariations("Ml1")
