from ROOT import *
import numpy as np

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
        return main_tree

    # Add remaining elements as friends
    for friend in root_dict[1:]:
        friendTreeName = friend["treeName"]
        friendTreePath = friend["filePath"].strip()  # Get the file path and remove leading/trailing whitespace
        main_tree.AddFriend(friendTreeName, TFile(friendTreePath))

    return main_tree,main_file