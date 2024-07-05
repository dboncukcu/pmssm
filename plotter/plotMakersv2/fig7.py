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

pmssm_Omegah2.impact1D("Omegah2",drawConfig={"XaxisSetTitleOffset":1.2,"yMaxOffsett": 1},xaxisDrawConfig={"1Dlogy":True})
pmssm_Omegah2.quantile1D_with_sigmaVariations("Omegah2",drawConfig={"legendFillWhite" : False})
pmssm_Omegah2.survivalProbability1D("Omegah2",drawConfig={"legendFillWhite" : False})


pmssm_cdm = PMSSM(config=c)

pmssm_cdm.constraints.printAnalysisList()

pmssm_cdm.impact1D("cdm_xsec_neutron_si_pb",legendStyle="leftTop",drawConfig={"yMaxOffsett":0.035,"bottomMargin":0.055,"rightMargin":0.01,"XaxisSetTitleOffset":1.2})
pmssm_cdm.quantile1D_with_sigmaVariations("cdm_xsec_neutron_si_pb",legendStyle="rightTop",drawConfig={"XaxisSetTitleOffset":1.2,"bottomMargin": 0.055,"yMaxOffsett":0.7,"legendFillWhite":False})
pmssm_cdm.survivalProbability1D("cdm_xsec_neutron_si_pb",legendStyle="leftBottom",drawConfig={"XaxisSetTitleOffset":1.2,"bottomMargin": 0.055})

pmssm_cdm.impact1D("cdm_xsec_neutron_sd_pb",legendStyle="leftTop",drawConfig={"yMaxOffsett":0.02,"bottomMargin":0.055,"rightMargin":0.01,"XaxisSetTitleOffset":1.2})
pmssm_cdm.quantile1D_with_sigmaVariations("cdm_xsec_neutron_sd_pb",drawConfig={"XaxisSetTitleOffset":1.2,"bottomMargin": 0.055, "rightBottom" : {"x1":0.6,"x2":1,"y1":0.2,"y2":0.34}})
pmssm_cdm.survivalProbability1D("cdm_xsec_neutron_sd_pb",legendStyle="rightBottom",drawConfig={"XaxisSetTitleOffset":1.2,"bottomMargin": 0.055, "rightBottom" : {"x1":0.6,"x2":1,"y1":0.2,"y2":0.34},})




pmssm_deltaEW = PMSSM(config=c)

pmssm_deltaEW.constraints.printAnalysisList()

pmssm_deltaEW.c.global_settings["logEps"] = 1e-13

pmssm_deltaEW.impact1D("deltaEW",drawConfig={"XaxisSetTitleOffset":1.2},xaxisDrawConfig={"1Dlogy":True})
pmssm_deltaEW.quantile1D_with_sigmaVariations("deltaEW",drawConfig={"legendFillWhite" : False})
pmssm_deltaEW.survivalProbability1D("deltaEW",drawConfig={"legendFillWhite" : False})