import os
from maxitex.maxitexparser import maxitexparser
from maxitex.file_initiailzer import create_footer
from maxitex.file_initiailzer import create_header

class PdfCreator():
    def __init__(self, projectdirectory,maximascript,pdfbasename):
        os.getcwd()
        self.projectdirectory=projectdirectory
        self.maximascript=maximascript
        self.pdfbasename=pdfbasename
        
    def CreatePdfFromMaximaScript(self):
        self.CreateBuildDirectory()
        os.system("rm -rf ./build/equations && cp -r equations ./build/")
        os.system("rm -rf ./build/graphs && cp -r graphs ./build/")
        os.chdir(self.BuildDirectory())
        self.CreateTexFileFromMaximaScript()
        self.GeneratePdfFromTexFile()                        
        
    def GeneratePdfFromTexFile(self):
        if (os.path.isfile(str(self.pdfbasename+".tex"))):  # Check that the .tex file has been created after parsing operations
            os.system("pdflatex "+str(self.pdfbasename+".tex"))            
        else:
            raise Exception("Error: no tex file found: "+str(self.pdfbasename+"tex"))
        if (os.path.isfile(str(self.pdfbasename+".bcf"))):  # Check that the .bcf file has been created before proceeding bilbiography
            os.system("/usr/bin/biber "+str(self.pdfbasename+".bcf"))  # Proceed bibliography via biber
        if (os.path.isfile(str(self.pdfbasename+".idx"))):  # Check that the .idx file has been created before proceeding index
            # Proceed index file (input and output are meant to be the same file) via makeindex
            os.system("/usr/bin/makeindex "+str(self.pdfbasename+".idx"))
            if (os.path.isfile(str(self.pdfbasename+".nlo"))):  # Check that the nlo file has been created before proceeding nomenclature
                os.system("/usr/bin/makeindex " + self.pdfbasename+".nlo"+" -s nomencl.ist -o " +
                        self.pdfbasename+".nls")  # Proceed nomenclature via makeindex
            os.system("/usr/bin/makeindex -s "+str(self.pdfbasename+".ist")+" -t " +
                    str(self.pdfbasename+".glg")+" -o "+str(self.pdfbasename+".gls")+" "+str(self.pdfbasename+".glo"))
            os.system("/usr/bin/makeindex -s "+str(self.pdfbasename+".ist")+" -t " +
                    str(self.pdfbasename+".alg")+" -o "+str(self.pdfbasename+".acr")+" "+str(self.pdfbasename+".acn"))
            os.system("pdflatex "+str(self.pdfbasename+".tex"))
        
    def CreateTexFileFromMaximaScript(self):
        parser=maxitexparser(self.projectdirectory,self.BuildDirectory())
        parser.GenerateTexFile(self.maximascript,self.pdfbasename+".tex")
        
    def InitializeHeaderAndFooter(self):
        create_footer(os.path.join(self.BuildDirectory(),"footer_maximatex.tex"))
        create_header(os.path.join(self.BuildDirectory(),"header_maximatex.tex"))
        pass
        
        
    def BuildDirectory(self):
        return os.path.join(self.projectdirectory,"build")
    
    def CreateBuildDirectory(self):
        os.system("mkdir -p "+self.BuildDirectory())
