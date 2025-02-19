import os
import pandas as pd
import sys
from surprise import Dataset, Reader
from collections import defaultdict
import numpy as np
import re

class MovieLens:
    ID2name = {}
    name2ID = {}
    ratingsPath = 'ml-latest-small/ratings.csv'
    moviesPath = 'ml-latest-small/movies.csv'
    df_ratings = None
    df_movies = None
    df_genre = {
        "Action": 0,
        "Adventure": 1,
        "Animation": 2,
        "Children": 3,
        "Comedy": 4,
        "Crime": 5,
        "Documentary": 6,
        "Drama": 7,
        "Fantasy": 8,
        "Film-Noir": 9,
        "Horror": 10,
        "Musical": 11,
        "Mystery": 12,
        "Romance": 13,
        "Sci-Fi": 14,
        "Thriller": 15,
        "War": 16,
        "Western": 17
    }

    def loadDataset(self):
        # Look for files relative to the directory we are running from
        # os.chdir(os.path.dirname(sys.argv[0]))
        df_ratings = pd.read_csv(self.ratingsPath)
        self.df_ratings = pd.DataFrame(df_ratings)
        df_movies = pd.read_csv(self.moviesPath)
        self.df_movies = pd.DataFrame(df_movies)

        # print(self.df_movies.head)
        # print(self.df_movies['genres'])
        for i in range(len(self.df_movies)):
            movieID = self.df_movies['movieId'][i]
            movieName = self.df_movies['genres'][i]
            self.ID2name[movieID] = movieName
            self.name2ID[movieName] = movieID

        reader = Reader(line_format='user item rating timestamp', sep=',',skip_lines=1)
        ratingsDataset = Dataset.load_from_file(self.ratingsPath, reader=reader)
        # print(ratingsDataset)
        return ratingsDataset

    def getUserRatings(self, user):
        userRatings = []
        # hit = False
        # print(self.df_ratings.columns)
        for i in range(len(self.df_ratings)):
            if(user == self.df_ratings["userId"][i]):
                userRatings.append((self.df_ratings['movieId'][i], self.df_ratings['rating'][i]))

        return userRatings

    def getPopularityRank(self):
        ratings = defaultdict(int)
        rankings = defaultdict(int)

        for i in range(len(self.df_ratings)):
            movieID = self.df_ratings['movieId'][i]
            ratings[movieID] += 1

        rank = 1
        for id, count in sorted(ratings.items(), key=lambda x: x[1], reverse=True):
            rankings[id] = rank
            rank += 1
        
        return rankings

    def getGenre(self):
        genres = defaultdict()

        num_genre = len(self.df_genre)
        for i in range(len(self.df_movies)):
            movieID = self.df_movies['movieId'][i]
            movieGenre = self.df_movies['genres'][i].split(sep="|")
            print(movieGenre)

            genre_encode = [0] * num_genre
            for gen in self.df_genre:
                if gen in movieGenre:
                    genre_encode[self.df_genre[gen]] = 1
            genres[movieID] = genre_encode

        return genres

    def getYears(self):
        years = defaultdict()
        p = re.compile(r"(?:\((\d{4})\))?\s*$")

        for i in range(len(self.df_movies)):
            movieID = self.df_movies['movieId'][i]
            movieName = self.df_movies['title'][i]
            m = p.search(movieName)
            year = m.group(1)
            if year:
                years[movieID] = int(year)
        
        return years

    def getMiseEnScene(self):
        pass 
    
    def getMovieName(self, movieID):
        movieName = ""
        if movieID in self.ID2name:
            movieName = self.ID2name[movieID]
        
        return movieName
    
    def getMovieID(self, movieName):
        movieID = 0
        if movieName in self.name2ID:
            movieID = self.name2ID[movieName]

        return movieID

