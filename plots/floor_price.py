from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd


def generate_floor_price_plot(df: pd.DataFrame, sorted_floor: list[str], path: str = None):
    plt.figure(figsize=(10, 6))
    sns.barplot(x="Floor", y="Price", data=df, order=sorted_floor)
    plt.title("Floor vs Price")

    if path:
        plt.savefig(path)

    plt.show()

