import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from dataclasses import dataclass, field


@dataclass
class Preprocessor:
    data: pd.DataFrame
    preprocessed_data: pd.DataFrame = field(init=False)
    encoders: dict = field(default_factory=dict)
    mappings: dict = field(default_factory=dict)

    def __post_init__(self):
        self.encoders = {
            'Furnished': OneHotEncoder(sparse_output=False, handle_unknown='ignore'),
            'Building type': OneHotEncoder(sparse_output=False, handle_unknown='ignore'),
            'Market': OneHotEncoder(sparse_output=False, handle_unknown='ignore'),
            'City': OneHotEncoder(sparse_output=False, handle_unknown='ignore'),
            'Floor': OneHotEncoder(sparse_output=False, handle_unknown='ignore'),
            'Rooms': OneHotEncoder(sparse_output=False, handle_unknown='ignore')
        }
        self.preprocessed_data = self.preprocess_data(self.data)

    def preprocess_data(self, df):
        """Preprocesses the data by encoding categorical features."""
        df = df.copy()

        df['Floor'] = df['Floor'].apply(
            lambda x: int(x.replace('floor_', '')) if isinstance(x, str) and 'floor_' in x else x)

        for column, encoder in self.encoders.items():
            df[column] = df[column].astype(str)
            encoder.fit(df[[column]])
            encoded = encoder.transform(df[[column]])
            encoded_df = pd.DataFrame(encoded, columns=encoder.get_feature_names_out([column]), index=df.index)
            self.mappings[column] = {
                'categories': encoder.categories_[0],
                'feature_names': encoder.get_feature_names_out([column])
            }
            df = df.drop(column, axis=1).join(encoded_df)

        return df

    def cast_input(self, input_data: pd.DataFrame):
        """Casts the input data to the same format as the preprocessed data."""
        input_data = input_data.copy()
        for column, encoder in self.encoders.items():
            input_data[column] = input_data[column].astype(str)
            encoded = encoder.transform(input_data[[column]])
            encoded_df = pd.DataFrame(encoded, columns=encoder.get_feature_names_out([column]), index=input_data.index)
            input_data = input_data.drop(column, axis=1).join(encoded_df)
        return input_data

    def encode_data(self, df):
        """Encodes the categorical features of the data."""
        df = df.copy()
        for column in self.mappings.keys():
            if column.endswith('_reverse'):
                continue
            encoder = self.encoders[column]
            df[column] = df[column].astype(str)
            encoded = encoder.transform(df[[column]])
            encoded_df = pd.DataFrame(encoded, columns=encoder.get_feature_names_out([column]), index=df.index)
            df = df.drop(column, axis=1).join(encoded_df)

        return df

    def decode_data(self, df):
        """Decodes the categorical features of the data."""
        df = df.copy()
        for column, encoder in self.encoders.items():
            feature_names = self.mappings[column]['feature_names']
            categories = self.mappings[column]['categories']
            encoded_columns = [col for col in df.columns if col in feature_names]
            for idx, category in enumerate(categories):
                df.loc[df[encoded_columns].idxmax(axis=1) == encoded_columns[idx], column] = category
            df = df.drop(columns=encoded_columns)

        return df

    def encode_single_value(self, column, value):
        """Encodes a single value of a categorical feature."""
        encoder = self.encoders[column]
        return encoder.transform([[value]]).tolist()[0]

    def decode_single_value(self, column, encoded_value):
        """Decodes a single value of a categorical feature."""
        feature_names = self.mappings[column]['feature_names']
        categories = self.mappings[column]['categories']
        encoded_series = pd.Series(encoded_value, index=feature_names)
        return categories[encoded_series.idxmax()]

