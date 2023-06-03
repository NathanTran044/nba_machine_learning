import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score
import desired_player
import csv

# desired_player_input = input("Enter a player: ")
# desired_player_year_input = input("Enter the year of this player: ")
# desired_year_input = input("What year would you like to place this player in? ")

desired_player_input = "Stephen Curry"
desired_player_year_input = 2020
desired_year_input = 1987

# csv = "{}.csv".format(desired_year_input)
def calculate_salary(desired_player_input, desired_player_year_input, desired_year_input):
    csv = "/Users/nathantran/Documents/VSCode/salary_predictor/backend/csv_data/{}.csv".format(desired_year_input)

    df = pd.read_csv(csv)

    # sorted_df = df.sort_values('Salary', ascending=False)
    # sorted_df.to_csv("hi.csv")

    target_column = ["Salary"]
    predictors = df.columns[~df.columns.isin(["Player", "Tm", "Lg", "Pos", "Salary"])]

    max_values = df[predictors].max()
    
    df[predictors] = df[predictors]/max_values

    rr = RandomForestRegressor(n_estimators=100, random_state=42)
    # rr = Ridge(alpha=0.1)

    X = df[predictors].values
    y = df[target_column].values
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=40)

    rr.fit(X, y.ravel())

    # print(rr.)

    # predicted_values = rr.predict(X_test)

    # mae = mean_absolute_error(y_test, predicted_values)

    # print(df["Salary"].mean())

    # print(mae)

    # print(r2_score(y_test, predicted_values))



    X_pred = desired_player.get_desired_player(desired_player_input, desired_player_year_input)

    if all(value == 0 for value in X_pred.values()):
        print(desired_player_input, "was not found in the", desired_player_year_input, "database")
    else:
        X_pred_df = pd.DataFrame(X_pred, index=[1])

        # X_pred_df[predictors].to_csv("test.csv")

        X_pred_df[predictors] = X_pred_df[predictors].apply(pd.to_numeric, errors='coerce').fillna(0) # takes care of dividing 0 by 0
        X_pred_df_normalized = X_pred_df[predictors] / max_values
        X_pred_df_normalized.fillna(0, inplace=True)
        X_test = X_pred_df_normalized.values

        # print(X_test)

        # print(rr.coef_)

        predicted_values = rr.predict(X_test)
        return predicted_values.item(0)
        # print(desired_player_input, predicted_values)

print(calculate_salary(desired_player_input, desired_player_year_input, desired_year_input))