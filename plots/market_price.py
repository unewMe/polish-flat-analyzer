from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd


def generate_market_price_plot(df: pd.DataFrame, path: str = None):
    plt.figure(figsize=(10, 6))
    sns.barplot(x="Market", y="Price", data=df)
    plt.title("Market vs Price")

    if path:
        plt.savefig(path)

    plt.show()
