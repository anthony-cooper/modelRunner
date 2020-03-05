import os
import re

genericIEF = r''
pathIEF = r''

#List of all event sets
eventsList = []

eventsList.append(['','50-00','CC00'])
eventsList.append(['','20-00','CC00'])
eventsList.append(['','10-00','CC00'])
eventsList.append(['','05-00','CC00'])
eventsList.append(['','02-00','CC00'])
eventsList.append(['','01-33','CC00'])
eventsList.append(['','01-00','CC00'])
eventsList.append(['','00-50','CC00'])
eventsList.append(['','00-10','CC00'])

eventsList.append(['','01-00','CC30'])

#List of all scenario sets
scenariosList = []

scenariosList.append(['','Existing'])



def genFileLines(genericIEF, events, scenarios):
    file = open(genericIEF,"r")
    #Split lines into lists using ' ' and tab as delimters
    fileLines =[]
    for line in file:
        if re.search('<<~.*~>>', line): #Replace Event/Scenario Operators
            #Replace e# and s#, if suitable scenario exists
            for e in range(0, len(events)):
                line = line.replace('<<~e'+str(e)+'~>>',events[e])
            for s in range(0, len(scenarios)):
                line = line.replace('<<~s'+str(s)+'~>>',scenarios[s])

            #Replace remaining with either e0, s0 or failing EVENT, SCENARIO
            try:
                line = re.sub('<<~e*.~>>',events[0],line)
            except:
                line = re.sub('<<~e*.~>>','EVENT',line)
            try:
                line = re.sub('<<~s*.~>>',scenarios[0],line)
            except:
                line = re.sub('<<~s*.~>>','SCENARIO',line)

        fileLines.append(line)

    file.close

    return fileLines

def genFileName(fileName, events, scenarios):
    if re.search('~.*~', fileName): #Replace Event/Scenario Operators
        #Replace e# and s#, if suitable scenario exists
        for e in range(0, len(events)):
            fileName = fileName.replace('~e'+str(e)+'~',events[e])
        for s in range(0, len(scenarios)):
            fileName = fileName.replace('~s'+str(s)+'~',scenarios[s])

        #Replace remaining with either e0, s0 or failing EVENT, SCENARIO
        try:
            fileName = re.sub('~e*.~',events[0],fileName)
        except:
            fileName = re.sub('~e*.~','EVENT',fileName)
        try:
            fileName = re.sub('~s*.~',scenarios[0],fileName)
        except:
            fileName = re.sub('~s*.~','SCENARIO',fileName)
    return fileName

def writeFile(fileName, fileLines):
    file = open(os.path.join(pathIEF, fileName),'w', newline='')
    file.write(''.join(fileLines))
    file.close()

def generateAll(eventsList,scenariosList):
    for eventSet in eventsList:
        for scenarioSet in scenariosList:
            print(str(eventSet) + ' - ' +str(scenarioSet))
            fileLines = genFileLines(os.path.join(pathIEF,genericIEF),events,scenarios)
            fileName = genFileName(genericIEF, events, scenarios)
            writeFile(fileName,fileLines)

generateAll(eventsList,scenariosList)
