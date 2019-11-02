import os
from maxitex.maximatexparser import MaximaTexParser


class PdfCreator():
    def __init__(self, projectdirectory, maximascript, pdfbasename):
        os.getcwd()
        self.projectdirectory = projectdirectory
        self.maximascript = maximascript
        self.pdfbasename = pdfbasename

    def _CopyFilesToBuildFolder(self):
        self.CreateBuildDirectory()
        os.system("rm -rf ./build/equations && cp -r equations ./build/")
        os.system("rm -rf ./build/graphs && cp -r graphs ./build/")
        os.system("cp "+self.pdfbasename+".tex ./build")

    def CreatePdfFromMaximaScript(self):
        self._CopyFilesToBuildFolder()
        os.chdir(self.BuildDirectory())
        self._GeneratePdfFromTexFile()
        if (os.path.isfile(self.pdfbasename+".pdf")):
            os.system("mv "+self.pdfbasename+".pdf"+" ..")

    def _GeneratePdfFromTexFile(self):
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
        return True

    def BuildDirectory(self):
        return os.path.join(self.projectdirectory, "build")

    def CreateBuildDirectory(self):
        os.system("mkdir -p "+self.BuildDirectory())
