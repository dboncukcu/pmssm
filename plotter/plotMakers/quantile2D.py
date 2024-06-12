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
c.global_settings["outputPath"] = "../../output/quantile2D"



pmssm = PMSSM(config=c)

pmssm.constraints.printAnalysisList()


pmssm.quantile2D("abs(chi10):abs(chi1pm)",quantile=0.99)
pmssm.quantile2D("abs(chi10):abs(chi20)",quantile=0.99)
pmssm.quantile2D("abs(chi10):t1",quantile=0.99)
pmssm.quantile2D("abs(chi10):b1",quantile=0.99)
pmssm.quantile2D("abs(chi10):lcsp",quantile=0.99,legendStyle="leftBottom")
pmssm.quantile2D("lcsp:abs(chi10)",quantile=0.99,legendStyle="leftBottom")
pmssm.quantile2D("abs(chi10):g",quantile=0.99)
pmssm.quantile2D("abs(chi1pm)-abs(chi10):abs(chi10)",quantile=0.99)
pmssm.quantile2D("g-abs(chi10):abs(chi10)",quantile=0.99)
pmssm.quantile2D("t1-abs(chi10):abs(chi10)",quantile=0.99)
pmssm.quantile2D("b1-abs(chi10):abs(chi10)",quantile=0.99)
pmssm.quantile2D("lcsp-abs(chi10):abs(chi10)",quantile=0.99)
