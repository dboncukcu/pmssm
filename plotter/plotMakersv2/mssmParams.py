import os
import sys
current_file_path = os.path.abspath(__file__)
parent_directory = os.path.dirname(os.path.dirname(current_file_path))
sys.path.append(parent_directory)

variantName = sys.argv[1]
print("variant Name: ", variantName)
# variantName = "NoCut"
# variantName = "DM"
# variantName = "DeltaEW"
# variantName = "DM_DeltaEW"

# dmcuts= (["Omegah2<=0.132","dd_exclusion_pval>=0.05"],"#Omega_{h}^{2}<=0.132 & p-value>=0.05")
dmcuts= (["Omegah2<=0.132","abs(dd_exclusion_pval_withlz)>=0.05"],"#Omega_{h}^{2}<=0.132 & p-value>=0.05")
deltaewcut = (["deltaEW<=200"],"#DeltaEW<=200")

if variantName == "NoCut":
    denum_constraint = []
elif variantName == "DM":
    denum_constraint = dmcuts[0]
elif variantName == "DeltaEW":
    denum_constraint = deltaewcut[0]
elif variantName == "DM_DeltaEW":
    denum_constraint = dmcuts[0] + deltaewcut[0]

from ROOT import  *

from PlotterConfig import PlotterConfig
from Plotter import PMSSM
mssmParamsConfig = {
    "default" : {
        "title" : "No Particle Found",
        "bins" : 50,
        "min" : -1,
        "max" : 1,
        "logScale" : False,
        "1Dlogy" : False,
        "linearScale": 1.0,
        "unit": "",
        "name" : "NoParticleFound"
        },
    "M1" : {
        "title" : "M_{1}",
        "bins" : 50,
        "min" : -2000,
        "max" : 2000,
        "logScale" : False,
        "1Dlogy" : False,
        "linearScale": 1000.0,
        "unit": "TeV",
        "name" : "M1"
        },
    "M2" : {
        "title" : "M_{2}",
        "bins" : 50,
        "min" : -2000,
        "max" : 2000,
        "logScale" : False,
        "1Dlogy" : False,
        "linearScale": 1000.0,
        "unit": "TeV",
        "name" : "M2"
        },
    "tanbeta" : {
        "title" : "tan#beta",
        "bins" : 50,
        "min" : 2,
        "max" : 60,
        "logScale" : False,
        "1Dlogy" : False,
        "linearScale": 1.0,
        "unit": "",
        "name" : "tanbeta"
        },
    "mu" : {
        "title" : "#mu",
        "bins" : 50,
        "min" : -2000,
        "max" : 2000,
        "logScale" : False,
        "1Dlogy" : False,
        "linearScale": 1000.0,
        "unit": "TeV",
        "name" : "mu"
        },
    "At" : {
        "title" : "A_{t}",
        "bins" : 50,
        "min" : -7000,
        "max" : 7000,
        "logScale" : False,
        "1Dlogy" : False,
        "linearScale": 1000.0,
        "unit": "TeV",
        "name" : "At"
        },
    "Ab" : {
        "title" : "A_{b}",
        "bins" : 50,
        "min" : -7000,
        "max" : 7000,
        "logScale" : False,
        "1Dlogy" : False,
        "linearScale": 1000.0,
        "unit": "TeV",
        "name" : "Ab"
        },
    "t1" : {
        "title": "m_{#tilde{t}_{1}}",
        "bins" : 100,
        "min" : 50,
        "max" : 4000,
        "logScale": False,
        "linearScale": 1000.0,
        "unit": "TeV",
        "name": "stop1"    
        },
    "mA" : {
        "title" : "m_{A}",
        "bins" : 50,
        "min" : 0,
        "max" : 2000,
        "Ndivisions" : 506,
        "logScale" : False,
        "1Dlogy" : False,
        "linearScale": 1000.0,
        "unit": "TeV",
        "name" : "mA"
        },
    "A_tau" : {
        "title" : "A_{#tau}",
        "bins" : 50,
        "min" : -7000,
        "max" : 7000,
        "logScale" : False,
        "1Dlogy" : False,
        "linearScale": 1000.0,
        "unit": "TeV",
        "name" : "Atau"
        },
    "tau1" : {
        "title": "m_{#tilde{#tau}}",
        "bins" : 100,
        "min" : 0,
        "max" : 2300,
        "logScale": False,
        "linearScale": 1000.0,
        "Ndivisions": 506,
        "unit": "TeV",
        "name": "stau"
        },
    "M3" : {
        "title" : "M_{3}",
        "bins" : 50,
        "min" : 0,
        "max" : 8000,
        "logScale" : False,
        "1Dlogy" : False,
        "linearScale": 1000.0,
        "unit": "TeV",
        "name" : "M3"
        },
    "Mq3" : {
            "title" : "m_{#tilde{q}_{3}}",
            "bins" : 50,
            "min" : 0,
            "max" : 7000,
            "logScale" : False,
            "1Dlogy" : False,
            "linearScale": 1000.0,
            "unit": "TeV",
            "name" : "Mq3"
            },
    "b1" :  {
                "title": "m_{#tilde{b}_{1}}",
                "bins" : 100,
                "min" : 50,
                "max" : 7000,
                "logScale": False,
                "linearScale": 1000.0,
                "unit": "TeV",
                "name": "sbottom"
                },
}
c = PlotterConfig()
c.global_settings["outputPath"] = "../../output/pmssmParams/"+variantName+"/"
c.particleConfig = mssmParamsConfig
pmssm = PMSSM(config=c)


#1
pmssm.survivalProbability2D("M1:M2",moreconstraints_prior = denum_constraint, moreconstraints= denum_constraint,customName = variantName)

#2
pmssm.survivalProbability2D("tanbeta:mu",moreconstraints_prior = denum_constraint, moreconstraints= denum_constraint,customName = variantName)

#3
pmssm.survivalProbability2D("At:t1",moreconstraints_prior = denum_constraint, moreconstraints= denum_constraint,customName = variantName)

#4
pmssm.survivalProbability2D("mA:tanbeta",moreconstraints_prior = denum_constraint, moreconstraints= denum_constraint,customName = variantName)

#5
pmssm.survivalProbability2D("M1:mu",moreconstraints_prior = denum_constraint, moreconstraints= denum_constraint,customName = variantName)

#6
pmssm.survivalProbability2D("A_tau:tau1",moreconstraints_prior = denum_constraint, moreconstraints= denum_constraint,customName = variantName)

#7
pmssm.survivalProbability2D("M3:Mq3",moreconstraints_prior = denum_constraint, moreconstraints= denum_constraint,customName = variantName)

#8
pmssm.survivalProbability2D("mu:mA",moreconstraints_prior = denum_constraint, moreconstraints= denum_constraint,customName = variantName)

#9
pmssm.survivalProbability2D("mu:t1",moreconstraints_prior = denum_constraint, moreconstraints= denum_constraint,customName = variantName)

#10
pmssm.survivalProbability2D("mu:M2",moreconstraints_prior = denum_constraint, moreconstraints= denum_constraint,customName = variantName)

#11
pmssm.survivalProbability2D("Ab:b1",moreconstraints_prior = denum_constraint, moreconstraints= denum_constraint,customName = variantName)

#12
pmssm.survivalProbability2D("tanbeta:M3",moreconstraints_prior = denum_constraint, moreconstraints= denum_constraint,customName = variantName)

#13
pmssm.survivalProbability2D("tanbeta:M2",moreconstraints_prior = denum_constraint, moreconstraints= denum_constraint,customName = variantName)