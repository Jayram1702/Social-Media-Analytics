"""
Social Media Analytics Project
Name:
Roll Number:
"""

from tkinter.font import names
import hw6_social_tests as test

project = "Social" # don't edit this

### PART 1 ###

import pandas as pd
import nltk
nltk.download('vader_lexicon', quiet=True)
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
endChars = [ " ", "\n", "#", ".", ",", "?", "!", ":", ";", ")" ]

'''
makeDataFrame(filename)
#3 [Check6-1]
Parameters: str
Returns: dataframe
'''
def makeDataFrame(filename):
    df = pd.read_csv(filename)
    return df


'''
parseName(fromString)
#4 [Check6-1]
Parameters: str
Returns: str
'''
def parseName(fromString):
    for rl in fromString.split("\n"):
        start = rl.find(":") + len(":")
        rl = rl[start:]
        end = rl.find(" (")
        rl = rl[:end]
        rl = rl.strip()
        # print(rl)
    return rl


'''
parsePosition(fromString)
#4 [Check6-1]
Parameters: str
Returns: str
'''
def parsePosition(fromString):
    for rl in fromString.split("\n"):
        start = rl.find("(") + len("(")
        rl = rl[start:]
        end = rl.find(" from")
        rl = rl[:end]
        rl = rl.strip()
        # print(rl)
    return rl


'''
parseState(fromString)
#4 [Check6-1]
Parameters: str
Returns: str
'''
def parseState(fromString):
    for rl in fromString.split("\n"):
        start = rl.find("from") + len("from")
        rl = rl[start:]
        end = rl.find(")")
        rl = rl[:end]
        rl = rl.strip()
        # print(rl)
    return rl


'''
findHashtags(message)
#5 [Check6-1]
Parameters: str
Returns: list of strs
'''
def findHashtags(message):
    sp = message.split("#")
    stri=""
    data=[]
    for x in sp[1:]:
        for y in x:
            if y not in endChars:
                stri+=y
            else:
                break
        data.append("#"+stri)
        stri = ""
    return data


'''
getRegionFromState(stateDf, state)
#6 [Check6-1]
Parameters: dataframe ; str
Returns: str
'''
def getRegionFromState(stateDf, state):
    df = stateDf
    row = df.loc[df["state"] == state,"region" ]
    val = row.values[0] 
    # print(val)
    return val


'''
addColumns(data, stateDf)
#7 [Check6-1]
Parameters: dataframe ; dataframe
Returns: None
'''
def addColumns(data, stateDf):
    name = []
    position = []
    states = []
    region = []
    hashtags = []
    for index, row in data.iterrows():
        name.append(parseName(row["label"]))
        position.append(parsePosition(row["label"]))
        states.append(parseState(row["label"]))
        region.append(getRegionFromState(stateDf,parseState(row["label"])))
        hashtags.append(findHashtags(row["text"]))
    data["name"] = name
    data["position"] = position
    data["state"] = states
    data["region"] = region
    data["hashtags"] = hashtags
    return None


### PART 2 ###

'''
findSentiment(classifier, message)
#1 [Check6-2]
Parameters: SentimentIntensityAnalyzer ; str
Returns: str
'''
def findSentiment(classifier, message):
    score = classifier.polarity_scores(message)['compound']
    if score < -0.1:
        return "negative"
    elif score > 0.1:
        return "positive"
    else:
        return "neutral"

'''
addSentimentColumn(data)
#2 [Check6-2]
Parameters: dataframe
Returns: None
'''
def addSentimentColumn(data):
    classifier = SentimentIntensityAnalyzer()
    sentiment = []
    for index, row in data.iterrows():
        # print(index, row)
        sentiment.append(findSentiment(classifier, row["text"]))
    data["sentiment"] = sentiment
    return None


'''
getDataCountByState(data, colName, dataToCount)
#3 [Check6-2]
Parameters: dataframe ; str ; str
Returns: dict mapping strs to ints
'''
def getDataCountByState(data, colName, dataToCount):
    dicts={}
    if len(colName)!=0 and len(dataToCount)!=0:
        for i,r in data.iterrows():
            if r[colName]==dataToCount:
                if r["state"] not in dicts:
                    dicts[r["state"]]=0
                dicts[r["state"]]+=1
    if len(colName)==0 or len(dataToCount)==0:
        for i,r in data.iterrows():
            if r["state"] not in dicts:
                dicts[r["state"]]=0
            dicts[r["state"]]+=1
    return dicts


'''
getDataForRegion(data, colName)
#4 [Check6-2]
Parameters: dataframe ; str
Returns: dict mapping strs to (dicts mapping strs to ints)
'''
def getDataForRegion(data, colName):
    dicts={}
    for i,row in data.iterrows():
        key=row["region"]
        if key not in dicts:
            dicts[key]={}
        if row[colName] not in dicts[key]:
            dicts[key][row[colName]]=1
        else:
            dicts[key][row[colName]]+=1
    return dicts


'''
getHashtagRates(data)
#5 [Check6-2]
Parameters: dataframe
Returns: dict mapping strs to ints
'''
def getHashtagRates(data):
    hash={}
    for a in data["hashtags"]:
        for b in a:
            if len(b)!=0 and b not in hash:
                hash[b]=1
            else:
                hash[b]+=1
    return hash

'''
mostCommonHashtags(hashtags, count)
#6 [Check6-2]
Parameters: dict mapping strs to ints ; int
Returns: dict mapping strs to ints
'''
def mostCommonHashtags(hashtags, count):
    cmh=dict(sorted(hashtags.items(), key=lambda x: x[1], reverse=True))
    cnt=dict([(i,j) for (i,j) in cmh.items()] [:count])
    return cnt


'''
getHashtagSentiment(data, hashtag)
#7 [Check6-2]
Parameters: dataframe ; str
Returns: float
'''
def getHashtagSentiment(data, hashtag):
    TotHasgs = 0
    Hasgcount = 0
    for i,r in data.iterrows():
        if hashtag in findHashtags(r["text"]):
            if r["sentiment"] == "positive":
                Hasgcount+=1
            elif r["sentiment"] == "negative":
                Hasgcount-=1
            elif r["sentiment"] == "neutral":
                Hasgcount+=0
            TotHasgs+=1
    return Hasgcount/TotHasgs


### PART 3 ###

'''
graphStateCounts(stateCounts, title)
#2 [Hw6]
Parameters: dict mapping strs to ints ; str
Returns: None
'''
def graphStateCounts(stateCounts, title):
    import matplotlib.pyplot as plt
    state=[i for i in stateCounts.keys()]
    num=[j for j in stateCounts.values()]
    plt.bar(state, num, width=0.6)
    plt.xticks(ticks=list(range(len(state))), labels=state, rotation="vertical")
    plt.xlabel("States")
    plt.ylabel("Values of states")
    plt.title(title)
    plt.show()
    return


'''
graphTopNStates(stateCounts, stateFeatureCounts, n, title)
#3 [Hw6]
Parameters: dict mapping strs to ints ; dict mapping strs to ints ; int ; str
Returns: None
'''
def graphTopNStates(stateCounts, stateFeatureCounts, n, title):
    stateCnt = {}
    for k,v in stateFeatureCounts.items():
        for a,b in stateCounts.items():
            if a == k:
                stateCnt[a]=v/b
    cmnhasg = mostCommonHashtags(stateCnt, n)
    graphStateCounts(cmnhasg,title)
    return


'''
graphRegionComparison(regionDicts, title)
#4 [Hw6]
Parameters: dict mapping strs to (dicts mapping strs to ints) ; str
Returns: None
'''
def graphRegionComparison(regionDicts, title):
    features=[]
    region=[]
    regionfeatures=[]
    for reg in regionDicts:
        for fea in regionDicts[reg]:
            if fea not in features:
                features.append(fea)
        region.append(reg)
    for reg in regionDicts:
        temp=[]
        for fea in features:
            if fea not in regionDicts[reg]:
                temp.append(0)
            else:
                temp.append(regionDicts[reg][fea])
        regionfeatures.append(temp)
    sideBySideBarPlots(features, region, regionfeatures, title)
    return


'''
graphHashtagSentimentByFrequency(data)
#4 [Hw6]
Parameters: dataframe
Returns: None
'''
def graphHashtagSentimentByFrequency(data):
    return


#### PART 3 PROVIDED CODE ####
"""
Expects 3 lists - one of x labels, one of data labels, and one of data values - and a title.
You can use it to graph any number of datasets side-by-side to compare and contrast.
"""
def sideBySideBarPlots(xLabels, labelList, valueLists, title):
    import matplotlib.pyplot as plt

    w = 0.8 / len(labelList)  # the width of the bars
    xPositions = []
    for dataset in range(len(labelList)):
        xValues = []
        for i in range(len(xLabels)):
            xValues.append(i - 0.4 + w * (dataset + 0.5))
        xPositions.append(xValues)

    for index in range(len(valueLists)):
        plt.bar(xPositions[index], valueLists[index], width=w, label=labelList[index])

    plt.xticks(ticks=list(range(len(xLabels))), labels=xLabels, rotation="vertical")
    plt.legend()
    plt.title(title)

    plt.show()

"""
Expects two lists of probabilities and a list of labels (words) all the same length
and plots the probabilities of x and y, labels each point, and puts a title on top.
Expects that the y axis will be from -1 to 1. If you want a different y axis, change plt.ylim
"""
def scatterPlot(xValues, yValues, labels, title):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()

    plt.scatter(xValues, yValues)

    # make labels for the points
    for i in range(len(labels)):
        plt.annotate(labels[i], # this is the text
                    (xValues[i], yValues[i]), # this is the point to label
                    textcoords="offset points", # how to position the text
                    xytext=(0, 10), # distance from text to points (x,y)
                    ha='center') # horizontal alignment can be left, right or center

    plt.title(title)
    plt.ylim(-1, 1)

    # a bit of advanced code to draw a line on y=0
    ax.plot([0, 1], [0.5, 0.5], color='black', transform=ax.transAxes)

    plt.show()


### RUN CODE ###

# This code runs the test cases to check your work
if __name__ == "__main__":
    print("\n" + "#"*15 + " WEEK 1 TESTS " +  "#" * 16 + "\n")
    # test.week1Tests()
    print("\n" + "#"*15 + " WEEK 1 OUTPUT " + "#" * 15 + "\n")
    # test.runWeek1()
    # test.testParseName()
    # test.testParsePosition()
    # test.testParseState()
    # test.testFindHashtags()
    # test.testGetRegionFromState()
    # test.testAddColumns()
    # test.testFindSentiment()
    # test.testAddSentimentColumn()
    
    ## Uncomment these for Week 2 ##
    """print("\n" + "#"*15 + " WEEK 2 TESTS " +  "#" * 16 + "\n")
    test.week2Tests()
    print("\n" + "#"*15 + " WEEK 2 OUTPUT " + "#" * 15 + "\n")
    test.runWeek2()"""
    # df = makeDataFrame("data/politicaldata.csv")
    # stateDf = makeDataFrame("data/statemappings.csv")
    # addColumns(df, stateDf)
    # addSentimentColumn(df)
    # # test.testGetDataCountByState(df)
    # # test.testGetDataForRegion(df)
    # # test.testGetHashtagRates(df)
    # # test.testMostCommonHashtags(df)
    # test.testGetHashtagSentiment(df)


    ## Uncomment these for Week 3 ##
    print("\n" + "#"*15 + " WEEK 3 OUTPUT " + "#" * 15 + "\n")
    test.runWeek3()
