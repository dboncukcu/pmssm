from ROOT import *
from PlotterConfig import PlotterConfig
import PlotterUtils
from cmsstylelib import cmsstyle as CMS
from Constraints import Constraints
from typing import Union
import numpy as np
import copy

gROOT.SetBatch(True)


class printStyle:
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    ORANGE = '\033[38;5;214m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    STRIKETHROUGH = '\033[9m'
    BOLD = '\033[1m'
    RESET = '\033[0m'
    BULLET = '•'

class CMSColors:
    
    class six:
        blue =  TColor.GetColor("#5790fc")
        orange =  TColor.GetColor("#f89c20")
        red =  TColor.GetColor("#e42536")
        purple =  TColor.GetColor("#964a8b")
        grey =  TColor.GetColor("#9c9ca1")
        violet =  TColor.GetColor("#7a21dd")
    
    class ten:
        blue = TColor.GetColor("#3f90da")
        lightorange = TColor.GetColor("#ffa90e")
        red = TColor.GetColor("#bd1f01")
        lightgrey = TColor.GetColor("#94a4a2")
        purple = TColor.GetColor("#832db6")
        brown = TColor.GetColor("#a96b59")
        darkorange = TColor.GetColor("#e76300")
        darkyellow = TColor.GetColor("#b9ac70")
        grey = TColor.GetColor("#717581")
        turquoise = TColor.GetColor("#92dadd")


class PMSSM:
    def __init__(
        self,
        root_dict: list[dict] = None,
        config: PlotterConfig = None
    ):  
        # Binding Config to the class
        if config is None:
            self.c = PlotterConfig()
        else:
            self.c = config
        
        if root_dict is None:
            root_dict = self.c.root_dict
        
        self.constraints = Constraints(self.c.analysisConfigs)
        
        if self.c.cms_label.get("energy") is not None:
            CMS.SetEnergy(str(self.c.cms_label.get("energy")))
        if self.c.cms_label.get("extraText") is not None:
            CMS.SetExtraText(self.c.cms_label.get("extraText"))
        if self.c.cms_label.get("lumi") is not None:
            CMS.SetLumi(self.c.cms_label.get("lumi"))
        CMS.setCMSStyle()
        # Reading root files
        self.tree,self.file = PlotterUtils.create_tree(root_dict)
        
        # create an output directory
        self.outputpath =  PlotterUtils.create_output_directory( self.c.global_settings["outputPath"])
        self.defaultFileFormat = self.c.global_settings["outputFileFormat"]
    def createName(self,xaxisDrawConfig, yaxisDrawConfig:dict= None, analysis:str="combined", plotType:str="",customName:str = ""):
        
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

        name = name + customName
        
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
        legendStyle: Union[dict, str] = None,
        customName:str = ""):
        print("_____________________________",f"{printStyle.BOLD}{printStyle.ORANGE}1D Impact{printStyle.RESET} for{printStyle.BOLD}{printStyle.BLUE}", drawstring, f"{printStyle.RESET}","_____________________________")
        
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
        legendConfig = drawConfig[legendConfig]
        
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
        
        name = self.createName(xaxisDrawConfig, analysis=analysis, plotType="impact1D",customName=customName)
        
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
        
        # PlotterUtils.histoStyler(prior, kBlue - 9, fill=True)
        # PlotterUtils.histoStyler(posterior, kBlack)
        # PlotterUtils.histoStyler(posterior_down, kRed, linestyle=kDashed)
        # PlotterUtils.histoStyler(posterior_up, kMagenta, linestyle=kDashed)
        
                
        PlotterUtils.histoStyler(prior, CMSColors.six.blue, fill=True)
        PlotterUtils.histoStyler(posterior, kBlack)
        PlotterUtils.histoStyler(posterior_down, CMSColors.six.red, linestyle=kDashed)
        PlotterUtils.histoStyler(posterior_up, CMSColors.six.violet, linestyle=kDashed)
        
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
            nameXaxis = f"{xtitle} [{xunit}]" if xunit != "" else xtitle,
            nameYaxis = f"{self.constraints.getAnalysisName(analysis)} pMSSM density",
            canvName = name,
            square = CMS.kSquare,
            iPos = 0,
            leftMargin = drawConfig.get("leftMargin", 0.08),
            bottomMargin = drawConfig.get("bottomMargin", 0.035),
            rightMargin = drawConfig.get("rightMargin", 0),
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
        

        # legend.SetHeader(self.constraints.getAnalysisName(analysis),"C")
        legend.AddEntry(prior,"prior")
        legend.AddEntry(posterior,"posterior (#sigma = #sigma_{nominal} )")
        legend.AddEntry(posterior_up,"posterior (#sigma = 1.5#times#sigma_{nominal} )")
        legend.AddEntry(posterior_down,"posterior (#sigma = 0.5#times#sigma_{nominal} )")
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
        legendStyle: Union[dict, str] = None,
        customName:str = ""):
        print("_____________________________",f"{printStyle.BOLD}{printStyle.ORANGE}1D Survival Probability{printStyle.RESET} for{printStyle.BOLD}{printStyle.BLUE}", drawstring, f"{printStyle.RESET}","_____________________________")
        
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
        
        name = self.createName(xaxisDrawConfig, analysis=analysis, plotType="survival1D",customName=customName)
        
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
        print(f"\n{printStyle.BULLET}{printStyle.BOLD}{printStyle.YELLOW}Posterior Z Score:{printStyle.RESET}\n{z}")
        self.tree.Draw(drawstring + ">>" + posterior.GetName(),
                "*".join([constraintstring, "(" + z + ">-1.64)"]), "")
        
        z_up = z.replace('mu1p0','mu1p5').replace('_100s','_150s')
        print(f"{printStyle.BULLET}{printStyle.BOLD}{printStyle.YELLOW}Posterior Up Z Score:{printStyle.RESET}\n{z_up}")

        self.tree.Draw(drawstring + ">>" + posterior_up.GetName(),
                   "*".join([constraintstring, "(" + z_up + ">-1.64)"]), "")

        z_down = z.replace('mu1p0','mu0p5').replace('_100s','_050s')
        print(f"{printStyle.BULLET}{printStyle.BOLD}{printStyle.YELLOW}Posterior Down Z Score:{printStyle.RESET}\n{z_down}")
        self.tree.Draw(drawstring + ">>" + posterior_down.GetName(),
                "*".join([constraintstring, "(" + z_down + ">-1.64)"]), "")#Down
        
        PlotterUtils.histoStyler(posterior, kBlack)
        PlotterUtils.histoStyler(posterior_up, CMSColors.six.violet, linestyle=kDashed)
        PlotterUtils.histoStyler(posterior_down, CMSColors.six.red, linestyle=kDashed)
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
            nameXaxis = f"{xtitle} [{xunit}]" if xunit != "" else xtitle,
            nameYaxis = f"{self.constraints.getAnalysisName(analysis)} Survival Probability",
            canvName = name,
            square = CMS.kSquare,
            iPos = 0,
            leftMargin = drawConfig.get("leftMargin", 0.05),
            bottomMargin = drawConfig.get("bottomMargin", 0.035),
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
        # legend.SetHeader(self.constraints.getAnalysisName(analysis),"C")
        legend.AddEntry(posterior,"#sigma = #sigma_{nominal}")
        legend.AddEntry(posterior_up,"#sigma = 1.5#times#sigma_{nominal}")
        legend.AddEntry(posterior_down,"#sigma = 0.5#times#sigma_{nominal}")

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
            # "0.5": {"color":kBlack},
            # "0.75": {"color":CMSColors.six.orange},
            # "0.9": {"color":CMSColors.six.red,"linestyle": kDashed},
            # "0.99": {"color":CMSColors.six.blue,"linestyle": kDashed},
            "0.99": {"color":kBlack},
        },
        analysis : str = "combined",
        moreconstraints : list = [], 
        xaxisDrawConfig : dict = None,
        drawConfig: Union[dict, str] = None,
        legendStyle: Union[dict, str] = None,
        customName:str = ""):
        print("_____________________________",f"{printStyle.BOLD}{printStyle.ORANGE}1D Quantile{printStyle.RESET} for{printStyle.BOLD}{printStyle.BLUE}", drawstring, f"{printStyle.RESET}","_____________________________")
        
        
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
        legendConfig = drawConfig[legendConfig]
        
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
                
        name = self.createName(xaxisDrawConfig, analysis=analysis, plotType="quantile1D",customName=customName)
        
        if "simplified" in analysis:  # reweighting is always done, in addition to removing unreasonable points
            constraintstring = "*".join([self.c.theconstraints["reweight"], self.c.theconstraints["reason_simplified"]])
            _drawstring = self.constraints.getConstraint(analysis,isSimplified=True) + ":" + drawstring
        else:
            constraintstring = "*".join([self.c.theconstraints["reweight"], self.c.theconstraints["reason"]])
            _drawstring = self.constraints.getConstraint(analysis,isSimplified=False) + ":" + drawstring

        print(f"{printStyle.BOLD}{printStyle.GREEN}Quantile Plot DrawString:{printStyle.RESET} {_drawstring}")     
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
            nameXaxis = f"{xtitle} [{xunit}]" if xunit != "" else xtitle,
            nameYaxis = f"{self.constraints.getAnalysisName(analysis)} Bayes Factor",
            canvName = name,
            square = CMS.kSquare,
            iPos = 0,
            leftMargin = drawConfig.get("leftMargin", 0.03),
            rightMargin = drawConfig.get("rightMargin", 0.01),
            bottomMargin = drawConfig.get("bottomMargin", 0.035),
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
        # legend.SetHeader(self.constraints.getAnalysisName(analysis),"C")
                
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
    
    def quantile1D_with_sigmaVariations(
        self,
        drawstring : str,
        quantile : dict = "0.99",
        analysis : str = "combined",
        moreconstraints : list = [], 
        xaxisDrawConfig : dict = None,
        drawConfig: Union[dict, str] = None,
        legendStyle: Union[dict, str] = None,
        customName:str = ""):
        print("_____________________________",f"{printStyle.BOLD}{printStyle.ORANGE}1D Quantile{printStyle.RESET} for{printStyle.BOLD}{printStyle.BLUE}", drawstring, f"{printStyle.RESET}","_____________________________")
        
        
        if drawConfig is None:
            drawConfig = self.c.drawConfig["quantile1DWVar"]
        else:
            drawConfigCopy = copy.copy(self.c.drawConfig["quantile1DWVar"])
            drawConfigCopy.update(drawConfig)
            drawConfig = drawConfigCopy
            
        if legendStyle is None:
            legendStyle = "rightBottom"
        if isinstance(legendStyle, str):
            legendConfig = drawConfig.get("legendStyle",legendStyle)
        if isinstance(legendStyle, dict):
            legendConfig = legendStyle
        legendConfig = drawConfig[legendConfig]
        
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
                
        name = self.createName(xaxisDrawConfig, analysis=analysis, plotType="quantile1D",customName=customName)
        
        if "simplified" in analysis:  # reweighting is always done, in addition to removing unreasonable points
            constraintstring = "*".join([self.c.theconstraints["reweight"], self.c.theconstraints["reason_simplified"]])
            _drawstring = self.constraints.getConstraint(analysis,isSimplified=True) + ":" + drawstring
        else:
            constraintstring = "*".join([self.c.theconstraints["reweight"], self.c.theconstraints["reason"]])
            _drawstring = self.constraints.getConstraint(analysis,isSimplified=False) + ":" + drawstring

        print(f"{printStyle.BOLD}{printStyle.GREEN}Quantile Plot DrawString:{printStyle.RESET} {_drawstring}")     
        for newc in moreconstraints:
            constraintstring += "*(" + newc + ")"
        
        
        if float(quantile) > 1:
            _quantiles = [float(quantile) / 100.]
        elif float(quantile) > 0:
            _quantiles = [float(quantile)]
        else:
            raise ValueError("Invalid quantile provided, please use positive values")

        probs = list(np.array([x]) for x in _quantiles)
        qs = list(np.array([0.]) for x in _quantiles)
        hists = {}
        
        
        ## NORMAL
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


        ## UP
        up_constraint = _drawstring.replace('mu1p0','mu1p5').replace('_100s','_150s')
        qhist_up = PlotterUtils.mkhistlogxy("qhist_up", "", xbins, xlow, xup, 3000, 0, 30, logy=ylog, logx=xlog)
        self.tree.Draw(_drawstring.replace('mu1p0','mu1p5').replace('_100s','_150s') + ">>" + qhist_up.GetName(), constraintstring, "")
        htemplate_up = qhist_up.ProfileX('OF UF')
        xax_up = htemplate_up.GetXaxis()
        for prob in probs:
            hists["quantile_up_" + str(int(100 * prob))] = htemplate_up.ProjectionX().Clone("quantile_up_" + str(int(100 * prob)))
            hists["quantile_up_" + str(int(100 * prob))].Reset()
        for ibinx in range(1, xax_up.GetNbins() + 1):
            hz = qhist_up.ProjectionY('hz', ibinx, ibinx)
            try:
                hz.Scale(1.0 / hz.Integral(-1, 99999))
            except:
                for hname, hist in hists.items():
                    hist.SetBinContent(ibinx, 0)
                continue
            quantiles_up_ = []
            for ix, prob in enumerate(probs):
                quantiles_up_.append(hz.GetQuantiles(1, qs[ix], prob))
                hists["quantile_up_" + str(int(100 * prob))].SetBinContent(ibinx, qs[ix][0])
        
        ## DOWN
        
        down_constraint = _drawstring.replace('mu1p0','mu0p5').replace('_100s','_050s')
        qhist_down = PlotterUtils.mkhistlogxy("qhist_down", "", xbins, xlow, xup, 3000, 0, 30, logy=ylog, logx=xlog)
        self.tree.Draw(down_constraint + ">>" + qhist_down.GetName(), constraintstring, "")
        htemplate_down = qhist_down.ProfileX('OF UF')
        xax_down = htemplate.GetXaxis()
        for prob in probs:
            hists["quantile_down_" + str(int(100 * prob))] = htemplate_down.ProjectionX().Clone("quantile_down_" + str(int(100 * prob)))
            hists["quantile_down_" + str(int(100 * prob))].Reset()
        for ibinx in range(1, xax_down.GetNbins() + 1):
            hz = qhist_down.ProjectionY('hz', ibinx, ibinx)
            try:
                hz.Scale(1.0 / hz.Integral(-1, 99999))
            except:
                for hname, hist in hists.items():
                    hist.SetBinContent(ibinx, 0)
                continue
            quantiles_down_ = []
            for ix, prob in enumerate(probs):
                quantiles_down_.append(hz.GetQuantiles(1, qs[ix], prob))
                hists["quantile_down_" + str(int(100 * prob))].SetBinContent(ibinx, qs[ix][0])
        
        ##
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
            y_min = 0.5,  #cymin,
            y_max = 1.1 * cymax,
            nameXaxis = f"{xtitle} [{xunit}]" if xunit != "" else xtitle,
            nameYaxis = str(int(100 * float(quantile)))+"^{th} Percentile Bayes Factor",
            canvName = name,
            square = CMS.kSquare,
            iPos = 0,
            leftMargin = drawConfig.get("leftMargin", 0.03),
            rightMargin = drawConfig.get("rightMargin", 0.01),
            bottomMargin = drawConfig.get("bottomMargin", 0.035),
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
        # legend.SetHeader(self.constraints.getAnalysisName(analysis) ,"C")
        
        for histname in hists.keys():
            hist = hists[histname]
            PlotterUtils.histoStyler(hist)
            if "down" in histname :
                hist.SetLineColor(CMSColors.six.red)
                hist.SetLineStyle(kDashed)
                legend.AddEntry(hist,"#sigma = 0.5#times#sigma_{nominal}")
            elif "up" in histname:
                hist.SetLineColor(CMSColors.six.violet)
                hist.SetLineStyle(kDashed)
                legend.AddEntry(hist,"#sigma = 1.5#times#sigma_{nominal}")
            else:
                hist.SetLineColor(kBlack)
                legend.AddEntry(hist,"#sigma = #sigma_{nominal}")
        
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
            legendStyle: Union[dict, str] = None,
            customName:str = "",
            colorPallette = kViridis):
            CMS.setCMSStyle()
            print("_____________________________",f"{printStyle.BOLD}{printStyle.ORANGE}2D Quantile {str(quantile)} Percentile {printStyle.RESET} for{printStyle.BOLD}{printStyle.BLUE}", drawstring, f"{printStyle.RESET}","_____________________________")
            
            
            if drawConfig is None:
                drawConfig = self.c.drawConfig["quantile2D"]
            else:
                drawConfigCopy = copy.copy(self.c.drawConfig["quantile2D"])
                drawConfigCopy.update(drawConfig)
                drawConfig = drawConfigCopy
                
            if legendStyle is None:
                legendStyle = "rightTop"
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
                    
            name = self.createName(xaxisDrawConfig, yaxisDrawConfig ,analysis=analysis, plotType = str(quantile)+ "_"+"quantile2D",customName=customName)
    
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
                    returnhist.SetBinContent(ibinx, ibiny, max(q[0], cutoff))
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
                    
            returnhist.GetZaxis().SetRangeUser(cutoff, max(1, zaxis_max + 0.1))
            returnhist.SetContour(999)
            returnhist.GetZaxis().SetTitle(str(int(100 * quantile)) + "th percentile Bayes factor"),
            returnhist.GetZaxis().SetTitleOffset(drawConfig.get("ZaxisSetTitleOffset",0.75))
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
                nameXaxis = f"{xtitle} [{xunit}]" if xunit != "" else xtitle,
                nameYaxis = f"{ytitle} [{yunit}]" if yunit != "" else ytitle,
                canvName = name,
                square = CMS.kSquare,
                iPos = 0,
                leftMargin = 0.035,
                bottomMargin = 0.037,
                rightMargin= 0.045,
                with_z_axis = True,
                scaleLumi = None,
                customStyle= {
                    "SetXNdivisions": xaxisDrawConfig.get("Ndivisions",510),
                    "SetYNdivisions": yaxisDrawConfig.get("Ndivisions",510)
                })
            CMS.SetCMSCustomPalette(colorPallette)
            if xlog:
                canvas.SetLogx()
            if ylog:
                canvas.SetLogy()
            canvas.SetLogz()
            returnhist.Draw("same colz")
            
            legend = CMS.cmsLeg(
                        x1 = legendConfig["x1"],
                        y1 = legendConfig["y1"],
                        x2 = legendConfig["x2"],
                        y2 = legendConfig["y2"],
                        columns = legendConfig.get("numberOfColumns",1),
                        textSize = 0.03)
            legend.SetHeader(self.constraints.getAnalysisName(analysis),"C")
            
            if drawConfig.get("legendColor") is not None:
                legend.SetTextColor(drawConfig["legendColor"])
            
            legend.Draw("same")

            hframe = CMS.GetcmsCanvasHist(canvas)
            hframe.GetYaxis().SetTitleOffset(drawConfig.get("YaxisSetTitleOffset",1.2))
            hframe.GetXaxis().SetTitleOffset(drawConfig.get("XaxisSetTitleOffset",1.05))
            CMS.UpdatePalettePosition(returnhist, canvas)

            CMS.SaveCanvas(canvas, self.outputpath+name+"."+self.defaultFileFormat, close=True)
            print("_______________________________________________________________________________________\n\n")
         
    def survivalProbability2D(
        self,
        drawstring : str,
        analysis : str = "combined",
        moreconstraints : list = [], 
        moreconstraints_prior : bool =False,
        xaxisDrawConfig : dict = None,
        yaxisDrawConfig : dict = None,
        drawConfig: Union[dict, str] = None,
        legendStyle: Union[dict, str] = None,
        showLegend: bool = False,
        customName:str = ""):
        CMS.setCMSStyle()
        print("_____________________________",f"{printStyle.BOLD}{printStyle.ORANGE}2D Survival Probability{printStyle.RESET} for{printStyle.BOLD}{printStyle.BLUE}", drawstring, f"{printStyle.RESET}","_____________________________")
        
        if drawConfig is None:
            drawConfig = self.c.drawConfig["survival2D"]
        else:
            drawConfigCopy = copy.copy(self.c.drawConfig["survival2D"])
            drawConfigCopy.update(drawConfig)
            drawConfig = drawConfigCopy

        if legendStyle is None:
            legendStyle = "rightBottom"
        if isinstance(legendStyle, str):
            legendConfig = drawConfig.get("legendStyle",legendStyle)
        if isinstance(legendStyle, dict):
            legendConfig = legendStyle
        legendConfig = self.c.drawConfig["survival2D"][legendConfig]
        
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
                
        name = self.createName(xaxisDrawConfig, yaxisDrawConfig ,analysis=analysis, plotType = "survival2D",customName=customName)
        
        ## color palette
        
        sprobcontours = np.float64([-0.01,1E-5,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1-1E-5,1.01])
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

        hdenom = PlotterUtils.mkhistlogxy("hdenom", '', xbins, xlow, xup, ybins, ylow, yup, logx=xlog, logy=ylog)
        
        hret = hdenom.Clone(name)
        
        hret.SetContour(len(sprobcontours) - 1, sprobcontours)

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
        
        print("constraintstring: ", constraintstring)
        print("constraintstring_prior: ", constraintstring_prior)
        
        self.tree.Draw(drawstring + ">>" + hdenom.GetName(), constraintstring_prior, "colz")
        z = self.constraints.getZScore(analysis,isSimplified)
        print("z: ", z)
        self.tree.Draw(drawstring + ">>" + hret.GetName(), "*".join([constraintstring, "(" + z + ">-1.64)"]), "colz")
        hret.GetZaxis().SetRangeUser(-0.001, 1)
        cutoff = 1E-3
        hret.GetZaxis().SetTitle("Survival Probability")
        hret.Divide(hdenom)
        for i in range(1, hret.GetNbinsX() + 1):
            for j in range(1, hret.GetNbinsY() + 1):
                if hret.GetBinContent(i, j) == 0 and hdenom.GetBinContent(i, j) > 0:
                    hret.SetBinContent(i, j, 0)
                elif hret.GetBinContent(i, j) == 0 and hdenom.GetBinContent(i, j) == 0:
                    hret.SetBinContent(i, j, -1)
                elif hret.GetBinContent(i, j) < cutoff and hdenom.GetBinContent(i, j) > 0:
                    hret.SetBinContent(i, j, cutoff)
        hret.SetContour(len(sprobcontours) - 1, sprobcontours)
        
        hret.GetZaxis().SetTitleOffset(drawConfig.get("ZaxisSetTitleOffset",0.85))
        hret.GetZaxis().SetTitleSize(0.06)
        
        prior_data =  self.get_prior_CI(
            analysis=analysis,
            hname = name + "_priorcontours",
            xbins = xbins, 
            xlow = xlow, 
            xup = xup,
            ybins = ybins, 
            ylow = ylow, 
            yup = yup, 
            _logx = xlog, 
            _logy = ylog, 
            drawstring = drawstring,
            moreconstraints= moreconstraints)
            
        posterior_data = self.get_posterior_CI(
            analysis = analysis, 
            hname = name + "_priorcontours", 
            xbins = xbins, 
            xlow = xlow, 
            xup = xup, 
            ybins = ybins, 
            ylow = ylow, 
            yup = yup, 
            _logx = xlog, 
            _logy = ylow, 
            drawstring = drawstring,
            moreconstraints = moreconstraints)


        if not xlog:
            PlotterUtils.scaleXaxis(hret,scaleFactor=xaxisDrawConfig.get("linearScale"))
        if not ylog:
            PlotterUtils.scaleYaxis(hret,scaleFactor=yaxisDrawConfig.get("linearScale"))
            
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
            nameXaxis = f"{xtitle} [{xunit}]" if xunit != "" else xtitle,
            nameYaxis = f"{ytitle} [{yunit}]" if yunit != "" else ytitle,
            canvName = name,
            square = CMS.kSquare,
            iPos = 0,
            leftMargin = 0.04,
            bottomMargin = drawConfig.get("bottomMargin",0.037),
            rightMargin = 0.04,
            with_z_axis = True,
            scaleLumi = None,
            customStyle= {
                "SetXNdivisions": xaxisDrawConfig.get("Ndivisions",510),
                "SetYNdivisions": yaxisDrawConfig.get("Ndivisions",510)
            })
        

        legend = CMS.cmsLeg(
            x1 = 0.2,
            y1 = 0,
            x2 = 0.8,
            y2 = 0.9,
            columns = 2,
            textSize = 0.06)
        legend.SetHeader(self.constraints.getAnalysisName(analysis),"C")

        hret.Draw("colz same")
        for ix,interval in enumerate(prior_data):
            for cont in prior_data[interval]:
                if not xaxisDrawConfig.get("logScale", False):
                    PlotterUtils.scaleGraphXaxis(cont,scaleFactor=xaxisDrawConfig.get("linearScale"))
                if not yaxisDrawConfig.get("logScale", False):
                    PlotterUtils.scaleGraphYaxis(cont,scaleFactor=yaxisDrawConfig.get("linearScale"))
                cont.Draw("same")
        for ix,interval in enumerate(posterior_data):
            for cont in posterior_data[interval]:
                if not xaxisDrawConfig.get("logScale", False):
                    PlotterUtils.scaleGraphXaxis(cont,scaleFactor=xaxisDrawConfig.get("linearScale"))
                if not yaxisDrawConfig.get("logScale", False):
                    PlotterUtils.scaleGraphYaxis(cont,scaleFactor=yaxisDrawConfig.get("linearScale"))
                cont.Draw("same")
        for ix,interval in enumerate(prior_data):
            if interval in prior_data.keys() and len(prior_data[interval])>0:
                legend.AddEntry(prior_data[interval][0],str(int(100*(interval)))+"%  prior CI","l",)
            if interval in posterior_data.keys() and len(posterior_data[interval])>0:
                legend.AddEntry(posterior_data[interval][0],str(int(100*(interval)))+"% posterior CI","l",)
        
        
        CMS.SetCustomPalette(custompalette)
        if xlog:
            canvas.SetLogx()
        if ylog:
            canvas.SetLogy()
            

        hframe = CMS.GetcmsCanvasHist(canvas)
        hframe.GetYaxis().SetTitleOffset(drawConfig.get("YaxisSetTitleOffset",1.2))
        hframe.GetXaxis().SetTitleOffset(drawConfig.get("XaxisSetTitleOffset",1.05))
        

        CMS.UpdatePalettePosition(hret, canvas)
        CMS.SaveCanvas(canvas, self.outputpath+name+"."+self.defaultFileFormat, close=True)
        if showLegend:
            c = TCanvas(name + "c", name + "c",60,40)
            c.cd()
            legend.SetTextAlign(22)
            legend.Draw()
            if drawConfig.get("legendFillWhite",False):
                PlotterUtils.makeLegendFillWhite(legend)
            CMS.SaveCanvas(c, self.outputpath+name+"_legend."+self.defaultFileFormat, close=True)
        else:
            del legend
            print("_______________________________________________________________________________________\n\n")      
        
    def get_prior_CI(self,analysis, hname, xbins, xlow, xup, ybins, ylow, yup, _logx, _logy, drawstring, moreconstraints=[],
                 intervals=[0.1, 0.67, 0.95], contourcolors=[kRed, kRed + 2, kMagenta],
                 contourstyle=[kSolid, kSolid, kSolid]):
        """
        Produce credibility intervals for the prior, defined here as the smallest number of bins that contain X% of the prior density.
        Returns the contours for the given intervals
        @param localtree: Function needs to be passed the ROOT tree from which to operate
        @param hname: Name of the returned histogram
        @param xbins: number of x-axis bins. The choice of binning can have some impact on the shape of the credibility intervals
        @param xlow: lower edge of zero'th bin. The axis ranges should always encompass ALL model points
        @param xup: upper edge of xbins's bin. The axis ranges should always encompass ALL model points
        @param ybins: number of y-axis bins
        @param ylow: lower edge of zero'th bin. The axis ranges should always encompass ALL model points
        @param yup: upper edge of ybins's bin. The axis ranges should always encompass ALL model points
        @param _logx: sets x-axis to logarithmic (base 10). If you use this, use linear Y:X in drawstring, not Y:log(X)
        @param _logy: sets y-axis to logarithmic (base 10). If you use this, use linear Y:X in drawstring, not log(Y):X
        @param drawstring: Draw string passed to root .Draw() function, of the form Y:X, where Y is drawn on the y-axis and X is drawn on the x-axis. Accepts tree branches and mathematical operations acted on them, such as for example log(Y):10*X. This should always be the same as the underlying histogram
        @param moreconstraints: list of logical expressions that constrain the tree. Can use tree branches and mathematical operations. Each constrain in the list is logically multiplied. For the prior, this should usually be empty.
        @param intervals: List of X% prior credibility intervals to produce if possible
        @param contourcolors: Specifies the colors for the contours. Must be a list of the same length as the intervals.
        @param contourstyle: Specifies the line style for the contours. Must be a list of the same length as the intervals.
        
        """
        if "simplified" in analysis:  # reweighting is always done, in addition to removing unreasonable points
            constraintstring = "*".join([self.c.theconstraints["reweight"], self.c.theconstraints["reason_simplified"]])
        else:
            constraintstring = "*".join([self.c.theconstraints["reweight"], self.c.theconstraints["reason"]])
        for newc in moreconstraints:
            constraintstring += "*(" + newc + ")"

        contours = PlotterUtils.mkhistlogxy(hname, '', xbins, xlow, xup, ybins, ylow, yup, logx=_logx, logy=_logy)
        self.tree.Draw(drawstring + ">>" + contours.GetName(), constraintstring, "cont2")
        contarrays = np.array(self.getThresholdForContainment(contours, intervals))
        # redraw the histogram with cont list option
        self.tree.Draw(drawstring + ">>" + contours.GetName(), constraintstring, "cont list")
        # optionally smooth the histogram, as the exact boundary is not important and this makes the intervals look nicer
        contours.Smooth()
        contours.SetContour(len(contarrays),
                            contarrays)  # this produces the contours for the thresholds given in contarrays
        the_contours = {}
        gPad.Update()
        conts = gROOT.GetListOfSpecials().FindObject("contours")
        for ix, contlist in enumerate(conts):
            the_contours[intervals[len(intervals) - ix - 1]] = []
            for cont in contlist:
                if cont.GetN() < 5: continue  # optionally only consider contours that are somewhat large
                cont.SetLineColor(contourcolors[ix])
                cont.SetMarkerColor(contourcolors[ix])
                cont.SetLineStyle(contourstyle[ix])
                cont.SetLineWidth(3)
                the_contours[intervals[len(intervals) - ix - 1]].append(cont.Clone())
        return the_contours

    def get_posterior_CI(self,analysis, hname, xbins, xlow, xup, ybins, ylow, yup, _logx, _logy, drawstring,
                        moreconstraints=[], intervals=[0.1, 0.67, 0.95], contourcolors=[kRed, kRed + 2, kMagenta],
                        contourstyle=[kDashed, kDashed, kDashed]):
        """
        Produce credibility intervals for the prior, defined here as the smallest number of bins that contain X% of the prior density.
        Returns the contours for the given intervals
        @param localtree: Function needs to be passed the ROOT tree from which to operate
        @param analysis: The analysis to use for LHC constraints. Can be any string for which a dictionary entry and corresponding ROOT branch exists in "branchnames". Currently does not allow for arbitrary combinations of analyses
        @param hname: Name of the returned histogram
        @param xbins: number of x-axis bins. The choice of binning can have some impact on the shape of the credibility intervals
        @param xlow: lower edge of zero'th bin. The axis ranges should always encompass ALL model points
        @param xup: upper edge of xbins's bin. The axis ranges should always encompass ALL model points
        @param ybins: number of y-axis bins
        @param ylow: lower edge of zero'th bin. The axis ranges should always encompass ALL model points
        @param yup: upper edge of ybins's bin. The axis ranges should always encompass ALL model points
        @param _logx: sets x-axis to logarithmic (base 10). If you use this, use linear Y:X in drawstring, not Y:log(X)
        @param _logy: sets y-axis to logarithmic (base 10). If you use this, use linear Y:X in drawstring, not log(Y):X
        @param drawstring: Draw string passed to root .Draw() function, of the form Y:X, where Y is drawn on the y-axis and X is drawn on the x-axis. Accepts tree branches and mathematical operations acted on them, such as for example log(Y):10*X. This should always be the same as the underlying histogram
        @param moreconstraints: list of logical expressions that constrain the tree. Can use tree branches and mathematical operations. Each constrain in the list is logically multiplied. For the prior, this should usually be empty.
        @param intervals: List of X% prior credibility intervals to produce if possible
        @param contourcolors: Specifies the colors for the contours. Must be a list of the same length as the intervals.
        @param contourstyle: Specifies the line style for the contours. Must be a list of the same length as the intervals.
        
        """
        if "simplified" in analysis:  # reweighting is always done, in addition to removing unreasonable points
            constraintstring = "*".join(
                [self.c.theconstraints["reweight"], self.c.theconstraints["reason_simplified"], self.constraints.getConstraint(analysis,isSimplified=True,verbose=False)])
        else:
            constraintstring = "*".join([self.c.theconstraints["reweight"], self.c.theconstraints["reason"], self.constraints.getConstraint(analysis,isSimplified=False,verbose=False)])
        for newc in moreconstraints:
            constraintstring += "*(" + newc + ")"

        contours = PlotterUtils.mkhistlogxy(hname, '', xbins, xlow, xup, ybins, ylow, yup, logx=_logx, logy=_logy)
        self.tree.Draw(drawstring + ">>" + contours.GetName(), constraintstring, "cont2")
        contarrays = np.array(self.getThresholdForContainment(contours, intervals))
        # redraw the histogram with cont list option
        self.tree.Draw(drawstring + ">>" + contours.GetName(), constraintstring, "cont list")
        # optionally smooth the histogram, as the exact boundary is not important and this makes the intervals look nicer
        contours.Smooth()
        contours.SetContour(len(contarrays),
                            contarrays)  # this produces the contours for the thresholds given in contarrays
        the_contours = {}
        gPad.Update()
        conts = gROOT.GetListOfSpecials().FindObject("contours")
        for ix, contlist in enumerate(conts):
            the_contours[intervals[len(intervals) - ix - 1]] = []
            for cont in contlist:
                if cont.GetN() < 5: continue  # optionally only consider contours that are somewhat large
                cont.SetLineColor(contourcolors[ix])
                cont.SetMarkerColor(contourcolors[ix])
                cont.SetLineStyle(contourstyle[ix])
                cont.SetLineWidth(3)
                the_contours[intervals[len(intervals) - ix - 1]].append(cont.Clone())
        return the_contours

    @staticmethod
    def getThresholdForContainment(hist, intervals):
        """
        Returns the thresholds for the given credibility intervals
        @param hist: Histogram from which to generate the thresholds
        @param intervals: list of credibility intervals for which to generate the thresholds
        """
        # interval needs to be sorted from low to high
        contents = []
        thresholds = []  # returned thresholds corresponding to asked containment intervals
        total = 0
        # sort the bin contentss in descending order
        for xbin in range(hist.GetNbinsX() + 1):
            for ybin in range(hist.GetNbinsY() + 1):
                val = hist.GetBinContent(xbin, ybin)
                if val >= 0:
                    contents.append(val)
                    total += val
        contents.sort(reverse=True)

        threshold = 0
        intervalix = 0
        for ix, val in enumerate(contents):
            threshold += val
            if threshold >= intervals[intervalix] * total:
                thresholds.append(val)
                intervalix += 1
                if intervalix == len(intervals):
                    break
        thresholds.sort()
        return thresholds
    
    def relicDensity1D(
        self,
        analysis="combined", 
        flavor_list = {
            "higgsino" : {"color" : kBlue,"lineStyle"  : 1, "fillStyle": 3006, "title" : "higgsino-like #chi^{0}_{1}"},
            "wino" : {"color" : kGreen,"lineStyle"  : 1, "fillStyle": 3004, "title" : "wino-like #chi^{0}_{1}"},
            "bino" : {"color" : kRed,"lineStyle"  : 1, "fillStyle": 3002, "title" : "bino-like #chi^{0}_{1}"},
            "all" : {"color" : kBlack,"lineStyle"  : 2, "title" : "All Points"},
        },
        xbin = 100,
        xmin = 0.001,
        xmax = 1E6,
        xlog = True,
        ylog = False,
        customName:str = ""
        ):
        CMS.setCMSStyle()
        print("_____________________________",f"{printStyle.BOLD}{printStyle.ORANGE}1D Relic Density{printStyle.RESET}_____________________________")
        
        drawConfig = self.c.drawConfig["relicDensity1D"]

        name = "relicDensity1D"+customName
        
        if "simplified" in analysis:  # reweighting is always done, in addition to removing unreasonable points
            constraintstring = "*".join(
                [self.c.theconstraints["reweight"], self.c.theconstraints["reason_simplified"], self.constraints.getConstraint(analysis,isSimplified=True,verbose=False)])
        else:
            constraintstring = "*".join([self.c.theconstraints["reweight"], self.c.theconstraints["reason"], self.constraints.getConstraint(analysis,isSimplified=False,verbose=False)])
        
        
        hists = {}
        for key in flavor_list.keys():
            print(f"{printStyle.BULLET} {printStyle.BOLD}{printStyle.YELLOW}{key}{printStyle.RESET}")
            if self.c.terms.get(key) is None:
                print(f"{printStyle.BOLD}{printStyle.RED}No term found for {key}{printStyle.RESET}. Skipping")
                continue
            hists[key] = PlotterUtils.mkhistlogx(key,key,xbin, xmin, xmax,logx= xlog)
            self.tree.Draw("Omegah2>>" + hists[key].GetName(),"("+constraintstring+")*"+self.c.terms[key])

        total = hists["all"].Integral()
        for key in hists.keys():
            hists[key].Scale(1/total)

        legend = CMS.cmsLeg(
            **drawConfig["legendLocation"],
            columns = 1,
            textSize = 0.03)
        legend.SetHeader(self.constraints.getAnalysisName(analysis),"C")

        cxmin, cxmax, cymin, cymax = PlotterUtils.getAxisRangeOfList(list(hists.values()))

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
            y_max = cymax + drawConfig.get("yMaxOffset",0),
            nameXaxis = "#Omega_{h^{2}}",
            nameYaxis = "# Scanned Points (normalized)",
            canvName = name,
            square = CMS.kSquare,
            iPos = 0,
            leftMargin = 0.04,
            bottomMargin = 0.037,
            rightMargin = 0.02,
            with_z_axis = False,
            scaleLumi = None)
        
        for i,key in enumerate(hists.keys()):
            # hists[key].Scale(1/hists[key].Integral())
            hists[key].SetStats(0)
            hists[key].SetLineWidth(1)    
            hists[key].SetFillColor(flavor_list[key].get("color",kBlack))
            hists[key].SetFillStyle(flavor_list[key].get("fillStyle",0))
            hists[key].SetLineWidth(flavor_list[key].get("lineWidth",3))
            hists[key].SetLineColor(flavor_list[key].get("color",kBlack))
            hists[key].SetLineStyle(flavor_list[key].get("lineStyle",1))
            # hists[key].SetFillColorAlpha(flavor_list[key].get("fillColor",flavor_list[key].get("color",kBlack)),0.5)
            print(key)
            hists[key].Draw("hist same")
        
        flavor_list_copy = list(hists.keys())
        flavor_list_copy.reverse()
        for key in flavor_list_copy:
            legend.AddEntry(hists[key], flavor_list[key].get("title", key), "lf")


        planck = 0.1199

        ymax = max([hists[key].GetMaximum() for key in hists.keys()])

        line = TLine(planck, canvas.GetUymin(), planck, ymax)
        line.SetLineWidth(2)
        line.Draw("same")
        latex = TLatex(planck + 0.01, ymax * 0.9, "Planck")
        latex.SetTextSize(0.04) 
        latex.SetTextAlign(11)
        latex.Draw("same")

        legend.Draw("same")
        if xlog:
            canvas.SetLogx()
        if ylog:
            canvas.SetLogy()
            
        hframe = CMS.GetcmsCanvasHist(canvas)
        hframe.GetYaxis().SetTitleOffset(drawConfig.get("YaxisSetTitleOffset",1.35))
        hframe.GetXaxis().SetTitleOffset(drawConfig.get("XaxisSetTitleOffset",1.15))
        CMS.SaveCanvas(canvas, self.outputpath+name+"."+self.defaultFileFormat, close=True)
        print("_______________________________________________________________________________________\n\n")
        
    def ZScorePlots(self,  
                    analysis:str = "combined",
                    moreconstraints:list = [],
                    xbin = 100,
                    xmin = -5,
                    xmax = 5,
                    xlog = False,
                    ylog = True):
        CMS.setCMSStyle()
        print("_____________________________",f"{printStyle.BOLD}{printStyle.ORANGE}Z Score{printStyle.RESET}", f"{printStyle.RESET}","_____________________________")
        

        if "simplified" in analysis:  # reweighting is always done, in addition to removing unreasonable points
                isSimplified = True
                constraintstring = "*".join([self.c.theconstraints["reweight"], self.c.theconstraints["reason_simplified"]])
        else:
            isSimplified = False
            constraintstring = "*".join([self.c.theconstraints["reweight"], self.c.theconstraints["reason"]])
        for newc in moreconstraints:
            constraintstring += "*(" + newc + ")"

        z = self.constraints.getZScore(analysis,isSimplified)
        print("z:",z)
        hist = PlotterUtils.mkhistlogx("z_score","z_score",xbin, xmin, xmax,logx= xlog)
        self.tree.Draw(f"{z}>>" + hist.GetName(),constraintstring)
        
        print("Total Entries: ", hist.Integral())
        hist.Scale(1/hist.Integral())

        cxmin, cxmax, cymin, cymax = PlotterUtils.getAxisRangeOfList([hist])

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
            y_max = cymax + (0.003),
            nameXaxis = "Z Score",
            nameYaxis = "# Entries (Normalized)",
            canvName = "z_score",
            square = CMS.kSquare,
            iPos = 0,
            leftMargin = 0.06,
            bottomMargin = 0.037,
            rightMargin = 0.02,
            with_z_axis = False,
            scaleLumi = None,
                  customStyle= {
                "SetXNdivisions":509
            })
        
        
        # hist.SetStats(0)
        # hist.SetLineWidth(1)    
        PlotterUtils.histoStyler(hist, CMSColors.six.blue, fill=True)
        hist.Draw("hist same")
        
        if xlog:
            canvas.SetLogx()
        if ylog:
            canvas.SetLogy()
            
        legend = CMS.cmsLeg(
            x1 = 0.25,
            y1 = 0.8,
            x2 = 0.4,
            y2 = 0.95,
            columns = 1,
            textSize = 0.03)
        legend.SetHeader(self.constraints.getAnalysisName(analysis),"C")
        legend.Draw("same")
        
        hframe = CMS.GetcmsCanvasHist(canvas)
        hframe.GetYaxis().SetTitleOffset(1.65)
        hframe.GetXaxis().SetTitleOffset(1.15)
        CMS.SaveCanvas(canvas, self.outputpath+"z_score."+self.defaultFileFormat, close=True)
        print("_______________________________________________________________________________________\n\n")
        