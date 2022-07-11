"""
Creator: João Marcos Viana
Date: 10 July. 2022
After the fetch step the raw data artifact was generated.
Now, we need to pre-processing the raw data to create a new artfiact (clean_data).
"""
import argparse
import logging
import os
import pandas as pd
import wandb

# configure logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(message)s",
                    datefmt='%d-%m-%Y %H:%M:%S')

# reference for a logging obj
logger = logging.getLogger()

def process_args(args):
    """
    Arguments
        args - command line arguments
        args.input_artifact: Fully qualified name for the raw data artifact
        args.artifact_name: Name for the W&B artifact that will be created
        args.artifact_type: Type of the artifact to create
        args.artifact_description: Description for the artifact
    """
    
    # create a new wandb project
    run = wandb.init(project="mlops_project_preprocess", 
                     job_type="process_data")
    
    logger.info("Downloading artifact")
    artifact = run.use_artifact(args.input_artifact)
    artifact_path = artifact.file()
    
    # create a dataframe from the artifact path
    df = pd.read_csv(artifact_path)
    
    # Delete duplicated rows
    logger.info("Dropping duplicates")
    df.drop_duplicates(inplace=True)

    # Delete useless columns
    features = ['host_listings_count', 'review_scores_rating', 'neighbourhood_cleansed', 
        'property_type', 'accommodates', 'room_type', 'bedrooms', 'beds', 'price',
        'minimum_nights', 'bathrooms_text','maximum_nights', 'number_of_reviews',
        'latitude', 'longitude',
       ]
    logger.info("Dropping useless columns")
    df = df[features]

    # Convert "price" column to float
    logger.info("Converting 'price' column to float")
    df.price = df.price.str.replace('$', '').str.replace(',', '', regex = 'true').astype(float)

    # Delete rows where 'price' = 0
    logger.info("Deleting rows where 'price' is 0")
    df = df.drop(df[df.price == 0].index)
    
    # Convert 'bathrooms_text' to float
    logger.info("Converting 'bathrooms_text' column to float")
    df.bathrooms_text = df.bathrooms_text.str.extract('(\d+)').astype(float)

    # Transform null rows in 'bathrooms_text' to 0
    logger.info("Transforming null rows in 'bathrooms_text' to 0")
    df['bathrooms_text'] = df['bathrooms_text'].fillna(0)

    # Transform null rows in 'beds' to 0
    logger.info("Transforming null rows in 'beds' to 0")
    df['beds'] = df['beds'].fillna(0)

    # Transform null rows in 'bedrooms' to 0
    logger.info("Transforming null rows in 'bedrooms' to 0")
    df['bedrooms'] = df['bedrooms'].fillna(0)

    # Transform null rows in 'review_scores_rating' to mean value
    logger.info("Transforming null rows in 'review_scores_rating' to mean value")
    df['review_scores_rating'] = df['review_scores_rating'].fillna(df['review_scores_rating'].mean())

    # Delete restant rows that contains some null value
    logger.info("Deleting restant rows that contains some null value")
    df = df.dropna()

    # Generate a "clean data file"
    filename = "preprocessed_data.csv"
    df.to_csv(filename,index=False)
    
    # Create a new artifact and configure with the necessary arguments
    artifact = wandb.Artifact(
        name=args.artifact_name,
        type=args.artifact_type,
        description=args.artifact_description
    )
    artifact.add_file(filename)
    
    # Upload the artifact to Wandb
    logger.info("Logging artifact")
    run.log_artifact(artifact)

    # Remote temporary files
    os.remove(filename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Preprocess a dataset",
        fromfile_prefix_chars="@"
    )

    parser.add_argument(
        "--input_artifact",
        type=str,
        help="Fully-qualified name for the input artifact",
        required=True
    )

    parser.add_argument(
        "--artifact_name", type=str, help="Name for the artifact", required=True
    )

    parser.add_argument(
        "--artifact_type", type=str, help="Type for the artifact", required=True
    )

    parser.add_argument(
        "--artifact_description",
        type=str,
        help="Description for the artifact",
        required=True
    )

    # get arguments
    ARGS = parser.parse_args()

    # process the arguments
    process_args(ARGS)

# mlflow run . -P input_artifact="jotaemi/mlops_project_etl/raw_data.csv:latest" -P artifact_name="data_preprocessed.csv" -P artifact_type="clean_data" -P artifact_description="preprocessed"