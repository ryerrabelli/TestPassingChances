import random
import time

startTime = time.time()

def pstdev(data):
    """Calculates the population standard deviation."""
    n = len(data)
    if n < 2:
        raise ValueError('variance requires at least two data points')
    ss = _ss(data)
    pvar = ss/n # the population variance
    return pvar**0.5

def _ss(data):
    """Return sum of square deviations of sequence data."""
    c = sum(data)/len(data)
    ss = sum((x-c)**2 for x in data)
    return ss

def percentile(data, percent):
    # 50% means median
    if percent == 0:
        return min(data)
    elif percent == 1:
        return max(data)

    length = len(data)
    trueSplit = length * percent - 0.5;
    #let's say truesplit is 1.5 Then you want 50% element[1] and 50% element[2]
    percentLower = trueSplit % 1;
    return data[ int(trueSplit) ] * percentLower + data[ int(trueSplit) ] * (1-percentLower)

def printDataMetrics(setOfdata, percentagePlaces, showDistribution, roundExp):
    #find data metrics
    medians = []
    interquartileRanges = []
    iterations = 0
    #if not printDataVertically:
    #    print("Min \t10% \t25% \t50% \t75% \t90% \tMax")
    results = []
    for data in setOfdata:
        iterations += 1
        p = {}
        for percentagePlace in percentagePlaces:
            p[percentagePlace] = percentile(data,percentagePlace)
        #minimum = min(data)
        #p10 = percentile(data, 0.1)
        p25 = percentile(data, 0.25)
        avg = sum(data)/len(data)
        med = percentile(data, 0.5)
        p75 = percentile(data, 0.75)
        #p90 = percentile(data, 0.9)
        #maximum = max(data)
        interquartileRange = p75 - p25
        popstdev = pstdev(data);
        if printDataVertically:
            for percentagePlace in percentagePlaces:
                percentageStr = ""
                if percentagePlace == 0:
                    percentageStr = "Min"
                elif percentagePlace == 1:
                    percentageStr = "Max"
                else:
                    percentageStr = str(percentagePlace*100)+"%"

                percentageStr = percentageStr + " \t" + str(p[percentagePlace])
                if (percentagePlace == 0.5):
                    print(percentageStr+ "\t\tAvg.\t"+str(round(avg,roundExp))+"\t\tMode\t"+str(max(set(data), key=data.count)))
                else:
                    print(percentageStr)
            '''print("Min \t" + str(minimum))
            print("10% \t" + str(round(p10)))
            print("25% \t" + str(round(p25)))
            print("50% \t" + str(round(med))+ "\t\tAvg.\t"+str(round(avg))+"\t\tMode\t"+str(max(set(data), key=data.count)))
            print("75% \t" + str(round(p75)))
            print("90% \t" + str(round(p90)))
            print("Max \t" + str(maximum))'''
            if showDistribution:
                print("St.Dev.\t" + str(round(popstdev,3)))
                print("Size\t" + str(len(data)))
        else:
            result = []
            for percentagePlace in percentagePlaces:
                result.append(str(round(p[percentagePlace],roundExp)))
            results.append(result)
            #print(str(minimum) + "\t\t"+str(round(p10))+ "\t\t" + str(round(p25))+ "\t\t" + str(round(med))+ "\t\t" + str(round(p75))+ "\t\t" + str(round(p90))+ "\t\t" + str(maximum))
            if showDistribution:
                print("Avg. "+str(round(avg))+"\tSt.Dev. " + str(round(popstdev,3))+"\tSize " + str(len(data))+"\tMode " +str(max(set(data), key=data.count)))
        medians.append(med)
        interquartileRanges.append(interquartileRange)

    if not printDataVertically:
        label = []
        padding = 2
        for percentagePlace in percentagePlaces:
            '''spaceLengths.append(0)
            resultsWithLabel = []
            resultsWithLabel.append(label)
            resultsWithLabel.extend(results)
            print(resultsWithLabel)
            for resultPiece in resultsWithLabel:
                spaceLengths[-1] = max(spaceLengths[-1], len(resultsWithLabel[len(spaceLengths)-1])+padding)'''

            if percentagePlace == 0:
                label.append("Min")
            elif percentagePlace == 1:
                label.append("Max")
            else:
                label.append(str(percentagePlace*100)+"%")
        spaceLengths = []
        resultsWithLabel = []
        resultsWithLabel.append(label)
        resultsWithLabel.extend(results)
        for percentagePlace in range(len(resultsWithLabel[0]) ):
            spaceLengths.append(0)
            for resultPiece in resultsWithLabel:
                newOption = len(resultPiece[len(spaceLengths)-1])+padding
                spaceLengths[-1] = max(spaceLengths[-1], newOption)
        labelStr = ""
        for i in range(len(label)):
            labelStr += label[i] + (" "*(spaceLengths[i]-len(label[i])) )
        print(labelStr)
        for i in range(len(results)):
            resultStr = ""
            resultPieceNum = 0
            for resultPiece in results[i]:
                resultStr += resultPiece + (" "*(spaceLengths[resultPieceNum]-len(resultPiece)))
                resultPieceNum += 1
            print("" + str(resultStr))
    if iterations==1:
        return (medians[0], interquartileRanges[0])
    else:
        return  (medians, interquartileRanges)



questionChance = []
for i in range(100):
    questionChance.append(-1)
qCount = 100
answerChoices = 4.0
passingScore = 70.0
printProgress = True
printDataVertically=False

mehQs = [4,29,30,39,67,68,70,72,84,86,88]
unsureQs = [6,14,18,19,20,21,25,27,34,35,44,56,60,64,81,94]
reallyUnsureQs = [11,23,24,28,51,55,77,89]
print("Sum of Unsure Questions: " + str(len(mehQs)+len(unsureQs)+len(reallyUnsureQs)))
#all else, I was pretty confident about

odds = ([[0.9,2.0/3.0,1.0/answerChoices,1.0/answerChoices], #Safer Bet. Note the comments below are based off this
     [0.91,2.0/3.0,2.0/5.0,1.0/3.0]]) #My personal prediction
Riskiness = 1

for question in range(qCount):
    questionChance[question] = odds[Riskiness][0] #assume I got 90% on the ones I'm confident about, probably higher but let's be safe

for question in mehQs:
    questionChance[question] = odds[Riskiness][1] #what I defined in my head as the separation of category

for question in unsureQs:
    questionChance[question] = odds[Riskiness][2] #assume for other questions, I could only eliminate one choice on average

for question in reallyUnsureQs:
    questionChance[question] = odds[Riskiness][3] #assume for other questions, I had no idea what I was doing to be safe

sampleSize = int(1.01460328568788 * 2.2982199291858 * 10000) #for statistics purposes, just going to find probability with a simulation. Should take a minute time
examScores = []
for examNum in range(sampleSize):
    qsAnsweredRight = 0.0
    for examQuestion in range(qCount):
        randSim = random.random() #will be between 0 inclusive and 1 exclusive
        if questionChance[examQuestion] > randSim:
            qsAnsweredRight += 1.0
    examScores.append(qsAnsweredRight/qCount)
    if printProgress and examNum % 10000 == 0:
        print("Avg " + str(examNum)+"/"+str(sampleSize) + ": " + str(sum(examScores)/len(examScores)))


#print("Average: " + str(sum(examScores)/len(examScores)))
#print("SD: " + str(pstdev(examScores)))
#print("Range: " + str(min(examScores))+"-"+str(max(examScores)))
examScores.sort()
printDataMetrics([examScores],[0,0.05,.1,.25,.5,.75,.9,.95,1],False,4)
print("Total Time: " + str(time.time()-startTime))

howManyTimesPassed = 0.0;
for examScore in examScores:
    if examScore >= (passingScore/qCount):
        howManyTimesPassed += 1.0

print("Passing Chance: " + str(howManyTimesPassed/sampleSize))



''' Average: 0.7183317599968689
 SD: 0.03573485378875961

Average: 0.7183958899968576
SD: 0.03578371879934585

Average: 0.7183694399968971
SD: 0.035770290382976105
Total Time: 26.10716199874878
Average: 0.7183556788838866
SD: 0.03578407567099617
Total Time: 59.13641405105591

# 33, 39.5, 37
Avg 2331700: 0.7182924397115699
Average: 0.7182925754896815
SD: 0.03577875907118532
Total Time: 278.0996470451355
Passing Chance: 0.7455876002077382
#Summation of results: most likely 0.7183-0.7184 average with SD: 0.0357-0.0358'''