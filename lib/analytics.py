import os

import numpy as np
import pandas as pd
from joblib import dump, load
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

from lib.util.constants import MODEL_DIR, MODEL_NAME


class Analytics:
    def __init__(self):
        self.inputCSV = 'examples/kaggle_yt.csv'
        self.outputCSV = 'examples/youtube_data.csv'

    def pre_process(self):
        df = pd.read_csv(self.inputCSV)
        names = ['duration', 'comments', 'likes', 'dislikes', 'views']

        ndf = pd.DataFrame({names[0]: df['duration_sec'],
                            names[1]: df['comment_count'],
                            names[2]: df['like_count'],
                            names[3]: df['dislike_count'],
                            names[4]: df['view_count']})

        ndf.to_csv(self.outputCSV, sep=',', index=False, header=names)
        print('[INFO] File processed......')

    def train(self):
        df = pd.read_csv(self.outputCSV, low_memory=False, )
        df.dropna(inplace=True)
        df = df[df.notnull().all(axis=1)]

        X = df.iloc[:, [0, 1, 2, 3]].values
        y = df.iloc[:, -1].values

        n_estimator = 150
        max_depth = 30
        min_sample_split = 5
        min_sample_leaf = 2

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=10)

        clf = RandomForestRegressor(n_estimators=n_estimator, max_depth=max_depth, min_samples_split=min_sample_split,
                                    min_samples_leaf=min_sample_leaf, n_jobs=-1)
        clf.fit(X_train, y_train)
        print(clf.score(X_test, y_test))

        if os.path.isdir(MODEL_DIR) is False:
            os.mkdir(MODEL_DIR)

        dump(clf, os.path.join(MODEL_DIR, MODEL_NAME))

        return clf

    @staticmethod
    def predict(duration):
        # 'duration', 'comments', 'likes', 'dislikes'
        X = np.array([[duration, 100, 10000, 100]])
        clf = load(os.path.join(MODEL_DIR, MODEL_NAME))
        return clf.predict(X)
