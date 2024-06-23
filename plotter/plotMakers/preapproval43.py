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
c.global_settings["outputPath"] = "/afs/cern.ch/user/d/dboncukc/pmssm/output/preapproval"


pmssm = PMSSM(config=c)
pmssm.c.global_settings["logEps"] = 1e-13
pmssm.constraints.printAnalysisList()


# pmssm.impact1D("deltaEW",
#                legendStyle="rightBottom",
#                drawConfig={"XaxisSetTitleOffset":1.2,"rightMargin":0.03,"rightBottom":{"x1":0.46,"x2":0.89,"y1":0.17,"y2":0.4},
#                            "yMaxOffsett":1},
#                )
# pmssm.quantile1D("deltaEW",xaxisDrawConfig={"1Dlogy":False},legendStyle="leftTop",drawConfig={"legendFillWhite" : False,"XaxisSetTitleOffset":1.15})
# pmssm.survivalProbability1D("deltaEW",xaxisDrawConfig={"1Dlogy":False},drawConfig={"legendFillWhite" : False})

pmssm.c.global_settings["logEps"] = 1e-7

# pmssm.impact1D("Omegah2",
#                legendStyle="rightBottom",
#                drawConfig={"XaxisSetTitleOffset":1.2,
#                            "yMaxOffsett":1,
#                            "rightMargin":0.03,
#                            "rightBottom" : {"x1":0.43,"x2":0.84,"y1":0.18,"y2":0.41}},xaxisDrawConfig={"1Dlogy":True})
# pmssm.quantile1D("Omegah2",xaxisDrawConfig={"1Dlogy":False},legendStyle="rightBottom",
#                  drawConfig={"legendFillWhite" : False,"rightBottom" : {"x1":0.47,"x2":0.8,"y1":0.17,"y2":0.4},"yMaxOffsett":0.1})
# pmssm.survivalProbability1D("Omegah2",xaxisDrawConfig={"1Dlogy":False},drawConfig={"legendFillWhite" : False})


pmssm.impact1D("cdm_xsec_neutron_si_pb",legendStyle="leftTop",drawConfig={"yMaxOffsett":0.055,"bottomMargin":0.055,"rightMargin":0.01,"XaxisSetTitleOffset":1.2})
pmssm.quantile1D("cdm_xsec_neutron_si_pb",legendStyle="rightTop",drawConfig={"XaxisSetTitleOffset":1.2,"bottomMargin": 0.055,"yMaxOffsett":0.7,"legendFillWhite":False})
pmssm.survivalProbability1D("cdm_xsec_neutron_si_pb",legendStyle="leftBottom",drawConfig={"XaxisSetTitleOffset":1.2,"bottomMargin": 0.055})

pmssm.impact1D("cdm_xsec_neutron_sd_pb",legendStyle="leftBottom",drawConfig={"bottomMargin":0.055,"rightMargin":0.01,"XaxisSetTitleOffset":1.2,"leftBottom" : {"x1":0.23,"x2":0.53,"y1":0.2,"y2":0.42},})
pmssm.quantile1D("cdm_xsec_neutron_sd_pb",legendStyle="rightTop",drawConfig={"XaxisSetTitleOffset":1.2,"bottomMargin": 0.055})
pmssm.survivalProbability1D("cdm_xsec_neutron_sd_pb",legendStyle="rightBottom",drawConfig={"XaxisSetTitleOffset":1.2,"bottomMargin": 0.055})
