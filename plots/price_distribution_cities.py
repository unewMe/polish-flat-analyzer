import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def generate_price_distribution_cities_plot(df: pd.DataFrame, save_path: str = None):
    unique_cities = df['City'].unique()

    fig, axes = plt.subplots(nrows=len(unique_cities) // 2 + len(unique_cities) % 2, ncols=2,
                             figsize=(15, 5 * len(unique_cities) // 2))

    axes = axes.flatten()

    for i, city in enumerate(unique_cities):
        ax = axes[i]
        city_data = df[df['City'] == city]
        sns.histplot(city_data['Price'], kde=True, ax=ax)
        ax.set_title(f'Price distribution in {city}')
        ax.set_xlabel('Price')
        ax.set_ylabel('Frequency')

        if save_path:
            plt.figure()
            sns.histplot(city_data['Price'], kde=True)
            plt.title(f'Price distribution in {city}')
            plt.xlabel('Price')
            plt.ylabel('Frequency')
            plt.savefig(f'{save_path}/price_distribution_{city}.png')
            plt.close()

    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()
