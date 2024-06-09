from ROOT import *
from PlotterConfig import PlotterConfig
import PlotterUtils
from cmsstylelib import cmsstyle as CMS
from Constraints import Constraints

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
        drawConfig: dict|str = None,
        legendStyle: dict|str = None):
        print("->Drawing 1D Impact for", drawstring)
        if drawConfig is None:
            drawConfig = self.c.drawConfig["impact1D"]
        
        if legendStyle is None:
            legendStyle = "rightBottom"
        if isinstance(legendStyle, str):
            legendConfig = drawConfig.get("legendStyle",legendStyle)
        if isinstance(legendStyle, dict):
            legendConfig = legendStyle
        legendConfig = self.c.drawConfig["impact1D"][legendConfig]
        
        if xaxisDrawConfig is None:
            xaxisDrawConfig = self.c.particleConfig[drawstring]
        
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
            scaleLumi = None)
        
        if xaxisDrawConfig.get("logScale", False):
            canvas.SetLogx()
        if xaxisDrawConfig.get("1Dlogy", False):
            canvas.SetLogy()
    
        prior.Draw("hist same")
        posterior.Draw("histsame")
        posterior_up.Draw("histsame")
        posterior_down.Draw("histsame")
        
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
        print("-> Done Drawing 1D Impact for", drawstring)