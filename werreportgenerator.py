import numpy
import re
import pandas as pd

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
    print("OWN_WER:" + str(result2))
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
    result = str("%.2f" % result) + "%"
    #alignedPrint(list, r, h, result)
    flager = 0
    return list, r, h, result, result2, flager


def sentencewer(predsen, truthsen):
    pred = predsen
    truth = truthsen
    pred = pred.replace("&","and")
    pred = pred.replace("%", " percentage")
    pred = pred.replace("eg.", "example")
    pred = pred.replace("e.g.", "example")
    pred = pred.replace("eg:", "example")
    pred = pred.replace("e.g", "example")
    pred = pred.replace("$", " dollars")
    pred = pred.replace("approx.", "approximately")
    pred = pred.replace("~", " approximately ")
    pred = pred.replace("+", " plus ")
    pred = pred.replace("i.e.", " that is ")
    pred = pred.replace("=", " equal to ")
    pred = pred.replace("equal", " equal to ")
    pred = pred.replace("equals", " equal to ")
    pred = pred.replace("/", " by ")
    pred = pred.replace("<", " less than ")
    pred = pred.replace(">", " greater than ")
    pred = pred.replace("≤"," less than or equal to ")
    pred = pred.replace("≥"," greater than or eqaul to ")

    truth = truth.replace("&","and")
    truth = truth.replace("%", " percentage")
    truth = truth.replace("eg.", "example")
    truth = truth.replace("e.g.", "example")
    truth = truth.replace("eg:", "example")
    truth = truth.replace("e.g", "example")
    truth = truth.replace("=", " equal to ")
    truth = truth.replace("equal", " equal to ")
    truth = truth.replace("equals", "equal")
    truth = truth.replace("/", " by ")    
    truth = truth.replace("$", " dollars")
    truth = truth.replace("approx.", "approximately")
    truth = truth.replace("~", " approximately ")
    truth = truth.replace("+", " plus ")
    truth = truth.replace("$", " dollars")
    truth = truth.replace("i.e.", " that is ")
    truth = truth.replace("<", " less than ")
    truth = truth.replace(">", " greater than ")
    truth = truth.replace("≤"," less than or equal to ")
    truth = truth.replace("≥"," greater than or eqaul to ")

    #truth = re.sub("(\d+)\-(\d+)", r"\1 to \2", truth)
    #pred = re.sub("(\d+)\-(\d+)", r"\1 to \2", pred)


    chars_to_ignore_regex = '(?!<\d)\.(?!\d)|[\,\?\!\|\।\;\-\—\-\–\:\(\)\[\]\_\±\“\”\α\↑\↓\®\×\§\°\¼\½\ê\ê\ò\β\γ\κ\λ\μ\™\→\≈\@\"\#\•]'
    pred = re.sub(chars_to_ignore_regex, ' ', pred).lower()+ " "
    truth = re.sub(chars_to_ignore_regex, ' ', truth).lower()+ " "
    r = pred.split()
    h = truth.split()

    #below snippet for similar word detection
    #for i in range(len(r)):
    #    for j in range(len(h)-2):
    #        if r[i] == (h[j]+h[j+1]):
    #            h[j] = h[j]+h[j+1]
    #           h[j+1] = " "
    #exist_count = h.count(" ")
    #if exist_count > 0:
    #    h.remove(" ")
    r_count = len(r)

    s1, s2, l1, l2, l3, flager = wer(r, h)

    if flager == 1:
        df = pd.DataFrame()
        return predsen, truthsen, l2, l3, df, flager

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

    return predsen, truthsen, l2, l3, df, flager

df = pd.read_excel("D:\ModelOutputDataanalysis\\files\\abhifinale.xlsx")
obt = []
rft = []
wrt = []
owert = []

allpairdf = []

for i in range(len(df['Obtainedsentence'])):
    ob, rf, wr, ower, pairdf, flager = sentencewer(str(df["Obtainedsentence"][i]),str(df["Groundtruth"][i]))
    if flager != 1:
        obt.append(ob)
        rft.append(rf)
        wrt.append(wr)
        owert.append(ower)
        if int(ower) <= 10 and int(ower) > 0:
        #print(pairdf)
            allpairdf.append(pairdf)

df = pd.DataFrame(list(zip(rft, obt, wrt, owert)),
               columns =['Reference Sentence', 'Obtained Sentence', 'WER Score', 'Own WER Score'])


allpairdfx = pd.concat(allpairdf).reset_index(drop=True)

allpairdfx = allpairdfx[allpairdfx.Label != 'C']

print(allpairdfx)

allpairdfx.to_excel("D:\ModelOutputDataanalysis\output/abhi_data_withouthyphen_below10p.xlsx")
