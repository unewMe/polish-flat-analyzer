from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd


def generate_building_price_plot(df: pd.DataFrame, path: str = None):
    plt.figure(figsize=(10, 6))
    sns.barplot(x="Building type", y="Price", data=df)
    plt.title("Building type vs Price")

    if path:
        plt.savefig(path)

    plt.show()
