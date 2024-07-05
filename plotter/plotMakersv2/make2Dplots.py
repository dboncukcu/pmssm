import os
import sys
current_file_path = os.path.abspath(__file__)
parent_directory = os.path.dirname(os.path.dirname(current_file_path))
sys.path.append(parent_directory)


from ROOT import  *

from PlotterConfig import PlotterConfig
from Plotter import PMSSM


c = PlotterConfig()
c.global_settings["outputPath"] = "../../output/"
pmssm = PMSSM(config=c)

# pmssm.ZScorePlots()

## QUANTILE 2D

color_palette = (kRainBow,"kRainBow")

c_quantile = PlotterConfig()
c_quantile.global_settings["outputPath"] = f"../../output/quantile2D_99/"+color_palette[1]
pmssm_quantile = PMSSM(config=c_quantile)

pmssm_quantile.constraints.printAnalysisList()
pmssm_quantile.quantile2D("abs(chi10):tau1",quantile=0.99, legendStyle="leftTop",colorPallette=color_palette[0])
exit()
pmssm_quantile.quantile2D("abs(chi10):abs(chi1pm)",quantile=0.99, legendStyle="leftTop")
pmssm_quantile.quantile2D("abs(chi10):abs(chi2pm)",quantile=0.99, legendStyle="leftTop")
pmssm_quantile.quantile2D("abs(chi10):abs(chi20)",quantile=0.99, legendStyle="leftTop")
pmssm_quantile.quantile2D("abs(chi10):abs(chi30)",quantile=0.99, legendStyle="leftTop")
pmssm_quantile.quantile2D("abs(chi10):abs(chi40)",quantile=0.99, legendStyle="leftTop")
pmssm_quantile.quantile2D("abs(chi10):t1",quantile=0.99, legendStyle="leftTop")
pmssm_quantile.quantile2D("abs(chi10):b1",quantile=0.99, legendStyle="leftTop")
pmssm_quantile.quantile2D("abs(chi10):lcsp",quantile=0.99, legendStyle="leftTop")
pmssm_quantile.quantile2D("abs(chi10):g",quantile=0.99, legendStyle="leftTop")
pmssm_quantile.quantile2D("abs(chi10):Mq1",quantile=0.99, legendStyle="leftTop")
pmssm_quantile.quantile2D("abs(chi10):Md1",quantile=0.99, legendStyle="leftTop")
pmssm_quantile.quantile2D("abs(chi10):Ml1",quantile=0.99, legendStyle="leftTop")

# c_quantile_ewk = PlotterConfig()
# c_quantile_ewk.global_settings["outputPath"] = "../../output/quantile2D"
# c_quantile_ewk.global_settings["logEps"] = 0.02 # 20MeV
# pmssm_quantile_ewk = PMSSM(config=c_quantile_ewk)

# c_quantile_strong = PlotterConfig()
# c_quantile_strong.global_settings["outputPath"] = "../../output/quantile2D"
# c_quantile_strong.global_settings["logEps"] = 8 # 8GeV
# pmssm_quantile_strong = PMSSM(config=c_quantile_strong)

# pmssm_quantile_ewk.quantile2D("tau1-abs(chi10):abs(chi10)",quantile=0.50)
# pmssm_quantile_ewk.quantile2D("abs(chi1pm)-abs(chi10):abs(chi10)",quantile=0.50)
# pmssm_quantile_ewk.quantile2D("abs(chi2pm)-abs(chi10):abs(chi10)",quantile=0.50)
# pmssm_quantile_ewk.quantile2D("abs(chi20)-abs(chi10):abs(chi10)",quantile=0.50)
# pmssm_quantile_ewk.quantile2D("abs(chi30)-abs(chi10):abs(chi10)",quantile=0.50)
# pmssm_quantile_ewk.quantile2D("abs(chi40)-abs(chi10):abs(chi10)",quantile=0.50)
# pmssm_quantile_strong.quantile2D("t1-abs(chi10):abs(chi10)",quantile=0.50)
# pmssm_quantile_strong.quantile2D("b1-abs(chi10):abs(chi10)",quantile=0.50)
# pmssm_quantile_strong.quantile2D("lcsp-abs(chi10):abs(chi10)",quantile=0.50)
# pmssm_quantile_strong.quantile2D("g-abs(chi10):abs(chi10)",quantile=0.50)
# pmssm_quantile_strong.quantile2D("Mq1-abs(chi10):abs(chi10)",quantile=0.50)
# pmssm_quantile_strong.quantile2D("Md1-abs(chi10):abs(chi10)",quantile=0.50)
# pmssm_quantile_ewk.quantile2D("Ml1-abs(chi10):abs(chi10)",quantile=0.50)


## SURVIVAL 2D

# c_survival = PlotterConfig()
# c_survival.global_settings["outputPath"] = "../../output/survival2D"
# pmssm_survival = PMSSM(config=c_survival)

# pmssm_survival.constraints.printAnalysisList()
# pmssm_survival.survivalProbability2D("abs(chi10):tau1")
# pmssm_survival.survivalProbability2D("abs(chi10):abs(chi1pm)")
# pmssm_survival.survivalProbability2D("abs(chi10):abs(chi2pm)")
# pmssm_survival.survivalProbability2D("abs(chi10):abs(chi20)")
# pmssm_survival.survivalProbability2D("abs(chi10):abs(chi30)")
# pmssm_survival.survivalProbability2D("abs(chi10):abs(chi40)")
# pmssm_survival.survivalProbability2D("abs(chi10):t1")
# pmssm_survival.survivalProbability2D("abs(chi10):b1")
# pmssm_survival.survivalProbability2D("abs(chi10):lcsp")
# pmssm_survival.survivalProbability2D("abs(chi10):g")
# pmssm_survival.survivalProbability2D("abs(chi10):Mq1")
# pmssm_survival.survivalProbability2D("abs(chi10):Md1")
# pmssm_survival.survivalProbability2D("abs(chi10):Ml1")

# c_survival_ewk = PlotterConfig()
# c_survival_ewk.global_settings["outputPath"] = "../../output/survival2D"
# c_survival_ewk.global_settings["logEps"] = 0.02 # 20MeV
# pmssm_survival_ewk = PMSSM(config=c_survival_ewk)

# c_survival_strong = PlotterConfig()
# c_survival_strong.global_settings["outputPath"] = "../../output/survival2D"
# c_survival_strong.global_settings["logEps"] = 8 # 8GeV
# pmssm_survival_strong = PMSSM(config=c_survival_strong)

# pmssm_survival_ewk.survivalProbability2D("tau1-abs(chi10):abs(chi10)")
# pmssm_survival_ewk.survivalProbability2D("abs(chi1pm)-abs(chi10):abs(chi10)")
# pmssm_survival_ewk.survivalProbability2D("abs(chi2pm)-abs(chi10):abs(chi10)")
# pmssm_survival_ewk.survivalProbability2D("abs(chi20)-abs(chi10):abs(chi10)")
# pmssm_survival_ewk.survivalProbability2D("abs(chi30)-abs(chi10):abs(chi10)")
# pmssm_survival_ewk.survivalProbability2D("abs(chi40)-abs(chi10):abs(chi10)")
# pmssm_survival_strong.survivalProbability2D("t1-abs(chi10):abs(chi10)")
# pmssm_survival_strong.survivalProbability2D("b1-abs(chi10):abs(chi10)")
# pmssm_survival_strong.survivalProbability2D("lcsp-abs(chi10):abs(chi10)")
# pmssm_survival_strong.survivalProbability2D("g-abs(chi10):abs(chi10)")
# pmssm_survival_strong.survivalProbability2D("Mq1-abs(chi10):abs(chi10)")
# pmssm_survival_strong.survivalProbability2D("Md1-abs(chi10):abs(chi10)")
# pmssm_survival_ewk.survivalProbability2D("Ml1-abs(chi10):abs(chi10)")

