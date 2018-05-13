import gmplot
import pandas as pd
from ast import literal_eval
from distances import DTW
from drawTrajectories import drawTrajectory


def main():
    trainSet = pd.read_csv('datasets/train_set.csv',
                            converters={'Trajectory': literal_eval})

    testSet = pd.read_csv('datasets/test_set_a1.csv',
                          converters={'Trajectory': literal_eval})
    
    trainSet = trainSet[:1000]

    # bruteforce to find the closest neighbors for every query.
    for testIndex, testRow in testSet.iterrows():
        dists = []

        for trainIndex, trainRow in trainSet.iterrows():
            dst = DTW(testRow['Trajectory'], trainRow['Trajectory'])
            dists.append((dst, trainRow['tripId']))

        dists.sort()
        latitudes, longitudes = [], []

        # draw testTrajectory
        for elem in testRow['Trajectory']:
            latitudes.append(elem[2])
            longitudes.append(elem[1])
        
        path = 'static/mymapDTW' + str(testIndex) + '.html'
        drawTrajectory(latitudes, longitudes, path)

        # operate on five closest neighbors
        for i in range(5):
            tripIdList = trainSet['tripId'].tolist()
            trajectList = trainSet['Trajectory'].tolist()

            neighId = dists[i][1]
            pos = tripIdList.index(neighId)

            latitudes, longitudes = [], []

            # elem[2] = latitude, elem[1] = longitude
            for elem in trajectList[pos]:
                latitudes.append(elem[2])
                longitudes.append(elem[1])
            
            path = 'static/mymapDTW' + str(testIndex) + '-' + str(i) + '.html'
            drawTrajectory(latitudes, longitudes, path)
 

if __name__ == '__main__':
    main()
