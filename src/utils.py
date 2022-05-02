import pandas as pd
from sklearn.linear_model import LogisticRegression
import numpy as np




def calculate_xg(df):
    df['goal'] = (df.outcome == 'goal').astype(int)
    df['xGoal'] = 100 - df.x
    df['yGoal'] = df.y - 50.
    df['distance'] = np.sqrt(df.xGoal**2 + df.yGoal**2)
    gsize = 9.6
    df['angle'] = np.arctan(gsize *df.xGoal /(df.xGoal**2 + df.yGoal**2 - (gsize/2)**2))
    df.loc[(df.angle < 0.), 'angle'] = np.pi +df.angle

    X = df[['distance', 'angle']].values
    y = df.goal.values

    clf = LogisticRegression()
    clf.fit(X,y)

    df['xG_calc'] = clf.predict_proba(X)[:,1]
    return df