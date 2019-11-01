import os.path
from bcolors import bcolors
import codecs
from os import listdir
from os.path import isfile, join
import re


class maxitexparser:    
    def __init__(self, directory,builddirectory):
        self.builddirectory=builddirectory
        self.headerfile = os.path.join(self.builddirectory, "header_maximatex.tex")
        self.footerfile = os.path.join(self.builddirectory, "footer_maximatex.tex")
        for f in [self.headerfile, self.footerfile]:
            if os.path.isfile(f) == False:
                print("Error: File {} not found".format(f))
                sys.exit(0)

        self.latexcontent = []
        self.latexabstract = []
        self.abstract = False
        self.nomenclature = False
        self.title = False

    def _writeheader(self, texfile):
        with open(self.headerfile) as f:  # This conserve the \n at en of lines
            content = f.readlines()
        with codecs.open(texfile, 'w', encoding='utf_8') as file:
            for i in range(0, len(content)):
                file.write(content[i])
            file.write("\n")

    def _writefooter(self, texfile):
        with open(self.footerfile) as f:  # This conserve the \n at en of lines
            content = f.readlines()
        with codecs.open(texfile, 'a', encoding='utf_8') as file:
            for i in range(0, len(content)):
                file.write(content[i])

    def _parsemaximafile(self, infile):
        with open(infile) as f:
            content = f.readlines()

        # print (bcolors.Yellow+"[DEBUG] Now parsing the file"+bcolors.NC)
        inlatex = False
        inabstract = False
        self.nomenclature = False
        self.abstract = False
        for i in range(0, len(content)):
            # print(content[i])
            if (content[i][:8] == "/*LATEX:"):
                inlatex = True
                continue
            if (content[i][:8] == ":LATEX*/"):
                inlatex = False
            if (content[i][:11] == "/*ABSTRACT:"):
                print (bcolors.Yellow+"[DEBUG] We are in abstract section"+bcolors.NC)
                self.abstract = True
                inabstract = True
                continue
            if (content[i][:11] == ":ABSTRACT*/"):
                inabstract = False

            if (content[i][:8] == "/*TITLE:"):
                self.title = True
                import re
                self.latextitle = re.sub(r'/\*TITLE:', '', content[i])
                self.latextitle = re.sub(r'\*/', '', self.latextitle)

            if (content[i][:9] == "/*AUTHOR:"):
                self.author = True
                import re
                self.latexauthor = re.sub(r'/\*AUTHOR:', '', content[i])
                self.latexauthor = re.sub(r'\*/', '', self.latexauthor)

            if (inlatex):
                # print (bcolors.Yellow+"[DEBUG] Content: "+content[i]+bcolors.NC)
                self.latexcontent.append(str(content[i]))
                # file.write(str(content[i]))
                if (content[i][:13] == "\\nomenclature"):
                    self.nomenclature = True
                    # print (bcolors.Yellow+"[DEBUG] THERE IS A NOMENCLATURE!!!!!"+bcolors.NC)
            if (inabstract):
                self.latexabstract.append(str(content[i]))

        print (bcolors.Yellow+"[DEBUG] File parsed"+bcolors.NC)

    def _writefile(self, texfile):
        with codecs.open(texfile, 'a', encoding='utf_8') as file:
            file.write(str("\\begin{document}\n"))
            if (self.author):
                file.write(str("\\author{"+self.latexauthor+"}\n"))
            if (self.title):
                file.write(str("\\title{"+self.latextitle+"}\n"))
                file.write(str("\\maketitle\n"))
            if (self.abstract == True):
                file.write(str("\\begin{abstract}\n"))
                for it in range(0, len(self.latexabstract)):
                    file.write(self.latexabstract[it])
                file.write(str("\\end{abstract}\n"))

            if (self.nomenclature):
                file.write(str("\\printnomenclature\n"))

            for it in range(0, len(self.latexcontent)):
                file.write(self.latexcontent[it])

    def __SwitchFrom_pmatrix_to_beginmatrix(self):
        #\pmatrix{a&b\cr c&d\cr }=\pmatrix{e&f\cr g&h\cr }
        #\begin{pmatrix}a&b\cr c&d\cr }=\pmatrix{e&f\cr g&h\cr }
        equationsfiles = [f for f in listdir("./equations") if isfile(join("./equations", f))]
        print(equationsfiles)
        for texfile in equationsfiles:
            print(texfile)
            with open(join("./equations", texfile)) as f:  # This conserve the \n at en of lines
                '''Strategy.
                First we relpace all occure of \pmatrix by a \begin{matrix}
                Second we parse the conten of each matrix, counting opening and lcosing { } to detectd the \end{pmatrix} and to adapt the newline symbols (cr -> \\)
                Third we replace \begin{pmatix}{ by \begin{pmatrix}
                '''
                content = f.readlines()
                allinone = ' '.join(content)
                tmp = re.sub(r'\\pmatrix', '\\\\begin{pmatrix}', allinone)
                allinone = tmp
                index = 0
                while index < len(allinone):
                    # place  ourselve at the index of next \begin{pmatrix}occurence
                    index = allinone.find("\\begin{pmatrix}", index)
                    if index == -1:
                        break
                    index += 15
                    if index > len(allinone):
                        break
                    # Now parse the subcontent of the matrix and adapt new line symbols, and count parantheses
                    openparanthesis = 0
                    while index < len(allinone):
                        if (allinone[index] == '\\' and allinone[index+1:index+3] == "cr"):
                            tmp = allinone[:index]+"\\\\"+allinone[index+3:]
                            allinone = tmp
                        if (allinone[index] == "{"):
                            openparanthesis += 1
                        if (allinone[index] == "}"):
                            openparanthesis -= 1
                            if openparanthesis == 0:
                                tmp = allinone[:index]+"\end{pmatrix}"+allinone[index+1:]
                                allinone = tmp
                                break
                        index = index+1
                allinone = re.sub(r'begin{pmatrix}{', 'begin{pmatrix}', allinone)
                with codecs.open(join("./equations", texfile), 'w', encoding='utf_8') as file:  # use a instead of w to append
                    file.write(allinone)

    def GenerateTexFile(self, maximascript, texfile):
        self._parsemaximafile(maximascript)
        self._writeheader(texfile)
        self._writefile(texfile)
        self._writefooter(texfile)
        self.__SwitchFrom_pmatrix_to_beginmatrix()
