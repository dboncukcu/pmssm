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
c.global_settings["outputPath"] = "../../output/fig7"


pmssm_Omegah2 = PMSSM(config=c)

pmssm_Omegah2.constraints.printAnalysisList()

pmssm_Omegah2.c.global_settings["logEps"] = 1e-7

pmssm_Omegah2.impact1D("Omegah2",drawConfig={"XaxisSetTitleOffset":1.2},xaxisDrawConfig={"1Dlogy":True})
pmssm_Omegah2.quantile1D_with_sigmaVariations("Omegah2",drawConfig={"legendFillWhite" : False})
pmssm_Omegah2.survivalProbability1D("Omegah2",drawConfig={"legendFillWhite" : False})



# pmssm_deltaEW = PMSSM(config=c)

# pmssm_deltaEW.constraints.printAnalysisList()

# pmssm_deltaEW.c.global_settings["logEps"] = 1e-13

# pmssm_deltaEW.impact1D("deltaEW",drawConfig={"XaxisSetTitleOffset":1.2},xaxisDrawConfig={"1Dlogy":True})
# pmssm_deltaEW.quantile1D_with_sigmaVariations("deltaEW",drawConfig={"legendFillWhite" : False})
# pmssm_deltaEW.survivalProbability1D("deltaEW",drawConfig={"legendFillWhite" : False})