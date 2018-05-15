import gmplot
import pandas as pd
from ast import literal_eval


def drawTrajectory(latitudes, longitudes, path, redPath = False):
    length = len(latitudes)

    if not redPath:
        gmap = gmplot.GoogleMapPlotter(latitudes[length / 2], longitudes[length / 2], 12)
        gmap.plot(latitudes, longitudes, 'cornflowerblue', edge_width = 5)
    else:
        gmap = gmplot.GoogleMapPlotter(latitudes[0][length / 2], longitudes[0][length / 2], 12)
        gmap.plot(latitudes[0], longitudes[0], '#008000', edge_width = 5)
        gmap.plot(latitudes[1], longitudes[1], '#FF0000', edge_width = 5)
        
    gmap.draw(path)
    print 'Result in ' + path


def main():
    trainSet = pd.read_csv('datasets/train_set.csv',
                            converters={'Trajectory': literal_eval})
    
    roadsId = {}
    
    # draw five distinct trajectories
    for index, row in trainSet.iterrows():
        if row['journeyPatternId'] in roadsId:
            continue
         
        roadsId[row['journeyPatternId']] = True
        latitudes, longitudes = [], []
        
        # elem[2] = latitude, elem[1] = longitude
        for elem in row['Trajectory']:
            latitudes.append(elem[2])
            longitudes.append(elem[1])
        
        path = 'static/mymap' + str(index) + '.html'
        drawTrajectory(latitudes, longitudes, path)
        
        if (len(roadsId) >= 5):
            break


if __name__ == '__main__':
    main()
