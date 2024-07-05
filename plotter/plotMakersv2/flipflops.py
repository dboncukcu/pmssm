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

mainPath = "/afs/cern.ch/user/d/dboncukc/pmssm/output/preapproval"


contourFix2ndWay = False

for par in ["abs(chi1pm)-abs(chi10)","g-abs(chi10)","t1-abs(chi10)","b1-abs(chi10)","lcsp-abs(chi10)","abs(chi20)-abs(chi10)"]:
    c.global_settings["outputPath"] = "/afs/cern.ch/user/a/agungord/pmssm/output/"+ c.particleConfig[par]["name"]
    pmssm_flipbook = PMSSM(config=c)
    pmssm_flipbook.c.particleConfig["abs(chi10)"]["min"] = 0
    pmssm_flipbook.c.particleConfig["abs(chi10)"]["max"] = 1400
    pmssm_flipbook.c.particleConfig["abs(chi10)"]["Ndivisions"] = 507
    pmssm_flipbook.c.particleConfig["abs(chi1pm)-abs(chi10)"]["min"] = 0.02
    pmssm_flipbook.survivalProbability2D(f"{par}:abs(chi10)", analysis="cms_sus_18_004",customName="_1",legendAddition="SUS-18-004",contourFix2ndWay=contourFix2ndWay)
    pmssm_flipbook.survivalProbability2D(f"{par}:abs(chi10)", analysis="cms_sus_18_004,cms_sus_20_001",customName="_2",legendAddition="+ SUS-20-001",contourFix2ndWay=contourFix2ndWay)
    pmssm_flipbook.survivalProbability2D(f"{par}:abs(chi10)", analysis="cms_sus_18_004,cms_sus_20_001,cms_sus_21_007,cms_sus_21_007_mb",customName="_3",legendAddition="+ SUS-21-007",contourFix2ndWay=contourFix2ndWay)
    pmssm_flipbook.survivalProbability2D(f"{par}:abs(chi10)", analysis="cms_sus_18_004,cms_sus_20_001,cms_sus_21_007,cms_sus_21_007_mb,cms_sus_21_006",customName="_4",legendAddition="+ SUS-21-006",contourFix2ndWay=contourFix2ndWay)
    pmssm_flipbook.survivalProbability2D(f"{par}:abs(chi10)", analysis="combined",customName="_5",legendAddition="+ SUS-19-006",contourFix2ndWay=contourFix2ndWay)
    pmssm_flipbook.survivalProbability2D(
        f"{par}:abs(chi10)", 
        analysis="combined",
        moreconstraints=["Omegah2<=0.132"],  customName="_6",legendAddition="+ DM relic density",contourFix2ndWay=contourFix2ndWay)
    pmssm_flipbook.survivalProbability2D(
        f"{par}:abs(chi10)", 
        analysis="combined",
        moreconstraints=["Omegah2<=0.132","abs(dd_exclusion_pval_withlz)>=0.05"],customName="_7", legendAddition="+DM direct detection",contourFix2ndWay=contourFix2ndWay)
       
    pmssm_flipbook.survivalProbability2D(
        f"{par}:abs(chi10)", 
        analysis="combined",
        moreconstraints=["Omegah2<=0.132","abs(dd_exclusion_pval_withlz)>=0.05","deltaEW<=500"],customName="_8",
        legendAddition="+ #Delta_{EW}<200",contourFix2ndWay=contourFix2ndWay)
    del pmssm_flipbook


