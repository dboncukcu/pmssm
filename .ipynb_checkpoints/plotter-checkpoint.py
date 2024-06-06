## Dorukhan Boncukçu
## 02/05/2024
## This styling is for CMS plots. It uses cmsstyle library 0.3.0 version.
import cmsstyle as CMS
from ROOT import *
from collections.abc import Iterable

class Plotter:
    def __init__(self,canvasSettings:dict = {},canvasLabel:dict = {"energy" : 13,"extraText" : "Preliminary","lumi" : "(137-139)"},):

        self.setCanvasLabel(canvasLabel)
        
        self.createCanvas(
            x_min = canvasSettings.get("xmin",0),
            x_max = canvasSettings.get("xmax",1),
            y_min = canvasSettings.get("ymin",0),
            y_max = canvasSettings.get("ymax",1),
            nameXaxis = canvasSettings.get("nameXaxis",""),
            nameYaxis = canvasSettings.get("nameYaxis",""),
            canvName = canvasSettings.get("canvName",None),
            square = canvasSettings.get("square",CMS.kSquare),
            iPos = canvasSettings.get("iPos",11),
            extraSpace = canvasSettings.get("extraSpace",0.01),
            with_z_axis = canvasSettings.get("is3D",False),
            scaleLumi = canvasSettings.get("scaleLumi",None)
        )
        self.canvasSettings = canvasSettings
        self.setPalette()
    
    @staticmethod
    def Reset():
        gROOT.GetListOfCanvases().Clear()
        gStyle.Reset()
            
        
    def setCanvasLabel(self,canvasLabel:dict):
        '''
        Set the canvas labels for the plot.
        '''
        if canvasLabel.get("energy") is not None:
            CMS.SetEnergy(str(canvasLabel.get("energy")))
        if canvasLabel.get("extraText") is not None:
            CMS.SetExtraText(canvasLabel.get("extraText"))
        if canvasLabel.get("lumi") is not None:
            CMS.SetLumi(canvasLabel.get("lumi"))
    
    def createCanvas(self,
        x_min,
        x_max,
        y_min,
        y_max,
        nameXaxis,
        nameYaxis,
        canvName = None,
        square=CMS.kSquare,
        iPos=11,
        extraSpace=0,
        with_z_axis=False,
        scaleLumi=None):
        """
            Draw a canvas with CMS style.

            canvName: Name of the canvas.
            x_min: Minimum value of the x-axis.
            x_max: Maximum value of the x-axis.
            y_min: Minimum value of the y-axis.
            y_max: Maximum value of the y-axis.
            nameXaxis: Label for the x-axis.
            nameYaxis: Label for the y-axis.
            square: If True, canvas is square.
            iPos: Position of the CMS logo in the plot.
                iPos=11 : top-left, left-aligned
                iPos=33 : top-right, right-aligned
                iPos=22 : center, centered
                iPos=0  : out of frame (in exceptional cases)
                mode generally : iPos = 10*(alignement 1/2/3) + position (1/2/3 = l/c/r)
            extraSpace: add extra space to the left margins to fit lable
        """
        self.canvas = CMS.cmsCanvas(
            x_min = x_min,
            x_max = x_max,
            y_min = y_min,
            y_max = y_max,
            nameXaxis = nameXaxis,
            nameYaxis = nameYaxis,
            canvName = canvName,
            square = square,
            iPos = iPos,
            extraSpace = extraSpace,
            with_z_axis = with_z_axis,
            scaleLumi = scaleLumi)
        self.hframe = CMS.GetcmsCanvasHist(self.canvas)
    
    def Draw2D(self,obj,option="colz"):
        '''
        Draw the object to the canvas.
        '''
        obj.Draw(option+ " same")
        CMS.UpdatePalettePosition(obj,self.canvas)
        # CMS.UpdatePad(self.canvas)
    
    def UpdatePalettePosition(self,hist2D):
        '''
        Update the palette position.
        '''
        CMS.UpdatePalettePosition(hist2D,self.canvas)
    
    def tuning(self,tuning:dict = {},hist=None):
        '''
        Tune the canvas.
        '''

        ## SetTitleOffset
        if (tuning.get("XaxisSetTitleOffset") is not None):
            self.hframe.GetXaxis().SetTitleOffset(tuning.get("XaxisSetTitleOffset"))
        if (tuning.get("YaxisSetTitleOffset") is not None):
            self.hframe.GetYaxis().SetTitleOffset(tuning.get("YaxisSetTitleOffset"))
        if (tuning.get("ZaxisSetTitleOffset") is not None and hist is not None):
            hist.GetZaxis().SetTitleOffset(tuning.get("ZaxisSetTitleOffset"))

        ## SetMaxDigits
        if (tuning.get("XaxisSetMaxDigits") is not None):
            self.hframe.GetXaxis().SetMaxDigits(tuning.get("XaxisSetMaxDigits"))
        if (tuning.get("YaxisSetMaxDigits") is not None):
            self.hframe.GetYaxis().SetMaxDigits(tuning.get("YaxisSetMaxDigits"))
        if (tuning.get("ZaxisSetMaxDigits") is not None and hist is not None):
            hist.GetZaxis().SetMaxDigits(tuning.get("ZaxisSetMaxDigits"))
            
        ##GetBottomMargin
        if (tuning.get("SetBottomMargin") is not None):
            self.canvas.SetBottomMargin( self.canvas.GetBottomMargin() + float(tuning.get("SetBottomMargin")))
        
        CMS.UpdatePad(self.canvas)
    
    ## CANVAS ##
    def SetLog(self,logx : bool | None = None,logy: bool | None = None,logz: bool | None = None):
        
        if hasattr(self, 'canvas'):
            if logx is not None:
                self.canvas.SetLogx(logx)
            if logy is not None:
                self.canvas.SetLogy(logy)
            if logz is not None:
                self.canvas.SetLogz(logz)
        else:
            print("Canvas is not defined.")
        
    ## CANVAS ##
    def SaveAs(self,path,redraw=False):
        '''
        Save the canvas.
        '''
        if redraw:
            CMS.CMS_lumi(self.canvas, self.canvasSettings.get("iPos",11), self.canvasSettings.get("scaleLumi",None))
        CMS.SaveCanvas(self.canvas, path, close=True)
    
    ## LEGEND ##
    def createLegend(self,x1,x2,y1,y2,textSize=0.02, columns=None, header=None):
        self.legend = CMS.cmsLeg(x1=x1,x2=x2,y1=y1,y2=y2,textSize = textSize, columns=columns)
        if header is not None:
            self.legend.SetHeader(header)
    
    def moveLegend(self, x1=None, x2=None, y1=None, y2=None):
        if not hasattr(self, 'legend'):
            print("Legend does not exist.")
            return

        if x1 is not None:
            self.legend.SetX1NDC(x1)
        if x2 is not None:
            self.legend.SetX2NDC(x2)
        if y1 is not None:
            self.legend.SetY1NDC(y1)
        if y2 is not None:
            self.legend.SetY2NDC(y2)
    
    def addEntryToLegend(self,entry,text,option = "l"):
        if not hasattr(self, 'legend'):
            print("Legend does not exist.")
            return
        self.legend.AddEntry(entry,text,option)

    def fillWhiteLegend(self):
        if not hasattr(self, 'legend'):
            print("Legend does not exist.")
            return
        self.legend.SetFillStyle(1001)
        self.legend.SetFillColor(kWhite)
    
    def whiteColorLegend(self):
        if not hasattr(self, 'legend'):
            print("Legend does not exist.")
            return
        self.legend.SetTextColor(kWhite)
        
    
    ## LEGEND ##

    ## Color Palette ##
    @staticmethod
    def setPalette(palette = None):
        
        # if palette is not None:
        #     global ColorPalette
        #     ColorPalette = palette
        ColorPalette = palette    
        if ColorPalette is not None:
            if isinstance(ColorPalette, Iterable):
                gStyle.SetPalette(len(ColorPalette),ColorPalette)
            else:
                gStyle.SetPalette(ColorPalette)
        
    ## Color Palette ##
    
    def __del__(self):
        '''
        Destructor to delete the canvas.
        '''
        try:
            del(self.canvas)
            del(self.hframe)
        except:
            pass
    
    # utils
    @staticmethod            
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
    @staticmethod
    def scaleXaxis(histogram,scaleFactor=1.0):
        x_axis = histogram.GetXaxis()

        Plotter.ScaleAxis(x_axis,lambda x: x / scaleFactor)
    @staticmethod
    def scaleYaxis(histogram,scaleFactor=1.0):
        y_axis = histogram.GetYaxis()

        Plotter.ScaleAxis(y_axis,lambda y: y / scaleFactor)
    @staticmethod
    def scaleGraphXaxis(graph, scaleFactor=1.0):
        n = graph.GetN()
        for i in range(n):
            x = graph.GetPointX(i)
            graph.SetPointX(i, x / scaleFactor)
    @staticmethod
    def scaleGraphYaxis(graph, scaleFactor=1.0):
        n = graph.GetN()
        for i in range(n):
            y = graph.GetPointY(i)
            graph.SetPointY(i, y / scaleFactor)
