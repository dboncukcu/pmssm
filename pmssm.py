from ROOT import *
from utils.utils import *
import numpy as np
from array import array
import os
from utils.plots import get_impact_plots, get_quantile_plot_1D, get_SP_plot_1D, get_SP_plot_2D, get_quantile_plot_2D, get_prior_CI, get_posterior_CI,sprobcontours
import copy
from plotter import Plotter

particleDrawConfig_TeV = {
    "defaults" : {
        "nbin": 100,
        "max": 1000,
        "min": 0,
        "logScale": False,
        "linearScale": 1000.0, # for TeV, 1GeV/1000
        "unit": "TeV",
        },
    "abs(chi10)" : {
        "title" : "m_{#tilde{#chi}^{0}_{1}}",
        "nbin" : 50,
        "min" : 0,
        "max" : 2500,
        "logScale" : False,
        "linearScale": 1000, # for TeV, 1GeV/1000
        "unit": "TeV",
        "name" : "chi10"
        },
    "abs(chi20)" : {
        "title" : "m_{#tilde{#chi}^{0}_{2}}",
        "nbin" : 50,
        "min" : 0,
        "max" : 2500,
        "logScale" : False,
        "linearScale": 1000, # for TeV, 1GeV/1000
        "unit": "TeV",
        "name" : "chi20"
    },
    "g": {
        "title" : "m_{#tilde{g}}",
        "nbin" : 100,
        "min" : 0,
        "max" : 7000,
        "logScale" : False,
        "linearScale": 1000, # for TeV, 1GeV/1000
        "unit": "TeV",
        "name" : "gluino"
        },
    "t1" : {
        "title": "m_{#tilde{t}_{1}}",
        "nbin" : 100,
        "min" : 0,
        "max" : 7000,
        "logScale": False,
        "linearScale": 1000.0,
        "unit": "TeV",
        "name": "stop1"
        
    },
    "t2" : {
        "title": "m_{#tilde{t}_{2}}",
        "nbin" : 100,
        "min" : 0,
        "max" : 7000,
        "logScale": False,
        "linearScale": 1000.0,
        "unit": "TeV",
        "name": "stop2"
        
    },
    "b1" : {
        "title": "m_{#tilde{b}_{1}}",
        "nbin" : 100,
        "min" : 0,
        "max" : 7000,
        "logScale": False,
        "linearScale": 1000.0,
        "unit": "TeV",
        "name": "sbottom"
    },
    "lcsp" : {
        "title" : "m_{LCSP}",
        "nbin" : 50,
        "min" : 0,
        "max" : 7000,
        "logScale" : False,
        "linearScale": 1000, # for TeV, 1GeV/1000
        "unit": "TeV",
        "name" : "lcsp"
        },
    "abs(chi1pm)-abs(chi10)": {
        "title": "#Deltam(#tilde{#chi}^{#pm}_{1},#tilde{#chi}^{0}_{1})",
        "nbin" : 100,
        "min" : 0.001,
        "max" : 3000,
        "logScale": True,
        "linearScale": 1.0,
        "unit": "GeV",
        "name" : "DmChi1pmChi10",
        "1Dlogy": False
    },
    "g-abs(chi10)": {
        "title": "#Deltam(#tilde{g},#tilde{#chi}^{0}_{1})",
        "nbin" : 100,
        "min" : 0,
        "max" : 7000,
        "logScale": True,
        "linearScale": 1.0,
        "unit": "GeV",
        "name" : "DmGluinoChi10",
        "1Dlogy": False
    },
    "t1-abs(chi10)": {
        "title": "#Deltam(#tilde{t}_{1},#tilde{#chi}^{0}_{1})",
        "nbin" : 100,
        "min" : 0,
        "max" : 7000,
        "logScale": True,
        "linearScale": 1.0,
        "unit": "GeV",
        "name" : "DmStop1Chi10",
        "1Dlogy": False
    },
    "b1-abs(chi10)": {
        "title": "#Deltam(#tilde{b}_{1},#tilde{#chi}^{0}_{1})",
        "nbin" : 100,
        "min" : 0,
        "max" : 7000,
        "logScale": True,
        "linearScale": 1.0,
        "unit": "GeV",
        "name" : "DmSbottom1Chi10",
        "1Dlogy": False
    },
    "lcsp-abs(chi10)": {
        "title": "#Deltam(LCSP,#tilde{#chi}^{0}_{1})",
        "nbin" : 100,
        "min" : 0,
        "max" : 7000,
        "logScale": True,
        "linearScale": 1.0,
        "unit": "GeV",
        "name" : "DmLcspChi10",
        "1Dlogy": False
    },
    "abs(chi20-chi10)": {
        "title": "#Deltam(#tilde{#chi}^{0}_{2},#tilde{#chi}^{0}_{1})",
        "nbin" : 100,
        "min" : 0.1,
        "max" : 3000,
        "logScale": True,
        "linearScale": 1.0,
        "unit": "GeV",
        "name" : "DmChi20Chi10",
        "1Dlogy": False
    },
    "abs(chi1pm)" : {
        "title" : "m_{#tilde{#chi}^{#pm}_{1}}",
        "nbin" : 50,
        "min" : 0,
        "max" : 2500,
        "logScale" : False,
        "linearScale": 1000,
        "unit": "TeV",
        "name" : "chi1pm"
        },
    }


class DotDict(dict):
    def __getitem__(self, item):
        item = dict.__getitem__(self, item)
        if isinstance(item, dict):
            return DotDict(item)
        return item

    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError:
            raise AttributeError(f"'DotDict' object has no attribute '{attr}'")

plot_settings = DotDict({
    "survival2D" : {
        "legend" : {
            "leftTop" : {"x1":0.18,"x2":0.52,"y1":0.8,"y2":0.9},
            "rightTop" : {"x1":0.5,"x2":0.82,"y1":0.8,"y2":0.9},
            "rightBottom" : {"x1":0.2,"x2":0.82,"y1":0.18,"y2":0.28},
            "leftBottom" : {"x1":0.18,"x2":0.52,"y1":0.18,"y2":0.28},
        },
        "variant" : {
            "variant1": {
                "fillWhiteLegend" : True,
                "whiteColorLegend": False,
                "extraSpace": 0.04,
                "iPos": 0,
                "YaxisSetTitleOffset":1.25,
                "XaxisSetTitleOffset":1,
                "YaxisSetMaxDigits":None,
                "ZaxisSetMaxDigits":3,
                "ZaxisSetTitleOffset":1.28,
                "SetBottomMargin":0.02,
                "loc" : "rightTop",
                
            },
            "variant2": {
                "fillWhiteLegend" : False,
                "whiteColorLegend": True,
                "extraSpace": 0.04,
                "iPos": 0,
                "YaxisSetTitleOffset":1.25,
                "XaxisSetTitleOffset":1,
                "YaxisSetMaxDigits":None,
                "ZaxisSetMaxDigits":3,
                "ZaxisSetTitleOffset":1.28,
                "SetBottomMargin":0.02,
                "loc" : "leftBottom",
                
            },
        }
    },
    "survival1D" : {
        "legend" : {
            "leftTop" : {"x1":0.17,"x2":0.47,"y1":0.8,"y2":0.9},
            "rightTop" : {"x1":0.72,"x2":0.93,"y1":0.8,"y2":0.9},
            "rightBottom" : {"x1":0.67,"x2":0.88,"y1":0.2,"y2":0.32},
            "leftBottom" : {"x1":0.17,"x2":0.47, "y1":0.2,"y2":0.32},
        },
        "variant" : {
            "variant1": {
                "fillWhiteLegend" : True,
                "extraSpace": 0.02,
                "iPos": 11,
                "YaxisSetTitleOffset":1.15,
                "XaxisSetTitleOffset":1.12,
                "YaxisSetMaxDigits":None,
                "SetBottomMargin":0.025,
                "loc" : "rightBottom"
            },
            "variant2": {
                "fillWhiteLegend" : True,
                "extraSpace": 0.01,
                "iPos": 0,
                "YaxisSetTitleOffset":1,
                "XaxisSetTitleOffset":1,
                "YaxisSetMaxDigits":None,
                "SetBottomMargin":0.02,
                "loc" : "leftTop"
            }
        }
    },
    "impact1D" : {
        "legend" : {
            "leftTop" : {"x1":0.23,"x2":0.53,"y1":0.8,"y2":0.9},
            "rightTop" : {"x1":0.63,"x2":0.93,"y1":0.8,"y2":0.9},
            "rightBottom" : {"x1":0.63,"x2":0.93,"y1":0.2,"y2":0.32},
            "leftBottom" : {"x1":0.23,"x2":0.53,"y1":0.2,"y2":0.32},
        },
        "variant" : {
            "variant1": {
                "fillWhiteLegend" : True,
                "extraSpace": 0.01,
                "iPos": 11,
                "YaxisSetTitleOffset":1,
                "XaxisSetTitleOffset":1.1,
                "YaxisSetMaxDigits":2,
                "SetBottomMargin":0.025,
                "loc" : "rightTop"
            },
            "variant2": {
                "fillWhiteLegend" : True,
                "extraSpace": 0.06,
                "iPos": 0,
                "YaxisSetTitleOffset":1.65,
                "XaxisSetTitleOffset":1.1,
                "YaxisSetMaxDigits":None,
                "SetBottomMargin":0.03,
                "loc" : "leftTop"
            }
        }
    },
    "quantile1D" : {
        "legend" : {
            "leftTop" : {"x1":0.17,"x2":0.47,"y1":0.8,"y2":0.9},
            "rightTop" : {"x1":0.72,"x2":0.93,"y1":0.8,"y2":0.9},
            "rightBottom" : {"x1":0.72,"x2":0.93,"y1":0.2,"y2":0.32},
            "leftBottom" : {"x1":0.17,"x2":0.47, "y1":0.2,"y2":0.32},
        },
        "variant" : {
            "variant1": {
                "fillWhiteLegend" : True,
                "extraSpace": 0.01,
                "iPos": 11,
                "YaxisSetTitleOffset":1,
                "XaxisSetTitleOffset":1,
                "YaxisSetMaxDigits":None,
                "SetBottomMargin":0.02,
                "loc" : "rightBottom"
            },
            "variant2": {
                "fillWhiteLegend" : True,
                "extraSpace": 0.01,
                "iPos": 0,
                "YaxisSetTitleOffset":1,
                "XaxisSetTitleOffset":1,
                "YaxisSetMaxDigits":None,
                "SetBottomMargin":0.02,
                "loc" : "leftTop"
            }
        }
    },
    "quantile2D" : {
        "legend" : {
            "leftTop" : {"x1":0.2,"x2":0.305,"y1":0.85,"y2":0.9},
            "rightTop" : {"x1":0.73,"x2":0.835,"y1":0.85,"y2":0.9},
            "rightBottom" : {"x1":0.73,"x2":0.835,"y1":0.18,"y2":0.23},
            "leftBottom" : {"x1":0.2,"x2":0.305, "y1":0.18,"y2":0.23}
        },
        "variant" : {
            "variant1": {
                "fillWhiteLegend" : True,
                "whiteColorLegend": False,
                "extraSpace": 0.04,
                "iPos": 0,
                "YaxisSetTitleOffset":1.25,
                "XaxisSetTitleOffset":1,
                "YaxisSetMaxDigits":None,
                "ZaxisSetMaxDigits":3,
                "ZaxisSetTitleOffset":1.28,
                "SetBottomMargin":0.02,
                "loc" : "rightTop",
                
            },
            "variant2": {
                "fillWhiteLegend" : False,
                "whiteColorLegend": True,
                "extraSpace": 0.04,
                "iPos": 0,
                "YaxisSetTitleOffset":1.25,
                "XaxisSetTitleOffset":1,
                "YaxisSetMaxDigits":None,
                "ZaxisSetMaxDigits":3,
                "ZaxisSetTitleOffset":1.28,
                "SetBottomMargin":0.02,
                "loc" : "leftBottom",
                
            },
        }
    }
})

class PMSSM:
    def __init__(
        self,
        intree,
        outdir : str,
        particleConfig : dict,
        canvasLabel :dict = {"energy" : "13","extraText" : "Preliminary","lumi" : "",},
        defaultOutputFileFormat : str = "pdf",
        friendAnalysis : list[dict] = [{"treeName":"cms_sus_20_001","path":"sus_20_001_likelihood.root"}],
        globalSettings : dict = {
            "logEps": 1e-5,
        }
        ):
        
        if outdir[-1]!="/":
                outdir+="/"
        if not os.path.exists(outdir):
                os.system("mkdir -p "+outdir)
                
        self.intree = intree
        self.outdir = outdir
        self.particelConfig = particleConfig
        self.outputFormat = defaultOutputFileFormat
        self.canvasLabel = canvasLabel
        self.globalSettings = globalSettings
        self.add_friends(self.intree,friendAnalysis)
        
        Plotter.setPalette(self.createSurvivalPlotPalette())
    
    @staticmethod
    def add_friends(intree,friendAnalysis):
        
        for friend in friendAnalysis:
            friendTreeName = friend["treeName"]
            friendTreePath = friend["path"]
            intree.AddFriend(friendTreeName,TFile(friendTreePath))
    
    @staticmethod
    def createSurvivalPlotPalette():
        custompalette = []
        cols = TColor.GetNumberOfColors()
        for i in range(cols):
            if i<19:
                col = kBlack
            # elif i > 253:
            #     col = kGray
            else:
                col = TColor.GetColorPalette(i)
            custompalette.append(col)
        custompalette = np.intc(custompalette)
        return custompalette
    
    def getParticleConfig(self,particleName:str,overWrite:dict=None):
                
        try:
            if self.particelConfig.get(particleName) is not None:
                particleConfig = self.particelConfig[particleName].copy()
            else:
                particleConfig = self.particelConfig["defaults"].copy()
                particleConfig["title"] = particleName 
        except:
                raise Exception("Missing Config for ",particleName)
        if overWrite is not None:
            for key in overWrite.keys():
                particleConfig[key] = overWrite[key]
        return particleConfig
    
    def createName(self,xaxisDrawConfig, yaxisDrawConfig:dict= None, analysis:str="combined",plotType:str=""):
        name = ""
        
        xname = xaxisDrawConfig.get("name","notfound")
        xlog1D = xaxisDrawConfig.get("1Dlogy", False)
        if xlog1D:
            xname += "_logy"
        yname = ""
        if yaxisDrawConfig is not None:
            yname = yaxisDrawConfig.get("name","")
            name = xname + "_" + yname
        else:
            name = xname
        
        if analysis !="":
            name += "_"+analysis.upper()
        if plotType !="":
            name += "_"+plotType
        
        
        name = name.replace(".","p")
        name = name.replace("(","")
        name = name.replace(")","")
        return  name
    
    def setGlobalSettings(self,settings:dict):
        for key in settings.keys():
            self.globalSettings[key] = settings[key]
    
    def getGlobalSettings(self):
        return self.globalSettings
    
    @staticmethod
    def getAxisRange(obj, offset:dict = {"xmin":0.0,"xmax":0.0,"ymin":0.0,"ymax":0.0}):
        """
        Get the range of the x and y axes of a TH1 or TGraph object.
        Parameters:
        obj : TH1|TGraph
            The object for which to get the axis range
        offset : dict
            A dictionary with the following
            keys:
            - xmin : float
                The offset for the lower limit of the x-axis
            - xmax : float
                The offset for the upper limit of the x-axis
            - ymin : float
                The offset for the lower limit of the y-axis
            - ymax : float
                The offset for the upper limit of the y-axis
        Returns:
        float,float,float,float
            The lower limit of the x-axis, the upper limit of the x-axis,
            the lower limit of the y-axis, and the upper limit of the y-axis
        """
        if isinstance(obj, TH1):
            xmin = obj.GetXaxis().GetXmin()
            xmax = obj.GetXaxis().GetXmax()
            ymin = obj.GetMinimum()
            ymax = obj.GetMaximum()
        elif isinstance(obj, TGraph):
            xmin = obj.GetXaxis().GetXmin()
            xmax = obj.GetXaxis().GetXmax()
            ymin = obj.GetHistogram().GetMinimum()
            ymax = obj.GetHistogram().GetMaximum()
        else:
            raise TypeError("Object must be TH1 or TGraph")
        
        xmin -= offset.get("xmin",0.0)
        xmax += offset.get("xmax",0.0)
        ymin -= offset.get("ymin",0.0)
        ymax += offset.get("ymax",0.0)
        return xmin, xmax, ymin, ymax

    @staticmethod
    def getCustomVariant(params:dict, plotType:str, basedOn:str=None):
        if basedOn is not None:
            variant = copy.deepcopy(plot_settings[plotType].variant[basedOn])
            for key in params.keys():
                variant[key] = params[key]
            return variant
        else:
            return params
    ##################################################################################################################
    #  ##########  ##       #########  ##########   ######     ##########  ##      ##  ##########  #######   ######  #
    #  ##      ##  ##       ##     ##      ##      ##    ##        ##       ##    ##   ##      ##  ##       ##    ## #
    #  ##      ##  ##       ##     ##      ##      ##              ##         ####     ##      ##  ##       ##       #
    #  #########   ##       ##     ##      ##       ######         ##          ##      #########   #######   ######  #
    #  ##          ##       ##     ##      ##            ##        ##          ##      ##          ##             ## #
    #  ##          ##       ##     ##      ##      ##    ##        ##          ##      ##          ##       ##    ## #
    #  ##          #######  #########      ##       ######         ##          ##      ##          #######   ######  #
    ##################################################################################################################
    def impact1D(
        self,
        drawstring : str, 
        analysis : str = "combined",
        moreconstraints : list = [], 
        moreconstraints_prior : bool =False,
        xaxisDrawConfig : dict = None,
        customVariant : dict|None = None,
        variant : str = "variant1"
        ):
        
        if customVariant is not None:
            styleSettings = self.getCustomVariant(customVariant, "impact1D", basedOn=variant)
        else:
            styleSettings = plot_settings.impact1D.variant[variant]
        
        xaxisParticleName = drawstring
        xaxisDrawConfig = self.getParticleConfig(xaxisParticleName,xaxisDrawConfig)
        
        name = self.createName(xaxisDrawConfig = xaxisDrawConfig ,analysis = analysis, plotType = "impact1D")
        
        impact_plots = get_impact_plots(
            localtree = self.intree,
            analysis = analysis,
            hname = name,
            xtitle = xaxisDrawConfig["title"] + " ["+xaxisDrawConfig["unit"]+"]",
            xbins = xaxisDrawConfig["nbin"],
            xlow = xaxisDrawConfig["min"],
            xup = xaxisDrawConfig["max"],
            _logx = xaxisDrawConfig.get("logScale", False),
            drawstring = drawstring,
            moreconstraints = moreconstraints,
            moreconstraints_prior = moreconstraints_prior)
                
        for key in impact_plots:
            hist = impact_plots[key]
            if not xaxisDrawConfig.get("logScale", False):
                Plotter.scaleXaxis(hist,scaleFactor=xaxisDrawConfig.get("linearScale"))
        
        axis_range = {"xmin": None,"xmax": None,"ymin": None,"ymax": None}
        for key in impact_plots:
            hist = impact_plots[key]
            xmin,xmax,ymin,ymax = self.getAxisRange(hist)    
            if xaxisDrawConfig.get("1Dlogy", False) and ymin==0:
                ymin = self.globalSettings.setdefault("logEps",1e-5)
                hist.GetYaxis().SetRangeUser(ymin,ymax)
                
            if axis_range["xmin"] is None or xmin < axis_range["xmin"]:
                axis_range["xmin"] = xmin
            if axis_range["xmax"] is None or xmax > axis_range["xmax"]:
                axis_range["xmax"] = xmax
            if axis_range["ymin"] is None or ymin < axis_range["ymin"]:
                axis_range["ymin"] = ymin
            if axis_range["ymax"] is None or ymax > axis_range["ymax"]:
                axis_range["ymax"] = ymax
        
        # axis_range["ymax"] += 0.01
        
        p = Plotter(
            canvasSettings={
                **axis_range,
                "nameXaxis": xaxisDrawConfig["title"]+ " ["+xaxisDrawConfig["unit"]+"]",
                "nameYaxis": "pMSSM Density",
                "canvName": f"canvas_{name}",
                "extraSpace": styleSettings.get("extraSpace",0.01),
                "iPos": styleSettings.get("iPos",11),
                })
        
        p.SetLog(logx = xaxisDrawConfig.get("logScale", False), logy=xaxisDrawConfig.get("1Dlogy", False))
        
        impact_plots["prior"].Draw("hist same")
        impact_plots["posterior"].Draw("histsame")
        impact_plots["posterior_up"].Draw("histsame")
        impact_plots["posterior_down"].Draw("histsame")
        
        p.tuning(tuning={"YaxisSetTitleOffset": styleSettings.get("YaxisSetTitleOffset",1)})
        p.tuning(tuning={"XaxisSetTitleOffset": styleSettings.get("XaxisSetTitleOffset",1)})
        p.tuning(tuning={"YaxisSetMaxDigits": styleSettings.get("YaxisSetMaxDigits",2)})
        p.tuning(tuning={"SetBottomMargin": styleSettings.get("SetBottomMargin",0.02)})
        
        p.createLegend(**plot_settings.impact1D.legend[styleSettings.get("loc","rightBottom")],header=analysis.upper())

        p.addEntryToLegend(impact_plots["prior"],"prior")
        p.addEntryToLegend(impact_plots["posterior"],"posterior (#sigma = #sigma_{nominal} )")
        p.addEntryToLegend(impact_plots["posterior_up"],"posterior (#sigma = 1.5#times#sigma_{nominal} )")
        p.addEntryToLegend(impact_plots["posterior_down"],"posterior (#sigma =0.5#times#sigma_{nominal} )")
        
        if (styleSettings.get("fillWhiteLegend",True)):
            p.fillWhiteLegend()
        
        p.SaveAs(self.outdir+name+"."+self.outputFormat)
    
    def quantile1D(
        self,
        drawstring : str, 
        quantiles : dict = {
            "0.5": {"color":kBlack},
            "0.75": {"color":kOrange},
            "0.9": {"color":kRed,"linestyle": kDashed},
            "0.99": {"color":kMagenta,"linestyle": kDashed}
            },
        analysis : str = "combined",
        moreconstraints : list = [], 
        xaxisDrawConfig : dict = None,
        customVariant : dict|None = None,
        variant : str = "variant1"
        ):
        
        if customVariant is not None:
            styleSettings = self.getCustomVariant(customVariant, "quantile1D", basedOn=variant)
        else:
            styleSettings = plot_settings.quantile1D.variant[variant]
        
        xaxisParticleName = drawstring
        xaxisDrawConfig = self.getParticleConfig(xaxisParticleName,xaxisDrawConfig)
        
        name = self.createName(xaxisDrawConfig = xaxisDrawConfig ,analysis = analysis, plotType = "quantile1D")
        
        quantiles_hists = get_quantile_plot_1D(
            localtree = self.intree,
            analysis = analysis,
            hname = name,
            xtitle = xaxisDrawConfig["title"] + " ["+xaxisDrawConfig["unit"]+"]",
            xbins = xaxisDrawConfig["nbin"],
            xlow = xaxisDrawConfig["min"],
            xup = xaxisDrawConfig["max"],
            _logx = xaxisDrawConfig.get("logScale",False),
            drawstring = drawstring,
            moreconstraints = moreconstraints,
            quantiles = [float(i) for i in quantiles.keys()],
            _logy = xaxisDrawConfig.get("1Dlogy", False)
        )
        
        
        for key in quantiles_hists:
            hist = quantiles_hists[key]
            if not xaxisDrawConfig.get("logScale", False):
                Plotter.scaleXaxis(hist,scaleFactor=xaxisDrawConfig.get("linearScale"))
        
        
        axis_range = {"xmin": None,"xmax": None,"ymin": None,"ymax": None}
        for key in quantiles_hists:
            hist = quantiles_hists[key]
            xmin,xmax,ymin,ymax = self.getAxisRange(hist)    
            if xaxisDrawConfig.get("1Dlogy", False) and ymin==0:
                ymin = self.globalSettings.setdefault("logEps",1e-5)
                hist.GetYaxis().SetRangeUser(ymin,ymax)
                
            if axis_range["xmin"] is None or xmin < axis_range["xmin"]:
                axis_range["xmin"] = xmin
            if axis_range["xmax"] is None or xmax > axis_range["xmax"]:
                axis_range["xmax"] = xmax
            if axis_range["ymin"] is None or ymin < axis_range["ymin"]:
                axis_range["ymin"] = ymin
            if axis_range["ymax"] is None or ymax > axis_range["ymax"]:
                axis_range["ymax"] = ymax
        
        p = Plotter(
            canvasSettings={
                **axis_range,
                "nameXaxis": xaxisDrawConfig["title"]+ " ["+xaxisDrawConfig["unit"]+"]",
                "nameYaxis": "pMSSM Density",
                "canvName": f"canvas_{name}",
                "extraSpace": styleSettings.get("extraSpace",0.01),
                "iPos": styleSettings.get("iPos",11),
                })
        
        p.SetLog(logx = xaxisDrawConfig.get("logScale", False), logy=xaxisDrawConfig.get("1Dlogy", False))
        
        p.createLegend(**plot_settings.quantile1D.legend[styleSettings.get("loc","rightBottom")],header=analysis.upper())

        for i in quantiles:
            histname = "quantile_" + str(int(100 * float(i)))
            hist_style = quantiles[i]
            hist = quantiles_hists[histname]
            
            if hist_style.get("color") is not None:
                hist.SetLineColor(hist_style["color"])
            if hist_style.get("linestyle") is not None:
                hist.SetLineStyle(hist_style["linestyle"])
            
            p.addEntryToLegend(hist,str(int(100 * float(i)))+"th Percentile")

        for key in quantiles_hists:
            hist = quantiles_hists[key]
            hist.Draw("hist same")

        
        p.tuning(tuning={"YaxisSetTitleOffset": styleSettings.get("YaxisSetTitleOffset",1)})
        p.tuning(tuning={"XaxisSetTitleOffset": styleSettings.get("XaxisSetTitleOffset",1)})
        p.tuning(tuning={"YaxisSetMaxDigits": styleSettings.get("YaxisSetMaxDigits",2)})
        p.tuning(tuning={"SetBottomMargin": styleSettings.get("SetBottomMargin",0.02)})
        
        
        if (styleSettings.get("fillWhiteLegend",True)):
            p.fillWhiteLegend()
        
        p.SaveAs(self.outdir+name+"."+self.outputFormat)

    def quantile2D(
        self,
        drawstring : str,
        quantile : float,
        analysis : str = "combined",
        moreconstraints : list = [], 
        moreconstraints_prior : bool =False,
        xaxisDrawConfig : dict = None,
        yaxisDrawConfig : dict = None,
        customVariant : dict|None = None,
        variant : str = "variant1"
        ):
        Plotter.Reset()

        if customVariant is not None:
            styleSettings = self.getCustomVariant(customVariant, "quantile2D", basedOn=variant)
        else:
            styleSettings = plot_settings.quantile2D.variant[variant]
        
        yaxisParticleName, xaxisParticleName = drawstring.split(":")
        
        xaxisDrawConfig = self.getParticleConfig(xaxisParticleName,xaxisDrawConfig)
        yaxisDrawConfig = self.getParticleConfig(yaxisParticleName,yaxisDrawConfig)
        
        name = self.createName(xaxisDrawConfig = xaxisDrawConfig ,analysis = analysis, plotType = "quantile2D")
        
        hist = get_quantile_plot_2D(
            localtree = self.intree,
            quantile=quantile,
            analysis = analysis,
            hname = name,
            xtitle = xaxisDrawConfig["title"] + " ["+xaxisDrawConfig["unit"]+"]",
            xbins = xaxisDrawConfig["nbin"],
            xlow = xaxisDrawConfig["min"],
            xup = xaxisDrawConfig["max"],
            ytitle = yaxisDrawConfig["title"] + " ["+yaxisDrawConfig["unit"]+"]",
            ybins = yaxisDrawConfig["nbin"],
            ylow = yaxisDrawConfig["min"],
            yup = yaxisDrawConfig["max"],
            _logx = xaxisDrawConfig.get("logScale",False),
            _logy = yaxisDrawConfig.get("logScale",False),
            drawstring = drawstring,
            moreconstraints = moreconstraints,
            moreconstraints_prior = moreconstraints_prior)
                
        if not xaxisDrawConfig.get("logScale", False):
            Plotter.scaleXaxis(hist,scaleFactor=xaxisDrawConfig.get("linearScale"))
        if not yaxisDrawConfig.get("logScale", False):
            Plotter.scaleYaxis(hist,scaleFactor=yaxisDrawConfig.get("linearScale"))
        

        axis_range = {
            "xmin": xaxisDrawConfig["min"]/xaxisDrawConfig.get("linearScale",1.0),
            "xmax": xaxisDrawConfig["max"]/xaxisDrawConfig.get("linearScale",1.0),
            "ymin": yaxisDrawConfig["min"]/yaxisDrawConfig.get("linearScale",1.0),
            "ymax": yaxisDrawConfig["max"]/yaxisDrawConfig.get("linearScale",1.0)
        }
        if xaxisDrawConfig.get("logScale", False):
            for key in ["xmin","xmax"]:
                if axis_range[key] == 0:
                    axis_range[key] = self.globalSettings.setdefault("logEps",1e-5)
                
                axis_range[key] = np.log10(axis_range[key])
        if yaxisDrawConfig.get("logScale", False):
            for key in ["ymin","ymax"]:
                if axis_range[key] == 0:
                    axis_range[key] = self.globalSettings.setdefault("logEps",1e-5)
                axis_range[key] = np.log10(axis_range[key])
                    
        p = Plotter(
            canvasSettings={
                **axis_range,
                "nameXaxis": xaxisDrawConfig["title"]+ " ["+xaxisDrawConfig["unit"]+"]",
                "nameYaxis": yaxisDrawConfig["title"]+ " ["+yaxisDrawConfig["unit"]+"]",
                "canvName": f"canvas_{name}",
                "extraSpace": 0.04,
                "iPos": 0,
                "is3D": True,
                })
        
        p.SetLog(logx = xaxisDrawConfig.get("logScale", False), logy=yaxisDrawConfig.get("logScale", False))
        
        p.tuning(tuning=styleSettings,hist=hist)
        p.setPalette(kViridis)
        hist.SetContour(999)
        
        hist.GetZaxis().SetTitle(str(int(100 * quantile)) + "th Percentile Bayes Factor")
        p.Draw2D(hist)
        p.createLegend(**plot_settings.quantile2D.legend[styleSettings.get("loc","rightBottom")],header=analysis.upper())
        if styleSettings.get("whiteColorLegend",True):
            p.whiteColorLegend()
        
        if (styleSettings.get("fillWhiteLegend",True)):
            p.fillWhiteLegend()
        
        p.SaveAs(self.outdir+name+"."+self.outputFormat)

        del(p)
        
    def survival2D(
            self,
            drawstring : str, 
            analysis : str = "combined",
            contourSwitch : bool= True,  
            moreconstraints : list = [], 
            moreconstraints_prior : bool =False,
            xaxisDrawConfig : dict = None,
            yaxisDrawConfig : dict = None,
            customVariant : dict|None = None,
            variant : str = "variant1"
        ):
        Plotter.Reset()
        if customVariant is not None:
            styleSettings = self.getCustomVariant(customVariant, "survival2D", basedOn=variant)
        else:
            styleSettings = plot_settings.quantile2D.variant[variant]
        
        yaxisParticleName, xaxisParticleName = drawstring.split(":")
        
        xaxisDrawConfig = self.getParticleConfig(xaxisParticleName,xaxisDrawConfig)
        
        yaxisDrawConfig = self.getParticleConfig(yaxisParticleName,yaxisDrawConfig)
        
        name = self.createName(xaxisDrawConfig = xaxisDrawConfig ,analysis = analysis, plotType = "survival2D")
                
        hist = get_SP_plot_2D(
            localtree=self.intree,
            analysis = analysis,
            hname = name,
            xtitle = xaxisDrawConfig["title"] + " ["+xaxisDrawConfig["unit"]+"]",
            xbins = xaxisDrawConfig["nbin"],
            xlow = xaxisDrawConfig["min"],
            xup = xaxisDrawConfig["max"],
            ytitle = yaxisDrawConfig["title"] + " ["+yaxisDrawConfig["unit"]+"]",
            ybins = yaxisDrawConfig["nbin"],
            ylow = yaxisDrawConfig["min"],
            yup = yaxisDrawConfig["max"],
            _logx = xaxisDrawConfig.get("logScale",False),
            _logy = yaxisDrawConfig.get("logScale",False),
            drawstring = drawstring,
            moreconstraints = moreconstraints,
            moreconstraints_prior = moreconstraints_prior)
        
        if contourSwitch:
        
            prior_data =  get_prior_CI(
                self.intree, 
                hname = name + "_priorcontours",
                xbins = xaxisDrawConfig["nbin"], 
                xlow = xaxisDrawConfig["min"], 
                xup = xaxisDrawConfig["max"],
                ybins = yaxisDrawConfig["nbin"], 
                ylow = yaxisDrawConfig["min"], 
                yup = yaxisDrawConfig["max"], 
                _logx = xaxisDrawConfig.get("logScale",False), 
                _logy = yaxisDrawConfig.get("logScale",False), 
                drawstring = drawstring,
                moreconstraints= moreconstraints)
            
            posterior_data = get_posterior_CI(
                self.intree, 
                analysis = analysis, 
                hname = name + "_priorcontours", 
                xbins = xaxisDrawConfig["nbin"], 
                xlow = xaxisDrawConfig["min"], 
                xup = xaxisDrawConfig["max"], 
                ybins = yaxisDrawConfig["nbin"], 
                ylow = yaxisDrawConfig["min"], 
                yup = yaxisDrawConfig["max"], 
                _logx = xaxisDrawConfig.get("logScale",False), 
                _logy = yaxisDrawConfig.get("logScale",False), 
                drawstring = drawstring,
                moreconstraints = moreconstraints)

        
        if not xaxisDrawConfig.get("logScale", False):
            Plotter.scaleXaxis(hist,scaleFactor=xaxisDrawConfig.get("linearScale"))
        if not yaxisDrawConfig.get("logScale", False):
            Plotter.scaleYaxis(hist,scaleFactor=yaxisDrawConfig.get("linearScale"))
        
        axis_range = {
            "xmin": xaxisDrawConfig["min"]/xaxisDrawConfig.get("linearScale",1.0),
            "xmax": xaxisDrawConfig["max"]/xaxisDrawConfig.get("linearScale",1.0),
            "ymin": yaxisDrawConfig["min"]/yaxisDrawConfig.get("linearScale",1.0),
            "ymax": yaxisDrawConfig["max"]/yaxisDrawConfig.get("linearScale",1.0)
        }
        if xaxisDrawConfig.get("logScale", False):
            for key in ["xmin","xmax"]:
                if axis_range[key] == 0:
                    axis_range[key] = self.globalSettings.setdefault("logEps",1e-5)
                axis_range[key] = np.log10(axis_range[key])
        if yaxisDrawConfig.get("logScale", False):
            for key in ["ymin","ymax"]:
                if axis_range[key] == 0:
                    axis_range[key] = self.globalSettings.setdefault("logEps",1e-5)
                axis_range[key] = np.log10(axis_range[key])
                    
        
        p = Plotter(
            canvasSettings={
                **axis_range,
                "nameXaxis": xaxisDrawConfig["title"]+ " ["+xaxisDrawConfig["unit"]+"]",
                "nameYaxis": yaxisDrawConfig["title"]+ " ["+yaxisDrawConfig["unit"]+"]",
                "canvName": f"canvas_{name}",
                "extraSpace": 0.04,
                "iPos": 0,
                "is3D": True,
                })
        p.setPalette(self.createSurvivalPlotPalette())

        p.SetLog(logx = xaxisDrawConfig.get("logScale", False), logy=yaxisDrawConfig.get("logScale", False))
        
        p.tuning(tuning=styleSettings,hist=hist)
        hist.GetZaxis().SetTitle("Survival Probability")
        p.Draw2D(hist,"colz")
        
        if contourSwitch:
            for ix,interval in enumerate(prior_data):
                for cont in prior_data[interval]:
                    p.scaleGraphXaxis(cont,xaxisDrawConfig.get("linearScale",1.0))
                    p.scaleGraphYaxis(cont,yaxisDrawConfig.get("linearScale",1.0))
                    cont.Draw("same")
            for ix,interval in enumerate(posterior_data):
                for cont in posterior_data[interval]:
                    p.scaleGraphXaxis(cont,xaxisDrawConfig.get("linearScale",1.0))
                    p.scaleGraphYaxis(cont,yaxisDrawConfig.get("linearScale",1.0))
                    cont.Draw("same")
            
            p.createLegend(**plot_settings.survival2D.legend[styleSettings.get("loc","rightBottom")],header=analysis.upper(),columns=2)
        
            for ix,interval in enumerate(prior_data):
                if interval in prior_data.keys() and len(prior_data[interval])>0:
                    p.addEntryToLegend(prior_data[interval][0],str(int(100*(interval)))+"%  prior CI","l",)
                if interval in posterior_data.keys() and len(posterior_data[interval])>0:
                    p.addEntryToLegend(posterior_data[interval][0],str(int(100*(interval)))+"% posterior CI","l",)
        else:
            p.createLegend(**plot_settings.survival2D.legend[styleSettings.get("loc","rightBottom")],header=analysis.upper(),columns=2)

        
        if styleSettings.get("whiteColorLegend",True):
            p.whiteColorLegend()
        
        if (styleSettings.get("fillWhiteLegend",True)):
            p.fillWhiteLegend()
        
        p.SaveAs(self.outdir+name+"."+self.outputFormat)
        del(p)

    def survival1D(
        self,
        drawstring : str, 
        analysis : str = "combined",
        moreconstraints : list = [],
        moreconstraints_prior : bool =False,
        xaxisDrawConfig : dict = None,
        customVariant : dict|None = None,
        variant : str = "variant1"
        ):
        
        if customVariant is not None:
            styleSettings = self.getCustomVariant(customVariant, "survival1D", basedOn=variant)
        else:
            styleSettings = plot_settings.survival1D.variant[variant]
        
        xaxisParticleName = drawstring
        xaxisDrawConfig = self.getParticleConfig(xaxisParticleName,xaxisDrawConfig)
        
        name = self.createName(xaxisDrawConfig = xaxisDrawConfig ,analysis = analysis, plotType = "survival1D")
        
        survive_plots = get_SP_plot_1D(
            localtree = self.intree,
            analysis = analysis,
            hname = name,
            xtitle = xaxisDrawConfig["title"] + " ["+xaxisDrawConfig["unit"]+"]",
            xbins = xaxisDrawConfig["nbin"],
            xlow = xaxisDrawConfig["min"],
            xup = xaxisDrawConfig["max"],
            _logx = xaxisDrawConfig.get("logScale",False),
            drawstring = drawstring,
            moreconstraints = moreconstraints,
            moreconstraints_prior = moreconstraints_prior)
        
        
        for key in survive_plots:
            hist = survive_plots[key]
            if not xaxisDrawConfig.get("logScale", False):
                Plotter.scaleXaxis(hist,scaleFactor=xaxisDrawConfig.get("linearScale"))
                
        axis_range = {"xmin": None,"xmax": None,"ymin": None,"ymax": None}
        for key in survive_plots:
            hist = survive_plots[key]
            xmin,xmax,ymin,ymax = self.getAxisRange(hist)    
            if xaxisDrawConfig.get("1Dlogy", False) and ymin==0:
                ymin = self.globalSettings.setdefault("logEps",1e-5)
                hist.GetYaxis().SetRangeUser(ymin,ymax)

            if axis_range["xmin"] is None or xmin < axis_range["xmin"]:
                axis_range["xmin"] = xmin
            if axis_range["xmax"] is None or xmax > axis_range["xmax"]:
                axis_range["xmax"] = xmax
            if axis_range["ymin"] is None or ymin < axis_range["ymin"]:
                axis_range["ymin"] = ymin
            if axis_range["ymax"] is None or ymax > axis_range["ymax"]:
                axis_range["ymax"] = ymax
        
        p = Plotter(
            canvasSettings={
                **axis_range,
                "nameXaxis": xaxisDrawConfig["title"]+ " ["+xaxisDrawConfig["unit"]+"]",
                "nameYaxis": "Survival Probability",
                "canvName": f"canvas_{name}",
                "extraSpace": styleSettings.get("extraSpace",0.01),
                "iPos": styleSettings.get("iPos",11),
                })
        
        p.SetLog(logx = xaxisDrawConfig.get("logScale", False), logy=xaxisDrawConfig.get("1Dlogy", False))
        
        p.createLegend(**plot_settings.survival1D.legend[styleSettings.get("loc","rightBottom")],header=analysis.upper())
    
        p.addEntryToLegend(survive_plots["posterior"],"posterior (#sigma = #sigma_{nominal} )")
        p.addEntryToLegend(survive_plots["posterior_up"],"posterior (#sigma = 1.5#times#sigma_{nominal} )")
        p.addEntryToLegend(survive_plots["posterior_down"],"posterior (#sigma =0.5#times#sigma_{nominal} )")

        survive_plots["posterior"].Draw("histsame")
        survive_plots["posterior_up"].Draw("histsame")
        survive_plots["posterior_down"].Draw("histsame")
        
        p.tuning(tuning={"YaxisSetTitleOffset": styleSettings.get("YaxisSetTitleOffset",1.2)})
        p.tuning(tuning={"XaxisSetTitleOffset": styleSettings.get("XaxisSetTitleOffset",1.2)})
        p.tuning(tuning={"YaxisSetMaxDigits": styleSettings.get("YaxisSetMaxDigits",2)})
        p.tuning(tuning={"SetBottomMargin": styleSettings.get("SetBottomMargin",0.02)})
        
        
        if (styleSettings.get("fillWhiteLegend",True)):
            p.fillWhiteLegend()
        
        p.SaveAs(self.outdir+name+"."+self.outputFormat)
