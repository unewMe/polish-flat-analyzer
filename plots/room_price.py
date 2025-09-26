from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd


def generate_room_price_plot(df: pd.DataFrame, sorted_rooms: list[str], path: str = None):
    plt.figure(figsize=(10, 6))
    sns.barplot(x="Rooms", y="Price", data=df, order=sorted_rooms)
    plt.title("Rooms vs Price")

    if path:
        plt.savefig(path)

    plt.show()
