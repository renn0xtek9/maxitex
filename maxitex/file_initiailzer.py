def create_header(path):
    content=[
    '\documentclass[a4paper,10pt]{article}',
    '\\usepackage[utf8]{inputenc}',
    '% \\usepackage[T1]{fontenc}',
    '\\usepackage{charter}',
    '\\usepackage[english]{babel}',
    '\\usepackage{amsmath}',
    '\\usepackage{amsfonts}',
    '\\usepackage{graphicx}',
    '\\usepackage{caption}',
    '\\usepackage{float}',
    '\\usepackage{hyperref}',
    '\\usepackage{setspace} %interlignes?',
    '\\usepackage[top=2cm,bottom=2cm,left=3cm,right=2cm]{geometry}',
    '\\usepackage[usenames,dvipsnames]{xcolor}',
    '\\usepackage{setspace}',
    '\\usepackage{fixltx2e}	% to get subscript',
    '\\usepackage[style=numeric,backend=biber]{biblatex}',
    '\\usepackage[acronym]{glossaries}',
    '\\usepackage{makeidx}',
    '\\usepackage{nomencl}	%Nomenclature des variables. doit etre utilise avec \makenomenclature',
    '\\usepackage{textcomp}',
    '\\usepackage{sfmath}',
    '\\usepackage{booktabs}	%to get bottomrule top rule and middlerun in tabular',
    '\\usepackage{algorithm}',
    '\\usepackage{algorithmic}',
    '\\usepackage{rotating}',
    '',
    '\\addbibresource{/home/max/Library/library.bib} %define so to work with mendeley',
    '\setlength{\parindent}{0pt}		% Avoid indentation on the first line',
    '\makeindex',
    '\makenomenclature',
    '\makeglossaries',
    '% \\begin{document}',
    '% \printnomenclature']
    with codecs.open(path, 'w', encoding ='utf_8' ) as file:		#use a instead of w to append a+ to append/create w+ for write/create
        file.write('\n'.join(content))
    
def create_footer(path):
    with codecs.open(path, 'w', encoding ='utf_8' ) as file:		#use a instead of w to append a+ to append/create w+ for write/create
        file.write("\end{document}")
    
    
    
