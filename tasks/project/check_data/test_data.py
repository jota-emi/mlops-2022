import pandas as pd
import scipy.stats

# Deterministic Test
def test_column_presence_and_type(data):
    print(type(data))
    # Disregard the reference dataset
    df = data

    required_columns = {
        "host_listings_count": pd.api.types.is_float_dtype,
        "review_scores_rating": pd.api.types.is_float_dtype,
        "neighbourhood_cleansed": pd.api.types.is_object_dtype,
        "property_type": pd.api.types.is_object_dtype,
        "accommodates": pd.api.types.is_int64_dtype,
        "room_type": pd.api.types.is_object_dtype,
        "bedrooms": pd.api.types.is_float_dtype,
        "beds": pd.api.types.is_float_dtype,
        "price": pd.api.types.is_float_dtype,
        "minimum_nights": pd.api.types.is_int64_dtype,
        "bathrooms_text": pd.api.types.is_float_dtype,
        "maximum_nights": pd.api.types.is_int64_dtype,
        "number_of_reviews": pd.api.types.is_int64_dtype,
        "latitude": pd.api.types.is_float_dtype,
        "longitude": pd.api.types.is_float_dtype,      
    }

    # Check column presence
    assert set(df.columns.values).issuperset(set(required_columns.keys()))

    for col_name, format_verification_funct in required_columns.items():

        assert format_verification_funct(df[col_name]), f"Column {col_name} failed test {format_verification_funct}"

# Deterministic Test
def test_column_ranges(data):
    
    # Disregard the reference dataset
    df = data

    ranges = {
        "price": (1, 1000000),
        "beds": (0, 99),
        "bathrooms_text": (0, 99),
        "accommodates": (1, 99999),
    }

    for col_name, (minimum, maximum) in ranges.items():

        assert df[col_name].dropna().between(minimum, maximum).all(), (
            f"Column {col_name} failed the test. Should be between {minimum} and {maximum}, "
            f"instead min={df[col_name].min()} and max={df[col_name].max()}"
        )

    
# mlflow run . -P reference_artifact=mlops_project_preprocess/data_preprocessed:latest