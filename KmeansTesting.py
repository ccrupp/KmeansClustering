from MyKmeans import MyKmeans
km = MyKmeans()
parsedData = km.readData("C:\Users\carso\Downloads\digits-embedding.csv")
parsedData = parsedData[0:10000, :]
clusters = km.cluster(parsedData, 50, 5, [])
print clusters
SC = km.calculateSC(clusters, parsedData)
print SC


