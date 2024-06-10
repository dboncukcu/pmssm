from ROOT import *
from PlotterConfig import PlotterConfig
import PlotterUtils
from cmsstylelib import cmsstyle as CMS
from Constraints import Constraints
from typing import Union
import numpy as np
import copy

gROOT.SetBatch(True)

YELLOW = '\033[93m'
BLUE = '\033[94m'
ORANGE = '\033[38;5;214m'
GREEN = '\033[92m'
STRIKETHROUGH = '\033[9m'
BOLD = '\033[1m'
RESET = '\033[0m'
BULLET = '•'


class PMSSM:
    def __init__(
        self,
        root_dict: list[dict],
        config: PlotterConfig = None
    ):  
        # Binding Config to the class
        if config is None:
            self.c = PlotterConfig()
        else:
            self.c = config
        
        self.constraints = Constraints(self.c.analysisConfigs)
        
        if self.c.cms_label.get("energy") is not None:
            CMS.SetEnergy(str(self.c.cms_label.get("energy")))
        if self.c.cms_label.get("extraText") is not None:
            CMS.SetExtraText(self.c.cms_label.get("extraText"))
        if self.c.cms_label.get("lumi") is not None:
            CMS.SetLumi(self.c.cms_label.get("lumi"))
        
        # Reading root files
        self.tree,self.file = PlotterUtils.create_tree(root_dict)
        
        # create an output directory
        self.outputpath =  PlotterUtils.create_output_directory( self.c.global_settings["outputPath"])
        self.defaultFileFormat = self.c.global_settings["outputFileFormat"]
    def createName(self,xaxisDrawConfig, yaxisDrawConfig:dict= None, analysis:str="combined", plotType:str=""):
        
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
        
        analysis = analysis.replace(" ","_")
        if analysis !="":
            name += "_"+analysis.upper()
        if plotType !="":
            name += "_"+plotType
        
        
        name = name.replace(".","p")
        name = name.replace("(","")
        name = name.replace(")","")

        return  name
    
    def getParticleConfigValue(self, drawConfig:dict, key:str):
        return drawConfig.get(key, self.c.particleConfig["default"][key])

    def impact1D(
        self,
        drawstring : str, 
        analysis : str = "combined",
        moreconstraints : list = [], 
        moreconstraints_prior : bool =False,
        xaxisDrawConfig : dict = None,
        drawConfig: Union[dict, str] = None,
        legendStyle: Union[dict, str] = None):
        print("_____________________________",f"{BOLD}{ORANGE}1D Impact{RESET} for{BOLD}{BLUE}", drawstring, f"{RESET}","_____________________________")
        
        if drawConfig is None:
            drawConfig = self.c.drawConfig["impact1D"]
        else:
            drawConfigCopy = copy.copy(self.c.drawConfig["impact1D"])
            drawConfigCopy.update(drawConfig)
            drawConfig = drawConfigCopy
            
        
        if legendStyle is None:
            legendStyle = "rightBottom"
        if isinstance(legendStyle, str):
            legendConfig = drawConfig.get("legendStyle",legendStyle)
        if isinstance(legendStyle, dict):
            legendConfig = legendStyle
        legendConfig = self.c.drawConfig["impact1D"][legendConfig]
        
        if xaxisDrawConfig is None:
            xaxisDrawConfig = self.c.particleConfig[drawstring]
        else:
            particleConfigCopy = copy.copy(self.c.particleConfig[drawstring])
            particleConfigCopy.update(xaxisDrawConfig)
            xaxisDrawConfig = particleConfigCopy
        ## Variables
        xbins = self.getParticleConfigValue(xaxisDrawConfig, "bins")
        xlow = self.getParticleConfigValue(xaxisDrawConfig, "min")
        xup = self.getParticleConfigValue(xaxisDrawConfig, "max")
        xlog = self.getParticleConfigValue(xaxisDrawConfig, "logScale")
        xtitle = self.getParticleConfigValue(xaxisDrawConfig, "title")
        xunit = self.getParticleConfigValue(xaxisDrawConfig, "unit")
        
        ## Create Histogram Name
        
        name = self.createName(xaxisDrawConfig, analysis=analysis, plotType="impact1D")
        
        if "simplified" in analysis:  # reweighting is always done, in addition to removing unreasonable points
            constraintstring_prior = "*".join([self.c.theconstraints["reweight"], self.c.theconstraints["reason_simplified"]])    
            constraintstring = "*".join([self.c.theconstraints["reweight"], self.c.theconstraints["reason_simplified"], self.constraints.getConstraint(analysis,isSimplified=True)])
        else:
            constraintstring_prior = "*".join([self.c.theconstraints["reweight"], self.c.theconstraints["reason"]]) 
            constraintstring = "*".join([self.c.theconstraints["reweight"], self.c.theconstraints["reason"],self.constraints.getConstraint(analysis,isSimplified=False)])
            
        for newc in moreconstraints:
            constraintstring += "*(" + newc + ")"
        if moreconstraints_prior:
            for newc_p in moreconstraints_prior:
                constraintstring_prior += "*(" + newc_p + ")"
                
        # get the scales to normalize all histograms to one
        htest = TH1F("scale", "", 1000, -1000, 1000)
        # print('constraintstring prior', constraintstring_prior)
        self.tree.Draw("PickProbability>>" + htest.GetName(), constraintstring_prior)
        prior_scalar = 1. / htest.Integral(-1, 9999999)
        htest.Delete()
        htest = TH1F("scale", "", 1000, -1000, 1000)
        # print('constraintstring posterior', constraintstring)
        self.tree.Draw("PickProbability>>" + htest.GetName(),constraintstring)
        # print("\n\n")
        posterior_scalar = 1. / htest.Integral(-1, 9999999)
        htest.Delete()
        htest = TH1F("scale", "", 1000, -1000, 1000)
        self.tree.Draw("PickProbability>>" + htest.GetName(),constraintstring.replace('mu1p0','mu1p5').replace('_100s','_150s'))#UP
        posterior_scalar_up = 1. / htest.Integral(-1, 9999999)
        htest.Delete()
        htest = TH1F("scale", "", 1000, -1000, 1000)
        self.tree.Draw("PickProbability>>" + htest.GetName(),constraintstring.replace('mu1p0','mu0p5').replace('_100s','_050s'))#Down
        posterior_scalar_down = 1. / htest.Integral(-1, 9999999)
        htest.Delete()
        
        prior = PlotterUtils.mkhistlogx("prior", "", xbins, xlow, xup, logx=xlog)
        posterior = prior.Clone(name)
        posterior_up = prior.Clone(name+"_up")
        posterior_down = prior.Clone(name+"_down")
        
        self.tree.Draw(drawstring + ">>" + prior.GetName(), constraintstring_prior)
        self.tree.Draw(drawstring + ">>" + posterior.GetName(), constraintstring)
        self.tree.Draw(drawstring + ">>" + posterior_up.GetName(), constraintstring.replace('mu1p0','mu1p5').replace('_100s','_150s'))
        self.tree.Draw(drawstring + ">>" + posterior_down.GetName(), constraintstring.replace('mu1p0','mu0p5').replace('_100s','_050s'))
        
        PlotterUtils.histoStyler(prior, kBlue - 9, fill=True)
        PlotterUtils.histoStyler(posterior, kBlack)
        PlotterUtils.histoStyler(posterior_down, kRed, linestyle=kDashed)
        PlotterUtils.histoStyler(posterior_up, kMagenta, linestyle=kDashed)
        
        
        prior.Scale(prior_scalar)
        posterior.Scale(posterior_scalar)
        posterior_up.Scale(posterior_scalar_up)
        posterior_down.Scale(posterior_scalar_down)
        
        maxy = max([prior.GetMaximum(), posterior.GetMaximum(), posterior_down.GetMaximum(), posterior_up.GetMaximum()])
        
        miny = 0 if not xaxisDrawConfig.get("1Dlogy", False) else self.c.global_settings["logEps"]
        
        prior.GetYaxis().SetRangeUser(miny, 1.1 * maxy)
        prior.GetXaxis().SetTitle(xtitle)
        
        posterior.GetYaxis().SetRangeUser(miny, 1.1 * maxy)
        posterior.GetXaxis().SetTitle(xtitle)
        
        posterior_up.GetYaxis().SetRangeUser(miny, 1.1 * maxy)
        posterior_up.GetXaxis().SetTitle(xtitle)
        
        posterior_down.GetYaxis().SetRangeUser(miny, 1.1 * maxy)
        posterior_down.GetXaxis().SetTitle(xtitle)
        
        prior.GetYaxis().SetTitle("pMSSM density")
        posterior.GetYaxis().SetTitle("pMSSM density")
        posterior_up.GetYaxis().SetTitle("pMSSM density")
        posterior_down.GetYaxis().SetTitle("pMSSM density")
        
        for hist in [prior, posterior, posterior_up, posterior_down]:
            if not xaxisDrawConfig.get("logScale", False):
                PlotterUtils.scaleXaxis(hist,scaleFactor=xaxisDrawConfig.get("linearScale"))
        
        
        cxmin, cxmax, cymin, cymax = PlotterUtils.getAxisRangeOfList([prior, posterior, posterior_up, posterior_down])
        
        if xaxisDrawConfig.get("1Dlogy", False):
            if cymin == 0:
                cymin = self.c.global_settings["logEps"]
        
        cymax += drawConfig.get("yMaxOffsett", 0)
        
        canvas = CMS.cmsCanvas(
            x_min = cxmin,
            x_max = cxmax,
            y_min = cymin,
            y_max = cymax,
            nameXaxis = f"{xtitle} [{xunit}]",
            nameYaxis = "pMSSM density",
            canvName = name,
            square = CMS.kSquare,
            iPos = 0,
            leftMargin = 0.08,
            bottomMargin = 0.035,
            with_z_axis = False,
            scaleLumi = None,
            customStyle= {
                "SetXNdivisions": xaxisDrawConfig.get("Ndivisions",510)
            })
        
        if xaxisDrawConfig.get("logScale", False):
            canvas.SetLogx()
        if xaxisDrawConfig.get("1Dlogy", False):
            canvas.SetLogy()

        prior.Draw("hist same")
        posterior.Draw("hist same")
        posterior_up.Draw("hist same")
        posterior_down.Draw("hist same")
        
        legend = CMS.cmsLeg(
            x1 = legendConfig["x1"],
            y1 = legendConfig["y1"],
            x2 = legendConfig["x2"],
            y2 = legendConfig["y2"],
            columns = legendConfig.get("numberOfColumns",1),
            textSize = 0.03)
        

        legend.SetHeader(self.constraints.getAnalysisName(analysis),"C")
        legend.AddEntry(prior,"prior")
        legend.AddEntry(posterior,"posterior (#sigma = #sigma_{nominal} )")
        legend.AddEntry(posterior_up,"posterior (#sigma = 1.5#times#sigma_{nominal} )")
        legend.AddEntry(posterior_down,"posterior (#sigma =0.5#times#sigma_{nominal} )")
        hframe = CMS.GetcmsCanvasHist(canvas)
        hframe.GetYaxis().SetTitleOffset(drawConfig.get("YaxisSetTitleOffset",1.7))
        hframe.GetXaxis().SetTitleOffset(drawConfig.get("XaxisSetTitleOffset",1.05))

        if drawConfig.get("legendFillWhite",False):
            PlotterUtils.makeLegendFillWhite(legend)

        legend.Draw("same")
        CMS.SaveCanvas(canvas, self.outputpath+name+"."+self.defaultFileFormat, close=True)
        print("_______________________________________________________________________________________\n\n")
        
    def survivalProbability1D(
        self,
        drawstring : str,
        analysis : str = "combined",
        moreconstraints : list = [], 
        moreconstraints_prior : bool =False,
        xaxisDrawConfig : dict = None,
        drawConfig: Union[dict, str] = None,
        legendStyle: Union[dict, str] = None):
        print("_____________________________",f"{BOLD}{ORANGE}1D Survival Probability{RESET} for{BOLD}{BLUE}", drawstring, f"{RESET}","_____________________________")
        
        if drawConfig is None:
            drawConfig = self.c.drawConfig["survival1D"]
        else:
            drawConfigCopy = copy.copy(self.c.drawConfig["survival1D"])
            drawConfigCopy.update(drawConfig)
            drawConfig = drawConfigCopy
            
        
        if legendStyle is None:
            legendStyle = "rightBottom"
        if isinstance(legendStyle, str):
            legendConfig = drawConfig.get("legendStyle",legendStyle)
        if isinstance(legendStyle, dict):
            legendConfig = legendStyle
        legendConfig = self.c.drawConfig["survival1D"][legendConfig]
        
        if xaxisDrawConfig is None:
            xaxisDrawConfig = self.c.particleConfig[drawstring]
        else:
            particleConfigCopy = copy.copy(self.c.particleConfig[drawstring])
            particleConfigCopy.update(xaxisDrawConfig)
            xaxisDrawConfig = particleConfigCopy
            
            
        ## Variables
        xbins = self.getParticleConfigValue(xaxisDrawConfig, "bins")
        xlow = self.getParticleConfigValue(xaxisDrawConfig, "min")
        xup = self.getParticleConfigValue(xaxisDrawConfig, "max")
        xlog = self.getParticleConfigValue(xaxisDrawConfig, "logScale")
        xtitle = self.getParticleConfigValue(xaxisDrawConfig, "title")
        xunit = self.getParticleConfigValue(xaxisDrawConfig, "unit")
        
        ## Create Histogram Name
        
        name = self.createName(xaxisDrawConfig, analysis=analysis, plotType="survival1D")
        
        if "simplified" in analysis:  # reweighting is always done, in addition to removing unreasonable points
            isSimplified = True
            constraintstring = "*".join([self.c.theconstraints["reweight"], self.c.theconstraints["reason_simplified"]])
            constraintstring_prior = "*".join([self.c.theconstraints["reweight"], self.c.theconstraints["reason_simplified"]])
        else:
            isSimplified = False
            constraintstring = "*".join([self.c.theconstraints["reweight"], self.c.theconstraints["reason"]])
            constraintstring_prior = "*".join([self.c.theconstraints["reweight"], self.c.theconstraints["reason"]])
        
        for newc in moreconstraints:
            constraintstring += "*(" + newc + ")"
        if moreconstraints_prior:
            for newc_p in moreconstraints_prior:
                constraintstring_prior += "*(" + newc_p + ")"
                
        prior = PlotterUtils.mkhistlogx("prior", "", xbins, xlow, xup, logx=xlog)
        posterior = prior.Clone(name)
        posterior_up = prior.Clone(name+"_up")
        posterior_down = prior.Clone(name+"_down")
        
        self.tree.Draw(drawstring + ">>" + prior.GetName(), constraintstring_prior, "")
        
        z = self.constraints.getZScore(analysis,isSimplified)
        print(f"\n{BULLET}{BOLD}{YELLOW}Posterior Z Score:{RESET}\n{z}")
        self.tree.Draw(drawstring + ">>" + posterior.GetName(),
                "*".join([constraintstring, "(" + z + ">-1.64)"]), "")
        
        z_up = z.replace('mu1p0','mu1p5').replace('_100s','_150s')
        print(f"{BULLET}{BOLD}{YELLOW}Posterior Up Z Score:{RESET}\n{z_up}")

        self.tree.Draw(drawstring + ">>" + posterior_up.GetName(),
                   "*".join([constraintstring, "(" + z_up + ">-1.64)"]), "")

        z_down = z.replace('mu1p0','mu0p5').replace('_100s','_050s')
        print(f"{BULLET}{BOLD}{YELLOW}Posterior Down Z Score:{RESET}\n{z_down}")
        self.tree.Draw(drawstring + ">>" + posterior_down.GetName(),
                "*".join([constraintstring, "(" + z_down + ">-1.64)"]), "")#Down
        
        PlotterUtils.histoStyler(posterior, kBlack)
        PlotterUtils.histoStyler(posterior_up, kMagenta, linestyle=kDashed)
        PlotterUtils.histoStyler(posterior_down, kRed, linestyle=kDashed)
        posterior.Divide(prior)
        posterior_up.Divide(prior)
        posterior_down.Divide(prior)

        maxy = max([posterior.GetMaximum(), posterior_up.GetMaximum(), posterior_down.GetMaximum()])
        miny = 0 if not xaxisDrawConfig.get("1Dlogy", False) else self.c.global_settings["logEps"]
                
        posterior.GetYaxis().SetRangeUser(miny, maxy + 0.1)
        posterior.GetXaxis().SetTitle(xtitle)
        
        posterior_up.GetYaxis().SetRangeUser(miny, maxy + 0.1)
        posterior_up.GetXaxis().SetTitle(xtitle)
        
        posterior_down.GetYaxis().SetRangeUser(miny, maxy + 0.1)
        posterior_down.GetXaxis().SetTitle(xtitle)
        
        posterior.GetYaxis().SetTitle("Survival Probability")
                
        for hist in [posterior, posterior_up, posterior_down]:
            if not xaxisDrawConfig.get("logScale", False):
                PlotterUtils.scaleXaxis(hist,scaleFactor=xaxisDrawConfig.get("linearScale"))
        
        cxmin, cxmax, cymin, cymax = PlotterUtils.getAxisRangeOfList([posterior, posterior_up, posterior_down])
        if xaxisDrawConfig.get("1Dlogy", False):
            if cymin == 0:
                cymin = self.c.global_settings["logEps"]
                
        cymax += drawConfig.get("yMaxOffsett", 0)
        
        canvas = CMS.cmsCanvas(
            x_min = cxmin,
            x_max = cxmax,
            y_min = cymin,
            y_max = cymax,
            nameXaxis = f"{xtitle} [{xunit}]",
            nameYaxis = "Survival Probability",
            canvName = name,
            square = CMS.kSquare,
            iPos = 0,
            leftMargin = 0.05,
            bottomMargin = 0.035,
            with_z_axis = False,
            scaleLumi = None,
            customStyle= {
                "SetXNdivisions": xaxisDrawConfig.get("Ndivisions",510)
            })
        
        if xaxisDrawConfig.get("logScale", False):
            canvas.SetLogx()
        if xaxisDrawConfig.get("1Dlogy", False):
            canvas.SetLogy()
            
        posterior.Draw("hist same")
        posterior_up.Draw("hist same")
        posterior_down.Draw("hist same")

        legend = CMS.cmsLeg(
            x1 = legendConfig["x1"],
            y1 = legendConfig["y1"],
            x2 = legendConfig["x2"],
            y2 = legendConfig["y2"],
            columns = legendConfig.get("numberOfColumns",1),
            textSize = 0.03)
        legend.SetHeader(self.constraints.getAnalysisName(analysis),"C")
        legend.AddEntry(posterior,"posterior (#sigma = #sigma_{nominal} )")
        legend.AddEntry(posterior_up,"posterior (#sigma = 1.5#times#sigma_{nominal} )")
        legend.AddEntry(posterior_down,"posterior (#sigma =0.5#times#sigma_{nominal} )")

        hframe = CMS.GetcmsCanvasHist(canvas)
        hframe.GetYaxis().SetTitleOffset(drawConfig.get("YaxisSetTitleOffset",1.7))
        hframe.GetXaxis().SetTitleOffset(drawConfig.get("XaxisSetTitleOffset",1.05))
        
        if drawConfig.get("legendFillWhite",False):
            PlotterUtils.makeLegendFillWhite(legend)

        legend.Draw("same")
        CMS.SaveCanvas(canvas, self.outputpath+name+"."+self.defaultFileFormat, close=True)
        print("_______________________________________________________________________________________\n\n")
        
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
        drawConfig: Union[dict, str] = None,
        legendStyle: Union[dict, str] = None):
        print("_____________________________",f"{BOLD}{ORANGE}1D Quantile{RESET} for{BOLD}{BLUE}", drawstring, f"{RESET}","_____________________________")
        
        
        if drawConfig is None:
            drawConfig = self.c.drawConfig["quantile1D"]
        else:
            drawConfigCopy = copy.copy(self.c.drawConfig["quantile1D"])
            drawConfigCopy.update(drawConfig)
            drawConfig = drawConfigCopy
            
        if legendStyle is None:
            legendStyle = "rightBottom"
        if isinstance(legendStyle, str):
            legendConfig = drawConfig.get("legendStyle",legendStyle)
        if isinstance(legendStyle, dict):
            legendConfig = legendStyle
        legendConfig = self.c.drawConfig["quantile1D"][legendConfig]
        
        if xaxisDrawConfig is None:
            xaxisDrawConfig = self.c.particleConfig[drawstring]
        else:
            particleConfigCopy = copy.copy(self.c.particleConfig[drawstring])
            particleConfigCopy.update(xaxisDrawConfig)
            xaxisDrawConfig = particleConfigCopy
        
        ## Variables
        xbins = self.getParticleConfigValue(xaxisDrawConfig, "bins")
        xlow = self.getParticleConfigValue(xaxisDrawConfig, "min")
        xup = self.getParticleConfigValue(xaxisDrawConfig, "max")
        xlog = self.getParticleConfigValue(xaxisDrawConfig, "logScale")
        ylog = self.getParticleConfigValue(xaxisDrawConfig, "1Dlogy")
        xtitle = self.getParticleConfigValue(xaxisDrawConfig, "title")
        xunit = self.getParticleConfigValue(xaxisDrawConfig, "unit")
        
        ## Create Histogram Name
                
        name = self.createName(xaxisDrawConfig, analysis=analysis, plotType="quantile1D")
        
        if "simplified" in analysis:  # reweighting is always done, in addition to removing unreasonable points
            constraintstring = "*".join([self.c.theconstraints["reweight"], self.c.theconstraints["reason_simplified"]])
            _drawstring = self.constraints.getConstraint(analysis,isSimplified=True) + ":" + drawstring
        else:
            constraintstring = "*".join([self.c.theconstraints["reweight"], self.c.theconstraints["reason"]])
            _drawstring = self.constraints.getConstraint(analysis,isSimplified=True) + ":" + drawstring

        print(f"{BOLD}{GREEN}Quantile Plot DrawString:{RESET} {_drawstring}")     
        for newc in moreconstraints:
            constraintstring += "*(" + newc + ")"
        
        _quantiles = []
        quantiles_values = [float(i) for i in quantiles.keys()]
        
        for qt in quantiles_values:
            if qt > 1:
                _quantiles.append(qt / 100.)
            elif qt > 0:
                _quantiles.append(qt)
            else:
                raise ValueError("Invalid quantile provided, please use positive values")

        probs = list(np.array([x]) for x in _quantiles)
        qs = list(np.array([0.]) for x in _quantiles)
        hists = {}
        
        qhist = PlotterUtils.mkhistlogxy("qhist", "", xbins, xlow, xup, 3000, 0, 30, logy=ylog, logx=xlog)
        self.tree.Draw(_drawstring + ">>" + qhist.GetName(), constraintstring, "")
        htemplate = qhist.ProfileX('OF UF')
        xax = htemplate.GetXaxis()
        for prob in probs:
            hists["quantile_" + str(int(100 * prob))] = htemplate.ProjectionX().Clone("quantile_" + str(int(100 * prob)))
            hists["quantile_" + str(int(100 * prob))].Reset()
        for ibinx in range(1, xax.GetNbins() + 1):
            hz = qhist.ProjectionY('hz', ibinx, ibinx)
            try:
                hz.Scale(1.0 / hz.Integral(-1, 99999))
            except:
                for hname, hist in hists.items():
                    hist.SetBinContent(ibinx, 0)
                continue
            quantiles_ = []
            for ix, prob in enumerate(probs):
                quantiles_.append(hz.GetQuantiles(1, qs[ix], prob))
                hists["quantile_" + str(int(100 * prob))].SetBinContent(ibinx, qs[ix][0])
        
        for key in hists:
            hist = hists[key]
            if not xaxisDrawConfig.get("logScale", False):
                PlotterUtils.scaleXaxis(hist,scaleFactor=xaxisDrawConfig.get("linearScale"))
        
        cxmin, cxmax, cymin, cymax = PlotterUtils.getAxisRangeOfList(list(hists.values()))

        if xaxisDrawConfig.get("1Dlogy", False):
            if cymin == 0:
                cymin = self.c.global_settings["logEps"]
        
        cymax += drawConfig.get("yMaxOffsett", 0)

        canvas = CMS.cmsCanvas(
            x_min = cxmin,
            x_max = cxmax,
            y_min = cymin,
            y_max = cymax,
            nameXaxis = f"{xtitle} [{xunit}]",
            nameYaxis = "Bayes Factor",
            canvName = name,
            square = CMS.kSquare,
            iPos = 0,
            leftMargin = 0.03,
            bottomMargin = 0.035,
            with_z_axis = False,
            scaleLumi = None,
            customStyle= {
                "SetXNdivisions": xaxisDrawConfig.get("Ndivisions",510)
            })

        if xlog:
            canvas.SetLogx()
        if ylog:
            canvas.SetLogy()
        
        
        legend = CMS.cmsLeg(
            x1 = legendConfig["x1"],
            y1 = legendConfig["y1"],
            x2 = legendConfig["x2"],
            y2 = legendConfig["y2"],
            columns = legendConfig.get("numberOfColumns",1),
            textSize = 0.03)
        legend.SetHeader(self.constraints.getAnalysisName(analysis),"C")
                
        for i in quantiles:
            histname = "quantile_" + str(int(100 * float(i)))
            hist_style = quantiles[i]
            hist = hists[histname]
            PlotterUtils.histoStyler(hist)
            if hist_style.get("color") is not None:
                hist.SetLineColor(hist_style["color"])
            if hist_style.get("linestyle") is not None:
                hist.SetLineStyle(hist_style["linestyle"])
            legend.AddEntry(hist,str(int(100 * float(i)))+"th Percentile")
            
        for hist in hists.values():
            hist.Draw("hist same")
            
        hframe = CMS.GetcmsCanvasHist(canvas)
        hframe.GetYaxis().SetTitleOffset(drawConfig.get("YaxisSetTitleOffset",1.2))
        hframe.GetXaxis().SetTitleOffset(drawConfig.get("XaxisSetTitleOffset",1.05))

        if drawConfig.get("legendFillWhite",False):
            PlotterUtils.makeLegendFillWhite(legend)

        legend.Draw("same")
        CMS.SaveCanvas(canvas, self.outputpath+name+"."+self.defaultFileFormat, close=True)
        print("_______________________________________________________________________________________\n\n")
    
    def quantile2D(
            self,
            drawstring : str,
            quantile: float,
            analysis : str = "combined",
            moreconstraints : list = [],
            moreconstraints_prior : bool =False,
            xaxisDrawConfig : dict = None,
            yaxisDrawConfig : dict = None,
            drawConfig: Union[dict, str] = None,
            legendStyle: Union[dict, str] = None):
            print("_____________________________",f"{BOLD}{ORANGE}2D Quantile {str(quantile)} Percentile {RESET} for{BOLD}{BLUE}", drawstring, f"{RESET}","_____________________________")
            
            
            if drawConfig is None:
                drawConfig = self.c.drawConfig["quantile2D"]
            else:
                drawConfigCopy = copy.copy(self.c.drawConfig["quantile2D"])
                drawConfigCopy.update(drawConfig)
                drawConfig = drawConfigCopy
                
            if legendStyle is None:
                legendStyle = "rightBottom"
            if isinstance(legendStyle, str):
                legendConfig = drawConfig.get("legendStyle",legendStyle)
            if isinstance(legendStyle, dict):
                legendConfig = legendStyle
            legendConfig = self.c.drawConfig["quantile2D"][legendConfig]
            
            yaxisParticleName, xaxisParticleName = drawstring.split(":")

            if xaxisDrawConfig is None:
                xaxisDrawConfig = self.c.particleConfig[xaxisParticleName]
            else:
                particleConfigCopy = copy.copy(self.c.particleConfig[xaxisParticleName])
                particleConfigCopy.update(xaxisDrawConfig)
                xaxisDrawConfig = particleConfigCopy
            
            if yaxisDrawConfig is None:
                yaxisDrawConfig = self.c.particleConfig[yaxisParticleName]
            else:
                particleConfigCopy = copy.copy(self.c.particleConfig[yaxisParticleName])
                particleConfigCopy.update(yaxisDrawConfig)
                yaxisDrawConfig = particleConfigCopy
            
            
            
            ## Variables
            xbins = self.getParticleConfigValue(xaxisDrawConfig, "bins")
            xlow = self.getParticleConfigValue(xaxisDrawConfig, "min")
            xup = self.getParticleConfigValue(xaxisDrawConfig, "max")
            xlog = self.getParticleConfigValue(xaxisDrawConfig, "logScale")
            xtitle = self.getParticleConfigValue(xaxisDrawConfig, "title")
            xunit = self.getParticleConfigValue(xaxisDrawConfig, "unit")
            
            ## Variables
            ybins = self.getParticleConfigValue(yaxisDrawConfig, "bins")
            ylow = self.getParticleConfigValue(yaxisDrawConfig, "min")
            yup = self.getParticleConfigValue(yaxisDrawConfig, "max")
            ylog = self.getParticleConfigValue(yaxisDrawConfig, "logScale")
            ytitle = self.getParticleConfigValue(yaxisDrawConfig, "title")
            yunit = self.getParticleConfigValue(yaxisDrawConfig, "unit")
            
            ## Create Histogram Name
                    
            name = self.createName(xaxisDrawConfig, yaxisDrawConfig ,analysis=analysis, plotType = str(quantile)+ "_"+"quantile2D")
    
            if quantile < 0 or quantile > 1:
                raise ValueError("Invalid quantile provided, please use values between 0 and 1")
            
            if "simplified" in analysis:
                constraintstring = "*".join([self.c.theconstraints["reweight"], self.c.theconstraints["reason_simplified"]])
                constraintstring_prior = "*".join([self.c.theconstraints["reweight"], self.c.theconstraints["reason_simplified"]])
                _drawstring = self.constraints.getConstraint(analysis,isSimplified=True) + ":" + drawstring
            else:
                constraintstring = "*".join([self.c.theconstraints["reweight"], self.c.theconstraints["reason"]])
                constraintstring_prior = "*".join([self.c.theconstraints["reweight"], self.c.theconstraints["reason"]])
                _drawstring = self.constraints.getConstraint(analysis,isSimplified=False) + ":" + drawstring

            prob = np.array([quantile])
            q = np.array([0.])
            htemp = PlotterUtils.mkhistlogxyz("htemp", '', xbins, xlow, xup, ybins, ylow, yup, 3000, 0, 30, logx=xlog, logy=ylog, logz=False)
            
            for newc in moreconstraints:
                constraintstring += "*(" + newc + ")"
            if moreconstraints_prior:
                for newc_p in moreconstraints_prior:
                    constraintstring_prior += "*(" + newc_p + ")"
                    
            prior = PlotterUtils.mkhistlogxy("prior", '', xbins, xlow, xup, ybins, ylow, yup, logx=xlog, logy=ylog)
            self.tree.Draw(drawstring + ">>" + prior.GetName(), constraintstring_prior, "")
            self.tree.Draw(_drawstring + ">>" + htemp.GetName(), constraintstring, "")

            htemplate = htemp.Project3DProfile('yx UF OF')
            xax, yax = htemplate.GetXaxis(), htemplate.GetYaxis()
            returnhist = htemplate.ProjectionXY().Clone(name)
            returnhist.Reset()
            cutoff = 1E-3
            
            for ibinx in range(1, xax.GetNbins() + 1):
                for ibiny in range(1, yax.GetNbins() + 1):
                    hz = htemp.ProjectionZ('hz', ibinx, ibinx, ibiny, ibiny)
                    try:
                        hz.Scale(1.0 / hz.Integral())
                    except:
                        returnhist.SetBinContent(ibinx, ibiny, 0)
                        continue
                    quant = hz.GetQuantiles(1, q, prob)
                    returnhist.SetBinContent(ibinx, ibiny, q[0])
            zaxis_max = -1
            
            for i in range(1, returnhist.GetNbinsX() + 1):
                for j in range(1, returnhist.GetNbinsY() + 1):
                    if returnhist.GetBinContent(i, j) == 0 and prior.GetBinContent(i, j) > 0:
                        returnhist.SetBinContent(i, j, 0)
                    elif returnhist.GetBinContent(i, j) == 0 and prior.GetBinContent(i, j) == 0:
                        returnhist.SetBinContent(i, j, -1)
                    elif returnhist.GetBinContent(i, j) < cutoff and prior.GetBinContent(i, j) > 0:
                        returnhist.SetBinContent(i, j, cutoff)
                    zaxis_max = max(zaxis_max, returnhist.GetBinContent(i, j))
                    
            returnhist.GetZaxis().SetRangeUser(-0.001, max(1, zaxis_max + 0.1))
            returnhist.SetContour(999)
            returnhist.GetZaxis().SetTitle(str(int(100 * quantile)) + "th percentile Bayes factor"),
            returnhist.GetZaxis().SetTitleOffset(drawConfig.get("ZaxisSetTitleOffset",0.25))
            returnhist.GetZaxis().SetTitleSize(0.06)
            if not xlog:
                PlotterUtils.scaleXaxis(returnhist,scaleFactor=xaxisDrawConfig.get("linearScale"))
            if not ylog:
                PlotterUtils.scaleYaxis(returnhist,scaleFactor=yaxisDrawConfig.get("linearScale"))
            
            cxmin = xlow/xaxisDrawConfig.get("linearScale")
            cxmax = xup/xaxisDrawConfig.get("linearScale")
            cymin = ylow/yaxisDrawConfig.get("linearScale")
            cymax = yup/yaxisDrawConfig.get("linearScale")

                        
            if xlog:
                if cxmin == 0:
                    cxmin = self.c.global_settings["logEps"]
            if ylog:
                if cymin == 0:
                    cymin = self.c.global_settings["logEps"]
                    
            canvas = CMS.cmsCanvas(
                x_min = cxmin,
                x_max = cxmax,
                y_min = cymin,
                y_max = cymax,
                nameXaxis = f"{xtitle} [{xunit}]",
                nameYaxis = f"{ytitle} [{yunit}]",
                canvName = name,
                square = CMS.kSquare,
                iPos = 0,
                leftMargin = 0.04,
                bottomMargin = 0.037,
                with_z_axis = True,
                scaleLumi = None,
                customStyle= {
                    "SetXNdivisions": xaxisDrawConfig.get("Ndivisions",510),
                    "SetYNdivisions": yaxisDrawConfig.get("Ndivisions",510)
                })
            CMS.SetCMSPalette()
            if xlog:
                canvas.SetLogx()
            if ylog:
                canvas.SetLogy()
            returnhist.Draw("same colz")

            hframe = CMS.GetcmsCanvasHist(canvas)
            hframe.GetYaxis().SetTitleOffset(drawConfig.get("YaxisSetTitleOffset",1.2))
            hframe.GetXaxis().SetTitleOffset(drawConfig.get("XaxisSetTitleOffset",1.05))

            CMS.SaveCanvas(canvas, self.outputpath+name+"."+self.defaultFileFormat, close=True)
            print("_______________________________________________________________________________________\n\n")