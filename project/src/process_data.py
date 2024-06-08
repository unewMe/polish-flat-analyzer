import re

import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from dataclasses import dataclass, field


@dataclass
class Preprocessor:
    data: pd.DataFrame
    preprocessed_data: pd.DataFrame | None = None
    encoders: dict = field(default_factory=dict)
    room_mapping = {'one': 1, 'two': 2, 'three': 3, 'four': 4}
    reverse_room_mapping = {1: 'one', 2: 'two', 3: 'three', 4: 'four'}

    def __post_init__(self):
        self.encoders = {
            'Furnished': OneHotEncoder(sparse_output=False),
            'Building type': OneHotEncoder(sparse_output=False),
            'Market': OneHotEncoder(sparse_output=False),
            'City': OneHotEncoder(sparse_output=False)
        }
        self.preprocessed_data = self.preprocess_data(self.data)

    def preprocess_data(self, df):
        df['Floor'] = df['Floor'].apply(lambda x: re.sub(r'\D', '', str(x)) if isinstance(x, str) else x)
        df['Floor'] = pd.to_numeric(df['Floor'], errors='coerce')

        # Fill NaN values in 'Floor' column with a default value, e.g., 0
        df['Floor'] = df['Floor'].fillna(0).astype(int)
        df['Rooms'] = df['Rooms'].map(self.room_mapping).astype(int)
        df['Area'] = pd.to_numeric(df['Area'], errors='coerce')

        for column, encoder in self.encoders.items():
            df[column] = df[column].astype(str)
            encoder.fit(df[[column]])
            encoded = encoder.transform(df[[column]])
            df = df.drop(column, axis=1).join(pd.DataFrame(encoded, columns=encoder.get_feature_names_out([column])))

        return df

    def cast_input(self, input_data: pd.DataFrame):
        input_data['Rooms'] = input_data['Rooms'].map(self.room_mapping).astype(int)

        for column, encoder in self.encoders.items():
            encoded = encoder.transform(input_data[[column]])
            input_data = input_data.drop(column, axis=1).join(
                pd.DataFrame(encoded, columns=encoder.get_feature_names_out([column])))

        return input_data

    def encode_data(self, df):
        df['Rooms'] = df['Rooms'].map(self.room_mapping).astype(int)

        for column, encoder in self.encoders.items():
            df[column] = df[column].astype(str)
            encoded = encoder.transform(df[[column]])
            df = df.drop(column, axis=1).join(pd.DataFrame(encoded, columns=encoder.get_feature_names_out([column])))

        return df

    def decode_data(self, df):
        for column, encoder in self.encoders.items():
            encoded_columns = encoder.get_feature_names_out([column])
            for i, col in enumerate(encoded_columns):
                df.loc[df[col] == 1, column] = encoder.categories_[0][i]
            df = df.drop(columns=encoded_columns)

        df['Rooms'] = df['Rooms'].map(self.reverse_room_mapping)
        return df

    def encode_single_value(self, column, value):
        encoder = self.encoders[column]
        return encoder.transform([[value]]).tolist()[0]

    def decode_single_value(self, column, encoded_value):
        encoder = self.encoders[column]
        return encoder.inverse_transform([encoded_value]).tolist()[0][0]
