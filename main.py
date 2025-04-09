import boto3
import os
import glob

root_folder = os.path.dirname(__file__)
data_folder = os.path.join(root_folder, 'data')

try:
    if os.path.exists(data_folder):
        csv_files = glob.glob(os.path.join(data_folder,'*.csv'))
    else:
        os.mkdir(data_folder)

    if csv_files:
        s3 = boto3.client('s3')
        bucket_name = 'backup-cloud-bootcamp'
        for csv_file in csv_files:
            file_name = os.path.basename(csv_file)
            s3.upload_file(csv_file, bucket_name, file_name)
            os.remove(csv_file)
    else:
        raise FileNotFoundError("There was not any csv files in the 'data' folder!")
except Exception as e:
    print(str(e))