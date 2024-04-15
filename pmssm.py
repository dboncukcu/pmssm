from ROOT import *
import os,sys
from utils.utils import *
import argparse
import numpy as np
from array import array

from utils.plots import get_impact_plots, get_quantile_plot_1D, get_SP_plot_1D, get_SP_plot_2D, get_quantile_plot_2D, get_prior_CI, get_posterior_CI,sprobcontours
import utils.cmsstyle as CMS

def ScaleAxis(axis, scale_function):
    if axis.GetXbins().GetSize():
        # Variable bin sizes
        X = TArrayD(axis.GetXbins())
        for i in range(X.GetSize()):
            X[i] = scale_function(X[i])
        axis.Set(X.GetSize() - 1, X.GetArray())
    else:
        # Fixed bin sizes
        axis.Set(axis.GetNbins(), scale_function(axis.GetXmin()), scale_function(axis.GetXmax()))
def scaleXaxis(histogram,scaleFactor=1.0):
    x_axis = histogram.GetXaxis()

    ScaleAxis(x_axis,lambda x: x / scaleFactor)
def scaleYaxis(histogram,scaleFactor=1.0):
    y_axis = histogram.GetYaxis()

    ScaleAxis(y_axis,lambda y: y / scaleFactor)
def scaleGraphXaxis(graph, scaleFactor=1.0):
    n = graph.GetN()
    for i in range(n):
        x = graph.GetPointX(i)
        graph.SetPointX(i, x / scaleFactor)
def scaleGraphYaxis(graph, scaleFactor=1.0):
    n = graph.GetN()
    for i in range(n):
        y = graph.GetPointY(i)
        graph.SetPointY(i, y / scaleFactor)

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
        "max" : 6500,
        "logScale" : False,
        "linearScale": 1000, # for TeV, 1GeV/1000
        "unit": "TeV",
        "name" : "gluon"
        },
    "t1" : {
        "title": "m_{#tilde{t}_{1}}",
        "nbin" : 100,
        "min" : 0,
        "max" : 6500,
        "logScale": False,
        "linearScale": 1000.0,
        "unit": "TeV",
        "name": "stop1"
        
    },
    "t2" : {
        "title": "m_{#tilde{t}_{2}}",
        "nbin" : 100,
        "min" : 0,
        "max" : 6500,
        "logScale": False,
        "linearScale": 1000.0,
        "unit": "TeV",
        "name": "stop2"
        
    },
    "b1" : {
        "title": "m_{#tilde{b}_{1}}",
        "nbin" : 100,
        "min" : 0,
        "max" : 6500,
        "logScale": False,
        "linearScale": 1000.0,
        "unit": "TeV",
        "name": "sbottom"
    },
    "lcsp" : {
        "title" : "m_{lcsp}",
        "nbin" : 50,
        "min" : 0,
        "max" : 2500,
        "logScale" : False,
        "linearScale": 1000, # for TeV, 1GeV/1000
        "unit": "TeV",
        "name" : "lcsp"
        },
    "abs(chi1pm-chi10)": {
        "title": "#Deltam(#tilde{#chi}^{#pm}_{1},#tilde{#chi}^{0}_{1})",
        "nbin" : 100,
        "min" : 0,
        "max" : 2000,
        "logScale": True,
        "linearScale": 1.0,
        "unit": "GeV",
        "name" : "deltaM_pm10",
        "1Dlogy": False
    },
    "abs(chi20-chi10)": {
        "title": "#Deltam(#tilde{#chi}^{0}_{2},#tilde{#chi}^{0}_{1})",
        "nbin" : 100,
        "min" : 0,
        "max" : 2000,
        "logScale": True,
        "linearScale": 1.0,
        "unit": "GeV",
        "name" : "deltaM_20_10",
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
        "name" : "chipm"
        },
    }


individualAnalysis = {
    
}


class PMSSM:
    def __init__(self,intree,
                outdir : str,
                particleDrawConfig : dict,
                canvasStyle :dict = {
                    "energy" : "13",
                    "extraText" : "Preliminary",
                    "lumi" : "",
                },
                defaultExportFileFormat : str = "pdf"
                ):
        
        if outdir[-1]!="/":
                outdir+="/"
        if not os.path.exists(outdir):
                os.system("mkdir -p "+outdir)
        
        self.setCanvasStyle(canvasStyle)

        self.canvas =  None
        self.legend = None

        self.intree = intree
        self.outdir = outdir
        self.particleDrawConfig = particleDrawConfig
        self.fileFormat = defaultExportFileFormat
    @staticmethod
    def createLegend(x1,y1,x2,y2,textSize=0.03):
        return CMS.cmsLeg(x1,y1,x2,y2,textSize)

    @staticmethod
    def createSurvivalPlotPalette():
        custompalette = []
        cols = TColor.GetNumberOfColors()# This gets the colors of the Palette currently set in ROOT
        #This part sets bins with a survival probability of zero (less than second entry of sprobcontours list to be exact) to Black color. Bins with a survival probability of exactly 1 (greater than second last entry of sprobcontours list) to Grey.
        for i in range(cols):
            if i<19: # The exact i was found by trial and error. Sorry.
                col = kBlack
            # elif i > 253:
            #     col = kGray
            else:
                col = TColor.GetColorPalette(i) # This part keeps the color from the currently set palette
                
            custompalette.append(col)
        custompalette = np.intc(custompalette)
        return custompalette
    
    def setCanvasStyle(self,canvasStyle : dict):
        """ 
        Set the CMS style for the canvas.
        Parameters:
        canvasStyle : dict
            A dictionary with the following keys:
            - energy : int
                The energy of the analysis
            - extraText : str
                Extra text to be displayed on the plot
            - lumi : str
                The luminosity of the analysis
        """
        if canvasStyle.get("energy") is not None:
            CMS.SetEnergy(str(canvasStyle.get("energy")))
        if canvasStyle.get("extraText") is not None:
            CMS.SetExtraText(canvasStyle.get("extraText"))
        if canvasStyle.get("lumi") is not None:
            CMS.SetLumi(canvasStyle.get("lumi"))
        CMS.SetAlternativePalette(self.createSurvivalPlotPalette())
    
    @staticmethod
    def createCanvas(
        canvName:str,
        xmin:float,
        xmax:float,
        ymin:float,
        ymax:float,
        xtitle:str,
        ytitle:str,
        with_z_axis:bool = False,
        y_offset:float = 1.6,
        leftMarginOffset:float = 0.0
        ):
        """
        This function will be moved to setCanvas function.
        """
        """
        Create a CMS canvas.
        Parameters:
        canvName : str
            The name of the canvas
        xmin : float|int
            The lower limit of the x-axis
        xmax : float|int
            The upper limit of the x-axis
        ymin : float|int
            The lower limit of the y-axis
        ymax : float|int
            The upper limit of the y-axis
        xtitle : str
            The title of the x-axis
        ytitle : str
            The title of the y-axis
        with_z_axis : bool
            Whether to include a z-axis
        y_offset : float
            The offset for the y-axis
        leftMarginOffset : float
            The offset for the left margin
        Returns:
            canvas
        """
        
        if canvName=="":
            canvName = "default"+str(np.random.randint(0,100000))
        
        canv = CMS.cmsCanvas(
            canvName=canvName,
            x_min=xmin,
            x_max=xmax,
            y_min=ymin,
            y_max=ymax,
            nameXaxis=xtitle,
            nameYaxis=ytitle,
            square = CMS.kSquare, 
            iPos=0,
            with_z_axis=with_z_axis,
            y_offset = y_offset,
            leftMarginOffset = leftMarginOffset
            )
        return canv

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

    def flushCanvas(self):
        if self.canvas is not None:
            self.canvas.Clear()
            self.flushLegend()
            del self.canvas
            self.canvas = None
    
    def flushLegend(self):      
        if self.legend is not None:
            self.legend.Clear()
            del self.legend
            self.legend = None
    
    def setCanvas(
        self,
        obj, # WILL BE DEPRECATED
        xtitle:str,
        ytitle:str,
        y_offset:float = 0,
        offset:dict = {},
        range:dict = None,
        with_z_axis:bool = False,
        leftMarginOffset:float = 0.0
        ):
        if range is None:
            xmin, xmax, ymin, ymax = self.getAxisRange(obj,offset=offset)
        else:
            xmin, xmax, ymin, ymax = range["xmin"],range["xmax"],range["ymin"],range["ymax"]
            
            xmin -= offset.get("xmin",0.0)
            xmax += offset.get("xmax",0.0)
            ymin -= offset.get("ymin",0.0)
            ymax += offset.get("ymax",0.0)
            
        self.canvas = self.createCanvas(
            canvName="",
            xmin=xmin,
            xmax=xmax,
            ymin=ymin,
            ymax=ymax,
            xtitle=xtitle,
            ytitle=ytitle,
            with_z_axis=with_z_axis,
            y_offset = y_offset,
            leftMarginOffset = leftMarginOffset
            )
    
    def setConfig(self, particleName: str, config: dict, verbose: bool = False) -> None:
        
        if particleName is None:
            particleName = list(self.particleDrawConfig.keys())
        elif isinstance(particleName, str):
            particleName = [particleName]
            
        for particle in particleName:
            particle_config = self.particleDrawConfig.get(particle, {})
            for key, value in config.items():
                if particle_config.get(key.lower()) is not None:
                    particle_config[key.lower()] = value
                else:
                    if verbose:
                        print(f"Adding new configuration for {particle}: {key.lower()}={value}")
                    particle_config[key.lower()] = value
            self.particleDrawConfig[particle] = particle_config.copy()
            if verbose:
                self.printConfig(particleName=particle)
    
    def printConfig(self,particleName=None):
        if particleName is not None:
            print("#"*15,particleName,"#"*15)
            print("-Title: ",self.particleDrawConfig[particleName].get("title"))
            print("-# of Bins: ",self.particleDrawConfig[particleName].get("nbin"))
            print("-Max Range:",self.particleDrawConfig[particleName].get("max"))
            print("-Min Range:",self.particleDrawConfig[particleName].get("min"))
            print("-Log Scale:",self.particleDrawConfig[particleName].get("logScale"))
            print("-Linear Scale:",self.particleDrawConfig[particleName].get("linearScale"))
            print("-Unit:",self.particleDrawConfig[particleName].get("unit"))
        else:
            for particleName in self.particleDrawConfig.keys():
                print("#"*15,particleName,"#"*15)
                print("-Title: ",self.particleDrawConfig[particleName].get("title"))
                print("-# of Bins: ",self.particleDrawConfig[particleName].get("nbin"))
                print("-Max Range:",self.particleDrawConfig[particleName].get("max"))
                print("-Min Range:",self.particleDrawConfig[particleName].get("min"))
                print("-Log Scale:",self.particleDrawConfig[particleName].get("logScale"))
                print("-Linear Scale:",self.particleDrawConfig[particleName].get("linearScale"))
                print("-Unit:",self.particleDrawConfig[particleName].get("unit"))

    def getParticleConfig(self,particleName:str,overWrite:dict=None):
                
        try:
            if self.particleDrawConfig.get(particleName) is not None:
                particleConfig = self.particleDrawConfig[particleName].copy()
            else:
                particleConfig = self.particleDrawConfig["defaults"].copy()
                particleConfig["title"] = particleName 
        except:
                raise Exception("Missing Config for ",particleName)
        if overWrite is not None:
            for key in overWrite.keys():
                particleConfig[key] = overWrite[key]
        return particleConfig


    def createName(self,drawstring:str,analysis:str="combined",plotType:str=""):
        splitted = drawstring.split(":")
        name = ""
        if (len(splitted) == 2):
            
            
            xaxisParticleName = splitted[0]
            yaxisParticleName = splitted[1]
        
            
            if self.particleDrawConfig.get(xaxisParticleName) is not None:
                xaxisDrawConfig = self.particleDrawConfig[xaxisParticleName]
                xname = xaxisDrawConfig.get("name","")
            else:
                xname = ""
                
            if self.particleDrawConfig.get(yaxisParticleName) is not None:
                yaxisDrawConfig = self.particleDrawConfig[yaxisParticleName]
                yname = yaxisDrawConfig.get("name","")
            else:
                yname = ""

            if yname == "":
                name = xname
            else:
                name = yname + "_" + xname
        else:
            if self.particleDrawConfig.get(drawstring) is not None:
                xaxisDrawConfig = self.particleDrawConfig[drawstring]
                name = xaxisDrawConfig.get("name","")
            else:
                name = ""
        
        if analysis !="":
            name += "_"+analysis.upper()
        if plotType !="":
            name += "_"+plotType
        
        
        name = name.replace(".","p")
        
        return  name
        
    @staticmethod
    def setPaletteStyle(palette,cmsStyle):
        palette.SetTitleFont(cmsStyle.GetTitleFont())
        palette.SetTitleSize(0.042)
        palette.SetLabelSize(0.0381)
        palette.SetTitleOffset(1.15)
        palette.SetLabelFont(cmsStyle.GetLabelFont())
                    
    
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
        canvasStyle : dict = {
            "offset": {
                "ymax":0.002
            },
            "legend": {
                "x1":0.19,
                "y1":0.71,
                "x2":0.36,
                "y2":0.9,
                "textSize":0.035
            }
        }
        ):
        
        self.flushCanvas()
        self.flushLegend()
        
        xaxisParticleName = drawstring
        
        name = self.createName(drawstring,analysis,"impact1D")
        
        xaxisDrawConfig = self.getParticleConfig(xaxisParticleName,xaxisDrawConfig)

        impact_plots = get_impact_plots(
            localtree = self.intree,
            analysis = analysis,
            hname = name,
            xtitle = xaxisDrawConfig["title"] + " ["+xaxisDrawConfig["unit"]+"]",
            xbins = xaxisDrawConfig["nbin"],
            xlow = xaxisDrawConfig["min"],
            xup = xaxisDrawConfig["max"],
            _logx = xaxisDrawConfig.get("logScale", False), # TODO DEBUG THIS
            drawstring = drawstring,
            moreconstraints = moreconstraints,
            moreconstraints_prior = moreconstraints_prior)
                
        for key in impact_plots:
            hist = impact_plots[key]
            if not xaxisDrawConfig.get("logScale", False):
                scaleXaxis(hist,scaleFactor=xaxisDrawConfig.get("linearScale"))
                
                
        axis_range = {
            "xmin": None,
            "xmax": None,
            "ymin": None,
            "ymax": None
        }
        for key in impact_plots:
            hist = impact_plots[key]
            xmin,xmax,ymin,ymax = self.getAxisRange(hist)    
            if xaxisDrawConfig.get("1Dlogy", False) and ymin==0:
                hist.GetYaxis().SetRangeUser(1,ymax)
                ymin = 1
            if axis_range["xmin"] is None or xmin < axis_range["xmin"]:
                axis_range["xmin"] = xmin
            if axis_range["xmax"] is None or xmax > axis_range["xmax"]:
                axis_range["xmax"] = xmax
            if axis_range["ymin"] is None or ymin < axis_range["ymin"]:
                axis_range["ymin"] = ymin
            if axis_range["ymax"] is None or ymax > axis_range["ymax"]:
                axis_range["ymax"] = ymax                
        self.setCanvas(impact_plots["prior"],xaxisDrawConfig["title"]+ " ["+xaxisDrawConfig["unit"]+"]", "pMSSM Density", offset={
            "xmin":canvasStyle.get("offset",{}).get("xmin",0.0),
            "xmax":canvasStyle.get("offset",{}).get("xmax",0.0),
            "ymin":canvasStyle.get("offset",{}).get("ymin",0.0),
            "ymax":canvasStyle.get("offset",{}).get("ymax",0.002)
            },range=axis_range, y_offset = 0.63, leftMarginOffset=0.03)
        
        if xaxisDrawConfig.get("logScale", False):
            self.canvas.SetLogx()
        if xaxisDrawConfig.get("1Dlogy", False):
            self.canvas.SetLogy()
        
        self.legend = self.createLegend(
            x1=canvasStyle.get("legend",{}).get("x1",0.19),
            y1=canvasStyle.get("legend",{}).get("y1",0.73),
            x2=canvasStyle.get("legend",{}).get("x2",0.36),
            y2=canvasStyle.get("legend",{}).get("y2",0.9),
            textSize=canvasStyle.get("legend",{}).get("textSize",0.035)
            )
        self.legend.SetHeader(analysis.upper())
        self.legend.AddEntry(impact_plots["prior"],"prior")
        self.legend.AddEntry(impact_plots["posterior"],"posterior (#sigma = #sigma_{nominal} )")
        self.legend.AddEntry(impact_plots["posterior_up"],"posterior (#sigma = 1.5#times#sigma_{nominal} )")
        self.legend.AddEntry(impact_plots["posterior_down"],"posterior (#sigma =0.5#times#sigma_{nominal} )")
                
        impact_plots["prior"].Draw("hist same")
        impact_plots["posterior"].Draw("histsame")
        impact_plots["posterior_up"].Draw("histsame")
        impact_plots["posterior_down"].Draw("histsame")
        self.legend.SetTextColor(canvasStyle.get("legend",{}).get("textColor",kBlack))
        self.legend.Draw("same")
        CMS.SaveCanvas(self.canvas,self.outdir+name+"."+self.fileFormat)
    
    def survivalProbability1D(
        self,
        drawstring : str, 
        analysis : str = "combined",
        moreconstraints : list = [], 
        moreconstraints_prior : bool =False,
        xaxisDrawConfig : dict = None,
        canvasStyle : dict = {
            "offset": {
                "ymax":0.002
            },
            "legend": {
                "x1":0.19,
                "y1":0.71,
                "x2":0.36,
                "y2":0.9,
                "textSize":0.035
            }
        }
        ):
        
        self.flushCanvas()
        self.flushLegend()
        
        xaxisParticleName = drawstring
        
        name = self.createName(drawstring,analysis,"survival1D")
        
        xaxisDrawConfig = self.getParticleConfig(xaxisParticleName,xaxisDrawConfig)

        survive_plots = get_SP_plot_1D(
            localtree = self.intree,
            analysis = analysis,
            hname = name,
            xtitle = xaxisDrawConfig["title"] + " ["+xaxisDrawConfig["unit"]+"]",
            xbins = xaxisDrawConfig["nbin"],
            xlow = xaxisDrawConfig["min"],
            xup = xaxisDrawConfig["max"],
            _logx = xaxisDrawConfig.get("logScale", False), # TODO DEBUG THIS
            drawstring = drawstring,
            moreconstraints = moreconstraints,
            moreconstraints_prior = moreconstraints_prior)
                
        for key in survive_plots:
            hist = survive_plots[key]
            if not xaxisDrawConfig.get("logScale", False):
                scaleXaxis(hist,scaleFactor=xaxisDrawConfig.get("linearScale"))
                
                
        axis_range = {
            "xmin": None,
            "xmax": None,
            "ymin": None,
            "ymax": None
        }
        for key in survive_plots:
            hist = survive_plots[key]
            xmin,xmax,ymin,ymax = self.getAxisRange(hist)    
            if xaxisDrawConfig.get("1Dlogy", False) and ymin==0:
                hist.GetYaxis().SetRangeUser(1,ymax)
                ymin = 1
            if axis_range["xmin"] is None or xmin < axis_range["xmin"]:
                axis_range["xmin"] = xmin
            if axis_range["xmax"] is None or xmax > axis_range["xmax"]:
                axis_range["xmax"] = xmax
            if axis_range["ymin"] is None or ymin < axis_range["ymin"]:
                axis_range["ymin"] = ymin
            if axis_range["ymax"] is None or ymax > axis_range["ymax"]:
                axis_range["ymax"] = ymax                
        self.setCanvas(survive_plots["posterior"],xaxisDrawConfig["title"]+ " ["+xaxisDrawConfig["unit"]+"]", "Survival Probability", offset={
            "xmin":canvasStyle.get("offset",{}).get("xmin",0.0),
            "xmax":canvasStyle.get("offset",{}).get("xmax",0.0),
            "ymin":canvasStyle.get("offset",{}).get("ymin",0.0),
            "ymax":canvasStyle.get("offset",{}).get("ymax",0.002)
            },range=axis_range, y_offset = 0.63, leftMarginOffset=0.03)
        
        if xaxisDrawConfig.get("logScale", False):
            self.canvas.SetLogx()
        if xaxisDrawConfig.get("1Dlogy", False):
            self.canvas.SetLogy()
        
        self.legend = self.createLegend(
            x1=canvasStyle.get("legend",{}).get("x1",0.19),
            y1=canvasStyle.get("legend",{}).get("y1",0.73),
            x2=canvasStyle.get("legend",{}).get("x2",0.36),
            y2=canvasStyle.get("legend",{}).get("y2",0.9),
            textSize=canvasStyle.get("legend",{}).get("textSize",0.035)
            )
        self.legend.SetHeader(analysis.upper())
        self.legend.AddEntry(survive_plots["posterior"],"posterior (#sigma = #sigma_{nominal} )")
        self.legend.AddEntry(survive_plots["posterior_up"],"posterior (#sigma = 1.5#times#sigma_{nominal} )")
        self.legend.AddEntry(survive_plots["posterior_down"],"posterior (#sigma =0.5#times#sigma_{nominal} )")
                
        survive_plots["posterior"].Draw("histsame")
        survive_plots["posterior_up"].Draw("histsame")
        survive_plots["posterior_down"].Draw("histsame")
        self.legend.SetTextColor(canvasStyle.get("legend",{}).get("textColor",kBlack))
        self.legend.Draw("same")
        CMS.SaveCanvas(self.canvas,self.outdir+name+"."+self.fileFormat)
    
    def survivalProbability2D(self,
                                drawstring : str,
                                analysis : str = "combined" ,
                                contourSwitch : bool= True,  
                                moreconstraints : list = [], 
                                moreconstraints_prior : bool =False,
                                xaxisDrawConfig : dict = None,
                                yaxisDrawConfig : dict = None,
                                canvasStyle : dict = {
                                    "offset": {
                                        "ymax":0.002
                                    },
                                    "legend": {
                                        "x1":0.15,
                                        "y1":0.76,
                                        "x2":0.62,
                                        "y2":0.9,
                                        "textSize":0.030,
                                        "legendNColumns": 2
                                    }
                                }
                            ):        
        self.flushCanvas()
        self.flushLegend()
    
        yaxisParticleName, xaxisParticleName = drawstring.split(":")
        
        name = self.createName(drawstring,analysis,"contours_survival2D"if contourSwitch else "survival2D")

        xaxisDrawConfig = self.getParticleConfig(xaxisParticleName,xaxisDrawConfig)
        yaxisDrawConfig = self.getParticleConfig(yaxisParticleName,yaxisDrawConfig)

        
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
        
        if not xaxisDrawConfig.get("logScale", False):
            scaleXaxis(hist,scaleFactor=xaxisDrawConfig.get("linearScale"))
        if not yaxisDrawConfig.get("logScale", False):
            scaleYaxis(hist,scaleFactor=yaxisDrawConfig.get("linearScale"))
        
        axisRange = {
            "xmin": xaxisDrawConfig["min"]/xaxisDrawConfig.get("linearScale",1.0),
            "xmax": xaxisDrawConfig["max"]/xaxisDrawConfig.get("linearScale",1.0),
            "ymin": yaxisDrawConfig["min"]/yaxisDrawConfig.get("linearScale",1.0),
            "ymax": yaxisDrawConfig["max"]/yaxisDrawConfig.get("linearScale",1.0)
        }
        
        
        if xaxisDrawConfig.get("logScale", False):
            for key in ["xmin","xmax"]:
                if axisRange[key] == 0:
                    axisRange[key] = 1
        if yaxisDrawConfig.get("logScale", False):
            for key in ["ymin","ymax"]:
                if axisRange[key] == 0:
                    axisRange[key] = 1
        
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
            
            self.setCanvas(
                hist,
                xaxisDrawConfig["title"] + " ["+xaxisDrawConfig["unit"]+"]", 
                yaxisDrawConfig["title"] + " ["+yaxisDrawConfig["unit"]+"]", 
                offset={
                    "xmin":canvasStyle.get("offset",{}).get("xmin",0.0),
                    "xmax":canvasStyle.get("offset",{}).get("xmax",0.0),
                    "ymin":canvasStyle.get("offset",{}).get("ymin",0.0),
                    "ymax":canvasStyle.get("offset",{}).get("ymax",0.0)
                    },
                range=axisRange,
                with_z_axis=True,
                )
            
            if xaxisDrawConfig.get("logScale", False):
                self.canvas.SetLogx()
            if yaxisDrawConfig.get("logScale", False):
                self.canvas.SetLogy()
            
            
            self.legend = self.createLegend(
                x1=canvasStyle.get("legend",{}).get("x1",0.15),
                y1=canvasStyle.get("legend",{}).get("y1",0.76),
                x2=canvasStyle.get("legend",{}).get("x2",0.62),
                y2=canvasStyle.get("legend",{}).get("y2",0.90),
                textSize=canvasStyle.get("legend",{}).get("textSize",0.030)
                )
            self.legend.SetHeader(analysis.upper())  
            
                        
            hist.GetZaxis().SetTitle("Survival Probability")
            # hist.GetZaxis().SetLabelSize(0.0375)
            # hist.GetZaxis().SetTitleSize(0.05)
            hist.Draw("same colz")
            cmsStyle = CMS.getCMSStyle()
            palette = CMS.GetPalette(hist)
            self.setPaletteStyle(palette,cmsStyle)
            # gStyle.SetPalette(len(self.createSurvivalPlotPalette()),self.createSurvivalPlotPalette())
            CMS.SetAlternativePalette(self.createSurvivalPlotPalette())
            CMS.SetAlternative2DColor(hist=hist)
            for ix,interval in enumerate(prior_data):
                for cont in prior_data[interval]:
                    if not xaxisDrawConfig.get("logScale", False):
                        scaleGraphXaxis(cont,scaleFactor=xaxisDrawConfig.get("linearScale"))
                    if not yaxisDrawConfig.get("logScale", False):
                        scaleGraphYaxis(cont,scaleFactor=yaxisDrawConfig.get("linearScale"))
                    cont.Draw("same")
            for ix,interval in enumerate(posterior_data):
                for cont in posterior_data[interval]:
                    if not xaxisDrawConfig.get("logScale", False):
                        scaleGraphXaxis(cont,scaleFactor=xaxisDrawConfig.get("linearScale"))
                    if not yaxisDrawConfig.get("logScale", False):
                        scaleGraphYaxis(cont,scaleFactor=yaxisDrawConfig.get("linearScale"))
                    cont.Draw("same")
            for ix,interval in enumerate(prior_data):
                if len(prior_data[interval])>0:
                    self.legend.AddEntry(prior_data[interval][0],str(int(100*(interval)))+"%  prior CI","l",)
                if len(posterior_data[interval])>0:
                    self.legend.AddEntry(posterior_data[interval][0],str(int(100*(interval)))+"% posterior CI","l",)
            self.legend.SetNColumns(canvasStyle.get("legend",{}).get("legendNColumns",2))
            self.legend.Draw("same")
            self.legend.SetTextColor(canvasStyle.get("legend",{}).get("textColor",kBlack))
            CMS.UpdatePalettePosition(hist,X1=0.855,X2=0.89,Y1=0.145,Y2=0.93)
        else:
            
            self.setCanvas(
                hist,
                xaxisDrawConfig["title"] + " ["+xaxisDrawConfig["unit"]+"]", 
                yaxisDrawConfig["title"] + " ["+yaxisDrawConfig["unit"]+"]", 
                offset={
                    "xmin":canvasStyle.get("offset",{}).get("xmin",0.0),
                    "xmax":canvasStyle.get("offset",{}).get("xmax",0.0),
                    "ymin":canvasStyle.get("offset",{}).get("ymin",0.0),
                    "ymax":canvasStyle.get("offset",{}).get("ymax",0.0)
                    },
                range=axisRange,
                with_z_axis=True,
                y_offset = 1,
                )
            
            hist.GetZaxis().SetTitle("Survival Probability")
            hist.GetZaxis().SetLabelSize(0.03)
            hist.GetZaxis().SetTitleSize(0.04)
            hist.GetZaxis().SetTitleOffset(1)
            CMS.SetAlternative2DColor(hist=hist)
            
            hist.Draw("same colz")
            self.legend = self.createLegend(
                x1=canvasStyle.get("legend",{}).get("x1",0.15),
                y1=canvasStyle.get("legend",{}).get("y1",0.87),
                x2=canvasStyle.get("legend",{}).get("x2",0.55),
                y2=canvasStyle.get("legend",{}).get("y2",0.91),
                textSize=canvasStyle.get("legend",{}).get("textSize",0.025)
                )
            self.legend.SetHeader(analysis.upper())
            self.legend.SetTextColor(canvasStyle.get("legend",{}).get("textColor",kBlack))
            CMS.UpdatePalettePosition(hist,X1=0.88,X2=0.91,Y1=0.108,Y2=0.93)
            
        CMS.SaveCanvas(self.canvas,self.outdir+name+"."+self.fileFormat)

    def quantilePlots1D(self,
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
                canvasStyle : dict = {
                    "offset": {
                        "ymax":0.1
                    },
                    "legend": {
                        "x1":0.19,
                        "y1":0.73,
                        "x2":0.36,
                        "y2":0.9,
                        "textSize":0.035
                    }
                },
                ):
        self.flushCanvas()
        self.flushLegend()
        
        xaxisParticleName = drawstring
        
        name = self.createName(drawstring,analysis,"quantile1D")
        
        xaxisDrawConfig = self.getParticleConfig(xaxisParticleName,xaxisDrawConfig)
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
                scaleXaxis(hist,scaleFactor=xaxisDrawConfig.get("linearScale"))
        axis_range = {
            "xmin": None,
            "xmax": None,
            "ymin": None,
            "ymax": None
        }
        for key in quantiles_hists:
            hist = quantiles_hists[key]
            xmin,xmax,ymin,ymax = self.getAxisRange(hist)    
            if xaxisDrawConfig.get("1Dlogy", False) and ymin==0:
                hist.GetYaxis().SetRangeUser(1,ymax)
                ymin = 1
            if axis_range["xmin"] is None or xmin < axis_range["xmin"]:
                axis_range["xmin"] = xmin
            if axis_range["xmax"] is None or xmax > axis_range["xmax"]:
                axis_range["xmax"] = xmax
            if axis_range["ymin"] is None or ymin < axis_range["ymin"]:
                axis_range["ymin"] = ymin
            if axis_range["ymax"] is None or ymax > axis_range["ymax"]:
                axis_range["ymax"] = ymax  
            
                            
        
        self.setCanvas(quantiles_hists[list(quantiles_hists.keys())[0]],
                       xaxisDrawConfig["title"]+ " ["+xaxisDrawConfig["unit"]+"]", 
                       "Bayes Factor", 
                       offset={
                            "xmin":canvasStyle.get("offset",{}).get("xmin",0.0),
                            "xmax":canvasStyle.get("offset",{}).get("xmax",0.0),
                            "ymin":canvasStyle.get("offset",{}).get("ymin",0.0),
                            "ymax":canvasStyle.get("offset",{}).get("ymax",0.0)
                            },
                       range=axis_range,y_offset = 0.5, leftMarginOffset=0.02)
        
        if xaxisDrawConfig.get("logScale", False):
            self.canvas.SetLogx()
        if xaxisDrawConfig.get("1Dlogy", False):
            self.canvas.SetLogy()
        
        self.legend = self.createLegend(
            x1=canvasStyle.get("legend",{}).get("x1",0.19),
            y1=canvasStyle.get("legend",{}).get("y1",0.73),
            x2=canvasStyle.get("legend",{}).get("x2",0.36),
            y2=canvasStyle.get("legend",{}).get("y2",0.9),
            textSize=canvasStyle.get("legend",{}).get("textSize",0.035)
            )
        self.legend.SetHeader(analysis.upper())
        
        for i in quantiles:
            histname = "quantile_" + str(int(100 * float(i)))
            hist_style = quantiles[i]
            hist = quantiles_hists[histname]
            
            if hist_style.get("color") is not None:
                hist.SetLineColor(hist_style["color"])
            if hist_style.get("linestyle") is not None:
                hist.SetLineStyle(hist_style["linestyle"])
            
            self.legend.AddEntry(hist,str(int(100 * float(i)))+"th Percentile")
            
        for key in quantiles_hists:
            hist = quantiles_hists[key]
            hist.Draw("hist same")
        
        CMS.SaveCanvas(self.canvas,self.outdir+name+"."+self.fileFormat)

    def quantilePlots2D(self,
                drawstring : str, 
                quantile : float,
                analysis : str = "combined",
                moreconstraints : list = [], 
                moreconstraints_prior : bool =False,
                xaxisDrawConfig : dict = None,
                yaxisDrawConfig : dict = None,
                canvasStyle : dict = {
                    "offset": {
                        "ymax":0.002
                    },
                    "legend": {
                        "x1":0.14,
                        "y1":0.86,
                        "x2":0.66,
                        "y2":0.9,
                        "textSize":0.030,
                        "legendNColumns": 2
                    }
                }
                ):
    

        self.flushCanvas()
        self.flushLegend()
        
        yaxisParticleName, xaxisParticleName = drawstring.split(":")
        
        name = self.createName(drawstring,analysis, str(quantile)+ "_"+"quantile2D")
        
        xaxisDrawConfig = self.getParticleConfig(xaxisParticleName,xaxisDrawConfig)
        yaxisDrawConfig = self.getParticleConfig(yaxisParticleName,yaxisDrawConfig)

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
            scaleXaxis(hist,scaleFactor=xaxisDrawConfig.get("linearScale"))
        if not yaxisDrawConfig.get("logScale", False):
            scaleYaxis(hist,scaleFactor=yaxisDrawConfig.get("linearScale"))
            
        axisRange = {
            "xmin": xaxisDrawConfig["min"]/xaxisDrawConfig.get("linearScale",1.0),
            "xmax": xaxisDrawConfig["max"]/xaxisDrawConfig.get("linearScale",1.0),
            "ymin": yaxisDrawConfig["min"]/yaxisDrawConfig.get("linearScale",1.0),
            "ymax": yaxisDrawConfig["max"]/yaxisDrawConfig.get("linearScale",1.0)
        }
        if xaxisDrawConfig.get("logScale", False):
            for key in ["xmin","xmax"]:
                if axisRange[key] == 0:
                    axisRange[key] = 1
        if yaxisDrawConfig.get("logScale", False):
            for key in ["ymin","ymax"]:
                if axisRange[key] == 0:
                    axisRange[key] = 1
        
        self.setCanvas(
            hist,
            xaxisDrawConfig["title"] + " ["+xaxisDrawConfig["unit"]+"]", 
            yaxisDrawConfig["title"] + " ["+yaxisDrawConfig["unit"]+"]", 
            offset={
                "xmin":canvasStyle.get("offset",{}).get("xmin",0.0),
                "xmax":canvasStyle.get("offset",{}).get("xmax",0.0),
                "ymin":canvasStyle.get("offset",{}).get("ymin",0.0),
                "ymax":canvasStyle.get("offset",{}).get("ymax",0.0)
                },
            range=axisRange,
            with_z_axis=True,
            y_offset=0.125 if yaxisDrawConfig.get("logScale", False) else 0
            )
        if xaxisDrawConfig.get("logScale", False):
            self.canvas.SetLogx()
        if yaxisDrawConfig.get("logScale", False):
            self.canvas.SetLogy()
            # self.canvas.GetPrimitive("hframe").GetYaxis().CenterTitle(True)
        hist.Draw("same colz")
        hist.GetZaxis().SetTitle(str(int(100 * quantile)) + "th Percentile Bayes Factor")
        cmsStyle = CMS.getCMSStyle()
        palette = CMS.GetPalette(hist)
        self.setPaletteStyle(palette,cmsStyle)
        CMS.SetAlternativePalette(self.createSurvivalPlotPalette())
        #CMS.SetAlternative2DColor(hist=hist)
        hist.SetContour(999)
        CMS.SetCMSPalette()
        # CMS.SetRootPalette(kBird)
        
        self.legend = self.createLegend(
            x1=canvasStyle.get("legend",{}).get("x1",0.14),
            y1=canvasStyle.get("legend",{}).get("y1",0.86),
            x2=canvasStyle.get("legend",{}).get("x2",0.66),
            y2=canvasStyle.get("legend",{}).get("y2",0.9),
            textSize=canvasStyle.get("legend",{}).get("textSize",0.030)
            )
        self.legend.SetHeader(analysis.upper())
        self.legend.SetTextColor(canvasStyle.get("legend",{}).get("textColor",kBlack))
        CMS.UpdatePalettePosition(hist,X1=0.855,X2=0.89,Y1=0.145,Y2=0.93)
        CMS.SaveCanvas(self.canvas,self.outdir+name+"."+self.fileFormat)