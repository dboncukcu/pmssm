import os
import sys
current_file_path = os.path.abspath(__file__)
parent_directory = os.path.dirname(os.path.dirname(current_file_path))
sys.path.append(parent_directory)
from ROOT import  *
from PlotterConfig import PlotterConfig
from Plotter import PMSSM

variantName = sys.argv[1]

# variantName = "NoCut"
# variantName = "DM"
# variantName = "DeltaEW"
# variantName = "DM_DeltaEW"


# dmcuts= (["Omegah2<=0.132","abs(dd_exclusion_pval)>=0.05"],["#Omega_{h^2}<1.1#dot#Omega_{h^2}^{Planck}","DD p-value>=0.05"])
dmcuts= (["Omegah2<=0.132","abs(dd_exclusion_pval_withlz)>=0.05"],["#Omega_{h^2}<1.1#dot#Omega_{h^2}^{Planck}","DD p-value>=0.05"])
deltaewcut = (["deltaEW<200"],"#Delta_{EW}<200")


if variantName == "NoCut":
    denum_constraint = []
elif variantName == "DM":
    denum_constraint = dmcuts[0]
elif variantName == "DeltaEW":
    denum_constraint = deltaewcut[0]
elif variantName == "DM_DeltaEW":
    denum_constraint = dmcuts[0] + deltaewcut[0]
    
if variantName == "NoCut":
    legend_constraints = None
elif variantName == "DM":
    legend_constraints = (dmcuts[1][0],dmcuts[1][1])
elif variantName == "DeltaEW":
    legend_constraints = (deltaewcut[1])
elif variantName == "DM_DeltaEW":
    legend_constraints = (dmcuts[1][0],dmcuts[1][1],deltaewcut[1]) 

legend_constraints = None
# outputPath = "../../output/survival2D/"+variantName+"/"
outputPath = "../../output/survival2D_NEW/"+variantName+"/"


c_survival_ewk = PlotterConfig()
c_survival_ewk.global_settings["outputPath"] = outputPath
c_survival_ewk.global_settings["logEps"] = 0.02 # 20MeV
c_survival_ewk.particleConfig["abs(chi10)"] = {
    "title" : "m_{#tilde{#chi}^{0}_{1}}",
    "bins" : 50,
    "min" : 0,
    "max" : 1900,
    "Ndivisions" : 506,
    "logScale" : False,
    "linearScale": 1000.0,
    "unit": "TeV",
    "name" : "chi10"
}

pmssm_survival_ewk = PMSSM(config=c_survival_ewk)

c_survival_strong = PlotterConfig()
c_survival_strong.global_settings["outputPath"] = outputPath
c_survival_strong.global_settings["logEps"] = 8 # 8GeV
c_survival_strong.particleConfig["abs(chi10)"] = {
    "title" : "m_{#tilde{#chi}^{0}_{1}}",
    "bins" : 50,
    "min" : 0,
    "max" : 1900,
    "Ndivisions" : 506,
    "logScale" : False,
    "linearScale": 1000.0,
    "unit": "TeV",
    "name" : "chi10"
}

pmssm_survival_strong = PMSSM(config=c_survival_strong)


pmssm_survival_strong.survivalProbability2D("lcsp-abs(chi10):abs(chi10)", moreconstraints_prior = denum_constraint, moreconstraints= denum_constraint,customName = variantName, drawConfig={"XaxisSetTitleOffset": 1.15, "YaxisSetTitleOffset" : 1.33,"bottomMargin":0.045},constraints=legend_constraints,contourFix2ndWay=True)

exit()
# pmssm_survival_ewk.testPlots()
pmssm_survival_ewk.survivalProbability2D("abs(chi1pm)-abs(chi10):abs(chi10)", moreconstraints_prior = denum_constraint, moreconstraints= denum_constraint,customName = variantName, drawConfig={"XaxisSetTitleOffset": 1.15, "YaxisSetTitleOffset" : 1.33,"bottomMargin":0.045},constraints=legend_constraints,contourFix2ndWay=True)
pmssm_survival_strong.survivalProbability2D("lcsp-abs(chi10):abs(chi10)", moreconstraints_prior = denum_constraint, moreconstraints= denum_constraint,customName = variantName, drawConfig={"XaxisSetTitleOffset": 1.15, "YaxisSetTitleOffset" : 1.33,"bottomMargin":0.045},constraints=legend_constraints,contourFix2ndWay=True)
pmssm_survival_ewk.survivalProbability2D("tau1-abs(chi10):abs(chi10)", moreconstraints_prior = denum_constraint, moreconstraints= denum_constraint,customName = variantName, drawConfig={"XaxisSetTitleOffset": 1.15, "YaxisSetTitleOffset" : 1.33,"bottomMargin":0.045},constraints=legend_constraints,contourFix2ndWay=True)
pmssm_survival_ewk.survivalProbability2D("abs(chi1pm)-abs(chi10):abs(chi10)", moreconstraints_prior = denum_constraint, moreconstraints= denum_constraint,customName = variantName, drawConfig={"XaxisSetTitleOffset": 1.15, "YaxisSetTitleOffset" : 1.33,"bottomMargin":0.045},constraints=legend_constraints,contourFix2ndWay=True)
pmssm_survival_ewk.survivalProbability2D("abs(chi2pm)-abs(chi10):abs(chi10)", moreconstraints_prior = denum_constraint, moreconstraints= denum_constraint,customName = variantName, drawConfig={"XaxisSetTitleOffset": 1.15, "YaxisSetTitleOffset" : 1.33,"bottomMargin":0.045},constraints=legend_constraints,contourFix2ndWay=True)
pmssm_survival_ewk.survivalProbability2D("abs(chi20)-abs(chi10):abs(chi10)", moreconstraints_prior = denum_constraint, moreconstraints= denum_constraint,customName = variantName, drawConfig={"XaxisSetTitleOffset": 1.15, "YaxisSetTitleOffset" : 1.33,"bottomMargin":0.045},constraints=legend_constraints,contourFix2ndWay=True)
pmssm_survival_ewk.survivalProbability2D("abs(chi30)-abs(chi10):abs(chi10)", moreconstraints_prior = denum_constraint, moreconstraints= denum_constraint,customName = variantName, drawConfig={"XaxisSetTitleOffset": 1.15, "YaxisSetTitleOffset" : 1.33,"bottomMargin":0.045},constraints=legend_constraints,contourFix2ndWay=True)
pmssm_survival_ewk.survivalProbability2D("abs(chi40)-abs(chi10):abs(chi10)", moreconstraints_prior = denum_constraint, moreconstraints= denum_constraint,customName = variantName, drawConfig={"XaxisSetTitleOffset": 1.15, "YaxisSetTitleOffset" : 1.33,"bottomMargin":0.045},constraints=legend_constraints,contourFix2ndWay=True)
pmssm_survival_strong.survivalProbability2D("t1-abs(chi10):abs(chi10)", moreconstraints_prior = denum_constraint, moreconstraints= denum_constraint,customName = variantName, drawConfig={"XaxisSetTitleOffset": 1.15, "YaxisSetTitleOffset" : 1.33,"bottomMargin":0.045},constraints=legend_constraints,contourFix2ndWay=True)
pmssm_survival_strong.survivalProbability2D("b1-abs(chi10):abs(chi10)", moreconstraints_prior = denum_constraint, moreconstraints= denum_constraint,customName = variantName, drawConfig={"XaxisSetTitleOffset": 1.15, "YaxisSetTitleOffset" : 1.33,"bottomMargin":0.045},constraints=legend_constraints,contourFix2ndWay=True)
pmssm_survival_strong.survivalProbability2D("lcsp-abs(chi10):abs(chi10)", moreconstraints_prior = denum_constraint, moreconstraints= denum_constraint,customName = variantName, drawConfig={"XaxisSetTitleOffset": 1.15, "YaxisSetTitleOffset" : 1.33,"bottomMargin":0.045},constraints=legend_constraints,contourFix2ndWay=True)
pmssm_survival_strong.survivalProbability2D("g-abs(chi10):abs(chi10)", moreconstraints_prior = denum_constraint, moreconstraints= denum_constraint,customName = variantName, drawConfig={"XaxisSetTitleOffset": 1.15, "YaxisSetTitleOffset" : 1.33,"bottomMargin":0.045},constraints=legend_constraints,contourFix2ndWay=True)
pmssm_survival_strong.survivalProbability2D("Mq1-abs(chi10):abs(chi10)", moreconstraints_prior = denum_constraint, moreconstraints= denum_constraint,customName = variantName, drawConfig={"XaxisSetTitleOffset": 1.15, "YaxisSetTitleOffset" : 1.33,"bottomMargin":0.045},constraints=legend_constraints,contourFix2ndWay=True)
pmssm_survival_strong.survivalProbability2D("Md1-abs(chi10):abs(chi10)", moreconstraints_prior = denum_constraint, moreconstraints= denum_constraint,customName = variantName, drawConfig={"XaxisSetTitleOffset": 1.15, "YaxisSetTitleOffset" : 1.33,"bottomMargin":0.045},constraints=legend_constraints,contourFix2ndWay=True)
pmssm_survival_ewk.survivalProbability2D("Ml1-abs(chi10):abs(chi10)", moreconstraints_prior = denum_constraint, moreconstraints= denum_constraint,customName = variantName, drawConfig={"XaxisSetTitleOffset": 1.15, "YaxisSetTitleOffset" : 1.33,"bottomMargin":0.045},constraints=legend_constraints,contourFix2ndWay=True)

