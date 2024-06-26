from ROOT import  *

from PlotterConfig import PlotterConfig
from Plotter import PMSSM

c = PlotterConfig()
c.global_settings["outputFileFormat"] = "pdf"

pmssm = PMSSM(config=c)

pmssm.constraints.printAnalysisList()


pmssm.survivalProbability2D("abs(chi20):tanbeta")

# pmssm.relicDensity1D()

# pmssm.survivalProbability1D("abs(chi10)")
# pmssm.survivalProbability1D("abs(chi1pm)")
# pmssm.survivalProbability1D("abs(chi20)")
# pmssm.survivalProbability1D("g")
# pmssm.survivalProbability1D("t1")
# pmssm.survivalProbability1D("lcsp")

# pmssm.impact1D("g")
# pmssm.impact1D("abs(chi10)")
# pmssm.impact1D("abs(chi10)")
# pmssm.impact1D("abs(chi20)")
# pmssm.impact1D("abs(chi1pm)")
# pmssm.impact1D("lcsp")
# pmssm.impact1D("t1",drawConfig={"yMaxOffsett": 0.001},legendStyle="leftTop")



# pmssm.quantile1D("g",drawConfig={"yMaxOffsett": 0.1})
# pmssm.quantile1D("abs(chi10)",drawConfig={"yMaxOffsett": 0.1})
# pmssm.quantile1D("t1",drawConfig={"yMaxOffsett": 0.1})
# pmssm.quantile1D("abs(chi20)",drawConfig={"yMaxOffsett": 0.1})
# pmssm.quantile1D("abs(chi1pm)",drawConfig={"yMaxOffsett": 0.1})
# pmssm.quantile1D("lcsp",drawConfig={"yMaxOffsett": 0.1})


# pmssm.quantile2D("abs(chi10):abs(chi1pm)",quantile=0.99)
# pmssm.quantile2D("abs(chi10):abs(chi20)",quantile=0.99)
# pmssm.quantile2D("abs(chi10):t1",quantile=0.99)
# pmssm.quantile2D("abs(chi10):b1",quantile=0.99)
# pmssm.quantile2D("abs(chi10):lcsp",quantile=0.99)
# pmssm.quantile2D("abs(chi10):g",quantile=0.99)

# pmssm.survivalProbability2D("abs(chi10):abs(chi1pm)")
# pmssm.survivalProbability2D("abs(chi10):abs(chi20)")
# pmssm.survivalProbability2D("abs(chi10):t1")
# pmssm.survivalProbability2D("abs(chi10):b1")
# pmssm.survivalProbability2D("abs(chi10):lcsp")
# pmssm.survivalProbability2D("abs(chi10):g", showLegend=True)
# for analysis in pmssm.constraints.getAnalysisList():
#     pmssm.survivalProbability2D("abs(chi10):g",analysis=analysis)

 
# pmssm.quantile2D("abs(chi10):g",analysis="combined simplified",quantile=0.99) 
# pmssm.quantile2D("abs(chi10):g",analysis="combined",quantile=0.99) 


# pmssm.quantile2D("abs(chi10):g",analysis="cms_sus_20_001",quantile=0.99) 
# pmssm.quantile2D("abs(chi10):g",analysis="cms_sus_19_006",quantile=0.99) 
# pmssm.quantile2D("abs(chi10):g",analysis="cms_sus_21_006",quantile=0.99) 
# pmssm.quantile2D("abs(chi10):g",analysis="cms_sus_18_004",quantile=0.99) 
# pmssm.quantile2D("abs(chi10):g",analysis="cms_sus_18_004,cms_sus_21_006,cms_sus_19_006",quantile=0.99) 

# pmssm.impact1D("t1",legendStyle="leftTop")





# pmssm.impact1D("t1",analysis="combined simplified",legendStyle="leftTop")

# for analysis in pmssm.constraints.getAnalysisList():
#     pmssm.impact1D("t1",analysis=analysis,legendStyle="leftTop")




# pmssm.quantile2D("abs(chi10):abs(chi1pm)",quantile=0.99)
# pmssm.quantile2D("abs(chi10):abs(chi20)",quantile=0.99)
# pmssm.quantile2D("abs(chi10):t1",quantile=0.99)
# pmssm.quantile2D("abs(chi10):b1",quantile=0.99)
# pmssm.quantile2D("abs(chi10):lcsp",quantile=0.99,legendStyle="leftBottom")
# pmssm.quantile2D("abs(chi10):g",quantile=0.99)

# pmssm.quantile2D("abs(chi1pm)-abs(chi10):abs(chi10)",quantile=0.99)
# pmssm.quantile2D("g-abs(chi10):abs(chi10)",quantile=0.99)
# pmssm.quantile2D("t1-abs(chi10):abs(chi10)",quantile=0.99)
# pmssm.quantile2D("b1-abs(chi10):abs(chi10)",quantile=0.99)
# pmssm.quantile2D("lcsp-abs(chi10):abs(chi10)",quantile=0.99)
# pmssm.quantile2D("abs(chi20-chi10):abs(chi10)",quantile=0.99)

