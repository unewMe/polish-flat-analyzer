import pandas as pd
from sklearn.preprocessing import LabelEncoder
from dataclasses import dataclass


@dataclass
class Preprocessor:
    data: pd.DataFrame
    preprocessed_data: pd.DataFrame | None = None
    furnished_mapping = {}
    room_mapping = {}
    development_mapping = {}
    market_mapping = {}
    city_mapping = {}

    def __post_init__(self):
        self.preprocessed_data = self.preprocess_data(self.data)

    def preprocess_data(self, df):

        df['Floor'] = df['Floor'].apply(lambda x: int(x.replace('floor_', '')) if isinstance(x, str) else -1).astype(int)

        le_furnished = LabelEncoder()
        df['Furnished'] = le_furnished.fit_transform(df['Furnished'])
        self.furnished_mapping = dict(zip(le_furnished.classes_, le_furnished.transform(le_furnished.classes_)))

        le_rooms = LabelEncoder()
        df['Rooms'] = le_rooms.fit_transform(df['Rooms'])
        self.room_mapping = dict(zip(le_rooms.classes_, le_rooms.transform(le_rooms.classes_)))

        le_building = LabelEncoder()
        df['Building type'] = le_building.fit_transform(df['Building type'])
        self.development_mapping = dict(zip(le_building.classes_, le_building.transform(le_building.classes_)))

        le_market = LabelEncoder()
        df['Market'] = le_market.fit_transform(df['Market'])
        self.market_mapping = dict(zip(le_market.classes_, le_market.transform(le_market.classes_)))

        le_city = LabelEncoder()
        df['City'] = le_city.fit_transform(df['City'])
        self.city_mapping = dict(zip(le_city.classes_, le_city.transform(le_city.classes_)))

        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = pd.to_numeric(df[col], errors='coerce')

        return df

    def cast_input(self, input_data: pd.DataFrame):
        input_data['Furnished'] = input_data['Furnished'].map(self.furnished_mapping)
        input_data['Building type'] = input_data['Building type'].map(self.development_mapping)
        input_data['Market'] = input_data['Market'].map(self.market_mapping)
        input_data['Rooms'] = input_data['Rooms'].map(self.room_mapping)
        input_data['City'] = input_data['City'].map(self.city_mapping)

        return input_data
