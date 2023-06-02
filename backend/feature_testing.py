import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2

file_path = "/Users/nathantran/Documents/VSCode/salary_predictor/test3.csv"

df = pd.read_csv("2018.csv")

for column in df.columns:
    if df[column].dtype == float:
        new_column_name = column + '_ratio'
        df[new_column_name] = df[column] / df[column].mean()

target_column = ["Salary"]
# predictors = df.columns[~df.columns.isin(["Player", "Tm", "Lg", "Pos", "Salary"])]
# predictor_columns = ["Age", "G","GS","MP","FG","FGA","FG%",
#         "3P","3PA","3P%","2P","2PA","2P%","eFG%","FT","FTA","FT%","ORB","DRB","TRB","AST","STL",
#         "BLK","TOV","PF","PTS"]

# predictor_columns = ["Age_ratio","G_ratio","GS_ratio","MP_ratio","FG_ratio","FGA_ratio","FG%_ratio",
#         "3P_ratio","3PA_ratio","3P%_ratio","2P_ratio","2PA_ratio","2P%_ratio","eFG%_ratio","FT_ratio",
#         "FTA_ratio","FT%_ratio","ORB_ratio","DRB_ratio","TRB_ratio","AST_ratio","STL_ratio","BLK_ratio",
#         "TOV_ratio","PF_ratio","PTS_ratio"]

# predictor_columns = ["Age_ratio","TOT_G","TOT_GS","TOT_MP","TOT_FG","TOT_FGA","TOT_FG%","TOT_3P",
#         "TOT_3PA","TOT_3P%","TOT_2P","TOT_2PA","TOT_2P%","TOT_eFG%","TOT_FT","TOT_FTA","TOT_FT%",
#         "TOT_ORB","TOT_DRB","TOT_TRB","TOT_AST","TOT_STL","TOT_BLK","TOT_TOV","TOT_PF","TOT_PTS"]
predictor_columns = ["Age", "G","GS","MP","FG","FGA","FG%",
        "3P","3PA","3P%","2P","2PA","2P%","eFG%","FT","FTA","FT%","ORB","DRB","TRB","AST","STL",
        "BLK","TOV","PF","PTS",

      "TOT_G","TOT_GS","TOT_MP","TOT_FG","TOT_FGA","TOT_FG%","TOT_3P",
        "TOT_3PA","TOT_3P%","TOT_2P","TOT_2PA","TOT_2P%","TOT_eFG%","TOT_FT","TOT_FTA","TOT_FT%",
        "TOT_ORB","TOT_DRB","TOT_TRB","TOT_AST","TOT_STL","TOT_BLK","TOT_TOV","TOT_PF","TOT_PTS",
        
      "Age_ratio","G_ratio","GS_ratio","MP_ratio","FG_ratio","FGA_ratio","FG%_ratio",
        "3P_ratio","3PA_ratio","3P%_ratio","2P_ratio","2PA_ratio","2P%_ratio","eFG%_ratio","FT_ratio",
        "FTA_ratio","FT%_ratio","ORB_ratio","DRB_ratio","TRB_ratio","AST_ratio","STL_ratio","BLK_ratio",
        "TOV_ratio","PF_ratio","PTS_ratio",

      "TOT_G_ratio","TOT_GS_ratio","TOT_MP_ratio","TOT_FG_ratio",
        "TOT_FGA_ratio","TOT_FG%_ratio","TOT_3P_ratio","TOT_3PA_ratio","TOT_3P%_ratio","TOT_2P_ratio",
        "TOT_2PA_ratio","TOT_2P%_ratio","TOT_eFG%_ratio","TOT_FT_ratio","TOT_FTA_ratio","TOT_FT%_ratio",
        "TOT_ORB_ratio","TOT_DRB_ratio","TOT_TRB_ratio","TOT_AST_ratio","TOT_STL_ratio","TOT_BLK_ratio",
        "TOT_TOV_ratio","TOT_PF_ratio","TOT_PTS_ratio"]
predictors = df[predictor_columns]
df[predictor_columns] = predictors / predictors.max()

rr = RandomForestRegressor(n_estimators=100, random_state=42)

X = df[predictor_columns].values
y = df[target_column].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=40)

rr.fit(X_train, y_train)

# coef_1d = np.reshape(rr.coef_, (-1,))
# coef_table = pd.DataFrame({'Feature': predictor_columns, 'Coefficient': coef_1d})
# coef_table = coef_table.sort_values(by='Coefficient', ascending=False)
# new_df = df[['Salary', 'Tm']]

# # Sort the DataFrame based on 'salary' in descending order
# new_df = new_df.sort_values(by='Salary', ascending=False)

# # Reset the index of the DataFrame
# new_df = new_df.reset_index(drop=True)
# new_df.to_csv(file_path)

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


# print(df.shape)

predicted_values = rr.predict(X_test)

median_difference = np.median(np.abs(y_test - predicted_values))
print(median_difference)
differences = np.abs(y_test - predicted_values)
first_quartile = np.percentile(differences, 25)
third_quartile = np.percentile(differences, 75)

print(first_quartile)
print(third_quartile)




mae = mean_absolute_error(y_test, predicted_values)

print(df["Salary"].mean())

print(mae)

print(r2_score(y_test, predicted_values))

#team data, ratios, look at median quartiles