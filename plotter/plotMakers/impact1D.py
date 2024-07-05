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
c.global_settings["outputPath"] = "../../output/impact1D_newcolors"



pmssm = PMSSM(config=c)

pmssm.constraints.printAnalysisList()



pmssm.impact1D("abs(chi10)",legendStyle="rightTop")
pmssm.impact1D("abs(chi1pm)")
pmssm.impact1D("abs(chi20)")
pmssm.impact1D("t1", legendStyle="leftTop")
pmssm.impact1D("b1")
pmssm.impact1D("lcsp",legendStyle="rightTop")
pmssm.impact1D("g")
