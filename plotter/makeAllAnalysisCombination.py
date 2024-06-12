from ROOT import *

from PlotterConfig import PlotterConfig 
from Plotter import PMSSM

c = PlotterConfig()
c.global_settings["outputFileFormat"] = "pdf"
c.global_settings["outputPath"] = "/eos/user/d/dboncukc/pMSSM/allAnalysis"

pmssm = PMSSM(config=c)

pmssm.constraints.printAnalysisList()


from itertools import combinations

def generate_combinations(analysisList):
    result = []
    
    # Tüm kombinasyonları oluştur
    for i in range(1, len(analysisList) + 1):
        combos = combinations(analysisList, i)
        for combo in combos:
            result.append(",".join(combo))
    
    return result

# Örnek kullanım
analysisList = pmssm.constraints.getAnalysisList()

combinations_list = generate_combinations(analysisList)


for i,analysis_combination in enumerate(combinations_list):
    print(f"{i}/{len(combinations_list)}: " + 25*"_"+analysis_combination+25*"_")
    c = PlotterConfig()
    c.global_settings["outputFileFormat"] = "pdf"
    c.global_settings["outputPath"] = "/eos/user/d/dboncukc/pMSSM/allAnalysis/"+ analysis_combination.replace(",", "_") + "/"
    pmssm = PMSSM(config=c)
    print("impact1D")
    pmssm.impact1D("g", analysis=analysis_combination)
    pmssm.impact1D("abs(chi10)",drawConfig={"yMaxOffsett": 0.0035},legendStyle="rightTop", analysis=analysis_combination)
    pmssm.impact1D("abs(chi20)", analysis=analysis_combination)
    pmssm.impact1D("abs(chi1pm)",drawConfig={"yMaxOffsett": 0.0035},legendStyle="rightTop", analysis=analysis_combination)
    pmssm.impact1D("lcsp",drawConfig={"yMaxOffsett": 0.0035},legendStyle="rightTop", analysis=analysis_combination)
    pmssm.impact1D("t1",drawConfig={"yMaxOffsett": 0.001},legendStyle="leftTop", analysis=analysis_combination)
    
    print("quantile1D")
    pmssm.quantile1D("abs(chi10)",drawConfig={"yMaxOffsett": 0.65},legendStyle="rightTop", analysis=analysis_combination)
    pmssm.quantile1D("abs(chi1pm)",legendStyle="rightBottom", analysis=analysis_combination)
    pmssm.quantile1D("abs(chi20)",drawConfig={"yMaxOffsett": 0.035},legendStyle="rightBottom", analysis=analysis_combination)
    pmssm.quantile1D("g",drawConfig={"yMaxOffsett": 0.65},legendStyle="leftTop", analysis=analysis_combination)
    pmssm.quantile1D("t1",drawConfig={"yMaxOffsett": 0.65},legendStyle="rightTop", analysis=analysis_combination)
    pmssm.quantile1D("lcsp",drawConfig={"yMaxOffsett": 0.2}, analysis=analysis_combination)
    pmssm.quantile1D("b1")
    
    print("quantile2D")
    pmssm.quantile2D("abs(chi10):abs(chi1pm)",quantile=0.99, analysis=analysis_combination)
    pmssm.quantile2D("abs(chi10):abs(chi20)",quantile=0.99, analysis=analysis_combination)
    pmssm.quantile2D("abs(chi10):t1",quantile=0.99, analysis=analysis_combination)
    pmssm.quantile2D("abs(chi10):b1",quantile=0.99, analysis=analysis_combination)
    pmssm.quantile2D("abs(chi10):lcsp",quantile=0.99,legendStyle="leftBottom", analysis=analysis_combination)
    pmssm.quantile2D("lcsp:abs(chi10)",quantile=0.99,legendStyle="leftBottom", analysis=analysis_combination)
    pmssm.quantile2D("abs(chi10):g",quantile=0.99, analysis=analysis_combination)
    
    pmssm.quantile2D("abs(chi1pm)-abs(chi10):abs(chi10)",quantile=0.99, analysis=analysis_combination)
    pmssm.quantile2D("abs(chi20)-abs(chi10):abs(chi10)",quantile=0.99, analysis=analysis_combination)
    pmssm.quantile2D("g-abs(chi10):abs(chi10)",quantile=0.99, analysis=analysis_combination)
    pmssm.quantile2D("t1-abs(chi10):abs(chi10)",quantile=0.99, analysis=analysis_combination)
    pmssm.quantile2D("b1-abs(chi10):abs(chi10)",quantile=0.99, analysis=analysis_combination)
    pmssm.quantile2D("lcsp-abs(chi10):abs(chi10)",quantile=0.99, analysis=analysis_combination)

    print("survaival1D")
    pmssm.survivalProbability1D("abs(chi10)", analysis=analysis_combination)
    pmssm.survivalProbability1D("abs(chi1pm)", analysis=analysis_combination)
    pmssm.survivalProbability1D("abs(chi20)", analysis=analysis_combination)
    pmssm.survivalProbability1D("g", analysis=analysis_combination)
    pmssm.survivalProbability1D("t1", analysis=analysis_combination)
    pmssm.survivalProbability1D("lcsp", analysis=analysis_combination)
    
    print("survaival2D")
    pmssm.survivalProbability2D("abs(chi10):abs(chi20)",showLegend=True,legendStyle="leftTop", analysis=analysis_combination)
    pmssm.survivalProbability2D("abs(chi10):abs(chi1pm)", analysis=analysis_combination)
    pmssm.survivalProbability2D("abs(chi1pm):abs(chi10)", analysis=analysis_combination)
    pmssm.survivalProbability2D("abs(chi10):g", analysis=analysis_combination)
    pmssm.survivalProbability2D("abs(chi10):t1", analysis=analysis_combination)
    pmssm.survivalProbability2D("abs(chi10):b1", analysis=analysis_combination)
    pmssm.survivalProbability2D("abs(chi10):lcsp", analysis=analysis_combination)


    pmssm.survivalProbability2D("abs(chi20)-abs(chi10):abs(chi10)",showLegend=True,legendStyle="rightBottom", analysis=analysis_combination)
    pmssm.survivalProbability2D("abs(chi1pm)-abs(chi10):abs(chi10)", analysis=analysis_combination)
    pmssm.survivalProbability2D("g-abs(chi10):abs(chi10)", analysis=analysis_combination)
    pmssm.survivalProbability2D("t1-abs(chi10):abs(chi10)", analysis=analysis_combination)
    pmssm.survivalProbability2D("b1-abs(chi10):abs(chi10)", analysis=analysis_combination)
    pmssm.survivalProbability2D("lcsp-abs(chi10):abs(chi10)", analysis=analysis_combination)
    
    del pmssm
    del c
print("..::Finished::..")