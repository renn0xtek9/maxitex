#!/usr/bin/python3
import sys, getopt,codecs
import os.path
from os import listdir
from os.path import isfile, join
import codecs
import re
from bcolors import bcolors


def usage():
	print(bcolors.LightRed +sys.argv[0] + bcolors.LightPurple+ '[-h -v --errocode -i --input -n --name]' +bcolors.NC)
	print(bcolors.LightGreen +"\tWhere:")
	print(bcolors.LightPurple +"\t-i|--input"+bcolors.LightCyan+"\tinput file")
	print(bcolors.LightPurple +"\t-n|--name"+bcolors.LightCyan+"\tname of the latex")
	print(bcolors.LightGreen +"\n\n\tDescription:")
	print(bcolors.LightCyan +"\tExecute a maxima script and dress a latex document automatically out of it")
	
	print(bcolors.LightGreen +"\n\n\tExample of use:")
	print(bcolors.LightRed +"\t"+sys.argv[0] + bcolors.LightPurple+' --input '+bcolors.LightCyan+"file.mac"+ bcolors.LightPurple+' --name '+bcolors.LightCyan+"calculation1")
       
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



class maxitexparser:
	latexheaderfie="/home/max/Templates/Latex/header_maximatex.tex"
	latexfooterfile="/home/max/Templates/Latex/footer_maximatex.tex"
	latexcontent=['']
	latexabstract=['']
	latextitle=''
	latexauthor=''
	abstract=False
	nomenclature=False
	title=False
	author=False
	
	def __init__(self):
		#print (bcolors.Yellow+"[DEBUG] Initialize"+bcolors.NC)
		self.latexcontent=[]
		self.latexabstract=[]
		self.abstract=False
		self.nomenclature=False
		self.title=False

	def _writeheader(self,outfile):
		latexheaderfile="/home/max/Templates/Latex/header_maximatex.tex"
		if (os.path.isfile(latexheaderfile)):
			with open(latexheaderfile) as f:  #This conserve the \n at en of lines
				content = f.readlines()	
			with codecs.open(str(outfile+".tex"), 'w', encoding ='utf_8' ) as file:
				for i in range (0,len(content)) :
					file.write(content[i])
				file.write("\n")
		else :
			errcode=3
			print(bcolors.LightRed+"Exit error code "+str(3)+": template not found in "+latexheaderfile +bcolors.NC)
			sys.exit(3)
	
	def _writefooter(self,outfile):
		latexfooterfile="/home/max/Templates/Latex/footer_maximatex.tex"
		if (os.path.isfile(latexfooterfile)):
			with open(latexfooterfile) as f:  #This conserve the \n at en of lines
				content = f.readlines()	
			with codecs.open(str(outfile+".tex"), 'a', encoding ='utf_8' ) as file:
				for i in range (0,len(content)) :
					file.write(content[i])
		else :
			errcode=3
			print(bcolors.LightRed+"Exit error code "+str(3)+": template not found in "+latexfooterfile +bcolors.NC)
			sys.exit(3)
			
			

	def _parsemaximafile(self,infile):
		with open(infile) as f:
			content = f.readlines()

		#print (bcolors.Yellow+"[DEBUG] Now parsing the file"+bcolors.NC)
		inlatex=False
		inabstract=False 
		self.nomenclature=False
		self.abstract=False
		for i in range (0,len(content)) :
			#print(content[i])
			if (content[i][:8]=="/*LATEX:") : 
				inlatex=True 
				continue
			if (content[i][:8]==":LATEX*/"):
				inlatex=False
			if (content[i][:11]=="/*ABSTRACT:") :
				print (bcolors.Yellow+"[DEBUG] We are in abstract section"+bcolors.NC)
				self.abstract=True
				inabstract=True 
				continue
			if (content[i][:11]==":ABSTRACT*/"):
				inabstract=False
				
			if (content[i][:8]=="/*TITLE:"):
				self.title=True 
				import re
				self.latextitle=re.sub(r'/\*TITLE:','',content[i])
				self.latextitle=re.sub(r'\*/','',self.latextitle)
				
			if (content[i][:9]=="/*AUTHOR:"):
				self.author=True 
				import re
				self.latexauthor=re.sub(r'/\*AUTHOR:','',content[i])
				self.latexauthor=re.sub(r'\*/','',self.latexauthor)			
				
			if (inlatex):
				#print (bcolors.Yellow+"[DEBUG] Content: "+content[i]+bcolors.NC)
				self.latexcontent.append(str(content[i]))
				#file.write(str(content[i]))
				if (content[i][:13]=="\\nomenclature"):
					self.nomenclature=True;
					#print (bcolors.Yellow+"[DEBUG] THERE IS A NOMENCLATURE!!!!!"+bcolors.NC)
			if (inabstract):
				self.latexabstract.append(str(content[i]))
		
		print (bcolors.Yellow+"[DEBUG] File parsed"+bcolors.NC)

	def _writefile(self,outfile):
		with codecs.open(str(outfile+".tex"), 'a', encoding ='utf_8' ) as file:
			file.write(str("\\begin{document}\n"))
			if (self.author):
				file.write(str("\\author{"+self.latexauthor+"}\n"))
			if (self.title):
				file.write(str("\\title{"+self.latextitle+"}\n"))
				file.write(str("\\maketitle\n"))
			if (self.abstract==True):
				file.write(str("\\begin{abstract}\n"))
				for it in range(0, len(self.latexabstract)):
					file.write(self.latexabstract[it])
				file.write(str("\\end{abstract}\n"))
			
			if (self.nomenclature):
				file.write(str("\\printnomenclature\n"))
						
			for it in range(0, len(self.latexcontent)):
				file.write(self.latexcontent[it])
	def SwitchFrom_pmatrix_to_beginmatrix(self):	
		#\pmatrix{a&b\cr c&d\cr }=\pmatrix{e&f\cr g&h\cr }
		#\begin{pmatrix}a&b\cr c&d\cr }=\pmatrix{e&f\cr g&h\cr }
		equationsfiles = [f for f in listdir("./equations") if isfile(join("./equations", f))]
		print(equationsfiles)
		for texfile in equationsfiles:
			print(texfile)
			with open(join("./equations",texfile)) as f:  #This conserve the \n at en of lines
				'''Strategy.
				First we relpace all occure of \pmatrix by a \begin{matrix}
				Second we parse the conten of each matrix, counting opening and lcosing { } to detectd the \end{pmatrix} and to adapt the newline symbols (cr -> \\)
				Third we replace \begin{pmatix}{ by \begin{pmatrix}
				'''
				content = f.readlines()
				allinone=' '.join(content)
				tmp=re.sub(r'\\pmatrix', '\\\\begin{pmatrix}', allinone)	 
				allinone=tmp
				index=0 
				while index<len(allinone):
					index=allinone.find("\\begin{pmatrix}",index)   #place  ourselve at the index of next \begin{pmatrix}occurence
					if index==-1:
						break
					index+=15
					if index>len(allinone):
						break
					#Now parse the subcontent of the matrix and adapt new line symbols, and count parantheses
					openparanthesis=0
					while index<len(allinone):	
						if (allinone[index]=='\\' and allinone[index+1:index+3]=="cr"):
							tmp=allinone[:index]+"\\\\"+allinone[index+3:]
							allinone=tmp
						if (allinone[index]=="{"):
							openparanthesis+=1
						if (allinone[index]=="}"):
							openparanthesis-=1
							if openparanthesis==0:
								tmp=allinone[:index]+"\end{pmatrix}"+allinone[index+1:]
								allinone=tmp
								break
						index=index+1
				allinone=re.sub(r'begin{pmatrix}{','begin{pmatrix}',allinone)
					#sys.exit(1)
				#Old code 
				
				#for iter in re.finditer("pmatrix",allinone):
					#index=iter.start()
					#print (index)
					#tmp=allinone[:index]+"begin{pmatrix}"+allinone[index+8:]
					#allinone=tmp
					#index=index+14
					#openparanthesis=0     #this track the number of "{" that are open
					#pass
					#while index<len(allinone):						
						#if (allinone[index]=='\\' and allinone[index+1:index+3]=="cr"):
							#tmp=allinone[:index]+"\\\\"+allinone[index+3:]
							#allinone=tmp
						#if (allinone[index]=="{"):
							#openparanthesis+=1
						#if (allinone[index]=="}"):
							#openparanthesis-=1
							#if openparanthesis==-1:
								#tmp=allinone[:index]+"\end{pmatrix}"+allinone[index+1:]
								#allinone=tmp
								#break
						#if (index>=len(allinone)):
							#break
						#index=index+1
				with codecs.open(join("./equations",texfile), 'w', encoding ='utf_8' ) as file:		#use a instead of w to append
					file.write(allinone)
									
	def proceed(self,infile,outfile):
		self._parsemaximafile(infile)
		self._writeheader(outfile)
		self._writefile(outfile)
		self._writefooter(outfile)
		self.SwitchFrom_pmatrix_to_beginmatrix()

def create_pdf(outfile):
	print (bcolors.Yellow+"[DEBUG] Enters the function that create the pdf"+bcolors.NC)
	if (os.path.isfile(str(outfile+".tex"))):	#Check that the .tex file has been created after parsing operations
		os.system("pdflatex "+str(outfile+".tex"))
	else :
		errcode=4
		print(bcolors.LightRed+"Exit error code "+str(4)+": no tex file found: "+str(outfile+".tex")+bcolors.NC)
		sys.exit(4)
	if (os.path.isfile(str(outfile+".bcf"))):	#Check that the .bcf file has been created before proceeding bilbiography
		os.system("/usr/bin/biber "+str(outfile+".bcf"))	#Proceed bibliography via biber
	if (os.path.isfile(str(outfile+".idx"))):	#Check that the .idx file has been created before proceeding index
		#print (bcolors.Yellow+"[DEBUG] ON VA RUNNER UN INDEX"+bcolors.NC)
		os.system("/usr/bin/makeindex "+str(outfile+".idx"))	#Proceed index file (input and output are meant to be the same file) via makeindex
		if (os.path.isfile(str(outfile+".nlo"))): #Check that the nlo file has been created before proceeding nomenclature
			#print (bcolors.Yellow+"[DEBUG] ON VA CREER UNE NOMENCLATURE"+bcolors.NC)
			os.system("/usr/bin/makeindex " +outfile+".nlo"+" -s nomencl.ist -o "+outfile+".nls") #Proceed nomenclature via makeindex
		os.system("/usr/bin/makeindex -s "+str(outfile+".ist")+" -t "+str(outfile+".glg")+" -o "+str(outfile+".gls")+" "+str(outfile+".glo"))
		os.system("/usr/bin/makeindex -s "+str(outfile+".ist")+" -t "+str(outfile+".alg")+" -o "+str(outfile+".acr")+" "+str(outfile+".acn"))
		os.system("pdflatex "+str(outfile+".tex"))	

def launch_maxima(infile):
	if (os.path.isfile(infile)==True) :
		os.system("maxima -b "+str(infile)) #Execute le script maxima
	else:
		errcode=2
		print(bcolors.LightRed+"Exit error code "+str(2)+": input file"+infile+"not found in"+str(os.getcwd())+bcolors.NC)
		sys.exit(2)


def main(argv):
	infile = ''
	outfile = ''
	try:
		opts, args = getopt.getopt(argv,"hi:n:",["errorcode","input=","name="])
	except getopt.GetoptError:
		usage
		sys.exit(1)
	for opt, arg in opts:
		if opt == '-h':
			usage()
			sys.exit()
		if opt == '--errorcode' :
			errorlist()
			sys.exit()
		elif opt in ("-i", "--input"):
			infile = arg
		elif opt in ("-n", "--name"):
			outfile = arg
	
	launch_maxima(infile)
	
	if len(outfile)==0 :
		errcode=5
		print(bcolors.LightRed+"Exit error code "+str(5)+": No output file name specified"+bcolors.NC)
		sys.exit(5)
	
	print (bcolors.Yellow+"[DEBUG] On es la"+bcolors.NC)
	p=maxitexparser()
	print (bcolors.Yellow+"[DEBUG] On a appeller"+bcolors.NC)
	p.proceed(infile,outfile)
	create_pdf(outfile)		
	if (os.path.isfile(str(outfile+".pdf"))):	#Check that the pdf has been created
		os.system("/usr/bin/okular "+str(outfile+".pdf & bg"))	#View the result via okular 
		

if __name__ == "__main__":
        main(sys.argv[1:])
	

#*********************************************Unit tests
def test_detectauthor():
	p=maxitexparser()
	p._parsemaximafile('maxitex_test/default.mac')
	assert (p.author==True)
	
def test_detectnomenclature():
	p=maxitexparser()
	p._parsemaximafile('maxitex_test/default.mac')
	assert (p.nomenclature==True)

def test_detecttitle():
	p=maxitexparser()
	p._parsemaximafile('maxitex_test/default.mac')
	assert (p.title==True)
	
def test_detectabstract():
	p=maxitexparser()
	p._parsemaximafile('maxitex_test/default.mac')
	assert (p.abstract==True)

def test_falsepositive_title():
	p=maxitexparser()
	p._parsemaximafile('maxitex_test/notitle.mac')
	assert (p.title==False)
	
def test_falsepositive_author():
	p=maxitexparser()
	p._parsemaximafile('maxitex_test/noauthor.mac')
	assert (p.author==False)
	
def test_falsepositive_abstract():
	p=maxitexparser()
	p._parsemaximafile('maxitex_test/noabstract.mac')
	assert (p.abstract==False)
	
def test_proceed_default_create_tex():
	import os
	if (os.path.isfile("maxitex_test/default.tex")):
		os.remove("maxitex_test/default.tex")
	p=maxitexparser()
	p.proceed("maxitex_test/default.mac","maxitex_test/default")
	import os.path
	assert (os.path.isfile("maxitex_test/default.tex")==True)

def test_proceed_default_create_pdf():
	launch_maxima("maxitex_test/default.tex")
	import os
	if (os.path.isfile("maxitex_test/default.tex")):
		os.remove("maxitex_test/default.tex")
	p=maxitexparser()
	p.proceed("maxitex_test/default.mac","maxitex_test/default")
	create_pdf("maxitex_test/default")
	import os.path
	assert (os.path.isfile("maxitex_test/default.pdf")==True)
		

	
