import numpy as np
from numpy import genfromtxt
import random


class MyKmeans:
    def __init__(self):
        idk = []

    def readData(self, filename):
        """Reads the data as an nparray"""
        data = genfromtxt(filename, delimiter=',')
        return data

    def calcDist(self, x1, y1, x2, y2):
        """Function for calculating the distance between two points with 2d features"""
        dist = np.math.sqrt(np.math.pow((x2 - x1), 2) + np.math.pow((y2 - y1), 2))
        return dist

    def avgX(self, xList):
        """Function for calculating the average x value of a list of x values"""
        xValue = 0
        for x in xList:
            xValue += x
        xValue = xValue / len(xList)
        return xValue

    def avgY(self, yList):
        """Function for calculating the average y value of a list of y values"""
        yValue = 0
        for y in yList:
            yValue += y
        xValue = yValue / len(yList)
        return xValue

    def cluster(self, parsedData, iterCount, k, centroids):
        random.seed(1111)
        # Creates a dictionary with points as ids as keys and xy coords as values
        pointDic = {}
        for point in parsedData:
            pointDic[int(point[0])] = (point[2], point[3])
        clusters = []
        # Makes k empty lists and adds them to clusters
        for i in range(k):
            cluster = []
            clusters.append(cluster)
        # Creates the first k centroids if not passed
        if len(centroids) == 0:
            for i in range(k):
                centroid = parsedData[random.randrange(len(parsedData))][0]
                # Catches if the random number generated is already a centroid
                while centroid in centroids:
                    centroid = parsedData[random.randrange(0, len(parsedData))][0]
                centroids.append(centroid)
        centroids.sort()
        # List of points stored as tuples
        centroidPts = []
        # Converts the ids in the centroid list to points
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
                    thisDist = MyKmeans.calcDist(self, centroidPts[j][0], centroidPts[j][1], x, y)
                    if thisDist < minDist:
                        minDist = thisDist
                        count = j
                clusters[count].append(int(parsedData[i, 0]))
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
                averageX = MyKmeans.avgX(self, xList)
                averageY = MyKmeans.avgY(self, yList)
                centroidPts.append((averageX, averageY))
        return clusters

    def calcA(self, thisid, clusters, parsedData, pointDic):
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
            totalDist += MyKmeans.calcDist(self, pointDic[int(xi)][0], pointDic[int(xi)][1],
                                           pointDic[int(id)][0], pointDic[int(id)][1])
        avgDist = totalDist / (len(currentcluster))
        return avgDist

    def calcB(self, thisid, clusters, parsedData, pointDic):
        xi = thisid
        minAvg = 10000
        for cluster in clusters:
            # Checks to see that the passed id is not in the current cluster
            if cluster != []:
                if xi not in cluster:
                    avgDist = 0
                    currentcluster = cluster
                    totalDist = 0
                    # Loops through each id in the cluster that doesnt contain the passed id
                    for id in currentcluster:
                        totalDist += MyKmeans.calcDist(self, pointDic[int(xi)][0], pointDic[int(xi)][1],
                                                       pointDic[int(id)][0], pointDic[int(id)][1])
                    avgDist = totalDist / len(currentcluster)
                    if avgDist < minAvg:
                        minAvg = avgDist
        return minAvg

    def calculateSC(self, clusters, parsedData):
        pointDic = {}
        for point in parsedData:
            pointDic[int(point[0])] = (point[2], point[3])
        sc = 0
        for point in parsedData:
            id = point[0]
            a = MyKmeans.calcA(self, id, clusters, parsedData, pointDic)
            b = MyKmeans.calcB(self, id, clusters, parsedData, pointDic)
            if b > a:
                max = b
            else:
                max = a
            s = (b - a) / max
            sc += s
        sc = sc / len(parsedData)
        return sc

