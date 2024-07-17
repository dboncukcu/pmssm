from ROOT import *
import numpy as np
import os
from array import array

# Scaling Hist
def ScaleAxis(axis, scale_function):
    """
    Scales the bins of a given axis using a provided scaling function.

    Args:
        axis (TAxis): The axis object to be scaled.
        scale_function (function): A function that takes a bin value as input and returns the scaled value.

    Functionality:
        The function checks if the axis has variable-sized bins (using `GetXbins()`).
        If so, it applies the scaling function to each bin edge and sets the new bin edges using `TAxis::Set()`.
        If the axis has fixed-sized bins, it sets the axis range using the scaled minimum and maximum values.
    """
    if axis.GetXbins().GetSize():
        X = TArrayD(axis.GetXbins())
        for i in range(X.GetSize()):
            X[i] = scale_function(X[i])
        axis.Set(X.GetSize() - 1, X.GetArray())
    else:
        axis.Set(axis.GetNbins(), scale_function(axis.GetXmin()), scale_function(axis.GetXmax()))

def scaleXaxis(histogram, scaleFactor=1.0):
    """
    Scales the x-axis of a histogram by a given scale factor.

    Args:
        histogram (TH1): The histogram object whose x-axis needs to be scaled.
        scaleFactor (float, optional): The scale factor to be applied to the x-axis. Default is 1.0.

    Functionality:
        The function retrieves the x-axis of the histogram using `GetXaxis()`
        and passes it to the `ScaleAxis()` function along with a lambda function
        that divides each bin value by the scale factor.
    """
    x_axis = histogram.GetXaxis()
    ScaleAxis(x_axis, lambda x: x / scaleFactor)

def scaleYaxis(histogram, scaleFactor=1.0):
    """
    Scales the y-axis of a histogram by a given scale factor.

    Args:
        histogram (TH1): The histogram object whose y-axis needs to be scaled.
        scaleFactor (float, optional): The scale factor to be applied to the y-axis. Default is 1.0.

    Functionality:
        The function retrieves the y-axis of the histogram using `GetYaxis()`
        and passes it to the `ScaleAxis()` function along with a lambda function
        that divides each bin value by the scale factor.
    """
    y_axis = histogram.GetYaxis()
    ScaleAxis(y_axis, lambda y: y / scaleFactor)

# Scaling Graph
def scaleGraphXaxis(graph, scaleFactor=1.0):
    """
    Scales the x-coordinates of a graph by a given scale factor.

    Args:
        graph (TGraph): The graph object whose x-coordinates need to be scaled.
        scaleFactor (float, optional): The scale factor to be applied to the x-coordinates. Default is 1.0.

    Functionality:
        The function iterates over each point in the graph using `GetN()` and `GetPointX()`.
        It scales each x-coordinate by dividing it by the scale factor and sets the new x-coordinate
        using `SetPointX()`.
    """
    n = graph.GetN()
    for i in range(n):
        x = graph.GetPointX(i)
        graph.SetPointX(i, x / scaleFactor)

def scaleGraphYaxis(graph, scaleFactor=1.0):
    """
    Scales the y-coordinates of a graph by a given scale factor.

    Args:
        graph (TGraph): The graph object whose y-coordinates need to be scaled.
        scaleFactor (float, optional): The scale factor to be applied to the y-coordinates. Default is 1.0.

    Functionality:
        The function iterates over each point in the graph using `GetN()` and `GetPointY()`.
        It scales each y-coordinate by dividing it by the scale factor and sets the new y-coordinate
        using `SetPointY()`.
    """
    n = graph.GetN()
    for i in range(n):
        y = graph.GetPointY(i)
        graph.SetPointY(i, y / scaleFactor)

# Custom Palette for Survival Plots
def createSurvivalPlotPalette():
    """
    Creates a custom color palette for survival plots.

    Returns:
        np.array: An array of color indices representing the custom palette.

    Functionality:
        This function generates a custom color palette by iterating over the existing ROOT color palette.
        - For the first 19 colors, it sets the color to black (`kBlack`).
        - For the remaining colors, it uses the default ROOT color palette.
        - The resulting color indices are stored in a NumPy array of type `intc` (C-style integers).
    """
    custompalette = []
    cols = TColor.GetNumberOfColors()
    for i in range(cols):
        if i < 19:
            col = kBlack
        else:
            col = TColor.GetColorPalette(i)
        custompalette.append(col)
    custompalette = np.intc(custompalette)
    return custompalette

# Axis Range
def getAxisRange(obj, offset: dict = {"xmin": 0.0, "xmax": 0.0, "ymin": 0.0, "ymax": 0.0}):
    """
    Retrieves the axis ranges of a given histogram or graph, with optional offsets.

    Args:
        obj (TH1 or TGraph): The object (either a histogram or a graph) whose axis ranges are to be retrieved.
        offset (dict, optional): A dictionary specifying the offsets to be applied to the axis ranges. 
                                 Default is {"xmin": 0.0, "xmax": 0.0, "ymin": 0.0, "ymax": 0.0}.

    Returns:
        tuple: A tuple containing the modified axis ranges (xmin, xmax, ymin, ymax).

    Functionality:
        - If the object is a histogram (`TH1`), it retrieves the x-axis minimum and maximum using `GetXaxis().GetXmin()` and `GetXaxis().GetXmax()`, and the y-axis minimum and maximum using `GetMinimum()` and `GetMaximum()`.
        - If the object is a graph (`TGraph`), it retrieves the x-axis minimum and maximum using `GetXaxis().GetXmin()` and `GetXaxis().GetXmax()`, and the y-axis minimum and maximum using `GetHistogram().GetMinimum()` and `GetHistogram().GetMaximum()`.
        - If the object is neither a histogram nor a graph, it raises a `TypeError`.
        - The function then adjusts the retrieved axis ranges by applying the specified offsets from the `offset` dictionary.
        - Finally, it returns the modified axis ranges as a tuple (xmin, xmax, ymin, ymax).
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

    xmin -= offset.get("xmin", 0.0)
    xmax += offset.get("xmax", 0.0)
    ymin -= offset.get("ymin", 0.0)
    ymax += offset.get("ymax", 0.0)
    
    return xmin, xmax, ymin, ymax

def getAxisRangeOfList(obj_list, offset: dict = {"xmin": 0.0, "xmax": 0.0, "ymin": 0.0, "ymax": 0.0}):
    """
    Retrieves the axis ranges of a list of histograms or graphs, with optional offsets.

    Args:
        obj_list (list of TH1 or TGraph): The list of objects (either histograms or graphs) whose axis ranges are to be retrieved.
        offset (dict, optional): A dictionary specifying the offsets to be applied to the axis ranges. 
                                 Default is {"xmin": 0.0, "xmax": 0.0, "ymin": 0.0, "ymax": 0.0}.

    Returns:
        tuple: A tuple containing the modified axis ranges (xmin, xmax, ymin, ymax).

    Functionality:
        - The function iterates over each object in the list and retrieves the axis ranges using the `getAxisRange()` function.
        - It then combines the axis ranges from all objects in the list to determine the overall minimum and maximum values.
        - Finally, it returns the combined axis ranges as a tuple (xmin, xmax, ymin, ymax).
    """
    xmin_list, xmax_list, ymin_list, ymax_list = zip(*[getAxisRange(obj, offset) for obj in obj_list])
    xmin = min(xmin_list)
    xmax = max(xmax_list)
    ymin = min(ymin_list)
    ymax = max(ymax_list)
    
    return xmin, xmax, ymin, ymax

# Reading root Files
def create_tree(root_dict):
    """
    Creates a main tree from the first element of root_dict and adds friend trees to it based on the provided dictionary.

    Args:
        root_dict (list of dict): A list of dictionaries, where each dictionary contains:
            - 'treeName' (str): The name of the tree.
            - 'filePath' (str): The path to the ROOT file containing the tree.

    Returns:
        TChain: The main tree with friend trees added if there are any.

    Functionality:
        The function uses the first element in the list as the main tree. It then iterates over the
        remaining elements in the list to add them as friend trees to the main tree using `AddFriend()`.
        Finally, it returns the main tree.
    """
    if not root_dict:
        raise ValueError("The root_dict list is empty")

    main_tree_info = root_dict[0]
    mainTreeName = main_tree_info["treeName"]
    mainTreePath = main_tree_info["filePath"].strip()

    main_file = TFile(mainTreePath)
    main_tree = main_file.Get(mainTreeName)

    if len(root_dict) == 1:
        return main_tree,main_file

    store = []

    for friend in root_dict[1:]:
        
        friendTreeName = friend["treeName"]
        friendTreePath = friend["filePath"].strip()
        
        newFriendName = friend.get("name", friendTreeName)
        
        friendTreeFile = TFile(friendTreePath)
        friendTree = friendTreeFile.Get(friendTreeName)
        
        friendTree.BuildIndex("Niteration","chain_index")
        
        store.append([friendTreeFile,friendTree])
        main_tree.AddFriend(friendTree, newFriendName)

    return main_tree,main_file,store

# Create Output Directory

def create_output_directory(output_path):
    if output_path[-1] != "/":
        output_path += "/"
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    return output_path
        

def mkhistlogx(name, title, nbins, xmin, xmax,logx=True):
    if logx:
    
        if xmin == 0:
            logxmin = 0
        else:                
            logxmin = TMath.Log10(xmin)
        if xmax == 0:
            logxmax = 0
        else:
            logxmax = TMath.Log10(xmax)
    else:
        logxmin=xmin
        logxmax=xmax
    binwidth = (logxmax-logxmin)/nbins
    xbins = array('d',[0]*(nbins+1))##might need to be defined out as 0's
    #xbins[0] = TMath.Power(10,logxmin)#xmin
    for i in range(0,nbins+1):
        if logx:
            xbins[i] =  TMath.Power(10,logxmin+i*binwidth)
        else:
            xbins[i]= xmin + i*binwidth

#    print ('xbins', xbins )       
    h = TH1F(name,title,nbins,xbins)
    return h

def mkhistlogxy(name, title, nbinsx, xmin, xmax,nbinsy,ymin,ymax,logx=True,logy=True):
    if logx:
        if xmin == 0:
            logxmin = 0
        else:                
            logxmin = TMath.Log10(xmin)
        if xmax == 0:
            logxmax = 0
        else:
            logxmax = TMath.Log10(xmax)
    else:
        logxmin=xmin
        logxmax=xmax
    if logy:
        if ymin == 0:
            logymin = 0
        else:                
            logymin = TMath.Log10(ymin)
        if ymax == 0:
            logymax = 0
        else:
            logymax = TMath.Log10(ymax)
    else:
        logymin=ymin
        logymax=ymax
    binwidthx = float(logxmax-logxmin)/nbinsx
    binwidthy = float(logymax-logymin)/nbinsy
    xbins = array('d',[0]*(nbinsx+1))##might need to be defined out as 0's
    ybins = array('d',[0]*(nbinsy+1))##might need to be defined out as 0's
    #xbins[0] = TMath.Power(10,logxmin)#xmin
    for i in range(0,nbinsx+1):
        if logx:
            xbins[i] = 0 + TMath.Power(10,logxmin+i*binwidthx)
        else:
            xbins[i]= xmin + i*binwidthx
    for i in range(0,nbinsy+1):
        if logy:
            ybins[i] = 0 + TMath.Power(10,logymin+i*binwidthy)
        else:
            ybins[i] = ymin + i*binwidthy
#    print 'xbins', xbins[0],xbins[-1]
#    print 'ybins', ybins
    h = TH2F(name,title,nbinsx,xbins,nbinsy,ybins)
    return h

def mkhistlogxyz(name, title, nbinsx, xmin, xmax,nbinsy,ymin,ymax,nbinsz,zmin,zmax,logx=True,logy=True,logz=True):
    if logx:
        if xmin == 0:
            logxmin = 0
        else:                
            logxmin = TMath.Log10(xmin)
        if xmax == 0:
            logxmax = 0
        else:
            logxmax = TMath.Log10(xmax)
    else:
        logxmin=xmin
        logxmax=xmax
    if logy:
        if ymin == 0:
            logymin = 0
        else:                
            logymin = TMath.Log10(ymin)
        if ymax == 0:
            logymax = 0
        else:
            logymax = TMath.Log10(ymax)
    else:
        logymin=ymin
        logymax=ymax
    if logz:
        if zmin == 0:
            logzmin = 0
        else:                
            logzmin = TMath.Log10(zmin)
        if zmax == 0:
            logzmax = 0
        else:
            logzmax = TMath.Log10(zmax)
    else:
        logzmin=zmin
        logzmax=zmax
    binwidthx = float(logxmax-logxmin)/nbinsx
    binwidthy = float(logymax-logymin)/nbinsy
    binwidthz = float(logzmax-logzmin)/nbinsz
    xbins = array('d',[0]*(nbinsx+1))##might need to be defined out as 0's
    ybins = array('d',[0]*(nbinsy+1))##might need to be defined out as 0's
    zbins = array('d',[0]*(nbinsz+1))##might need to be defined out as 0's
    #xbins[0] = TMath.Power(10,logxmin)#xmin
    for i in range(0,nbinsx+1):
        if logx:
            xbins[i] = TMath.Power(10,logxmin+i*binwidthx)
        else:
            xbins[i]= xmin + i*binwidthx
    for i in range(0,nbinsy+1):
        if logy:
            ybins[i] =  TMath.Power(10,logymin+i*binwidthy)
        else:
            ybins[i] = ymin + i*binwidthy
    for i in range(0,nbinsz+1):
        if logz:
            zbins[i] =  TMath.Power(10,logzmin+i*binwidthz)
        else:
            zbins[i] = zmin + i*binwidthz
#    print 'xbins', xbins[0],xbins[-1]
#    print 'ybins', ybins        
    h = TH3F(name,title,nbinsx,xbins,nbinsy,ybins,nbinsz,zbins)
    return h

def histoStyler(h,color = kBlue,fill = False,linestyle = 1,linewidth = 3,fillstyle = 3009,markerstyle = 1,markersize = 1):
    h.SetLineWidth(linewidth)
    h.SetLineColor(color)
    h.SetMarkerColor(color)
    h.SetMarkerStyle(markerstyle)
    h.SetMarkerSize(markersize)
    h.SetLineStyle(linestyle)
    if fill:
        h.SetFillColor(color)
        h.SetFillStyle(fillstyle)    
    h.Sumw2()

def makeLegendFillWhite(legend):
        legend.SetFillStyle(1001)
        legend.SetTextColor(kBlack)
        legend.SetFillColor(kWhite)