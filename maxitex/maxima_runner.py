import os
class MaximaRunnner():
    """@class MaximaRunnner
    @brief Runn a maxima script
    """
    
    def __init__(self,inputscript):
        """Insanciante but does not run MaximaRunnner
        undefined
        """
        self.inputscript=inputscript
    def Run(self):
        if (os.path.isfile(self.inputscript) == True):
            os.system("maxima -b "+str(self.inputscript))  # Execute le script maxima
        else:
            raise FileNotFoundError("input file"+self.inputscript+"not found")
    

        
