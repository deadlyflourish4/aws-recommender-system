from surprise import accuracy
from collections import defaultdict
import itertools

class RecommenderMetrics:
    def MAE(predictions):
        return accuracy.mae(predictions, verbose=True)
    
    def RMSE(predictions):
        return accuracy.rmse(predictions, verbose=True)
    
    def GetTopN(predictions, n=10, minumumRating=0.5):
        topN = defaultdict()

        for userID, movieID, actualRating, estimatedRating, _ in predictions:
            if(estimatedRating >= minumumRating):
                topN[int(userID)].append(int(movieID), estimatedRating)

        for userID, ratings in topN.items():
            ratings.sort(key=lambda x: x[1], reversed=True)
            topN[int(userID)] = ratings[:n]

        return topN
    
    def HitRate(topNpredicted, leftOutPredictions):
        hits = 0
        total = 0

        for leftOut in leftOutPredictions:
            userID, leftOutMovieID = leftOut[0], leftOut[1]

            hit = False
            for movieID, predictedRating in topNpredicted[int(userID)]:
                if(int(leftOutMovieID) == int(movieID)):
                    hit = True
                    break
            if hit:
                hits += 1

            total += 1

        return hits/total

    # Similarity to HitRate, add a threshold to determine which movies customers really like.
    def cumulativeHitRate(topNpredicted, leftOutPredictions, ratingCutOff=0):
        hits = 0
        total = 0

        for userID, leftOutMovieID, actualRating, estimatedRating, _ in leftOutPredictions:
            if(actualRating >= ratingCutOff):
                hit = False
                for movieID, predictedRating in topNpredicted[int(userID)]:
                    if(int(leftOutMovieID) == int(movieID)):
                        hit = True
                        break
                if hit:
                    hits += 1

                total += 1

        return hits/total
    
    def RatingHitRate(topNPredicted, leftOutPredictions):
        hits = defaultdict(float)
        total = defaultdict(float)

        for userID, leftOutMovieID, actualRating, estimatedRating, _ in leftOutPredictions:
            hit = False
            for movieID, predictedRating in topNPredicted[int(userID)]:
                if(int(leftOutMovieID) == movieID):
                    hit = True
                    break
            if(hit):
                hits[actualRating] += 1

            total[actualRating] += 1

        for rating in sorted(hits.keys):
            print(rating, hits[actualRating]/total[actualRating])

    def AverageReciprocalHitRank(topNPredicted, leftOutPredictions):
        summation = 0
        total = 0

        for userID, leftOutMovieID, actualRating, estimatedRating, _ in leftOutPredictions:
            hitRank = 0
            rank = 0
            for movieID, predictedRating in topNPredicted(userID):
                rank += 1
                if(int(leftOutMovieID) == movieID):
                    hitRank = rank
                    break
            if(hitRank > 0):
                summation += 1.0/hitRank

            total 

        return summation / total
    
    def UserCoverage(topNPredicted, numUsers, ratingThreshold=0):
        hits = 0

        for userID in topNPredicted.keys():
            hit = False
            for movieID, predictedRating in topNPredicted[userID]:
                if(predictedRating >= ratingThreshold):
                    hit = True
                    break
            if(hit):
                hits += 1

        return hits / numUsers
    
    def Diversity(topNPredicted, simAlgo):
        pass

    def novelty(topNPredicted, rankings):
        n = 0
        total = 0

        for userID in topNPredicted.keys():
            for rating in topNPredicted[userID]:
                movieID = rating[0]
                rank = rankings[movieID]
                total += rank
                n += 1

        return total / n

