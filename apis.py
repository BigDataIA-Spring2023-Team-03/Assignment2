from fastapi import FastAPI, Depends, status, Response, HTTPException
import os
print(os.getcwd())
import schemas # Import from same directory
import boto3
from botocore import UNSIGNED
from botocore.config import Config
from botocore.errorfactory import ClientError # checking if file exists already
from decouple import config 

app = FastAPI()

########################################################################################################################
# AWS Destination Credentials:
aws_access_key_id = config('aws_access_key_id')
aws_secret_access_key = config('aws_secret_access_key')

# Destination S3 Directory:
dest_bucket = 'damg7245'
dest_folder = 'assignment1'
########################################################################################################################


# for TESTING
@app.get("/hello") # , status_code=status.HTTP_200_OK)
async def read_main():
    return {"msg": "Hello World"}



# GET all files based on metadata filters


# POST file to S3 bucket from Streamlit UI
@app.post("/s3_transfer", status_code=status.HTTP_201_CREATED, tags=['files'])
# def copy_file_to_dest_s3(src_bucket, dest_bucket, dest_folder, prefix, files_selected):
def copy_file_to_dest_s3(request: schemas.S3_Transfer):
    # Get S3 File:
    s3_src = boto3.client('s3', config=Config(signature_version=UNSIGNED))
    
    src_response = s3_src.get_object(Bucket=request.src_bucket, Key=request.prefix+request.files_selected)
    src_response = s3_src.get_object(Bucket='noaa-goes18', Key=request.prefix+request.files_selected)


    # Upload S3 to Destination:
    s3_dest = boto3.client('s3',
                      aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key)
    
    dest_file_name = f'{request.dest_folder}/{request.src_bucket}/{request.files_selected}'

    # Raise except if file has already been transferred
    try:
        # raise client error
        s3_dest.head_object(Bucket='damg7245', Key=dest_file_name)
        # TODO: CHANGE STATUS
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{request.files_selected} already transferred to S3!')
    # Transfer file
    except:
        test = s3_dest.upload_fileobj(src_response['Body'], request.dest_bucket, dest_file_name)
        
        dest_url = f'https://{request.dest_bucket}.s3.amazonaws.com/{dest_file_name}'

    # API Response
    # TODO: 
    return dest_url

