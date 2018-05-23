import gmplot
import pandas as pd
from ast import literal_eval
from distances import DTW, LCS
from drawTrajectories import drawTrajectory


def findClosestNeighbors(trainSet, testSet, method):
    # bruteforce to find the closest neighbors for every query.
    for testIndex, testRow in testSet.iterrows():
        dists = []

        for trainIndex, trainRow in trainSet.iterrows():
            ret = None 

            if method == 'DTW':
                ret = DTW(testRow['Trajectory'], trainRow['Trajectory'])
            elif method == 'LCS':
                ret = LCS(testRow['Trajectory'], trainRow['Trajectory'])
                ret = (-ret[0], ret[1])
            
            dists.append((ret, trainRow['tripId']))

        dists.sort()
        latitudes, longitudes = [], []

        # draw testTrajectory
        for elem in testRow['Trajectory']:
            latitudes.append(elem[2])
            longitudes.append(elem[1])
        
        path = 'static/mymap' + method + str(testIndex) + '.html'
        drawTrajectory(latitudes, longitudes, path)

        # operate on five closest neighbors
        for i in range(5):
            tripIdList = trainSet['tripId'].tolist()
            jupIdList = trainSet['journeyPatternId'].tolist()
            trajectList = trainSet['Trajectory'].tolist()

            neighId = dists[i][1]
            pos = tripIdList.index(neighId)

            latitudes, longitudes =  [], []

            # elem[2] = latitude, elem[1] = longitude
            for elem in trajectList[pos]:
                latitudes.append(elem[2])
                longitudes.append(elem[1])
            
            # merge real path with lcs path
            if method == 'LCS':
                lcsPath = dists[i][0][1]
                redLat, redLong = [], []
                
                for elem in lcsPath:
                    redLat.append(elem[2])
                    redLong.append(elem[1])

                latitudes = [latitudes, redLat]
                longitudes = [longitudes, redLong]

            print
            path = 'static/mymap' + method + str(testIndex) + '-' + str(i) + '.html'
            drawTrajectory(latitudes, longitudes, path, method == 'LCS')
 
            print 'Neighbor', (i + 1)
            print 'JP_ID:', jupIdList[pos]

            if method == 'DTW':
                print 'DTW:', dists[i][0]
            elif method == 'LCS':
                print '#Matching Points:', -dists[i][0][0]

        print '----------------------------------'


def main():
    trainSet = pd.read_csv('datasets/train_set.csv',
                            converters={'Trajectory': literal_eval})

    testSet = pd.read_csv('datasets/test_set_a1.csv', #TODO USE THE APPROPRIATE FILE
                          converters={'Trajectory': literal_eval})
    
    trainSet = trainSet[:1000]
    findClosestNeighbors(trainSet, testSet, 'DTW')


if __name__ == '__main__':
    main()
