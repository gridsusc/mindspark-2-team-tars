from sklearn.cluster import KMeans
from sklearn import metrics, preprocessing
from scipy.spatial.distance import cdist
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv('result.csv')
X = preprocessing.normalize(data.drop(columns=['Category']))

best_k = 10

best_kmeans_model = KMeans(n_clusters=best_k, random_state=3).fit(X)
kmeans_labels = best_kmeans_model.labels_
data['cluster'] = kmeans_labels

print(data['cluster'].value_counts())

data.to_csv('clustered_data.csv', index=False)