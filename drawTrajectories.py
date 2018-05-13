import gmplot
import pandas as pd
from ast import literal_eval


def main():
    trainSet = pd.read_csv('datasets/small_train_set.csv',
                            converters={'Trajectory': literal_eval})
    
    roadsId = {}

    for index, row in trainSet.iterrows():
        if row['journeyPatternId'] in roadsId:
            continue
         
        roadsId[row['journeyPatternId']] = True
        latitudes, longitudes = [], []
        
        # elem[2] = latitude, elem[1] = longitude
        for elem in row['Trajectory']:
            latitudes.append(elem[2])
            longitudes.append(elem[1])
        
        length = len(latitudes)
        gmap = gmplot.GoogleMapPlotter(latitudes[length / 2], longitudes[length / 2], 12)
        gmap.plot(latitudes, longitudes, 'cornflowerblue', edge_width=5)

        path = 'static/mymap' + str(index) + '.html'
        gmap.draw(path)
        print 'Result in ' + path
        
        if (len(roadsId) >= 5):
            break


if __name__ == '__main__':
    main()
