from ROOT import *
from pmssm import PMSSM, particleDrawConfig_TeV

root_file_path = "pmssmtree_11aug2023.root"
tree_name = "mcmc"
outdir = "plotsdmtest"

root_file = TFile(root_file_path) # type: ignore
intree = root_file.Get(tree_name)

pmssm_plotter = PMSSM(
    intree = intree, 
    outdir = outdir,
    particleDrawConfig= particleDrawConfig_TeV,
    canvasStyle = {
                    "energy" : "13",
                    "extraText" : "Preliminary",
                    "lumi" : "(137-139)",
                }
    )

# pmssm_plotter.printConfig("abs(chsi1pm-chi10)")

# pmssm_plotter.quantilePlots1D(drawstring="abs(chi1pm-chi10)", xaxisDrawConfig={"1Dlogy":True,}, canvasStyle={"offset": {"ymax":5}})
# pmssm_plotter.quantilePlots1D(drawstring="abs(chi1pm-chi10)", xaxisDrawConfig={"1Dlogy":False},    canvasStyle={
#         "legend" :{
#              "x1":0.7,
#                     "y1":0.18,
#                     "x2":0.86,
#                     "y2":0.3,
#             "textSize":0.030,
#         }
#     })
pmssm_plotter.impact1D(drawstring="abs(chi1pm-chi10)",canvasStyle={
        "legend" :{
              "x1":0.6,
                    "y1":0.75,
                    "x2":0.72,
                    "y2":0.90,
            "textSize":0.030,
        }
    })

# print("#"*50)



# print("#"*50)
# pmssm_plotter.survivalProbability2D(drawstring="abs(chi10):abs(chi1pm-chi10)", xaxisDrawConfig={"logScale":False,"linearScale":1000,"unit":"TeV"})

# pmssm_plotter.survivalProbability2D(drawstring="abs(chi10):t1", xaxisDrawConfig={"logScale":False,"linearScale":1000,"unit":"TeV"})


pmssm_plotter.quantilePlots2D(
    drawstring="abs(chi1pm-chi10):abs(chi10)", 
    quantile=0.99,
    canvasStyle={
        "legend" :{
               "x1":0.43,
                "y1":0.78,
                "x2":0.75,
                "y2":0.9,
            "textSize":0.030,
            "textColor":kWhite,
        }
    })

# print("#"*50)

# pmssm_plotter.quantilePlots2D(
#     drawstring="abs(chi1pm-chi10):abs(chi10)", 
#     quantile=0.99,
#     canvasStyle={
#         "legend" :{
#             "textColor":kWhite,
#         }
#     })

# pmssm_plotter.quantilePlots2D(
#     drawstring="abs(chi10):abs(chi1pm-chi10)", 
#     quantile=0.99)