#!/usr/bin/python3
import maxitex
import sys
import getopt
import codecs
import os.path
from os import listdir
from os.path import isfile, join
from pathlib import Path
import codecs
import re
from bcolors import bcolors
from maxitex import file_initiailzer
from maxitex.file_initiailzer import create_footer
from maxitex.file_initiailzer import create_header
from maxitex.maxitexparser import maxitexparser


def usage():
    print(bcolors.LightRed + sys.argv[0] + bcolors.LightPurple + '[-h -v --errocode -i --input -n --name]' + bcolors.NC)
    print(bcolors.LightGreen + "\tWhere:")
    print(bcolors.LightPurple + "\t-i|--input"+bcolors.LightCyan+"\tinput file")
    print(bcolors.LightPurple + "\t-n|--name"+bcolors.LightCyan+"\tname of the latex")
    print(bcolors.LightPurple + "\t--init"+bcolors.LightCyan+"\tcreate heder and footer file")
    print(bcolors.LightPurple + "\t--view"+bcolors.LightCyan+"\tview the pdf ones it is produce")
    print(bcolors.LightGreen + "\n\n\tDescription:")
    print(bcolors.LightCyan + "\tExecute a maxima script and dress a latex document automatically out of it")

    print(bcolors.LightGreen + "\n\n\tExample of use:")
    print(bcolors.LightRed + "\t"+sys.argv[0] + bcolors.LightPurple+' --input '+bcolors.LightCyan +
          "file.mac" + bcolors.LightPurple+' --name '+bcolors.LightCyan+"calculation1")

    print(bcolors.NC)


def errorlist():
    print(bcolors.Red+"--------------------------------------------------------")
    print("EXIT CODE       |MEANING")
    print("--------------------------------------------------------")
    print("0               |Success")
    print("1               |Error when parsing argument")
    print("2               |Maxima file not found")
    print("3               |No template found for header")
    print("4               |The .tex file has somehow not being produced/found and can not be processed")
    print("5               |No output file name specified (see -n argument)")
    print("255             |Exit returning information (help, version, list of error codes etc)"+bcolors.NC)


def create_pdf(path, outfile):
    if (os.path.isfile(str(outfile+".tex"))):  # Check that the .tex file has been created after parsing operations
        os.system("pdflatex "+str(outfile+".tex"))
    else:
        errcode = 4
        print(bcolors.LightRed+"Exit error code "+str(4)+": no tex file found: "+str(outfile+".tex")+bcolors.NC)
        sys.exit(4)
    if (os.path.isfile(str(outfile+".bcf"))):  # Check that the .bcf file has been created before proceeding bilbiography
        os.system("/usr/bin/biber "+str(outfile+".bcf"))  # Proceed bibliography via biber
    if (os.path.isfile(str(outfile+".idx"))):  # Check that the .idx file has been created before proceeding index
        # Proceed index file (input and output are meant to be the same file) via makeindex
        os.system("/usr/bin/makeindex "+str(outfile+".idx"))
        if (os.path.isfile(str(outfile+".nlo"))):  # Check that the nlo file has been created before proceeding nomenclature
            os.system("/usr/bin/makeindex " + outfile+".nlo"+" -s nomencl.ist -o " +
                      outfile+".nls")  # Proceed nomenclature via makeindex
        os.system("/usr/bin/makeindex -s "+str(outfile+".ist")+" -t " +
                  str(outfile+".glg")+" -o "+str(outfile+".gls")+" "+str(outfile+".glo"))
        os.system("/usr/bin/makeindex -s "+str(outfile+".ist")+" -t " +
                  str(outfile+".alg")+" -o "+str(outfile+".acr")+" "+str(outfile+".acn"))
        os.system("pdflatex "+str(outfile+".tex"))


def launch_maxima(infile):
    if (os.path.isfile(infile) == True):
        os.system("maxima -b "+str(infile))  # Execute le script maxima
    else:
        errcode = 2
        print(bcolors.LightRed+"Exit error code "+str(2)+": input file" +
              infile+"not found in"+str(os.getcwd())+bcolors.NC)
        sys.exit(2)


def intialize_files(path):
    create_footer(os.path.join(path, "footer_maximatex.tex"))
    create_header(os.path.join("header_maximatex.tex"))


def main():
    infile = ''
    outfile = ''
    viewoutput = False
    should_intialize_header_and_footer = False
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hvi:n:", ["errorcode","view","init", "input=", "name="])
    except getopt.GetoptError:
        usage
        sys.exit(1)
    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        if opt == '--errorcode':
            errorlist()
            sys.exit()
        elif opt == "--init":
            should_intialize_header_and_footer = True
        elif opt in ("-i", "--input"):
            infile = arg
        elif opt in ("-n", "--name"):
            outfile = arg
        elif opt in ("-v", "--view"):
            viewoutput = True

    if len(outfile) == 0:
        print(bcolors.LightRed+"Exit error code "+str(5)+": No output file name specified"+bcolors.NC)
        sys.exit(5)

    if (not os.path.isfile(infile)):
        print(bcolors.LightRed+"WANRING file {} not found".format(infile))
        sys.exit(2)

    projectdirectory = Path(infile).parent
    if should_intialize_header_and_footer:
        print("will initialize")
        intialize_files(projectdirectory)

    launch_maxima(infile)

    p = maxitexparser(projectdirectory)
    p.proceed(infile, outfile)
    create_pdf(projectdirectory, outfile)
    if (os.path.isfile(str(outfile+".pdf")) and viewoutput):  # Check that the pdf has been created
        os.system("/usr/bin/xdg-open "+str(outfile+".pdf & bg"))  # View the result via okular


# TODO move this to a unittest
#*********************************************Unit tests
def test_detectauthor():
    p = maxitexparser()
    p._parsemaximafile('maxitex_test/default.mac')
    assert (p.author == True)


def test_detectnomenclature():
    p = maxitexparser()
    p._parsemaximafile('maxitex_test/default.mac')
    assert (p.nomenclature == True)


def test_detecttitle():
    p = maxitexparser()
    p._parsemaximafile('maxitex_test/default.mac')
    assert (p.title == True)


def test_detectabstract():
    p = maxitexparser()
    p._parsemaximafile('maxitex_test/default.mac')
    assert (p.abstract == True)


def test_falsepositive_title():
    p = maxitexparser()
    p._parsemaximafile('maxitex_test/notitle.mac')
    assert (p.title == False)


def test_falsepositive_author():
    p = maxitexparser()
    p._parsemaximafile('maxitex_test/noauthor.mac')
    assert (p.author == False)


def test_falsepositive_abstract():
    p = maxitexparser()
    p._parsemaximafile('maxitex_test/noabstract.mac')
    assert (p.abstract == False)


def test_proceed_default_create_tex():
    import os
    if (os.path.isfile("maxitex_test/default.tex")):
        os.remove("maxitex_test/default.tex")
    p = maxitexparser()
    p.proceed("maxitex_test/default.mac", "maxitex_test/default")
    import os.path
    assert (os.path.isfile("maxitex_test/default.tex") == True)


def test_proceed_default_create_pdf():
    launch_maxima("maxitex_test/default.tex")
    import os
    if (os.path.isfile("maxitex_test/default.tex")):
        os.remove("maxitex_test/default.tex")
    p = maxitexparser()
    p.proceed("maxitex_test/default.mac", "maxitex_test/default")
    create_pdf("maxitex_test/default")
    import os.path
    assert (os.path.isfile("maxitex_test/default.pdf") == True)
