import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from project.src.process_data import Preprocessor

class HousingPricePredictor:
    def __init__(self, data, preprocessor=None, model=None):
        self.data = data.dropna()
        self.categorical_features = ['City', 'Furnished', 'Market', 'Building type']
        self.numerical_features = ['Area', 'Floor', 'Rooms']
        self.model = model if model is not None else RandomForestRegressor(random_state=42)

        self.preprocessor = preprocessor if preprocessor is not None else Preprocessor(data.copy())

        self.processed_data = self.preprocessor.preprocessed_data.copy()
        self.processed_data = self.processed_data.dropna()

        print(len(self.processed_data))

        self.split_data()

        self.train_model()

    def split_data(self):
        test_size = 0.15
        X_train_list, X_test_list, y_train_list, y_test_list = [], [], [], []
        decoded_data = self.preprocessor.decode_data(self.processed_data.copy())

        for city in self.data['City'].unique():
            city_data = self.processed_data[decoded_data['City'] == city]
            X_city = city_data.drop('Price', axis=1)
            y_city = city_data['Price']

            X_city_train, X_city_test, y_city_train, y_city_test = train_test_split(
                X_city, y_city, test_size=test_size)

            X_train_list.append(X_city_train)
            X_test_list.append(X_city_test)
            y_train_list.append(y_city_train)
            y_test_list.append(y_city_test)

        self.X_train = pd.concat(X_train_list)
        self.X_test = pd.concat(X_test_list)
        self.y_train = pd.concat(y_train_list)
        self.y_test = pd.concat(y_test_list)

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

    def predict_price(self, city=None, floor=None, furnished=None, market=None,
                      building_type=None, area=None, rooms=None, distance_to_city_center=None):
        input_data = {
            'City': [city if city is not None else 'Poznań'],
            'Floor': [floor if floor is not None else 1],
            'Furnished': [furnished if furnished is not None else 'yes'],
            'Market': [market if market is not None else 'secondary'],
            'Building type': [building_type if building_type is not None else 'blok'],
            'Area': [area if area is not None else self.data['Area'].mean()],
            'Rooms': [rooms if rooms is not None else "two"],
            'Distance to city center': [distance_to_city_center if distance_to_city_center is not None else 5.0]
        }
        input_df = pd.DataFrame(input_data)

        input_processed_data = self.preprocessor.cast_input(input_df)

        predicted_price = self.model.predict(input_processed_data)
        return predicted_price[0]

    def evaluate_model(self):
        y_pred = self.model.predict(self.X_test)
        mae = mean_absolute_error(self.y_test, y_pred)
        return mae

    def evaluate_model_by_city(self):
        decoded_test_data = self.preprocessor.decode_data(self.X_test.copy())
        results = {}
        for city in self.data['City'].unique():
            city_mask = decoded_test_data['City'] == city
            if city_mask.any():
                y_pred_city = self.model.predict(self.X_test[city_mask])
                mae_city = mean_absolute_error(self.y_test[city_mask], y_pred_city)
                results[city] = mae_city
        return results