from matplotlib import pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import pandas as pd


def generate_area_price_plot(df: pd.DataFrame, path: str = None, if_regression: bool = False):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x="Area", y="Price", data=df)
    plt.title("Area vs Price")

    if if_regression:
        X = df["Area"].values.reshape(-1, 1)
        y = df["Price"].values
        reg = LinearRegression().fit(X, y)
        y_pred = reg.predict(X)

        slope = reg.coef_[0]
        intercept = reg.intercept_
        equation = f"y = {slope:.2f}x + {intercept:.2f}"

        plt.plot(df["Area"], y_pred, color='red', linewidth=2, label=f'Regression Line: {equation}')
        plt.legend()

    if path:
        plt.savefig(path)

    plt.show()
