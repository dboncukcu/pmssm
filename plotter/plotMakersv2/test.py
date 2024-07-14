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
c_quantile.global_settings["outputPath"] = "../../output/quantile1D_with_sigmaVariations2"
pmssm = PMSSM(config=c_quantile)

tree = pmssm.tree