import os
import sys
current_file_path = os.path.abspath(__file__)
parent_directory = os.path.dirname(os.path.dirname(current_file_path))
sys.path.append(parent_directory)
from ROOT import  *
from PlotterConfig import PlotterConfig
from Plotter import PMSSM


# variantName = "NoCut"
# variantName = "DM"
# variantName = "DeltaEW"
# variantName = "DM_DeltaEW"


deltaewcut = (["Omegah2<=0.132","dd_exclusion_pval>=0.05"],"#Omega_{h}^{2}<=0.132 & p-value>=0.05")
dmcuts = (["deltaEW<=200"],"#DeltaEW<=200")


if variantName == "NoCut":
    denum_constraint = []
elif variantName == "DM":
    denum_constraint = [dmcuts[0]]
elif variantName == "DeltaEW":
    denum_constraint = [deltaewcut[0]]
elif variantName == "DM_DeltaEW":
    denum_constraint = dmcuts[0] + deltaewcut[0]


outputPath = "../../output/survival2D/"+variantName+"/"


c_survival_ewk = PlotterConfig()
c_survival_ewk.global_settings["outputPath"] = outputPath
c_survival_ewk.global_settings["logEps"] = 0.02 # 20MeV
pmssm_survival_ewk = PMSSM(config=c_survival_ewk)

c_survival_strong = PlotterConfig()
c_survival_strong.global_settings["outputPath"] = outputPath
c_survival_strong.global_settings["logEps"] = 8 # 8GeV
pmssm_survival_strong = PMSSM(config=c_survival_strong)

pmssm_survival_ewk.survivalProbability2D("tau1-abs(chi10):abs(chi10)", moreconstraints_prior = denum_constraint, moreconstraints= denum_constraint,customName = variantName)
pmssm_survival_ewk.survivalProbability2D("abs(chi1pm)-abs(chi10):abs(chi10)", moreconstraints_prior = denum_constraint, moreconstraints= denum_constraint,customName = variantName)
pmssm_survival_ewk.survivalProbability2D("abs(chi2pm)-abs(chi10):abs(chi10)", moreconstraints_prior = denum_constraint, moreconstraints= denum_constraint,customName = variantName)
pmssm_survival_ewk.survivalProbability2D("abs(chi20)-abs(chi10):abs(chi10)", moreconstraints_prior = denum_constraint, moreconstraints= denum_constraint,customName = variantName)
pmssm_survival_ewk.survivalProbability2D("abs(chi30)-abs(chi10):abs(chi10)", moreconstraints_prior = denum_constraint, moreconstraints= denum_constraint,customName = variantName)
pmssm_survival_ewk.survivalProbability2D("abs(chi40)-abs(chi10):abs(chi10)", moreconstraints_prior = denum_constraint, moreconstraints= denum_constraint,customName = variantName)
pmssm_survival_strong.survivalProbability2D("t1-abs(chi10):abs(chi10)", moreconstraints_prior = denum_constraint, moreconstraints= denum_constraint,customName = variantName)
pmssm_survival_strong.survivalProbability2D("b1-abs(chi10):abs(chi10)", moreconstraints_prior = denum_constraint, moreconstraints= denum_constraint,customName = variantName)
pmssm_survival_strong.survivalProbability2D("lcsp-abs(chi10):abs(chi10)", moreconstraints_prior = denum_constraint, moreconstraints= denum_constraint,customName = variantName)
pmssm_survival_strong.survivalProbability2D("g-abs(chi10):abs(chi10)", moreconstraints_prior = denum_constraint, moreconstraints= denum_constraint,customName = variantName)
pmssm_survival_strong.survivalProbability2D("Mq1-abs(chi10):abs(chi10)", moreconstraints_prior = denum_constraint, moreconstraints= denum_constraint,customName = variantName)
pmssm_survival_strong.survivalProbability2D("Md1-abs(chi10):abs(chi10)", moreconstraints_prior = denum_constraint, moreconstraints= denum_constraint,customName = variantName)
pmssm_survival_ewk.survivalProbability2D("Ml1-abs(chi10):abs(chi10)", moreconstraints_prior = denum_constraint, moreconstraints= denum_constraint,customName = variantName)

