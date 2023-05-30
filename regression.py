import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score


df = pd.read_csv("2018.csv")

target_column = ["Salary"]
predictors = df.columns[~df.columns.isin(["Player", "Tm", "Lg", "Pos", "Salary"])]

print(predictors)

df[predictors] = df[predictors]/df[predictors].max()

rr = Ridge(alpha=0.1)

X = df[predictors].values
y = df[target_column].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=40)

rr.fit(X_train, y_train)

# print(df.shape())

print(df.columns)

print(rr.coef_)

# feature_index = predictors.tolist().index("TOV")
# print(rr.coef_[0][feature_index])

predicted_values = rr.predict(X_test)

mae = mean_absolute_error(y_test, predicted_values)

print(df["Salary"].mean())

print(mae)

print(r2_score(y_test, predicted_values))