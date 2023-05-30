import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2


df = pd.read_csv("2018.csv")

target_column = ["Salary"]
# predictors = df.columns[~df.columns.isin(["Player", "Tm", "Lg", "Pos", "Salary"])]
predictor_columns = ['Age', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%',
       '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%',
       'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']  #0.44745749913313604
# predictor_columns = ['Age', 'TOT_G', 'TOT_GS', 'TOT_MP', 'TOT_FG', 'TOT_FGA', 'TOT_FG%', 'TOT_3P',
#        'TOT_3PA', 'TOT_3P%', 'TOT_2P', 'TOT_2PA', 'TOT_2P%', 'TOT_eFG%',
#        'TOT_FT', 'TOT_FTA', 'TOT_FT%', 'TOT_ORB', 'TOT_DRB', 'TOT_TRB',
#        'TOT_AST', 'TOT_STL', 'TOT_BLK', 'TOT_TOV', 'TOT_PF', 'TOT_PTS']
# predictor_columns = ['Age', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%',
#        '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%',
#        'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS',
#        'TOT_G', 'TOT_GS', 'TOT_MP', 'TOT_FG', 'TOT_FGA', 'TOT_FG%', 'TOT_3P',
#        'TOT_3PA', 'TOT_3P%', 'TOT_2P', 'TOT_2PA', 'TOT_2P%', 'TOT_eFG%',
#        'TOT_FT', 'TOT_FTA', 'TOT_FT%', 'TOT_ORB', 'TOT_DRB', 'TOT_TRB',
#        'TOT_AST', 'TOT_STL', 'TOT_BLK', 'TOT_TOV', 'TOT_PF', 'TOT_PTS']
predictors = df[predictor_columns]
df[predictor_columns] = predictors / predictors.max()

# df[predictors] = df[predictors]/df[predictors].max()

rr = Lasso(alpha=0.1)

X = df[predictor_columns].values
y = df[target_column].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=40)

rr.fit(X_train, y_train)

# bestfeatures = SelectKBest(score_func=chi2, k=10)
# fit = bestfeatures.fit(X,y)
# dfscores = pd.DataFrame(fit.scores_)
# dfcolumns = pd.DataFrame(predictor_columns)
# #concat two dataframes for better visualization 
# featureScores = pd.concat([dfcolumns,dfscores],axis=1)
# featureScores.columns = ['Specs','Score']  #naming the dataframe columns
# print(featureScores.nlargest(10,'Score'))  #print 10 best features

# from sklearn.ensemble import ExtraTreesClassifier
# import matplotlib.pyplot as plt
# model = ExtraTreesClassifier()
# model.fit(X,y)
# print(model.feature_importances_) #use inbuilt class feature_importances of tree based classifiers
# #plot graph of feature importances for better visualization
# feat_importances = pd.Series(model.feature_importances_, index=predictor_columns)
# feat_importances.nlargest(10).plot(kind='barh')
# plt.show()

# import seaborn as sns
# import matplotlib.pyplot as plt
# corrmat = df[predictor_columns].corr()
# top_corr_features = corrmat.index
# plt.figure(figsize=(20,20))
# #plot heat map
# g=sns.heatmap(df[top_corr_features].corr(),annot=True,cmap="RdYlGn")


print(df.shape)

predicted_values = rr.predict(X_test)

mae = mean_absolute_error(y_test, predicted_values)

print(df["Salary"].mean())

print(mae)

print(r2_score(y_test, predicted_values))