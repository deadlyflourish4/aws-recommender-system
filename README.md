# 
## aws-recommender-system
![Top N Recommendation Algorithm](https://github.com/user-attachments/assets/e8eda9e1-745c-43f2-8d3d-466da70fb9f0)

## Evaluation 
- k-fold cross validation
- Leave one out cross validation (LOOCV)

## metric
- MAE, RMSE (netflix)
- Top n-hits, average reciprocal hit rate (ARHR), cumulative hit rate(cHR), rating hit rate(rHR)
-balance between: Coverage, diversity, novelty, churn, responsiveness,...
- Surrogate problem
- A/B online tests

# Type of recommender system
1. Content-based 
- similarity of content: genre > release date > actor, review, ...
- Genre: cosine similarity, euclid distance, pearson correlation, (weighted average: users rating - cosine similarity)
- Year: knn,  