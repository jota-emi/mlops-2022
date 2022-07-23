"""
Creator: João Marcos Viana
Date: 22 July 2022
Test the inference artifact using test dataset.
"""

import argparse
import logging
import pandas as pd
import wandb
import mlflow.sklearn
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import roc_auc_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# configure logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(message)s",
                    datefmt='%d-%m-%Y %H:%M:%S')

# reference for a logging obj
logger = logging.getLogger()

def process_args(args):
    
    run = wandb.init(job_type="test")

    logger.info("Downloading and reading test artifact")
    test_data_path = run.use_artifact(args.test_data).file()
    df_test = pd.read_csv(test_data_path)

    # Extract the target from the features
    logger.info("Extracting target from dataframe")
    x_test = df_test.copy()
    y_test = x_test.pop("price")
    

    ## Download inference artifact
    logger.info("Downloading and reading the exported model")
    model_export_path = run.use_artifact(args.model_export).download()

    ## Load the inference pipeline
    pipe = mlflow.sklearn.load_model(model_export_path)

    ## Predict test data
    predict = pipe.predict(x_test)

    # Evaluation Metrics
    logger.info("Evaluation metrics")
    # Metric: MAE
    mae = mean_absolute_error(y_test, predict)
    run.summary["MAE"] = mae
    
    # Metric: MSE
    mse = mean_squared_error(y_test, predict)
    run.summary["MSE"] = mse

    r2 = r2_score(y_test, predict)
    run.summary["R2"] = r2

    
    # Metric: Confusion Matrix
    # Metric: Actual vs Predicted graph
    fig, ax = plt.subplots()
    ax.scatter(predict, y_test, edgecolors=(0, 0, 1))
    ax.set_ylim([0, 200000])
    ax.plot([y_test.min(), 200000], [y_test.min(), 200000], 'r--', lw=3)
    ax.set_xlabel('Predicted')
    ax.set_ylabel('Actual')
    
    # Uploading figures
    logger.info("Uploading figures")
    run.log(
        {
            "confusion_matrix": wandb.Image(fig)
        }
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Test the provided model on the test artifact",
        fromfile_prefix_chars="@",
    )

    parser.add_argument(
        "--model_export",
        type=str,
        help="Fully-qualified artifact name for the exported model to evaluate",
        required=True,
    )

    parser.add_argument(
        "--test_data",
        type=str,
        help="Fully-qualified artifact name for the test data",
        required=True,
    )

    ARGS = parser.parse_args()

    process_args(ARGS)