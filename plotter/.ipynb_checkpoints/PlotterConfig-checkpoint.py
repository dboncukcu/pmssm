

class PlotterConfig:
    def __init__(self):
        ###################################################################
        ###################### Global Settings ######################
        self.global_settings = {}
        self.global_settings["logEps"] = 1e-5 # Minimum Treshold for log scaling
        self.global_settings["defaultOutputFileFormat"] = "pdf" # Default file format for saving
        
        ###################################################################
        ###################### CMS Label Information ######################
        self.cms_label = {}
        self.cms_label["energy"] = "13" # TeV
        self.cms_label["extraText"] = "Preliminary"
        self.cms_label["lumi"] = "137-139" # fb^-1
        
        ###################################################################
        ################### Particle Drawing Information ###################
        # - nbin [int] : Number of bins in the histogram
        # - max [int] : Maximum value for the histogram axis before scaling
        # - min [int] : Minimum value for the histogram axis before scaling
        # - logScale [bool] : Flag for logarithmic scale
        # - linearScale [float] : Linear scale factor
        # - unit [str] : Unit of measurement
        # - title [str] : Title for the histogram (with latex)
        # - name [str]: Name of the particle or parameter for saving filename
        # - 1Dlogy [bool] : Flag for logarithmic scale in 1D histograms
        
        self.particleConfig_TeV = {
            "defaults" : {
                "nbin": 100,
                "max": 1000,
                "min": 0,
                "logScale": False,
                "linearScale": 1000.0,
                "unit": "TeV",
                },
            "abs(chi10)" : {
                "title" : "m_{#tilde{#chi}^{0}_{1}}",
                "nbin" : 50,
                "min" : 0,
                "max" : 1000,
                "logScale" : False,
                "linearScale": 1000,
                "unit": "TeV",
                "name" : "chi10"
                },
            "abs(chi20)" : {
                "title" : "m_{#tilde{#chi}^{0}_{2}}",
                "nbin" : 50,
                "min" : 0,
                "max" : 2500,
                "logScale" : False,
                "linearScale": 1000,
                "unit": "TeV",
                "name" : "chi20"
            },
            "g": {
                "title" : "m_{#tilde{g}}",
                "nbin" : 100,
                "min" : 0,
                "max" : 7000,
                "logScale" : False,
                "linearScale": 1000,
                "unit": "TeV",
                "name" : "gluino"
                },
            "t1" : {
                "title": "m_{#tilde{t}_{1}}",
                "nbin" : 100,
                "min" : 0,
                "max" : 7000,
                "logScale": False,
                "linearScale": 1000.0,
                "unit": "TeV",
                "name": "stop1"
                
            },
            "t2" : {
                "title": "m_{#tilde{t}_{2}}",
                "nbin" : 100,
                "min" : 0,
                "max" : 7000,
                "logScale": False,
                "linearScale": 1000.0,
                "unit": "TeV",
                "name": "stop2"
                
            },
            "b1" : {
                "title": "m_{#tilde{b}_{1}}",
                "nbin" : 100,
                "min" : 0,
                "max" : 7000,
                "logScale": False,
                "linearScale": 1000.0,
                "unit": "TeV",
                "name": "sbottom"
            },
            "lcsp" : {
                "title" : "m_{LCSP}",
                "nbin" : 50,
                "min" : 0,
                "max" : 7000,
                "logScale" : False,
                "linearScale": 1000, # for TeV, 1GeV/1000
                "unit": "TeV",
                "name" : "lcsp"
                },
            "abs(chi1pm)-abs(chi10)": {
                "title": "#Deltam(#tilde{#chi}^{#pm}_{1},#tilde{#chi}^{0}_{1})",
                "nbin" : 100,
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
                "nbin" : 100,
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
                "nbin" : 100,
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
                "nbin" : 100,
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
                "nbin" : 100,
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
                "nbin" : 100,
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
                "nbin" : 50,
                "min" : 0,
                "max" : 2500,
                "logScale" : False,
                "linearScale": 1000,
                "unit": "TeV",
                "name" : "chi1pm"
                }
            }

    def print(self, name: str = None):
        if name is None:
            print("Global Settings:")
            for key, value in self.global_settings.items():
                print(f"{key}: {value}")
            
            print("\nCMS Label Information:")
            for key, value in self.cms_label.items():
                print(f"{key}: {value}")
            
            print("\nParticle Drawing Information:")
            for particle, config in self.particleConfig_TeV.items():
                print(f"\nParticle: {particle}")
                for key, value in config.items():
                    print(f"{key}: {value}")
        else:

            if hasattr(self,name):
                print(f"Configuration for {name}:")
                for key, value in getattr(self,name).items():
                    print(f"{key}: {value}")
            else:
                print(f"No configuration found for {name}")