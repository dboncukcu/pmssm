YELLOW = '\033[93m'
BLUE = '\033[94m'
ORANGE = '\033[38;5;214m'
GREEN = '\033[92m'
STRIKETHROUGH = '\033[9m'
BOLD = '\033[1m'
RESET = '\033[0m'
BULLET = '•'

class Constraints:
    def __init__(
        self, 
        config :dict, 
        order:list = ["llhd", "bf"],
        expressions :dict = {
            "llhd_individual": "(exp({signal}-{background}))",
            "llhd_combined" : "(exp({signal}-{background}))",
            "bf_individual": "(max({bf},1E-20))",
            "bf_combined": "(max({bf},1E-20))"
        }
        ):
        self.config = config
        self.order = order
        self.expressions = expressions
    def printConfig(self, data = None, indent=0, is_top_level=True):
        
        data = self.config if data is None else data

        for key, value in data.items():
            if isinstance(value, dict):
                if indent == 0:
                    print('-' * 7 + f' {YELLOW}{BOLD}{key}{RESET} ' + '-' * 7)
                else:
                    color = ORANGE if key in ['llhd', 'bf'] else BLUE
                    print(' ' * indent + f'{color}{BOLD}{BULLET} {key}{RESET}' + ':')
                self.printConfig(value, indent + 2, is_top_level=False)
            else:
                if key in ['signal', 'background']:
                    color = GREEN
                elif key in ['llhd', 'bf']:
                    color = ORANGE
                else:
                    color = BLUE
                value_str = str(value) if value is not None else f'{STRIKETHROUGH}None{RESET}'
                print(' ' * indent + f'{color}{BOLD}{BULLET} {key}{RESET}' + ': ' + value_str)
        
        if is_top_level:
            print('-' * 40)
    def printAnalysisList(self):
        analysisList = list(self.config.keys())
        for i,analysis in enumerate(analysisList):
            print(f"{i+1}. {analysis}")
    def getAnalysisList(self):
        return list(self.config.keys())
    def findMetric(self,analysisConfig):
        for metric in self.order:
            metric_data = analysisConfig.get(metric, {})
            if metric == "llhd":
                if metric_data.get('signal') is not None and metric_data.get('background') is not None:
                    return metric
            elif metric == "bf":
                if metric_data is not None:
                    return metric
        raise ValueError("No non-empty metric found. llhd or bf must be non-empty.")
    
    def getIndividualConstraint(self,analysisConfig, analysisType = "individual"):
        metricName = self.findMetric(analysisConfig)
        metricInfo =analysisConfig[metricName]
        if metricName == "bf":
            metricInfo = {"bf" : metricInfo}
        expType = f"{metricName}_{analysisType}"
        return self.expressions[expType].format(**metricInfo)
    
    def getConstraint(self,analysis, isSimplified = True, verbose=True):
        typeKey = "simplified" if isSimplified else "full"
        
        analysisList = analysis.split(",")
        if "combined" in analysis or len(analysisList) > 1:
            
            if len(analysisList) == 1:
                analysisList = self.getAnalysisList()
        
            analysisConstraintList = []
            ## analysis list given
            if verbose:
                print(f"_____________________________{BOLD}{GREEN}" + ("SIMPLIFIED" if isSimplified else "FULL") + f" COMBINED{RESET}_______________________")
            for analysis in analysisList:
                currentAnalysisConstraint = self.getIndividualConstraint(self.config[analysis][typeKey], "combined")
                if verbose:
                    print(f"{BULLET}{YELLOW}Analysis:{RESET} {analysis} {ORANGE}Constraint{RESET}: {currentAnalysisConstraint}")
                analysisConstraintList.append(currentAnalysisConstraint)
            return "*".join(analysisConstraintList)
        else: 
            analysisConfig = self.config[analysis][typeKey]
            individualConstraint = self.getIndividualConstraint(analysisConfig, analysisType = "individual")
            if verbose:
                print(f"_____________________________{BOLD}{GREEN}" + ("SIMPLIFIED" if isSimplified else "FULL") + f" {analysis}{RESET}_______________________")  
                print(f"{BULLET}{YELLOW}Analysis:{RESET} {analysis} {ORANGE}Constraint{RESET}: {individualConstraint}")
            return individualConstraint
        
    def getAnalysisName(self, analysis):
        analysisList = analysis.split(",")
        if "combined" in analysis or len(analysisList) > 1:
            return "COMBINED"
        else:
            return self.config[analysis]["analysisName"]
    
    def getZScore(self,analysis,isSimplified = True, verbose = True):
        
        constraint = self.getConstraint(
            analysis=analysis,
            isSimplified = isSimplified,
            verbose = verbose)
        
        return "TMath::Abs(TMath::Log(%s))/(TMath::Log(%s)) * TMath::Sqrt(2 * TMath::Abs(TMath::Log(%s)))" % (constraint,constraint,constraint)