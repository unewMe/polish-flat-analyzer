from matplotlib import pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import pandas as pd


def generate_city_center_price_plot(df: pd.DataFrame, path: str = None, if_regression: bool = False):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x="Distance to city center", y="Price", data=df)
    plt.title("Distance to City Center vs Price")

    if if_regression:
        X = df[["Distance to city center"]]
        y = df["Price"]
        reg = LinearRegression().fit(X, y)
        y_pred = reg.predict(X)

        slope = reg.coef_[0]
        intercept = reg.intercept_
        equation = f"y = {slope:.2f}x + {intercept:.2f}"

        plt.plot(df["Distance to city center"], y_pred, color='red', linewidth=2, label=f'Regression Line: {equation}')
        plt.legend()

    if path:
        plt.savefig(path)

    plt.show()
