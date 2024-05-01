
from ROOT import *
import os,sys
from utils.utils import *
import argparse
import numpy as np
# terms defining
terms = {}
terms["higgsino"] = "(Re_N_13**2+Re_N_14**2)"
terms["bino"] = "Re_N_11**2"
terms["wino"] = "Re_N_12**2"

#constraints relating to the analyses likelihoods and others
theconstraints = {}
theconstraints["reason"] = "(!(xsec_tot_pb>1E3 && Zsig_combined==0))" # this excludes points with enormous weights that could not be excluded, almost certaintly due to these large weights and statistical chance
theconstraints["reason"] = "(1)"

theconstraints["reason_simplified"] = "(!(xsec_tot_pb>1E3 && Zsig_combined_simplified==0))"# this excludes points with enormous weights that could not be excluded, almost certaintly due to these large weights and statistical chance
theconstraints["reason_simplified"] = "(1)"

theconstraints["reweight"] = "(1/PickProbability)" #this reweights each point to remove the effect of over-sampling and under-sampling. Important for Bayesian interpretation of results that require a meaningful prior.

#The following are Bayes factors using simplified or (where available) full combine likelihoods

#Note from Sam 18 April, 2024: I am doing away with all the up and down keys and using replace() statements
#*_100s is the likelihood assuming a signal strength of 1, *_050s assumes a signal strength of 0.5, *_150s assumes a signal strength of 1.5, and *_0s assumes no signal (SM-only likelihood)
theconstraints["cms_sus_19_006"] = "(exp(llhd_cms_sus_19_006_100s-llhd_cms_sus_19_006_0s))"
theconstraints["cms_sus_18_004_simplified"] = "(exp(llhd_cms_sus_18_004_100s-llhd_cms_sus_18_004_0s))"
#At some point we switches to saving the Bayes factor directly in the tree, instead of the signal and signal-less likelihoods
#Here, muXpYf refers to signal strength of X.Y, and f refers to "full" as in full combine likelihood. The max sometimes has to be taken because root can't handle extremely small floats.
theconstraints["cms_sus_18_004"] = "(max(bf_cms_sus_18_004_mu1p0f,1E-5))"
theconstraints["cms_sus_21_007"] = "(exp(llhd_cms_sus_21_007_100s-llhd_cms_sus_21_007_0s))"
theconstraints["cms_sus_21_007_simplified"] = "(exp(llhd_cms_sus_21_007_100s-llhd_cms_sus_21_007_0s))"
theconstraints["cms_sus_21_006_simplified"] = "(exp(llhd_cms_sus_21_006_100s-llhd_cms_sus_21_006_0s))"
theconstraints["cms_sus_21_006"] = "(max(bf_cms_sus_21_006_mu1p0f,1E-5))"


theconstraints["cms_sus_20_001"] = "(max(bf_cms_sus_20_001_mu1p0s,1E-5))"
theconstraints["cms_sus_20_001_simplified"] = "(exp(llhd_cms_sus_20_001_mu1p0s-llhd_cms_sus_20_001_mu0p0s))"



#this part combines the various analysis Bayes factors, once including full combine likelihoods where possible, and once using only counts-based simplified likelihoods
#This sums up the likelihoods assuming the different signal strengths, and the SM-only likelihoods. The sum does not include the analyses where the Bayes factor is saved in the tree instead of the likelihoods
signals       = "+".join(["llhd_cms_sus_19_006_100s","llhd_cms_sus_20_001_mu1p0s"])
_backgrounds  = "+".join(["llhd_cms_sus_19_006_0s","llhd_cms_sus_20_001_mu0p0s"])
#Because we switched to saving Bayes factors, this became a little more complicated
#again, the max is taken because ROOT has problems with small floats

bfs = []
bfs.append("(max(bf_cms_sus_21_006_mu1p0f,1E-20))")
bfs.append("(max(bf_cms_sus_18_004_mu1p0f,1E-20))")


#We only started storing the Bayes factors for the full combine likelihoods, so the simplified version is simpler
signals_simplified = "+".join(["llhd_cms_sus_19_006_100s","llhd_cms_sus_21_006_100s","llhd_cms_sus_18_004_100s","llhd_cms_sus_19_006_mu1p0s"])
_backgrounds_simplified = "+".join(["llhd_cms_sus_19_006_0s","llhd_cms_sus_21_006_0s","llhd_cms_sus_18_004_0s","llhd_cms_sus_19_006_mu0p0s"])

#these are the Bayes factors for the combination of all analyses. The first term handles the analyses where the log likelihood is stored, the second term handles the analyses where the Bayes factor is stored in the tree 
theconstraints["combined"] = "(exp(("+signals+")-("+_backgrounds+"))"+(len(bfs)>0)*"*"+"*".join(bfs)+")"
theconstraints["combined_simplified"] = "(exp(("+signals_simplified+")-("+_backgrounds_simplified+")))"
# theconstraints["combined_with_cms_sus_20_001"] = "(exp(("+signals+"+llhd_cms_sus_20_001_mu1p0s"+")-("+_backgrounds+"+llhd_cms_sus_20_001_mu0p0s"+"))"+(len(bfs)>0)*"*"+"*".join(bfs)+")"


#some useful constraints
theconstraints["pure higgsino"] = "("+terms["higgsino"]+">0.95)"
theconstraints["pure wino"] = "("+terms["wino"]+">0.95)"
theconstraints["pure bino"] = "("+terms["bino"]+">0.95)"

theconstraints["bino-wino mix"] = "(!("+"||".join([theconstraints["pure bino"],theconstraints["pure wino"],theconstraints["pure higgsino"]])+") && "+terms["bino"]+">"+terms["higgsino"]+" && "+terms["bino"]+">"+terms["wino"]+")"
theconstraints["bino-higgsino mix"] = "(!("+"||".join([theconstraints["pure bino"],theconstraints["pure wino"],theconstraints["pure higgsino"]])+") && "+terms["bino"]+">"+terms["wino"]+" && "+terms["higgsino"]+">"+terms["wino"]+")"
theconstraints["wino-higgsino mix"] = "(!("+"||".join([theconstraints["pure bino"],theconstraints["pure wino"],theconstraints["pure higgsino"]])+") && "+terms["bino"]+"<"+terms["wino"]+" && "+terms["bino"]+"<"+terms["higgsino"]+")"

zscore = {}
for key in ['combined',"cms_sus_20_001","cms_sus_21_007"]:#, 'combined_simplified']:
    value = theconstraints[key]
    zscore[key] = "TMath::Abs(TMath::Log(%s))/(TMath::Log(%s)) * TMath::Sqrt(2 * TMath::Abs(TMath::Log(%s)))" % (value,value,value)

# print(zscore)
# print("-"*50)
# print(theconstraints["cms_sus_20_001"])
# print("-"*50)
# # print(theconstraints["combined_with_cms_sus_20_001"])
# print("-"*50)
# print(theconstraints["combined"])
# print("-"*50)


#z-axis colors
sprobcontours = np.float64([-0.01,1E-5,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1-1E-5,1.01])
custompalette = []
cols = TColor.GetNumberOfColors()# This gets the colors of the Palette currently set in ROOT
#This part sets bins with a survival probability of zero (less than second entry of sprobcontours list to be exact) to Black color. Bins with a survival probability of exactly 1 (greater than second last entry of sprobcontours list) to Grey.
for i in range(cols):
    if i<19: # The exact i was found by trial and error. Sorry.
        col = kBlack
    elif i > 253:
        col = kGray
    else:
        col = TColor.GetColorPalette(i) # This part keeps the color from the currently set palette
        
    custompalette.append(col)
custompalette = np.intc(custompalette)

#dictionary mapping the z-scores for the different analyses to the tree branches 
branchnames = {}
for analysis in ["cms_sus_19_006","cms_sus_21_006","cms_sus_18_004","combined", "combined_simplified","cms_sus_21_006_simplified","cms_sus_21_007","cms_sus_21_007_simplified"]:
    branchnames[analysis] = {}
    branchnames[analysis+"_up"] = {}
    branchnames[analysis+"_down"] = {}
    #now do the defaults
    if analysis in ["cms_sus_18_004","cms_sus_21_006"]:
        branchnames[analysis]["Z"] = "Zsig_"+analysis+"_mu1p0f"
        branchnames[analysis+"_up"]["Z"] = "Zsig_"+analysis+"_mu1p5f"
        branchnames[analysis+"_down"]["Z"] = "Zsig_"+analysis+"_mu0p5f"
    elif analysis == "combined_simplified":
        branchnames[analysis]["Z"] = "Zsig_"+analysis
    else:
        branchnames[analysis]["Z"] = "Zsig_"+analysis.replace("_simplified","")
        branchnames[analysis+"_up"]["Z"] = "Zsig_"+analysis.replace("_simplified","")+"_15s"
        branchnames[analysis+"_down"]["Z"] = "Zsig_"+analysis.replace("_simplified","")+"_05s"
# print(branchnames)


def get_SP_plot_2D(localtree, analysis, hname, xtitle, xbins, xlow, xup, ytitle, ybins, ylow, yup, _logx, _logy,
                   drawstring, moreconstraints=[], moreconstraints_prior=False):
    """
    This creates a 2D survival probability plot
    @param localtree: Function needs to be passed the ROOT tree from which to operate
    @param analysis: The analysis to use for LHC constraints. Can be any string for which a dictionary entry and corresponding ROOT branch exists in "branchnames". Currently does not allow for arbitrary combinations of analyses
    @param hname: Name of the returned histogram
    @param xtitle: x-axis label
    @param xbins: number of x-axis bins
    @param xlow: lower edge of zero'th bin
    @param xup: upper edge of xbins's bin
    @param ytitle: y-axis label
    @param ybins: number of y-axis bins
    @param ylow: lower edge of zero'th bin
    @param yup: upper edge of ybins's bin
    @param _logx: sets x-axis to logarithmic (base 10). If you use this, use linear Y:X in drawstring, not Y:log(X)
    @param _logy: sets y-axis to logarithmic (base 10). If you use this, use linear Y:X in drawstring, not log(Y):X
    @param drawstring: Draw string passed to root .Draw() function, of the form Y:X, where Y is drawn on the y-axis and X is drawn on the x-axis. Accepts tree branches and mathematical operations acted on them, such as for example log(Y):10*X.
    @param moreconstraints: list of logical expressions that constrain the tree. Can use tree branches and mathematical operations. Each constrain in the list is logically multiplied
    @param moreconstraints_prior: list of logical expressions that should apply to the prior. Default is to NOT apply constraints on the prior. Can use tree branches and mathematical operations. Each constrain in the list is logically multiplied
    """
    hdenom = mkhistlogxy("hdenom", '', xbins, xlow, xup, ybins, ylow, yup, logx=_logx, logy=_logy)
    hret = hdenom.Clone(
        hname)  # this makes sure that the denominator and the numerator histograms are identically set up
    hret.SetContour(len(sprobcontours) - 1, sprobcontours)  # this defines the z-axis color palette and tick length
    if "simplified" in analysis:  # reweighting is always done, in addition to removing unreasonable points
        constraintstring = "*".join([theconstraints["reweight"], theconstraints["reason_simplified"]])
        constraintstring_prior = "*".join([theconstraints["reweight"], theconstraints["reason_simplified"]])
    else:
        constraintstring = "*".join([theconstraints["reweight"], theconstraints["reason"]])
        constraintstring_prior = "*".join([theconstraints["reweight"], theconstraints["reason"]])
    for newc in moreconstraints:
        constraintstring += "*(" + newc + ")"
    if moreconstraints_prior:
        for newc_p in moreconstraints_prior:
            constraintstring_prior += "*(" + newc_p + ")"

    c_temp = TCanvas()
    
    localtree.Draw(drawstring + ">>" + hdenom.GetName(), constraintstring_prior, "colz")
    z = zscore[analysis]
    localtree.Draw(drawstring + ">>" + hret.GetName(), "*".join([constraintstring, "(" + z + ">-1.64)"]), "colz")
    
    c_temp.Clear()
    c_temp.Close()
    del c_temp
    
    hret.GetZaxis().SetRangeUser(-0.001, 1)
    cutoff = 1E-3
    # hret.GetZaxis().SetTitle("survival probability")
    hret.Divide(hdenom)
    for i in range(1, hret.GetNbinsX() + 1):
        for j in range(1, hret.GetNbinsY() + 1):
            if hret.GetBinContent(i, j) == 0 and hdenom.GetBinContent(i, j) > 0:
                hret.SetBinContent(i, j, 0)
            elif hret.GetBinContent(i, j) == 0 and hdenom.GetBinContent(i, j) == 0:
                hret.SetBinContent(i, j, -1)
            elif hret.GetBinContent(i, j) < cutoff and hdenom.GetBinContent(i, j) > 0:
                hret.SetBinContent(i, j, cutoff)
                
    
    # always run gStyle.SetPalette(len(custompalette),custompalette) when drawing SP, otherwise gStyle.SetPalette(kBird) or other preferred Palette
    # gStyle.SetNumberContours(999)
    # histoStyler(hret)
    # hret.GetXaxis().SetTitle(xtitle)
    # hret.GetYaxis().SetTitle(ytitle)
    # hret.GetZaxis().SetTitle("survival probability")
    hret.SetContour(len(sprobcontours) - 1, sprobcontours)  

    return hret