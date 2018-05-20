from collections import Counter
from sklearn.base import BaseEstimator 


class KNN(BaseEstimator):
    def __init__(self, K, distFunc):
        self.data = []
        self.K = K
        self.distFunc = distFunc

    def fit(self, data, ids):
        self.data.extend(zip(data, ids))
        
    def predict(self, predData):
        result = []

        for query in predData:
            allDstQuer, closerIds = [], Counter() 
            
            # find distance from every other point
            for vec in self.data:
                dst = self.distFunc(vec[0], query)
                allDstQuer.append((dst, vec[1]))
            
            # sort distances so as to find K smallest
            allDstQuer.sort()
            
            for i in range(self.K):
                vecId = allDstQuer[i][1]
                closerIds[vecId] += 1
            
            predId = closerIds.most_common(1)[0][0]
            result.append(predId)
        
        return result
