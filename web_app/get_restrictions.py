import pandas as pd
import statistics
from sklearn.neighbors import NearestCentroid, NearestNeighbors, KNeighborsClassifier
import numpy as np
import math

dg_count = {0: 172, 1: 497, 2: 136, 3: 244, 4: 89, 5: 217, 6: 334, 7: 72, 8: 251, 9: 16}
db_count = {0: 3, 1: 26, 2: 31, 3: 5, 4: 16, 5: 19, 6: 66, 7: 24, 8: 34, 9: 16}
hg_count = {0: 146, 1: 331, 2: 111, 3: 197, 4: 35, 5: 286, 6: 157, 7: 80, 8: 166, 9: 10}
hb_count = {0: 50, 1: 89, 2: 46, 3: 49, 4: 32, 5: 59, 6: 146, 7: 67, 8: 76, 9: 23}
og_count = {0: 19, 1: 50, 2: 44, 3: 20, 4: 20, 5: 14, 6: 130, 7: 30, 8: 34, 9: 7}
ob_count = {0: 79, 1: 215, 2: 59, 3: 77, 4: 53, 5: 73, 6: 308, 7: 32, 8: 153, 9: 16}
sg_count = {0: 120, 1: 265, 2: 55, 3: 67, 4: 38, 5: 170, 6: 107, 7: 69, 8: 98, 9: 6}
sb_count = {0: 34, 1: 211, 2: 94, 3: 78, 4: 34, 5: 85, 6: 175, 7: 41, 8: 110, 9: 18}
lg_count = {0: 59, 1: 124, 2: 126, 3: 39, 4: 47, 5: 24, 6: 163, 7: 38, 8: 78, 9: 41}
lb_count = {0: 90, 1: 207, 2: 53, 3: 76, 4: 30, 5: 77, 6: 259, 7: 51, 8: 136, 9: 15}
bg_count = {0: 189, 1: 470, 2: 116, 3: 252, 4: 67, 5: 332, 6: 227, 7: 113, 8: 249, 9: 20}
bb_count = {0: 175, 1: 515, 2: 82, 3: 201, 4: 60, 5: 126, 6: 362, 7: 61, 8: 316, 9: 30}

def get_key(dct, val):
    for key, value in dct.items():
         if val == value:
             return key

def recommendation(desired_food,health_condition):
    df = pd.read_csv('clustered_data.csv')
    if health_condition=='Diabetes':
        good_food = dg_count
        bad_food = db_count
    if health_condition=='Heart Disease':
        good_food = hg_count
        bad_food = hb_count
    if health_condition=='Obesity':
        good_food = og_count
        bad_food = ob_count
    if health_condition=='Skin Problems':
        good_food = sg_count
        bad_food = sb_count
    if health_condition=='Liver Damage':
        good_food = lg_count
        bad_food = lb_count
    if health_condition=='Blood Pressure':
        good_food = bg_count
        bad_food = bb_count
    target_cluster = int(df[df['Category']==desired_food]['cluster'])
    test_point = df[df['Category']==desired_food].drop(columns=['Category','cluster'])
    good_cluster = get_key(good_food,max(list(good_food.values())))
    bad_cluster = get_key(bad_food,max(list(bad_food.values())))
    target_data = df[df['cluster']==target_cluster]
    good_data = df[df['cluster']==good_cluster]
    bad_data = df[df['cluster']==bad_cluster]
    target_centroid = target_data.drop(columns=['Category', 'cluster']).mean(axis=0).to_numpy()
    good_centroid = good_data.drop(columns=['Category', 'cluster']).mean(axis=0).to_numpy()
    bad_centroid = bad_data.drop(columns=['Category', 'cluster']).mean(axis=0).to_numpy()
    distance_from_good = np.linalg.norm(good_centroid - target_centroid)
    distance_from_bad = np.linalg.norm(bad_centroid - target_centroid)
    good_knn_model = NearestNeighbors(n_neighbors=5).fit(good_data.drop(columns=['Category','cluster']))
    good_nearest_neighbors = good_knn_model.kneighbors(test_point, n_neighbors=5, return_distance=False)[0].tolist()
    good_items = good_data.iloc[good_nearest_neighbors]['Category'].tolist()
    bad_knn_model = NearestNeighbors(n_neighbors=5).fit(bad_data.drop(columns=['Category','cluster']))
    bad_nearest_neighbors = bad_knn_model.kneighbors(test_point, n_neighbors=5, return_distance=False)[0].tolist()
    bad_items = bad_data.iloc[bad_nearest_neighbors]['Category'].tolist()
    return distance_from_good, distance_from_bad, good_items, bad_items

