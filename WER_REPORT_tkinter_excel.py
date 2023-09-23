from tkinter import Tk 
from tkinter import *
import tkinter as tk    # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
import numpy
import re
import pandas as pd
import sys
import jiwer 
from jiwer import cer
import re
import pandas as pd
import os

############################################ REPLACEMENT PROGRAM ################################################

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

def is_number(x):
    if type(x) == str:
        x = x.replace(',', '')
    try:     
      if float(x):
          return False
      else: 
        return True
    except:
      return False

def text2int (textnum, numwords={}):
    units = [
        'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight',
        'nine', 'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen',
        'sixteen', 'seventeen', 'eighteen', 'nineteen',
    ]
    tens = ['', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety']
    scales = ['hundred', 'thousand', 'million', 'billion', 'trillion']
    ordinal_words = {'first':1, 'second':2, 'third':3, 'fifth':5, 'eighth':8, 'ninth':9, 'twelfth':12}
    ordinal_endings = [('ieth', 'y')]

    if not numwords:
        numwords['and'] = (1, 0)
        for idx, word in enumerate(units): numwords[word] = (1, idx)
        for idx, word in enumerate(tens): numwords[word] = (1, idx * 10)
        for idx, word in enumerate(scales): numwords[word] = (10 ** (idx * 3 or 2), 0)

    #textnum = textnum.replace('-', ' ')

    current = result = 0
    curstring = ''
    onnumber = False
    lastunit = False
    lastscale = False

    def is_numword(x):
        if is_number(x):
            return True
        if word in numwords:
            return True
        return False

    def from_numword(x):
        if is_number(x):
            scale = 0
            increment = int(x.replace(',', ''))
            return scale, increment
        return numwords[x]

    for word in textnum.split():
        worder = re.findall(r"[A-Za-z-0-9.,!/'%*:;\(\)\{\}]+|\S", word)
        symbol = worder[1:]
        word = worder[0]
        final  =[]
        if word in ordinal_words:
            scale, increment = (1, ordinal_words[word])
            current = current * scale + increment
            if scale > 100:
                result += current
                current = 0
            onnumber = True
            lastunit = False
            lastscale = False
        else:
            for ending, replacement in ordinal_endings:
                if word.endswith(ending):
                    word = "%s%s" % (word[:-len(ending)], replacement)

            if (not is_numword(word)) or (word == 'and' and not lastscale) or (isfloat(word)):
                if onnumber:
                    curstring += repr(result + current) + " "
                curstring += word + " "
                result = current = 0
                onnumber = False
                lastunit = False
                lastscale = False
            else:
                scale, increment = from_numword(word)
                onnumber = True

                if lastunit and (word not in scales):                                                                                                                                                                                                              
                    curstring += repr(result + current)                                                                                                                                                                                                                                       
                    result = current = 0                                                                                                                                                                                                                                                      

                if scale > 1:                                                                                                                                                                                                                                                                 
                    current = max(1, current)                                                                                                                                                                                                                                                 

                current = current * scale + increment                                                                                                                                                                                                                                         
                if scale > 100:                                                                                                                                                                                                                                                               
                    result += current                                                                                                                                                                                                                                                         
                    current = 0                                                                                                                                                                                                                                                               

                lastscale = False                                                                                                                                                                                                              
                lastunit = False                                                                                                                                                
                if word in scales:                                                                                                                                                                                                             
                    lastscale = True                                                                                                                                                                                                         
                elif word in units:                                                                                                                                                                                                             
                    lastunit = True
        final.append(str(curstring))
        final = final+symbol
        word = ''.join(final)
        

    if onnumber:
        curstring += repr(result + current)

    return curstring


def replace_function(sentence):
    pred = sentence

    pred = pred.replace("<", " < ")
    pred = pred.replace(">", " > ")
    
    pred = pred.replace("\"", " \" ")
    
    pred = pred.replace("#","number ")

    df2 = pd.read_excel(r"D:\\units.xlsx")

    #for i in range(len(df2["Short Form"])):
    #    df2["Short Form"][i] = " "+str(df2["Short Form"][i])+" "
    #    df2["Abbreviation"][i] = " "+str(df2["Abbreviation"][i])+" "

    for i in range(len(df2["Short Form"])):
        pred = re.sub(str(df2["Abbreviation"][i]), str(df2["Short Form"][i]), pred)

    df = pd.read_excel(r"D:\\UK_US.xlsx")
    df = df.drop("Unnamed: 0", axis=1)
    for i in range(len(df["US"])):
        df["US"][i] = " "+str(df["US"][i])+" "
        df["UK"][i] = " "+str(df["UK"][i])+" "


    for i in range(len(df['US'])):
        pred = pred.replace(df["US"][i], df["UK"][i])

    pred = text2int(pred)

    pred = re.sub("(\d+)to(\d+)", r"\1-\2", pred)
    pred = re.sub("(\d+) to (\d+)", r"\1-\2", pred) 
    pred = re.sub("(\d+)into(\d+)", r"\1 x \2", pred)
    pred = re.sub("(\d+) into (\d+)", r"\1 x \2", pred)
    pred = re.sub("(\d+)times(\d+)", r"\1 x \2", pred)
    pred = re.sub("(\d+) times (\d+)", r"\1 x \2", pred)
    pred = re.sub("(\d+) by (\d+)", r"\1/\2", pred)
    pred = re.sub("(\d+)by(\d+)", r"\1/\2", pred)
    pred = re.sub("(\d+) slash (\d+)", r"\1/\2", pred)
    pred = re.sub("(\d+)slash(\d+)", r"\1/\2", pred)
    
    #spoken punctuation 
    pred = pred.replace("fullstop",".")
    pred = pred.replace("full stop",".")
    pred = pred.replace("Full Stop",".")
    pred = pred.replace("Full stop",".")
    pred = pred.replace("Fullstop",".")
    pred = pred.replace("..", ".")

    pred = pred.replace("comma",",")
    pred = pred.replace(" semicolon",";")
    pred = pred.replace(" semi colon",";")
    pred = pred.replace(" hyphen ","-")
    pred = pred.replace(" en dash","–")
    pred = pred.replace(" endash","–")
    pred = pred.replace(" em dash","—")
    pred = pred.replace(" Apostrophe","'")
    pred = pred.replace(" open double quote","“")
    pred = pred.replace(" open double quotes","“")
    pred = pred.replace(" close double quote","”")
    pred = pred.replace(" close double quotes","”")
    pred = pred.replace(" double quotes"," \" ")
    pred = pred.replace(" double quote"," \" ")
    pred = pred.replace("double quotes"," \" ")
    pred = pred.replace("double quote"," \" ")
    pred = pred.replace(" exclamation point","!")
    pred = pred.replace(" exclamation","!")
    pred = pred.replace(" exclamation mark","!")
    pred = pred.replace(" ellipses","...")
    pred = pred.replace(" per ","/")
    pred = pred.replace("yrs","years")
    pred = pred.replace(" versus ","vs")
    pred = pred.replace("versus","vs")
    # Added temporarily
    pred = pred.replace("colon",":")

    #braces
    normalopenparenthesis = re.compile(re.escape("open parenthesis"), re.IGNORECASE)
    pred = normalopenparenthesis.sub("(", pred)
    normalcloseparenthesis = re.compile(re.escape("close parenthesis"), re.IGNORECASE)
    pred = normalcloseparenthesis.sub(")", pred)
    normalclosedparenthesis = re.compile(re.escape("closed parenthesis"), re.IGNORECASE)
    pred = normalclosedparenthesis.sub(")", pred)
    normalparenthesisopen = re.compile(re.escape("parenthesis open"), re.IGNORECASE)
    pred = normalparenthesisopen.sub("(", pred)
    normalparenthesisclosed = re.compile(re.escape("parenthesis closed"), re.IGNORECASE)
    pred = normalparenthesisclosed.sub(")", pred)
    normalparenthesisclose = re.compile(re.escape("parenthesis close"), re.IGNORECASE)
    pred = normalparenthesisclose.sub(")", pred)


    normalbracketopen = re.compile(re.escape("bracket open"), re.IGNORECASE)
    pred  = normalbracketopen.sub("(", pred)
    normalbracketsopen = re.compile(re.escape("brackets open"), re.IGNORECASE)
    pred = normalbracketsopen.sub("(", pred)
    normalbracketclosed = re.compile(re.escape("bracket closed"), re.IGNORECASE)
    pred  = normalbracketclosed.sub(")", pred)
    normalbracketsclosed = re.compile(re.escape("brackets closed"), re.IGNORECASE)
    pred = normalbracketsclosed.sub(")", pred)
    normalbracketclose = re.compile(re.escape("bracket close"), re.IGNORECASE)
    pred  = normalbracketclose.sub(")", pred)
    normalbracketsclose = re.compile(re.escape("brackets close"), re.IGNORECASE)
    pred = normalbracketsclose.sub(")", pred)
    normalbracesopen = re.compile(re.escape("braces open"), re.IGNORECASE)
    pred = normalbracesopen.sub("(", pred)
    normalbracesclosed = re.compile(re.escape("braces closed"), re.IGNORECASE)
    pred = normalbracesclosed.sub(")", pred)
    normalbracesclose = re.compile(re.escape("braces close"), re.IGNORECASE)
    pred = normalbracesclose.sub(")", pred)

    normalopenbracket = re.compile(re.escape("open bracket"), re.IGNORECASE)
    pred  = normalopenbracket.sub("(", pred)
    normalopenbrackets = re.compile(re.escape("open brackets"), re.IGNORECASE)
    pred = normalopenbrackets.sub("(", pred)
    normalclosebracket = re.compile(re.escape("close bracket"), re.IGNORECASE)
    pred  = normalclosebracket.sub(")", pred)
    normalclosebrackets = re.compile(re.escape("close brackets"), re.IGNORECASE)
    pred = normalclosebrackets.sub(")", pred)
    normalclosedbracket = re.compile(re.escape("closed bracket"), re.IGNORECASE)
    pred  = normalclosedbracket.sub(")", pred)
    normalclosedbrackets = re.compile(re.escape("closed brackets"), re.IGNORECASE)
    pred = normalclosedbrackets.sub(")", pred)
    normalopenbraces = re.compile(re.escape("open braces"), re.IGNORECASE)
    pred = normalopenbraces.sub("(", pred)
    normalclosebraces = re.compile(re.escape("close braces"), re.IGNORECASE)
    pred = normalclosebraces.sub(")", pred)
    normalclosedbraces = re.compile(re.escape("closed braces"), re.IGNORECASE)
    pred = normalclosedbraces.sub(")", pred)

    pred = pred.replace("( ","(")
    pred = pred.replace(" )",")")

    squareopenparenthesis = re.compile(re.escape("open square parenthesis"), re.IGNORECASE)
    pred = squareopenparenthesis.sub("[", pred)
    squarecloseparenthesis = re.compile(re.escape("close square parenthesis"), re.IGNORECASE)
    pred = squarecloseparenthesis.sub("]", pred)
    squareclosedparenthesis = re.compile(re.escape("closed square parenthesis"), re.IGNORECASE)
    pred = squareclosedparenthesis.sub("]", pred)
    squareparenthesisopen = re.compile(re.escape("square parenthesis open"), re.IGNORECASE)
    pred = squareparenthesisopen.sub("[", pred)
    squareparenthesisclosed = re.compile(re.escape("square parenthesis closed"), re.IGNORECASE)
    pred = squareparenthesisclosed.sub("]", pred)
    squareparenthesisclose = re.compile(re.escape("square parenthesis close"), re.IGNORECASE)
    pred = squareparenthesisclose.sub("]", pred)

    squarebracketopen = re.compile(re.escape("square bracket open"), re.IGNORECASE)
    pred  = squarebracketopen.sub("[", pred)
    squarebracketsopen = re.compile(re.escape("square brackets open"), re.IGNORECASE)
    pred = squarebracketsopen.sub("[", pred)
    squarebracketclosed = re.compile(re.escape("square bracket closed"), re.IGNORECASE)
    pred  = squarebracketclosed.sub("]", pred)
    squarebracketsclosed = re.compile(re.escape("square brackets closed"), re.IGNORECASE)
    pred = squarebracketsclosed.sub("]", pred)
    squarebracketclose = re.compile(re.escape("square bracket close"), re.IGNORECASE)
    pred  = squarebracketclose.sub("]", pred)
    squarebracketsclose = re.compile(re.escape("square brackets close"), re.IGNORECASE)
    pred = squarebracketsclose.sub("]", pred)
    squarebracesopen = re.compile(re.escape("square braces open"), re.IGNORECASE)
    pred = squarebracesopen.sub("[", pred)
    squarebracesclosed = re.compile(re.escape("square braces closed"), re.IGNORECASE)
    pred = squarebracesclosed.sub("]", pred)
    squarebracesclose = re.compile(re.escape("square braces close"), re.IGNORECASE)
    pred = squarebracesclose.sub("]", pred)

    squareopenbracket = re.compile(re.escape("open square bracket"), re.IGNORECASE)
    pred  = squareopenbracket.sub("[", pred)
    squareopenbrackets = re.compile(re.escape("open square brackets"), re.IGNORECASE)
    pred = squareopenbrackets.sub("[", pred)
    squareclosebracket = re.compile(re.escape("close square bracket"), re.IGNORECASE)
    pred  = squareclosebracket.sub("]", pred)
    squareclosebrackets = re.compile(re.escape("close square brackets"), re.IGNORECASE)
    pred = squareclosebrackets.sub("]", pred)
    squareclosedbracket = re.compile(re.escape("closed square bracket"), re.IGNORECASE)
    pred  = squareclosedbracket.sub("]", pred)
    squareclosedbrackets = re.compile(re.escape("closed square brackets"), re.IGNORECASE)
    pred = squareclosedbrackets.sub("]", pred)
    squareopenbraces = re.compile(re.escape("open square braces"), re.IGNORECASE)
    pred = squareopenbraces.sub("[", pred)
    squareclosebraces = re.compile(re.escape("close square braces"), re.IGNORECASE)
    pred = squareclosebraces.sub("]", pred)
    squareclosedbraces = re.compile(re.escape("closed square braces"), re.IGNORECASE)
    pred = squareclosedbraces.sub("]", pred)


    pred = pred.replace("[ ","[")
    pred = pred.replace(" ]","]")

    curlyopenparenthesis = re.compile(re.escape("open curly parenthesis"), re.IGNORECASE)
    pred = curlyopenparenthesis.sub("{", pred)
    curlycloseparenthesis = re.compile(re.escape("close curly parenthesis"), re.IGNORECASE)
    pred = curlycloseparenthesis.sub("}", pred)
    curlyclosedparenthesis = re.compile(re.escape("closed curly parenthesis"), re.IGNORECASE)
    pred = curlyclosedparenthesis.sub("}", pred)
    curlyparenthesisopen = re.compile(re.escape("curly parenthesis open"), re.IGNORECASE)
    pred = curlyparenthesisopen.sub("{", pred)
    curlyparenthesisclosed = re.compile(re.escape("curly parenthesis closed"), re.IGNORECASE)
    pred = curlyparenthesisclosed.sub("}", pred)
    curlyparenthesisclose = re.compile(re.escape("curly parenthesis close"), re.IGNORECASE)
    pred = curlyparenthesisclose.sub("}", pred)


    curlybracketopen = re.compile(re.escape("curly bracket open"), re.IGNORECASE)
    pred  = curlybracketopen.sub("{", pred)
    curlybracketsopen = re.compile(re.escape("curly brackets open"), re.IGNORECASE)
    pred = curlybracketsopen.sub("{", pred)
    curlybracketclosed = re.compile(re.escape("curly bracket closed"), re.IGNORECASE)
    pred  = curlybracketclosed.sub("}", pred)
    curlybracketsclosed = re.compile(re.escape("curly brackets closed"), re.IGNORECASE)
    pred = curlybracketsclosed.sub("}", pred)
    curlybracketclose = re.compile(re.escape("curly bracket close"), re.IGNORECASE)
    pred  = curlybracketclose.sub("}", pred)
    curlybracketsclose = re.compile(re.escape("curly brackets close"), re.IGNORECASE)
    pred = curlybracketsclose.sub("}", pred)
    curlybracesopen = re.compile(re.escape("curly braces open"), re.IGNORECASE)
    pred = curlybracesopen.sub("{", pred)
    curlybracesclosed = re.compile(re.escape("curly braces closed"), re.IGNORECASE)
    pred = curlybracesclosed.sub("}", pred)
    curlybracesclose = re.compile(re.escape("curly braces close"), re.IGNORECASE)
    pred = curlybracesclose.sub("}", pred)

    curlyopenbracket = re.compile(re.escape("open curly bracket"), re.IGNORECASE)
    pred  = curlyopenbracket.sub("{", pred)
    curlyopenbrackets = re.compile(re.escape("open curly brackets"), re.IGNORECASE)
    pred = curlyopenbrackets.sub("{", pred)
    curlyclosebracket = re.compile(re.escape("close curly bracket"), re.IGNORECASE)
    pred  = curlyclosebracket.sub("}", pred)
    curlyclosebrackets = re.compile(re.escape("close curly brackets"), re.IGNORECASE)
    pred = curlyclosebrackets.sub("}", pred)
    curlyclosedbracket = re.compile(re.escape("closed curly bracket"), re.IGNORECASE)
    pred  = curlyclosedbracket.sub("}", pred)
    curlyclosedbrackets = re.compile(re.escape("closed curly brackets"), re.IGNORECASE)
    pred = curlyclosedbrackets.sub("}", pred)
    curlyopenbraces = re.compile(re.escape("open curly braces"), re.IGNORECASE)
    pred = curlyopenbraces.sub("{", pred)
    curlyclosebraces = re.compile(re.escape("close curly braces"), re.IGNORECASE)
    pred = curlyclosebraces.sub("}", pred)
    curlyclosedbraces = re.compile(re.escape("closed curly braces"), re.IGNORECASE)
    pred = curlyclosedbraces.sub("}", pred)
   
    pred = pred.replace("{ ","{")
    pred = pred.replace(" }","}")

    angleopenparenthesis = re.compile(re.escape("open angle parenthesis"), re.IGNORECASE)
    pred = angleopenparenthesis.sub("<", pred)
    anglecloseparenthesis = re.compile(re.escape("close angle parenthesis"), re.IGNORECASE)
    pred = anglecloseparenthesis.sub(">", pred)
    angleclosedparenthesis = re.compile(re.escape("closed angle parenthesis"), re.IGNORECASE)
    pred = angleclosedparenthesis.sub(">", pred)
    angleparenthesisopen = re.compile(re.escape("angle parenthesis open"), re.IGNORECASE)
    pred = angleparenthesisopen.sub("<", pred)
    angleparenthesisclosed = re.compile(re.escape("angle parenthesis closed"), re.IGNORECASE)
    pred = angleparenthesisclosed.sub(">", pred)
    angleparenthesisclose = re.compile(re.escape("angle parenthesis close"), re.IGNORECASE)
    pred = angleparenthesisclose.sub(">", pred)

    anglebracketopen = re.compile(re.escape("angle bracket open"), re.IGNORECASE)
    pred  = anglebracketopen.sub("<", pred)
    anglebracketsopen = re.compile(re.escape("angle brackets open"), re.IGNORECASE)
    pred = anglebracketsopen.sub("<", pred)
    anglebracketclosed = re.compile(re.escape("angle bracket closed"), re.IGNORECASE)
    pred  = anglebracketclosed.sub(">", pred)
    anglebracketsclosed = re.compile(re.escape("angle brackets closed"), re.IGNORECASE)
    pred = anglebracketsclosed.sub(">", pred)
    anglebracketclose = re.compile(re.escape("angle bracket close"), re.IGNORECASE)
    pred  = anglebracketclose.sub(">", pred)
    anglebracketsclose = re.compile(re.escape("angle brackets close"), re.IGNORECASE)
    pred = anglebracketsclose.sub(">", pred)
    anglebracesopen = re.compile(re.escape("angle braces open"), re.IGNORECASE)
    pred = anglebracesopen.sub("<", pred)
    anglebracesclosed = re.compile(re.escape("angle braces closed"), re.IGNORECASE)
    pred = anglebracesclosed.sub(">", pred)
    anglebracesclose = re.compile(re.escape("angle braces close"), re.IGNORECASE)
    pred = anglebracesclose.sub(">", pred)

    angleopenbracket = re.compile(re.escape("open angle bracket"), re.IGNORECASE)
    pred  = angleopenbracket.sub("<", pred)
    angleopenbrackets = re.compile(re.escape("open angle brackets"), re.IGNORECASE)
    pred = angleopenbrackets.sub("<", pred)
    angleclosebracket = re.compile(re.escape("close angle bracket"), re.IGNORECASE)
    pred  = angleclosebracket.sub(">", pred)
    angleclosebrackets = re.compile(re.escape("close angle brackets"), re.IGNORECASE)
    pred = angleclosebrackets.sub(">", pred)
    angleclosedbracket = re.compile(re.escape("closed angle bracket"), re.IGNORECASE)
    pred  = angleclosedbracket.sub(">", pred)
    angleclosedbrackets = re.compile(re.escape("closed angle brackets"), re.IGNORECASE)
    pred = angleclosedbrackets.sub(">", pred)
    angleopenbraces = re.compile(re.escape("open angle braces"), re.IGNORECASE)
    pred = angleopenbraces.sub("<", pred)
    angleclosebraces = re.compile(re.escape("close angle braces"), re.IGNORECASE)
    pred = angleclosebraces.sub(">", pred)     
    angleclosedbraces = re.compile(re.escape("closed angle braces"), re.IGNORECASE)
    pred = angleclosedbraces.sub(">", pred) 

    

    #symbols
    pred = pred.replace("alpha","α")
    pred = pred.replace("Alpha","α")
    pred = pred.replace("beta", "β")
    pred = pred.replace("Beta", "β")
    pred = pred.replace("gamma", "γ")
    pred = pred.replace("Gamma", "γ")
    pred = pred.replace("lambda", "λ")
    pred = pred.replace("Lambda", "λ")
    pred = pred.replace(" underscore","_")
    pred = pred.replace("asterisk","*")
    pred = pred.replace("ampersand","&")
    pred = pred.replace("backslash","\\")
    pred = pred.replace(" tilde","~")
    pred = pred.replace(" At symbol","@")
    pred = pred.replace(" pound symbol","#")
    pred = pred.replace(" slash symbol","/")
    pred = pred.replace(" caret symbol","^")
    pred = pred.replace(" pipe symbol","|")
    pred = pred.replace("percentage","%")
    pred = pred.replace("plus","+")
    pred = pred.replace("plus or minus","±")
    pred = pred.replace(" less than equal to ","≤")
    pred = pred.replace("greater than equal to ","≥")
    pred = pred.replace("less than or equal to ","≤")
    pred = pred.replace("greater than or equal to ","≥")
    pred = pred.replace("is equal to", "=")
    pred = pred.replace("equal to", "=")
    pred = pred.replace("equal", "=")
    pred = pred.replace("equals", "=")
    pred = pred.replace("less than ","<")
    pred = pred.replace("greater than ", ">")



    #others
    pred = pred.replace(" newline ", "\n")
    pred = pred.replace(" nextline ", "\n")
    pred = pred.replace(" next line ", "\n")
    pred = pred.replace(" new line ", "\n")
    pred = pred.replace(" next paragraph ", "\n\n")
    pred = pred.replace(" new paragraph ", "\n\n")

    pred = pred.replace(" .", ".")
    pred = pred.replace("..",".")

    return pred


#################################################################################################################
############################################# WER REPORT GENERATOR ###############################################


list_ref = []
list_pred = []
vars = []
check_box_list = []
flag = 0
r_count = 0
sum = 0

def editDistance(r, h):
    '''
    This function is to calculate the edit distance of reference sentence and the hypothesis sentence.
    Main algorithm used is dynamic programming.
    Attributes: 
        r -> the list of words produced by splitting reference sentence.
        h -> the list of words produced by splitting hypothesis sentence.
    '''
    d = numpy.zeros((len(r)+1)*(len(h)+1), dtype=numpy.uint8).reshape((len(r)+1, len(h)+1))
    for i in range(len(r)+1):
        d[i][0] = i
    for j in range(len(h)+1):
        d[0][j] = j
    for i in range(1, len(r)+1):
        for j in range(1, len(h)+1):
            if r[i-1] == h[j-1]:
                d[i][j] = d[i-1][j-1]
            else:
                substitute = d[i-1][j-1] + 1
                insert = d[i][j-1] + 1
                delete = d[i-1][j] + 1
                d[i][j] = min(substitute, insert, delete)
    return d

def getStepList(r, h, d):
    '''
    This function is to get the list of steps in the process of dynamic programming.
    Attributes: 
        r -> the list of words produced by splitting reference sentence.
        h -> the list of words produced by splitting hypothesis sentence.
        d -> the matrix built when calulating the editting distance of h and r.
    '''
    x = len(r)
    y = len(h)
    list = []
    while True:
        if x == 0 and y == 0: 
            break
        elif x >= 1 and y >= 1 and d[x][y] == d[x-1][y-1] and r[x-1] == h[y-1]: 
            list.append("c")
            x = x - 1
            y = y - 1
        elif y >= 1 and d[x][y] == d[x][y-1]+1:
            list.append("i")
            x = x
            y = y - 1
        elif x >= 1 and y >= 1 and d[x][y] == d[x-1][y-1]+1:
            list.append("s")
            x = x - 1
            y = y - 1
        else:
            list.append("d")
            x = x - 1
            y = y
    return list[::-1]


def alignedPrint(list, r, h, result, result2):
    '''
    This funcition is to print the result of comparing reference and hypothesis sentences in an aligned way.
    
    Attributes:
        list   -> the list of steps.
        r      -> the list of words produced by splitting reference sentence.
        h      -> the list of words produced by splitting hypothesis sentence.
        result -> the rate calculated based on edit distance.
    '''
    print("REF_SENT:", end=" ")
    for i in range(len(list)):
        if list[i] == "i":
            count = 0
            for j in range(i):
                if list[j] == "d":
                    count += 1
            index = i - count
            print(" "*(len(h[index])), end=" ")
            
            list_ref.append(" "*len(h[index]))
        elif list[i] == "s":
            count1 = 0
            for j in range(i):
                if list[j] == "i":
                    count1 += 1
            index1 = i - count1
            count2 = 0
            for j in range(i):
                if list[j] == "d":
                    count2 += 1
            index2 = i - count2
            if len(r[index1]) < len(h[index2]):
                list_ref.append(r[index1] + " " * (len(h[index2])-len(r[index1])))
            else:
                print(r[index1], end=" "),
                list_ref.append(r[index1])
        else:
            count = 0
            for j in range(i):
                if list[j] == "i":
                    count += 1
            index = i - count
            print(r[index], end=" "),
            list_ref.append(r[index])
    print("\nOBT_SENT:", end=" ")
    for i in range(len(list)):
        if list[i] == "d":
            count = 0
            for j in range(i):
                if list[j] == "i":
                    count += 1
            index = i - count
            print(" " * (len(r[index])), end=" ")
            list_pred.append(" " * (len(r[index])))
        elif list[i] == "s":
            count1 = 0
            for j in range(i):
                if list[j] == "i":
                    count1 += 1
            index1 = i - count1
            count2 = 0
            for j in range(i):
                if list[j] == "d":
                    count2 += 1
            index2 = i - count2
            if len(r[index1]) > len(h[index2]):
                print(h[index2] + " " * (len(r[index1])-len(h[index2])), end=" ")
                list_pred.append(h[index2] + " " * (len(r[index1])-len(h[index2])))
            else:
                print(h[index2], end=" ")
                list_pred.append(h[index2])
        else:
            count = 0
            for j in range(i):
                if list[j] == "d":
                    count += 1
            index = i - count
            print(h[index], end=" ")
            list_pred.append(h[index])
    print("\nEVA_LOCA:", end=" ")
    for i in range(len(list)):
        if list[i] == "d":
            count = 0
            for j in range(i):
                if list[j] == "i":
                    count += 1
            index = i - count
            print("D" + " " * (len(r[index])-1), end=" ")
        elif list[i] == "i":
            count = 0
            for j in range(i):
                if list[j] == "d":
                    count += 1
            index = i - count
            print("I" + " " * (len(h[index])-1), end=" ")
        elif list[i] == "s":
            count1 = 0
            for j in range(i):
                if list[j] == "i":
                    count1 += 1
            index1 = i - count1
            count2 = 0
            for j in range(i):
                if list[j] == "d":
                    count2 += 1
            index2 = i - count2
            if len(r[index1]) > len(h[index2]):
                print("S" + " " * (len(r[index1])-1), end=" ")
            else:
                print("S" + " " * (len(h[index2])-1), end=" ")
        else:
            count = 0
            for j in range(i):
                if list[j] == "i":
                    count += 1
            index = i - count
            print(" " * (len(r[index])), end=" ")
    print("\n*********************************")
    print("WER: " + result)
    #print("---------------------------------")
    #print("LIST:" + str(list))
    #print("REF LIST:" + str(list_ref))
    #print("PRD LIST:" + str(list_pred))
    print("*********************************")

def wer(r, h):
    """
    This is a function that calculate the word error rate in ASR.
    You can use it like this: wer("what is it".split(), "what is".split()) 
    """
    # build the matrix
    d = editDistance(r, h)

    # find out the manipulation steps
    list = getStepList(r, h, d)

    #getting own WER. 
    s_count = list.count("s")
    i_count = list.count("i")
    d_count = list.count("d")
    r_count = len(r)

    if r_count == 0:
        flager = 1
        return list, r, h, "", 0, flager

    result2 = (s_count + i_count + d_count)/len(r) * 100

    # print the result in aligned way
    result = float(d[len(r)][len(h)]) / len(r) * 100
    result = str("%.2f" % result)
    #alignedPrint(list, r, h, result)
    flager = 0
    return list, r, h, result, result2, flager


def sentencewer(predsen, truthsen):
    pred = predsen
    truth = truthsen
    r = truth.split()
    h = pred.split()

    r_count = len(r)

    s1, s2, l1, l2, l3, flager = wer(r, h)

    if flager == 1:
        df = pd.DataFrame()
        return pred, truth, l2, l3, df, flager

    print("-----------------------------------------------------------------------")
    list_pred.clear()
    list_ref.clear()
    alignedPrint(s1, s2, l1, l2, l3)
    print("-----------------------------------------------------------------------")
    print("-----------------------------------------------------------------------")

    di= {}
    pair = []
    allpair = []

    for i in range(len(s1)):
        allpair.append([list_ref[i],list_pred[i],str(s1[i]).upper()])
        if s1[i] != "c":
            di.update({s1[i]:1})
            pair.append([s1[i],list_ref[i],list_pred[i]])

    df = pd.DataFrame(allpair)
    df.columns = ["Groundtruth", "Prediction", "Label"]
    referencesent = " ".join(df['Groundtruth'])
    obtainedsent = " ".join(df['Prediction'])

    print(referencesent)
    print(obtainedsent)
    flager = 0

    return pred, truth, l2, l3, df, flager


def runwer(file, rempunc, remrep, remcomp):
    dfm = pd.read_excel(file)
    dfm = dfm.dropna()
    dfm = dfm.reset_index(drop = True)
    print(dfm)
    obt = []
    rft = []
    wrt = []
    err= []
    owert = []
    aud = []
    count  = 0
    sum = 0
    dfx = pd.DataFrame()

    resultfilename = "generated_("+file.rsplit('/', 1)[-1]+")"

    if rempunc == 1:
        resultfilename = resultfilename+"_(removedPunctuation)_"

    if remrep == 1: 
        resultfilename = resultfilename+"_(withReplacement)_"

    if remcomp == 1: 
        resultfilename = resultfilename+"_(withCompound)_"

    for j in range(len(dfm['Obtainedsentence'])):
        
        #condition for adding the replacement.
        if remrep == 1:
            dfm["Obtainedsentence"][j] = replace_function(str(dfm["Obtainedsentence"][j]))
            dfm["Groundtruth"][j] = replace_function(str(dfm["Groundtruth"][j]))
            dfm["Groundtruth"][j] = jiwer.RemoveMultipleSpaces()(str(dfm["Groundtruth"][j]))
            dfm["Obtainedsentence"][j] = jiwer.RemoveMultipleSpaces()(str(dfm["Obtainedsentence"][j]))

        #condition for removing symbols and punctuations.
        if rempunc == 1:
            chars_to_ignore_regex = '(?!<\d)\.(?!\d)|[\,\?\!\|\।\;\:\(\)\[\]\_\±\“\”\α\↑\↓\®\×\§\°\¼\½\ê\ê\ò\β\γ\κ\λ\™\→\≈\@\"\#\•]'
            dfm["Obtainedsentence"][j] = re.sub(chars_to_ignore_regex, ' ', str(dfm["Obtainedsentence"][j])).lower()+ " "
            dfm["Groundtruth"][j] = re.sub(chars_to_ignore_regex, ' ', str(dfm["Groundtruth"][j])).lower()+ " "

        #condition for compound words.
        if remcomp == 1:
            ob, rf, wr, ower, pairdf, flager = sentencewer(str(dfm["Obtainedsentence"][j]),str(dfm["Groundtruth"][j]))
            print(pairdf)
            for i in range((len(pairdf['Label']))-1):
                if pairdf['Label'][i] == 'D':
                    stri = pairdf['Groundtruth'][i]
                    stri = ''.join(e for e in stri if e.isalnum())
                    stri2 = pairdf['Prediction'][i]
                    stri2 = ''.join(e for e in stri2 if e.isalnum())
                    if pairdf['Label'][i+1] == 'S':
                        stri = pairdf['Groundtruth'][i]+""+pairdf['Groundtruth'][i+1]
                        stri = ''.join(e for e in stri if e.isalnum()) 
                        stri2 = pairdf['Prediction'][i+1]
                        if stri == stri2:
                            pairdf['Groundtruth'][i]= stri
                            pairdf["Groundtruth"][i+1]= ""
                            print(pairdf['Groundtruth'][i+1])
                            print("same: ",stri)

                if pairdf['Label'][i] == 'S':
                    stri = pairdf['Groundtruth'][i]
                    stri = ''.join(e for e in stri if e.isalnum())
                    stri2 = pairdf['Prediction'][i]
                    stri2 = ''.join(e for e in stri2 if e.isalnum())
                    if stri == stri2:
                        pairdf['Groundtruth'][i]= stri
                        pairdf['Prediction'][i]= stri
                        print("same: ",stri)
                    elif pairdf['Label'][i+1] == 'I':
                        stri2 = pairdf['Prediction'][i]+""+pairdf['Prediction'][i+1]
                        stri2 = ''.join(e for e in stri2 if e.isalnum())
                        if stri == stri2:
                            pairdf['Groundtruth'][i]= stri
                            pairdf['Prediction'][i]= stri
                            print("same insertions: ",stri)
                        elif pairdf['Label'][i+1] == 'D':
                            stri = pairdf['Groundtruth'][i]+""+pairdf['Groundtruth'][i+1]
                            stri = ''.join(e for e in stri if e.isalnum())
                            if stri == stri2:
                                pairdf['Groundtruth'][i]= stri
                                pairdf['Prediction'][i]= stri
                                print("same deletions: ",stri)
                    
            
            dfm["Groundtruth"][j] = ' '.join(word for word in pairdf['Groundtruth'])
            dfm["Obtainedsentence"][j] = ' '.join(word for word in pairdf['Prediction']) 
            dfm["Groundtruth"][j] = jiwer.RemoveMultipleSpaces()(str(dfm["Groundtruth"][j]))
            dfm["Obtainedsentence"][j] = jiwer.RemoveMultipleSpaces()(str(dfm["Obtainedsentence"][j]))

              

        print("Before final compute:--------------------------------------")
        print("Groundtruth :: ",dfm["Groundtruth"][j])
        print("Obtainedsentence :: ",dfm["Obtainedsentence"][j])
        ob, rf, wr, ower, pairdf, flager = sentencewer(str(dfm["Obtainedsentence"][j]),str(dfm["Groundtruth"][j]))
        error = jiwer.wer(str(dfm["Groundtruth"][j]), str(dfm["Obtainedsentence"][j]))
        #error = jiwer.wer(ground, obtained)
        error = error*100
        if flager != 1:
            aud.append(dfm['Audiofile'][j])
            obt.append(ob)
            rft.append(rf)
            err.append(error)
            wrt.append(wr)
            owert.append(ower)
            count  = count+1
            sum = sum + float(wr)
            dfx = dfx.append(pairdf)

    avg = sum/count

    df = pd.DataFrame(list(zip(aud, rft, obt, wrt,err)),
                columns =['Audiofile','Reference Sentence', 'Obtained Sentence', 'WER Score', 'Jiwer WER'])

    resultfilename = resultfilename+"report.xlsx"
    df.to_excel(resultfilename)
    print("========>AVG: ", avg)


##################################################################################################################
window = Tk()
Title = tk.Label(text="WER Report Generator")

txt = Text(window, width= 170) 


class PrintToTXT(object):
 def write(self, s): 
     txt.insert(END, s)



def fileopener():
    sys.stdout = PrintToTXT() 
    print("Punctuation: ", CheckVar1.get() )
    print("Replacement: ", CheckVar2.get() )
    print("Compoundwords: ", CheckVar3.get() )
    filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    print(filename)
    runwer(file=filename, rempunc=CheckVar1.get(), remrep= CheckVar2.get(), remcomp = CheckVar3.get())

CheckVar1 = IntVar()
CheckVar2 = IntVar()
CheckVar3 = IntVar()

C1 = Checkbutton(window, text = "Remove Symbols and Punctuations", variable = CheckVar1, \
                 onvalue = 1, offvalue = 0, height=3, \
                 width = 50)
C2 = Checkbutton(window, text = "Enable Replacement Progam", variable = CheckVar2, \
                 onvalue = 1, offvalue = 0, height=3, \
                 width = 50)
C3 = Checkbutton(window, text = "Enable Compound word Detection", variable = CheckVar3, \
                 onvalue = 1, offvalue = 0, height=3, \
                 width = 50)


button = tk.Button(
    text="Select File",
    width=25,
    height=5,
    command= lambda: fileopener()
)

Title.grid(sticky=N)
C1.grid()
C2.grid()
C3.grid()
button.grid(sticky=S)
txt.grid() 

window.mainloop()

