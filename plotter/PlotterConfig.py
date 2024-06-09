class PlotterConfig:
    
    def print(self, name: str):
        if hasattr(self,name):
            print(f"Configuration for {name}:")
            config = getattr(self,name)
            
            for key, value in getattr(self,name).items():
                print(f"{key}: {value}")
        else:
            print(f"No configuration found for {name}")
    
    def __init__(self):
        ###################################################################
        ###################### Global Settings ######################
        self.global_settings = {}
        self.global_settings["logEps"] = 1e-5 # Minimum Treshold for log scaling
        self.global_settings["outputFileFormat"] = "pdf" # Default file format for saving
        self.global_settings["outputPath"] = "output/" # Default output path for saving
        
        ###################################################################
        ###################### CMS Label Information ######################
        self.cms_label = {}
        self.cms_label["energy"] = "13" # TeV
        self.cms_label["extraText"] = "Preliminary"
        self.cms_label["lumi"] = "137-139" # fb^-1
        
        ###################################################################
        ################### Particle Drawing Information ###################
        # - bins [int] : Number of bins in the histogram
        # - max [int] : Maximum value for the histogram axis before scaling
        # - min [int] : Minimum value for the histogram axis before scaling
        # - logScale [bool] : Flag for logarithmic scale
        # - linearScale [float] : Linear scale factor
        # - unit [str] : Unit of measurement
        # - title [str] : Title for the histogram (with latex)
        # - name [str]: Name of the particle or parameter for saving filename
        # - 1Dlogy [bool] : Flag for logarithmic scale in 1D histograms
        
        self.particleConfig = {
            "default" : {
                "bins": 100,
                "max": 1000,
                "min": 0,
                "logScale": False,
                "linearScale": 1000.0,
                "unit": "TeV",
                "title": "",
                },
            "abs(chi10)" : {
                "title" : "m_{#tilde{#chi}^{0}_{1}}",
                "bins" : 50,
                "min" : 0,
                "max" : 1000,
                "logScale" : False,
                "linearScale": 1000,
                "unit": "TeV",
                "name" : "chi10"
                },
            "abs(chi20)" : {
                "title" : "m_{#tilde{#chi}^{0}_{2}}",
                "bins" : 50,
                "min" : 0,
                "max" : 2500,
                "logScale" : False,
                "linearScale": 1000,
                "unit": "TeV",
                "name" : "chi20"
            },
            "g": {
                "title" : "m_{#tilde{g}}",
                "bins" : 100,
                "min" : 0,
                "max" : 7000,
                "logScale" : False,
                "linearScale": 1000,
                "unit": "TeV",
                "name" : "gluino"
                },
            "t1" : {
                "title": "m_{#tilde{t}_{1}}",
                "bins" : 100,
                "min" : 0,
                "max" : 7000,
                "logScale": False,
                "linearScale": 1000.0,
                "unit": "TeV",
                "name": "stop1"
                
            },
            "t2" : {
                "title": "m_{#tilde{t}_{2}}",
                "bins" : 100,
                "min" : 0,
                "max" : 7000,
                "logScale": False,
                "linearScale": 1000.0,
                "unit": "TeV",
                "name": "stop2"
                
            },
            "b1" : {
                "title": "m_{#tilde{b}_{1}}",
                "bins" : 100,
                "min" : 0,
                "max" : 7000,
                "logScale": False,
                "linearScale": 1000.0,
                "unit": "TeV",
                "name": "sbottom"
            },
            "lcsp" : {
                "title" : "m_{LCSP}",
                "bins" : 50,
                "min" : 0,
                "max" : 7000,
                "logScale" : False,
                "linearScale": 1000, # for TeV, 1GeV/1000
                "unit": "TeV",
                "name" : "lcsp"
                },
            "abs(chi1pm)-abs(chi10)": {
                "title": "#Deltam(#tilde{#chi}^{#pm}_{1},#tilde{#chi}^{0}_{1})",
                "bins" : 100,
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
                "bins" : 100,
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
                "bins" : 100,
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
                "bins" : 100,
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
                "bins" : 100,
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
                "bins" : 100,
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
                "bins" : 50,
                "min" : 0,
                "max" : 2500,
                "logScale" : False,
                "linearScale": 1000,
                "unit": "TeV",
                "name" : "chi1pm"
                }
            }
        
        ###################################################################
        ################### Analysis Configs ###################
        
        self.analysisConfigs = {
            'cms_sus_20_001': {
                'analysisName': 'SUS-20-001',
                'simplified': {
                    'llhd': {
                        'signal': 'llhd_cms_sus_20_001_mu1p0s',
                        'background': 'llhd_cms_sus_20_001_mu0p0s'
                    },
                    'bf': 'bf_cms_sus_20_001_mu1p0s'
                },
                'full': {
                    'llhd': {
                        'signal': 'llhd_cms_sus_20_001_mu1p0s',
                        'background': 'llhd_cms_sus_20_001_mu0p0s'
                    },
                    'bf': 'bf_cms_sus_20_001_mu1p0s'
                }
            },
            'cms_sus_19_006': {
                'analysisName': 'SUS-19-006',
                'simplified': {
                    'llhd': {
                        'signal': 'llhd_cms_sus_19_006_100s',
                        'background': 'llhd_cms_sus_19_006_0s'
                    },
                    'bf': None
                },
                'full': {
                    'llhd': {
                        'signal': 'llhd_cms_sus_19_006_100s',
                        'background': 'llhd_cms_sus_19_006_0s'
                    },
                    'bf': None
                }
            },
            'cms_sus_21_006': {
                'analysisName': 'SUS-21-006',
                'simplified': {
                    'llhd': {
                        'signal': 'llhd_cms_sus_21_006_100s',
                        'background': 'llhd_cms_sus_21_006_0s'
                    },
                    'bf': None
                },
                'full': {
                    'llhd': {
                        'signal': None,
                        'background': None
                    },
                    'bf': 'bf_cms_sus_21_006_mu1p0f'
                }
            },
            'cms_sus_18_004': {
                'analysisName': 'SUS-18-004',
                'simplified': {
                    'llhd': {
                        'signal': 'llhd_cms_sus_18_004_100s',
                        'background': 'llhd_cms_sus_18_004_0s'
                    },
                    'bf': None
                },
                'full': {
                    'llhd': {
                        'signal': None,
                        'background': None
                    },
                    'bf': 'bf_cms_sus_18_004_mu1p0f'
                }
            }
        }
        ###################################################################
        ################### Physical Definings ###################
        
        self.terms = {}
        self.terms["higgsino"] = "(Re_N_13**2+Re_N_14**2)"
        self.terms["bino"] = "Re_N_11**2"
        self.terms["wino"] = "Re_N_12**2"
        
        
        ###################################################################
        ################### Signal Definings ###################
        
        self.signals       = "+".join(["llhd_cms_sus_19_006_100s","llhd_cms_sus_20_001_mu1p0s"])
        self._backgrounds  = "+".join(["llhd_cms_sus_19_006_0s","llhd_cms_sus_20_001_mu0p0s"])
        
        self.bfs = []
        self.bfs.append("(max(bf_cms_sus_21_006_mu1p0f,1E-20))")
        self.bfs.append("(max(bf_cms_sus_18_004_mu1p0f,1E-20))")
        
        self.signals_simplified = "+".join(["llhd_cms_sus_19_006_100s","llhd_cms_sus_21_006_100s","llhd_cms_sus_18_004_100s","llhd_cms_sus_19_006_mu1p0s"])
        self._backgrounds_simplified = "+".join(["llhd_cms_sus_19_006_0s","llhd_cms_sus_21_006_0s","llhd_cms_sus_18_004_0s","llhd_cms_sus_19_006_mu0p0s"])

        
        ###################################################################
        ################### Constraints Definings ###################
        
        self.theconstraints = {}
        self.theconstraints["reason"] = "(!(xsec_tot_pb>1E3 && Zsig_combined==0))" # this excludes points with enormous weights that could not be excluded, almost certaintly due to these large weights and statistical chance
        self.theconstraints["reason"] = "(1)"
        self.theconstraints["reason_simplified"] = "(!(xsec_tot_pb>1E3 && Zsig_combined_simplified==0))"# this excludes points with enormous weights that could not be excluded, almost certaintly due to these large weights and statistical chance
        self.theconstraints["reason_simplified"] = "(1)"
        self.theconstraints["reweight"] = "(1/PickProbability)" #this reweights each point to remove the effect of over-sampling and under-sampling. Important for Bayesian interpretation of results that require a meaningful prior.
        self.theconstraints["cms_sus_19_006"] = "(exp(llhd_cms_sus_19_006_100s-llhd_cms_sus_19_006_0s))"
        self.theconstraints["cms_sus_18_004_simplified"] = "(exp(llhd_cms_sus_18_004_100s-llhd_cms_sus_18_004_0s))"
        #At some point we switches to saving the Bayes factor directly in the tree, instead of the signal and signal-less likelihoods
        #Here, muXpYf refers to signal strength of X.Y, and f refers to "full" as in full combine likelihood. The max sometimes has to be taken because root can't handle extremely small floats.
        self.theconstraints["cms_sus_18_004"] = "(max(bf_cms_sus_18_004_mu1p0f,1E-5))"
        self.theconstraints["cms_sus_21_007"] = "(exp(llhd_cms_sus_21_007_100s-llhd_cms_sus_21_007_0s))"
        self.theconstraints["cms_sus_21_007_simplified"] = "(exp(llhd_cms_sus_21_007_100s-llhd_cms_sus_21_007_0s))"
        self.theconstraints["cms_sus_21_006_simplified"] = "(exp(llhd_cms_sus_21_006_100s-llhd_cms_sus_21_006_0s))"
        self.theconstraints["cms_sus_21_006"] = "(max(bf_cms_sus_21_006_mu1p0f,1E-5))"
        self.theconstraints["cms_sus_20_001"] = "(max(bf_cms_sus_20_001_mu1p0s,1E-5))"
        self.theconstraints["cms_sus_20_001_simplified"] = "(exp(llhd_cms_sus_20_001_mu1p0s-llhd_cms_sus_20_001_mu0p0s))"
        self.theconstraints["combined"] = "(exp(("+self.signals+")-("+self._backgrounds+"))"+(len(self.bfs)>0)*"*"+"*".join(self.bfs)+")"
        self.theconstraints["combined_simplified"] = "(exp(("+self.signals_simplified+")-("+self._backgrounds_simplified+")))" ## ?????
        #some useful constraints
        self.theconstraints["pure higgsino"] = "("+self.terms["higgsino"]+">0.95)"
        self.theconstraints["pure wino"] = "("+self.terms["wino"]+">0.95)"
        self.theconstraints["pure bino"] = "("+self.terms["bino"]+">0.95)"
        self.theconstraints["bino-wino mix"] = "(!("+"||".join([self.theconstraints["pure bino"],self.theconstraints["pure wino"],self.theconstraints["pure higgsino"]])+") && "+self.terms["bino"]+">"+self.terms["higgsino"]+" && "+self.terms["bino"]+">"+self.terms["wino"]+")"
        self.theconstraints["bino-higgsino mix"] = "(!("+"||".join([self.theconstraints["pure bino"],self.theconstraints["pure wino"],self.theconstraints["pure higgsino"]])+") && "+self.terms["bino"]+">"+self.terms["wino"]+" && "+self.terms["higgsino"]+">"+self.terms["wino"]+")"
        self.theconstraints["wino-higgsino mix"] = "(!("+"||".join([self.theconstraints["pure bino"],self.theconstraints["pure wino"],self.theconstraints["pure higgsino"]])+") && "+self.terms["bino"]+"<"+self.terms["wino"]+" && "+self.terms["bino"]+"<"+self.terms["higgsino"]+")"
        
        ###################################################################
        ################### Z Score Definings ###################
        self.zscore = {}
        for key in ['combined',"cms_sus_20_001","cms_sus_21_007","cms_sus_21_006"]:#, 'combined_simplified']:
            value = self.theconstraints[key]
            self.zscore[key] = "TMath::Abs(TMath::Log(%s))/(TMath::Log(%s)) * TMath::Sqrt(2 * TMath::Abs(TMath::Log(%s)))" % (value,value,value)
            
        
        ###################################################################
        ################### drawConfig Settings ###################
        
        self.drawConfig = {}
        
        self.drawConfig["impact1D"] = {
            "leftTop" : {"x1":0.23,"x2":0.66,"y1":0.67,"y2":0.9},
            "rightTop" : {"x1":0.63,"x2":0.93,"y1":0.8,"y2":0.9},
            "rightBottom" : {"x1":0.49,"x2":0.92,"y1":0.17,"y2":0.4},
            "leftBottom" : {"x1":0.23,"x2":0.53,"y1":0.2,"y2":0.32},
            "YaxisSetTitleOffset" : 1.7,
            "XaxisSetTitleOffset" : 1.05, 
            "legendFillWhite" : True,
        }