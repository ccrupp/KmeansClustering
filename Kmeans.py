import numpy as np
from numpy import genfromtxt
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import random

# plt.plot([1,2],[3,4])
def readData(filename):
    # df = pd.read_csv(filename)
    # print df
    data = genfromtxt(filename, delimiter=',')
    # plt.show()
    # plt.scatter(data[:,2],data[:,3])
    # plt.show()
    # print np.shape(data)
    # ID = data[:,0]
    # value = data[:,1]
    # point1 = data[:,2]
    # point2 = data[:,3]
    return data


# def cluster(parsedData, iterCount, k):

def calcDist(x1, y1, x2, y2):
    """Function for calculating the distance between two points with 2d features"""
    dist = np.math.sqrt(np.math.pow((x2 - x1), 2) + np.math.pow((y2 - y1), 2))
    return dist


def avgX(xList):
    """Function for calculating the average x value of a list of x values"""
    xValue = 0
    for x in xList:
        xValue += x
    xValue = xValue / len(xList)
    return xValue


def avgY(yList):
    """Function for calculating the average y value of a list of y values"""
    yValue = 0
    for y in yList:
        yValue += y
    xValue = yValue / len(yList)
    return xValue


def cluster(parsedData, iterCount, k, centroids):
    random.seed(1111)
    clusters = []
    # Makes k empty lists and adds them to clusters
    for i in range(k):
        cluster = []
        clusters.append(cluster)
    # Creates the first k centroids if not passed
    if len(centroids) == 0:
        for i in range(k):
            centroid = parsedData[random.randrange(len(parsedData))][0]
            while centroid in centroids:
                centroid = parsedData[random.randrange(0, len(parsedData))][0]
            # Catches if the random number generated is already a centroid
            # while centroid in centroids:
            #    centroid = random.randrange(0,len(parsedData))
            #    print centroid
            centroids.append(centroid)
    centroids.sort()
    print "Centroids Used"
    for centroid in centroids:
        print centroid
    # List of points stored as tuples
    centroidPts = []
    for centroid in centroids:
        x = (pointDic[centroid])[0]
        y = pointDic[centroid][1]
        centroidPts.append((x, y))
    # Repeats iterCount times
    for e in range(iterCount):
        clusters = []
        # Makes k empty lists and adds them to clusters
        for i in range(k):
            cluster = []
            clusters.append(cluster)
        # Loops through each data point in the csv, i is the row
        for i in range(len(parsedData)):
            minDist = 10000000
            x = parsedData[i][2]
            y = parsedData[i][3]
            thisDist = 0
            count = 0
            # Loops through all points in centroidPts
            for j in range(len(centroidPts)):
                # Distance from the current centroid to the data point
                thisDist = calcDist(centroidPts[j][0], centroidPts[j][1], x, y)
                if thisDist < minDist:
                    minDist = thisDist
                    count = j
            clusters[count].append(int(parsedData[i, 0]))
        print "current"
        for cluster in clusters:
            print cluster
        # Calculating new centroids
        centroidPts = []
        # Loops through each cluster
        for thiscluster in clusters:
            xList = []
            yList = []
            # Loops through each id in the cluster
            for currentid in thiscluster:
                xList.append(pointDic[currentid][0])
                yList.append(pointDic[currentid][1])
            averageX = avgX(xList)
            averageY = avgY(yList)
            centroidPts.append((averageX, averageY))
    return clusters


def calcA(thisid, clusters, parsedData):
    avgDist = 0
    xi = thisid
    totalDist = 0
    currentcluster = []
    # Loops through each cluster
    for cluster in clusters:
        if cluster != []:
            if xi in cluster:
                # The cluster the passed id
                currentcluster = cluster
    totalDist = 0
    # Loops through each id in the cluster
    for id in currentcluster:
        totalDist += calcDist(pointDic[int(xi)][0], pointDic[int(xi)][1],
                              pointDic[int(id)][0], pointDic[int(id)][1])
    avgDist = totalDist / (len(currentcluster))
    return avgDist


def calcB(thisid, clusters, parsedData):
    xi = thisid
    minAvg = 10000
    # currentcluster = []
    for cluster in clusters:
        # Checks to see that the passed id is not in the current cluster
        if cluster != []:
            if xi not in cluster:
                avgDist = 0
                currentcluster = cluster
                totalDist = 0
                # Loops through each id in the cluster that doesnt contain the passed id
                for id in currentcluster:
                    totalDist += calcDist(pointDic[int(xi)][0], pointDic[int(xi)][1],
                                          pointDic[int(id)][0], pointDic[int(id)][1])
                avgDist = totalDist / len(currentcluster)
                if avgDist < minAvg:
                    minAvg = avgDist
    return minAvg


def calculateSc(clusters, parsedData):
    sc = 0
    for point in parsedData:
        id = point[0]
        a = calcA(id, clusters, parsedData)
        b = calcB(id, clusters, parsedData)
        if b > a:
            max = b
        else:
            max = a
        s = (b - a) / max
        sc += s
    sc = sc / len(parsedData)
    return sc


def experiments(parsedData):
    # Creates a subset of data 2 4 6 7
    for i in range(len(parsedData) - 1, 0, -1):
        data = parsedData[i]
        if data[1] != 4 and data[1] != 2 and data[1] != 6 and data[1] != 7:
            parsedData = np.delete(parsedData, i, axis=0)
    print "done subsetting"
    clusters = cluster(parsedData, 4, 9, [])
    print "done clustering"
    sc = calculateSc(clusters, parsedData)
    print "sc"
    print sc


parsedData = readData("C:\Users\carso\Downloads\digits-embedding.csv")
parsedData = parsedData[0:20000, :]
for i in range(len(parsedData) - 1, -1, -1):
    data = parsedData[i]
    if data[1] != 6 and data[1] != 7 and data[1] != 2 and data[1] != 4:
        parsedData = np.delete(parsedData, (i), axis=0)
for point in parsedData:
    if int(point[1]) == 6:
        plt.scatter(point[2],point[3],c = 'b')
    if int(point[1]) == 7:
        plt.scatter(point[2], point[3], c='r')
    if int(point[1]) == 4:
        plt.scatter(point[2], point[3], c='g')
    if int(point[1]) == 2:
        plt.scatter(point[2], point[3], c='y')
plt.show()
pointDic = {}
#for point in parsedData:
#    pointDic[int(point[0])] = (point[2], point[3])
#clusters = cluster(parsedData, 5, 16, [])
#print "clusters used"
#print clusters
#print calculateSc(clusters, parsedData)
# Trial 1 - 0.493616131591
# Trial 2 - 0.442979922471
# Trial 3 - 0.493616131591
# Trial 4 - 0.493616131591
# Trial 5 - 0.442979922471
# clusters = cluster(parsedData, 5, 4, [])
# Trial 1 - 0.694480025284
# Trial 2 - 0.695548938773
# Trial 3 - 0.695548938773
# Trial 4 - 0.695548938773
# Trial 5 - 0.4750132
# clusters = cluster(parsedData, 5, 8, [])
# Trial 1 - 0.481186644797
# Trial 2 - 0.466500559947
# Trial 3 - 0.530626873264
# Trial 4 - 0.520949506426
# Trial 5 - 0.545557867632
# clusters = cluster(parsedData, 5, 16, [])
# Trial 1 - 0.381289405563
# Trial 2 - 0.416314673801
# Trial 3 - 0.377837423677
# Trial 4 - 0.381110678351
# Trial 5 - 0.385340354188
# clusters = cluster(parsedData, 5, 2, [])
# Trial 1 - 0.821833046381
# Trial 2 - 0.821833046381
# Trial 3 - 0.821833046381
# Trial 4 - 0.821833046381
# Trial 5 - 0.821833046381
# clusters = cluster(parsedData, 5, 4, [])
# Trial 1 - 0.594181957887
# Trial 2 - 0.563042796919
# Trial 3 - 0.442024113759
# Trial 4 - 0.441495846095
# Trial 5 - 0.604734084572
# clusters = cluster(parsedData, 5, 8, [])
# Trial 1 - 0.406694655338
# Trial 2 - 0.360901186029
# Trial 3 - 0.409198281042
# Trial 4 - 0.379816508013
# Trial 5 - 0.411225292884
# clusters = cluster(parsedData, 5, 16, [])
# Trial 1 - 0.350539079794
# Trial 2 - 0.348100243052
# Trial 3 - 0.307414328267
# Trial 4 - 0.32731287156
# Trial 5 - 0.352258957903
