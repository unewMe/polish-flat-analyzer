import pandas as pd
import abc
import os
from matplotlib import pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.linear_model import LinearRegression
from project.src.process_data import Preprocessor


class HousingPricePredictor(metaclass=abc.ABCMeta):
    def __init__(self, data, preprocessor=None, model=None, subname =''):
        self.data = data.dropna()
        self.categorical_features = ['City', 'Furnished', 'Market', 'Building type']
        self.numerical_features = ['Area', 'Floor', 'Rooms']

        self.preprocessor = preprocessor if preprocessor is not None else Preprocessor(data.copy())

        self.processed_data = self.preprocessor.preprocessed_data.copy()
        self.processed_data = self.processed_data.dropna()

        self.model = model

        self.subname = subname

        self.split_data()

    def split_data(self):
        """Splits the data into training and testing sets."""
        test_size = 0.15
        X_train_list, X_test_list, y_train_list, y_test_list = [], [], [], []
        decoded_data = self.preprocessor.decode_data(self.processed_data.copy())

        for city in self.data['City'].unique():
            city_data = self.processed_data[decoded_data['City'] == city]
            X_city = city_data.drop('Price', axis=1)
            y_city = city_data['Price']

            X_city_train, X_city_test, y_city_train, y_city_test = train_test_split(
                X_city, y_city, test_size=test_size, random_state=42)

            X_train_list.append(X_city_train)
            X_test_list.append(X_city_test)
            y_train_list.append(y_city_train)
            y_test_list.append(y_city_test)

        self.X_train = pd.concat(X_train_list)
        self.X_test = pd.concat(X_test_list)
        self.y_train = pd.concat(y_train_list)
        self.y_test = pd.concat(y_test_list)

    @abc.abstractmethod
    def train_model(self):
        """Trains the model."""
        pass

    def predict_price(self, city=None, floor=None, furnished=None, market=None,
                      building_type=None, area=None, rooms=None, distance_to_city_center=None):
        """Predicts the price of a flat based on the input data."""
        input_data = {
            'City': [city if city is not None else 'Katowice'],
            'Floor': [floor if floor is not None else 2],
            'Furnished': [furnished if furnished is not None else 'no'],
            'Market': [market if market is not None else 'secondary'],
            'Building type': [building_type if building_type is not None else 'blok'],
            'Area': [area if area is not None else self.processed_data['Area'].mean()],
            'Rooms': [rooms if rooms is not None else "two"],
            'Distance to city center': [distance_to_city_center if distance_to_city_center is not None else 5.0]
        }
        input_df = pd.DataFrame(input_data)

        input_processed_data = self.preprocessor.cast_input(input_df) # encode input data

        predicted_price = self.model.predict(input_processed_data)
        return predicted_price[0]

    def evaluate_model(self):
        """Evaluates the model using the Mean Absolute Error (MAE)."""
        y_pred = self.model.predict(self.X_test)
        mae = mean_absolute_error(self.y_test, y_pred)
        return mae

    def evaluate_model_by_city(self):
        """Evaluates the model by city using the Mean Absolute Error (MAE)."""
        decoded_test_data = self.preprocessor.decode_data(self.X_test.copy())
        results = {}
        for city in self.data['City'].unique(): # for each city
            city_mask = decoded_test_data['City'] == city
            if city_mask.any():
                y_pred_city = self.model.predict(self.X_test[city_mask])
                mae_city = mean_absolute_error(self.y_test[city_mask], y_pred_city)
                results[city] = mae_city
        return results

    def is_occasional(self, price, city=None, floor=None, furnished=None, market=None,
                      building_type=None, area=None, rooms=None, distance_to_city_center=None):
        """Checks if the price is occasional based on the input data and MAE."""

        predicted_price = self.predict_price(city=city, floor=floor, furnished=furnished, market=market,
                                             building_type=building_type, area=area, rooms=rooms,
                                             distance_to_city_center=distance_to_city_center)
        return price <= predicted_price - self.evaluate_model()

    def plot_actual_vs_predicted_by_city(self, save_dir=None, subname=''):
        """Plots the actual vs predicted prices by city."""
        decoded_test_data = self.preprocessor.decode_data(self.X_test.copy())
        y_pred = self.model.predict(self.X_test)

        for city in self.data['City'].unique():
            city_mask = decoded_test_data['City'] == city
            if city_mask.any():
                plt.figure(figsize=(10, 8))
                plt.scatter(self.y_test[city_mask], y_pred[city_mask], alpha=0.3)
                plt.plot([self.y_test[city_mask].min(), self.y_test[city_mask].max()],
                         [self.y_test[city_mask].min(), self.y_test[city_mask].max()], 'k--', lw=2)
                plt.xlabel('Actual Prices')
                plt.ylabel('Predicted Prices')
                plt.title(f'{self.subname}: Actual vs Predicted Prices - {city}')

                if save_dir and os.path.isdir(save_dir):
                    plt.savefig(f"{save_dir}/rvp_{city}_{subname}.png")

                plt.show()

    def plot_residuals_by_city(self, save_dir=None, subname=''):
        """Plots the distribution of residuals by city."""
        decoded_test_data = self.preprocessor.decode_data(self.X_test.copy())
        y_pred = self.model.predict(self.X_test)

        for city in self.data['City'].unique():
            city_mask = decoded_test_data['City'] == city
            if city_mask.any():
                residuals = self.y_test[city_mask] - y_pred[city_mask]
                plt.figure(figsize=(10, 8))
                sns.histplot(residuals, kde=True)
                plt.xlabel('Residuals')
                plt.ylabel('Frequency')
                plt.title(f'{self.subname}: Distribution of Residuals - {city}')

                if save_dir and os.path.isdir(save_dir):
                    plt.savefig(f"{save_dir}/residuals_{city}_{subname}.png")

                plt.show()

    def plot_mae_by_city(self, save_dir=None, subname=''):
        """Plots the Mean Absolute Error (MAE) by city."""
        mae_by_city = self.evaluate_model_by_city()
        cities = list(mae_by_city.keys())
        mae_values = list(mae_by_city.values())

        mid_index = len(cities) // 2
        cities_first_half = cities[:mid_index]
        cities_second_half = cities[mid_index:]
        mae_values_first_half = mae_values[:mid_index]
        mae_values_second_half = mae_values[mid_index:]

        plt.figure(figsize=(15, 8))
        ax1 = sns.barplot(x=cities_first_half, y=mae_values_first_half)
        plt.xlabel('City')
        plt.ylabel('Mean Absolute Error (MAE)')
        plt.title(f'{self.subname}: Mean Absolute Error (MAE) by City - First Half')
        plt.xticks(rotation=0)

        for i, value in enumerate(mae_values_first_half):
            ax1.text(i, value + 0.01, f'{value:.2f}', ha='center', va='bottom')

        if save_dir and os.path.isdir(save_dir):
            plt.savefig(f"{save_dir}/mae_first_half_{subname}.png")

        plt.show()

        plt.figure(figsize=(15, 8))
        ax2 = sns.barplot(x=cities_second_half, y=mae_values_second_half)
        plt.xlabel('City')
        plt.ylabel('Mean Absolute Error (MAE)')
        plt.title(f'{self.subname}: Mean Absolute Error (MAE) by City - Second Half')
        plt.xticks(rotation=0)

        for i, value in enumerate(mae_values_second_half):
            ax2.text(i, value + 0.01, f'{value:.2f}', ha='center', va='bottom')

        if save_dir and os.path.isdir(save_dir):
            plt.savefig(f"{save_dir}/mae_second_half_{subname}.png")

        plt.show()


class RandomForestPredictor(HousingPricePredictor):
    """Random Forest Predictor class."""
    _SUBNAME: str = 'Random_forest'
    def __init__(self, data, preprocessor=None):
        super().__init__(data, preprocessor, model=RandomForestRegressor(random_state=42), subname=self._SUBNAME)
        self.train_model()

    def train_model(self):
        # Optimize hyperparameters
        param_grid = {
            'n_estimators': [100, 200],
            'max_depth': [10, 20, None],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4]
        }
        grid_search = GridSearchCV(estimator=self.model, param_grid=param_grid, cv=3, n_jobs=-1, verbose=2)
        grid_search.fit(self.X_train, self.y_train)
        self.model = grid_search.best_estimator_

    def plot_residuals_by_city(self, save_dir=None, subname=''):
        subname = subname if subname else self.subname
        super().plot_residuals_by_city(save_dir, subname)

    def plot_actual_vs_predicted_by_city(self, save_dir=None, subname=''):
        subname = subname if subname else self.subname
        super().plot_actual_vs_predicted_by_city(save_dir, subname)

    def plot_mae_by_city(self, save_dir=None, subname=''):
        subname = subname if subname else self.subname
        super().plot_mae_by_city(save_dir, subname)


class LinearPredictor(HousingPricePredictor):
    """Linear Predictor class."""
    _SUBNAME: str = 'Linear'

    def __init__(self, data, preprocessor=None):
        super().__init__(data, preprocessor, model=LinearRegression(), subname=self._SUBNAME)
        self.train_model()

    def train_model(self):
        self.model.fit(self.X_train, self.y_train)

    def plot_residuals_by_city(self, save_dir=None, subname=''):
        subname = subname if subname else self.subname
        super().plot_residuals_by_city(save_dir, subname)

    def plot_actual_vs_predicted_by_city(self, save_dir=None, subname=''):
        subname = subname if subname else self.subname
        super().plot_actual_vs_predicted_by_city(save_dir, subname)

    def plot_mae_by_city(self, save_dir=None, subname=''):
        subname = subname if subname else self.subname
        super().plot_mae_by_city(save_dir, subname)
