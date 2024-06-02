def preprocess_data(df):
    df['Floor'] = df['Floor'].apply(lambda x: x.replace('floor_', '') if isinstance(x, str) else x)

    df['Furnished'] = df['Furnished'].map({'no': '0', 'yes': '1'})

    room_mapping = {'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5'}
    df['Rooms'] = df['Rooms'].map(room_mapping)

    development_mapping = {'kamienica': '2', 'apartamentowiec': '3', 'blok': '1', 'pozostale': '0', 'loft': '4'}
    df['Building type'] = df['Building type'].map(development_mapping)

    market_mapping = {'secondary': '2', 'primary': '1'}
    df['Market'] = df['Market'].map(market_mapping)

    return df
