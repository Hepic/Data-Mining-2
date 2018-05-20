import pandas as pd
import numpy as np
from knn import KNN 
from ast import literal_eval
from distances import DTW
from sklearn import svm, preprocessing
from sklearn.model_selection import cross_val_score, KFold
from sklearn.metrics import accuracy_score


def crossValidation(clf, allSequences, categoryIds, le):
    splits, accur = 4, 0
    kf = KFold(n_splits=splits)
    
    # Splits data to train and test data
    for trainIndex, testIndex in kf.split(allSequences):
        kfSeqTrain = [allSequences[ind] for ind in trainIndex]
        kfSeqTest = [allSequences[ind] for ind in testIndex]
    
        clf.fit(kfSeqTrain, categoryIds[trainIndex])
        kfTestPredIds = clf.predict(kfSeqTest)
        
        accur += accuracy_score(categoryIds[testIndex], kfTestPredIds)
    
    accur /= float(splits)
    print 'Accuracy: ', accur


def main():
    trainSet = pd.read_csv('datasets/small_train_set.csv', # TODO CHANGE TO REAL DATASET
                            converters={'Trajectory': literal_eval})

    testSet = pd.read_csv('datasets/test_set_a1.csv',
                          converters={'Trajectory': literal_eval})
    
    trainSet = trainSet[:40]

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

    crossValidation(clf, allSequences, categoryIds, le)

    
if __name__ == '__main__':
    main()
