import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from utils import data_string_to_float, status_calc


# The percentage by which a stock has to beat the S&P500 to be considered a 'buy'
OUTPERFORMANCE = 20


def build_data_set(outperformance):
    """
    Reads the keystats.csv file and prepares it for scikit-learn
    :return: X_train and y_train numpy arrays
    """
    training_data = pd.read_csv("keystats.csv", index_col="Date")
    training_data.dropna(axis=0, how="any", inplace=True)
    features = training_data.columns[6:]

    X_train = training_data[features].values
    # Generate the labels: '1' if a stock beats the S&P500 by more than 10%, else '0'.
    y_train = list(
        status_calc(
            training_data["stock_p_change"],
            training_data["SP500_p_change"],
            outperformance,
        )
    )

    return X_train, y_train


def predict_stocks(outperformance):
    X_train, y_train = build_data_set(outperformance)
    # Remove the random_state parameter to generate actual predictions
    clf = RandomForestClassifier(n_estimators=100, random_state=0)
    clf.fit(X_train, y_train)

    # Now we get the actual data from which we want to generate predictions.
    data = pd.read_csv("forward_sample.csv", index_col="Date")
    data.dropna(axis=0, how="any", inplace=True)
    features = data.columns[6:]
    X_test = data[features].values
    z = data["Ticker"].values

    # Get the predicted tickers
    y_pred = clf.predict(X_test)
    if sum(y_pred) == 0:
        print("No stocks predicted!")
    else:
        invest_list = z[y_pred].tolist()
        #print(invest_list)
        #print(
        #    f"{len(invest_list)} stocks predicted to outperform the S&P500 by more than {outperformance}%:"
        #)
        #print(invest_list)
        return invest_list


if __name__ == "__main__":
    print("Building dataset and predicting stocks...")
    print("outperformance = 20")
    print(predict_stocks(20))
    print("outperformance = 10")
    print(list(set(predict_stocks(10)) - set(predict_stocks(20))))
    print("outperformance = 5")
    print(list(set(predict_stocks(5)) - set(predict_stocks(10))))
    print("outperformance = 0")
    print(list(set(predict_stocks(0)) - set(predict_stocks(5))))
    #print("outperformance = -10")
    #print(list(set(predict_stocks(-10)) - set(predict_stocks(0))))
