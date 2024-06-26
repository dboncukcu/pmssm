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
c.global_settings["outputPath"] = "../../output/survival2D"



pmssm = PMSSM(config=c)

pmssm.constraints.printAnalysisList()

pmssm.survivalProbability2D("abs(chi10):abs(chi20)",showLegend=True,legendStyle="leftTop")
exit()
pmssm.survivalProbability2D("abs(chi10):abs(chi1pm)")
pmssm.survivalProbability2D("abs(chi1pm):abs(chi10)")
pmssm.survivalProbability2D("abs(chi10):g")
pmssm.survivalProbability2D("abs(chi10):t1")
pmssm.survivalProbability2D("abs(chi10):b1")
pmssm.survivalProbability2D("abs(chi10):lcsp")


pmssm.survivalProbability2D("abs(chi20)-abs(chi10):abs(chi10)",showLegend=True,legendStyle="rightBottom")
pmssm.survivalProbability2D("abs(chi1pm)-abs(chi10):abs(chi10)")
pmssm.survivalProbability2D("g-abs(chi10):abs(chi10)")
pmssm.survivalProbability2D("t1-abs(chi10):abs(chi10)")
pmssm.survivalProbability2D("b1-abs(chi10):abs(chi10)")
pmssm.survivalProbability2D("lcsp-abs(chi10):abs(chi10)")