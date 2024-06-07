import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from project.src.process_data import Preprocessor


class HousingPricePredictor:
    def __init__(self, data, preprocessor=None, model=None):
        self.data = data
        self.categorical_features = ['City', 'Furnished', 'Market', 'Building type']
        self.numerical_features = ['Area', 'Floor', 'Rooms']
        self.model = model if model is not None else LinearRegression()

        self.preprocessor = preprocessor if preprocessor is not None else Preprocessor(data)

        self.processed_data = self.preprocessor.preprocessed_data

        self.split_data()

        self.train_model()

    def split_data(self):
        X = self.processed_data.drop('Price', axis=1)
        y = self.processed_data['Price']
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.05, random_state=42)

    def train_model(self):
        self.model.fit(self.X_train, self.y_train)

    def predict_price(self, city=None, floor=None, furnished=None, market=None,
                      building_type=None, area=None, rooms=None):
        input_data = {
            'City': [city if city is not None else 'Poznań'],
            'Floor': [floor if floor is not None else 1],
            'Furnished': [furnished if furnished is not None else 'yes'],
            'Market': [market if market is not None else 'secondary'],
            'Building type': [building_type if building_type is not None else 'blok'],
            'Area': [area if area is not None else self.data['Area'].mean()],
            'Rooms': [rooms if rooms is not None else "two"]
        }
        input_df = pd.DataFrame(input_data)

        input_processed_data = self.preprocessor.cast_input(input_df)

        predicted_price = self.model.predict(input_processed_data)
        return predicted_price[0]

    def evaluate_model(self):
        y_pred = self.model.predict(self.X_test)
        mae = mean_absolute_error(self.y_test, y_pred)
        return mae


if __name__ == '__main__':
    data = pd.DataFrame([
        {"City": "Białystok", "Floor": "floor_4", "Furnished": "yes", "Market": "secondary",
         "Price": 395000.0, "Building type": "blok", "Area": 42, "Rooms": "two"},
        {"City": "Białystok", "Floor": "floor_3", "Furnished": "yes",
         "Market": "secondary",
         "Price": 455900.0, "Building type": "blok", "Area": 39, "Rooms": "three"},
        {"City": "Białystok", "Floor": "floor_0", "Furnished": "yes",
         "Market": "secondary",
         "Price": 700000.0, "Building type": "blok", "Area": 58.7, "Rooms": "three"},
        {"City": "Białystok", "Floor": "floor_0", "Furnished": "no", "Market": "secondary",
         "Price": 412000.0, "Building type": "blok", "Area": 56, "Rooms": "three"},
        {"City": "Białystok", "Floor": "floor_1", "Furnished": "yes",
         "Market": "secondary",
         "Price": 585000.0, "Building type": "blok", "Area": 54.5, "Rooms": "three"}
    ])

    predictor = HousingPricePredictor(data)
    predicted_price = predictor.predict_price(city='Białystok', area=50)
    print(f'Przewidywana cena mieszkania: {predicted_price:.2f} PLN')

    mae = predictor.evaluate_model()
    print(f'Sredni błąd absolutny (MAE) na danych testowych: {mae:.2f} PLN')
