from surprise import AlgoBase, PredictionImpossible
import numpy as np
import math
import heapq
from movieLens import MovieLens

class ContentBased(AlgoBase):
    def __init__(self, k=40, sim_options={}):
        AlgoBase().__init__(self)
        self.k = k

    def fit(self, trainset):
        AlgoBase.fit(self, trainset)

        df = MovieLens()
        genres = df.getGenre()
        years = df.getYears()

        print("Computing content-based similarity matrix...")
            
        # Compute genre distance for every movie combination as a 2x2 matrix
        self.similarities = np.zeros((self.trainset.n_items, self.trainset.n_items))

        for ratings in range(self.trainset.n_items):
            if(ratings % 100 == 0):
                print(ratings, "of", self.trainset.n_items)
            for otherRatings in range(ratings + 1, self.trainset.n_items):
                movie1_ID = int(self.trainset.to_raw_iid(ratings))
                movie2_ID = int(self.trainset.to_raw_iid(otherRatings))
                genreSimilarity = self.genreSimilarity(movie1_ID, movie2_ID, genres)
                yearSimilarity = self.yearSimilarity(movie1_ID, movie2_ID, years)

                self.similarities[movie1_ID, movie2_ID] = genreSimilarity * yearSimilarity
        
        print("...done.")
                
        return self

    # Cosine similarity for genre
    def genreSimilarity(self, movieID1, movieID2, genres):
        movie1_genre = genres[movieID1]
        movie2_genre = genres[movieID2]

        sumxy = np.sum(movie1_genre * movie2_genre)
        sumxx = np.sqrt(np.sum(np.square(movie1_genre)))
        sumyy = np.sqrt(np.sum(np.square(movie2_genre)))

        return sumxy / (sumxx * sumyy)

    def yearSimilarity(self, movieID1, movieID2, years):
        diff = np.abs(years[movieID1] - years[movieID2])
        
        return np.exp(-diff / 10.0)

    def estimate(self, u, i):

        if not (self.trainset.knows_user(u) and self.trainset.knows_item(i)):
            raise PredictionImpossible('User and/or item is unkown.')
        
        # Build up similarity scores between this item and everything the user rated
        neighbors = []
        for rating in self.trainset.ur[u]:
            genreSimilarity = self.similarities[i,rating[0]]
            neighbors.append( (genreSimilarity, rating[1]) )
        
        # Extract the top-K most-similar ratings
        k_neighbors = heapq.nlargest(self.k, neighbors, key=lambda t: t[0])
        
        # Compute average sim score of K neighbors weighted by user ratings
        simTotal = weightedSum = 0
        for (simScore, rating) in k_neighbors:
            if (simScore > 0):
                simTotal += simScore
                weightedSum += simScore * rating
            
        if (simTotal == 0):
            raise PredictionImpossible('No neighbors')

        predictedRating = weightedSum / simTotal

        return predictedRating
