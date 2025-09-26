from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd


def generate_city_price_plot(df: pd.DataFrame, sorted_cities: list[str], path: str = None):
    mid_index = len(sorted_cities) // 2
    first_half_cities = sorted_cities[:mid_index]
    second_half_cities = sorted_cities[mid_index:]

    df_first_half = df[df['City'].isin(first_half_cities)]
    df_second_half = df[df['City'].isin(second_half_cities)]

    plt.figure(figsize=(15, 12))
    sns.barplot(x="City", y="Price", data=df_first_half, order=first_half_cities)
    plt.title("City vs Price (First Half)")

    if path:
        plt.savefig(f"{path}_first_half.png")
    plt.show()

    plt.figure(figsize=(15, 12))
    sns.barplot(x="City", y="Price", data=df_second_half, order=second_half_cities)
    plt.title("City vs Price (Second Half)")

    if path:
        plt.savefig(f"{path}_second_half.png")
    plt.show()
