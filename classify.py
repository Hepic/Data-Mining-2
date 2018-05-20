import pandas as pd
from knn import KNN 
from ast import literal_eval
from distances import DTW
from sklearn import svm, preprocessing


def main():
    trainSet = pd.read_csv('datasets/small_train_set.csv', # TODO CHANGE TO REAL DATASET
                            converters={'Trajectory': literal_eval})

    testSet = pd.read_csv('datasets/test_set_a1.csv',
                          converters={'Trajectory': literal_eval})
    
    # labels for categories
    le = preprocessing.LabelEncoder()
    categoryIds = le.fit_transform(trainSet['journeyPatternId'])   

    allSequences = []

    for trainIndex, trainRow in trainSet.iterrows():
        allSequences.append(trainRow['Trajectory'])
    
    # initialize KNN classifier
    clf = KNN(5, DTW)
    clf.fit(allSequences, categoryIds)
    
    # predict the categories for the testSet
    predIds = clf.predict(testSet['Trajectory'])
    predCategs = le.inverse_transform(predIds)

    print predCategs

    
if __name__ == '__main__':
    main()
