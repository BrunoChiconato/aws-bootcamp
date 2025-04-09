"""This Python script checks the existence of a data directory, retrieves a CSV file from it,
and uploads the file to an S3 bucket.
"""

import boto3
import os
import glob


def ensure_path_exists(data_path: str) -> str:
    """
    Ensures that the specified directory exists.

    Args:
        data_path (str): The path of the directory to check.

    Returns:
        str: The validated directory path if it exists.

    Raises:
        FileNotFoundError: If the specified directory does not exist.
    """
    if os.path.exists(data_path):
        return data_path
    else:
        raise FileNotFoundError("Given directory not found.")


def remove_csv_file(csv_path: str) -> None:
    """
    Removes the specified CSV file from the filesystem.

    Args:
        csv_path (str): The full path of the CSV file to be removed.

    Returns:
        None
    """
    file_name = os.path.basename(csv_path)
    os.remove(csv_path)
    print(f'Successfully removed "{file_name}" from the given directory.')


def get_csv_file(csv_path: str) -> str:
    """
    Searches for a CSV file in the given directory.

    Args:
        csv_path (str): The path of the directory to search for CSV files.

    Returns:
        str: The full path of the found CSV file.

    Raises:
        RuntimeError: If more than one CSV file is found in the directory.
        FileNotFoundError: If no CSV file is found in the directory.
    """
    valid_csv_path = ensure_path_exists(csv_path)
    csv_files = glob.glob(os.path.join(valid_csv_path, "*.csv"))

    if len(csv_files) > 1:
        raise RuntimeError(
            f"Expected one csv file in the given directory. Got {len(csv_files)}."
        )
    elif not csv_files:
        raise FileNotFoundError(
            "There was not any csv files in the given directory."
        )
    else:
        return csv_files[0]


def upload_backup_to_s3(bucket_name: str, file_to_upload: str) -> None:
    """
    Uploads the specified file to the given S3 bucket and removes the file after successful upload.

    Args:
        bucket_name (str): The name of the S3 bucket.
        file_to_upload (str): The full path of the file to be uploaded.

    Returns:
        None
    """
    s3 = boto3.client("s3")
    file_to_upload_name = os.path.basename(file_to_upload)

    s3.upload_file(file_to_upload, bucket_name, file_to_upload_name)
    print(
        f'Successfully uploaded "{file_to_upload_name}" to "{bucket_name}" bucket.'
    )

    remove_csv_file(file_to_upload)


def main():
    """
    Main function that sets up the data directory and bucket name,
    then initiates the CSV upload process.

    Returns:
        None
    """
    root_folder = os.path.dirname(__file__)
    data_folder = os.path.join(root_folder, "data")
    bucket_name = "backup-cloud-bootcamp"

    try:
        upload_backup_to_s3(bucket_name, get_csv_file(data_folder))
    except Exception as e:
        print(str(e))


if __name__ == "__main__":
    main()
