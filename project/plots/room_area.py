from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd


def generate_room_area_plot(df: pd.DataFrame, sorted_rooms: list[str], path: str = None):
    plt.figure(figsize=(10, 6))
    sns.barplot(x="Rooms", y="Area", data=df, order=sorted_rooms)
    plt.title("Rooms vs Area")

    if path:
        plt.savefig(path)

    plt.show()
