## This styling is for CMS plots. It uses cmsstyle library 0.3.0 version.
import cmsstyle as CMS


class Plotter:
    def __init__(self,canvasSettings:dict = {},canvasLabel:dict = {"energy" : 132,"extraText" : "Preliminary","lumi" : "(137-139)"},):
        
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
    
    def Draw(self,obj,option=""):
        '''
        Draw the object to the canvas.
        '''
        obj.Draw(option+ " same")
    
    def tuning(self,tuning:dict = {}):
        '''
        Tune the canvas.
        '''

        ## SetTitleOffset
        if (tuning.get("XaxisSetTitleOffset") is not None):
            self.hframe.GetXaxis().SetTitleOffset(tuning.get("XaxisSetTitleOffset"))
        if (tuning.get("YaxisSetTitleOffset") is not None):
            self.hframe.GetYaxis().SetTitleOffset(tuning.get("YaxisSetTitleOffset"))

        ## SetMaxDigits
        if (tuning.get("XaxisSetMaxDigits") is not None):
            self.hframe.GetXaxis().SetMaxDigits(tuning.get("XaxisSetMaxDigits"))
        if (tuning.get("YaxisSetMaxDigits") is not None):
            self.hframe.GetYaxis().SetMaxDigits(tuning.get("YaxisSetMaxDigits"))
            
        ##GetBottomMargin
        if (tuning.get("SetBottomMargin") is not None):
            self.canvas.SetBottomMargin( self.canvas.GetBottomMargin() + float(tuning.get("SetBottomMargin")))

    def SaveAs(self,path,redraw=True):
        '''
        Save the canvas.
        '''
        if redraw:
            CMS.CMS_lumi(self.canvas, self.canvasSettings.get("iPos",11), self.canvasSettings.get("scaleLumi",None))
        CMS.SaveCanvas(self.canvas, path, close=True)
    
    def __del__(self):
        '''
        Destructor to delete the canvas.
        '''
        try:
            del(self.canvas)
            del(self.hframe)
        except:
            pass