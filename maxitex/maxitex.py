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
from maxitex.maximatexparser import MaximaTexParser
from maxitex.pdfcreator import PdfCreator
from maxitex.maxima_runner import MaximaRunnner


def usage():
    print(bcolors.LightRed + sys.argv[0] + bcolors.LightPurple + '[-h -v --errocode -i --input -n --name]' + bcolors.NC)
    print(bcolors.LightGreen + "\tWhere:")
    print(bcolors.LightPurple + "\t-i|--input"+bcolors.LightCyan+"\tinput file")
    print(bcolors.LightPurple + "\t-n|--name"+bcolors.LightCyan+"\tname of the latex")
    print(bcolors.LightPurple + "\t--view"+bcolors.LightCyan+"\tview the pdf ones it is produce")
    print(bcolors.LightGreen + "\n\n\tDescription:")
    print(bcolors.LightCyan + "\tExecute a maxima script and dress a latex document automatically out of it")

    print(bcolors.LightGreen + "\n\n\tExample of use:")
    print(bcolors.LightRed + "\t"+sys.argv[0] + bcolors.LightPurple+' --input '+bcolors.LightCyan +
          "file.mac" + bcolors.LightPurple+' --name '+bcolors.LightCyan+"calculation1")

    print(bcolors.NC)


def main():
    infile = ''
    outfile = ''
    viewoutput = False
    should_intialize_header_and_footer = False
    projectdirectory = os.getcwd()
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hvi:n:", ["errorcode", "view", "input=", "name="])
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
        elif opt in ("-i", "--input"):
            infile = os.path.join(projectdirectory, arg)
        elif opt in ("-n", "--name"):
            outfile = arg
        elif opt in ("-v", "--view"):
            viewoutput = True

    runner = MaximaRunnner(infile)
    runner.Run()
    parser = MaximaTexParser(projectdirectory, infile, outfile)
    parser.GenerateTexFile()
    pdc = PdfCreator(projectdirectory, infile, outfile)
    pdc.CreatePdfFromMaximaScript()

    if (os.path.isfile(str(outfile+".pdf")) and viewoutput):  # Check that the pdf has been created
        os.system("/usr/bin/xdg-open "+str(outfile+".pdf & bg"))  # View the result via okular
