from Util.DbUtil import DbUtil

from fastapi import FastAPI, Depends, status, HTTPException, Response
import os
print(os.getcwd())
import schemas # Import from same directory
from Authentication import auth, auth_bearer
import boto3
from botocore import UNSIGNED
from botocore.config import Config
from decouple import config 

app = FastAPI()
dbUtil = DbUtil('metadata.db')

########################################################################################################################
# AWS Destination Credentials:
aws_access_key_id = config('aws_access_key_id')
aws_secret_access_key = config('aws_secret_access_key')

# Destination S3 Directory:
dest_bucket = 'damg7245'
dest_folder = 'assignment1'
########################################################################################################################


# for TESTING
@app.get("/") # , status_code=status.HTTP_200_OK)
async def read_main():
    return {"msg": "Hello World"}


# POST file to S3 bucket from Streamlit UI
# test without token
# @app.post("/s3_transfer", status_code=status.HTTP_201_CREATED, tags=['files'])
@app.post("/s3_transfer", status_code=status.HTTP_201_CREATED, dependencies=[Depends(auth_bearer.JWTBearer())], tags=['files'])
# def copy_file_to_dest_s3(src_bucket, dest_bucket, dest_folder, prefix, files_selected):
def copy_file_to_dest_s3(request: schemas.S3_Transfer, response: Response):
    # Get S3 File:
    s3_src = boto3.client('s3', config=Config(signature_version=UNSIGNED))
    
    # determined by search method:
    if request.search_method == 'Field Selection':
        src_response = s3_src.get_object(Bucket=request.src_bucket, Key=request.prefix+request.file_name)
        # src_response = s3_src.get_object(Bucket='noaa-goes18', Key=request.prefix+request.file_name)
    elif request.search_method == 'File Name':
        src_response = s3_src.get_object(Bucket=request.src_bucket, Key=request.prefix+request.file_name)
        # src_response = s3_src.get_object(Bucket='noaa-goes18', Key=request.prefix+request.file_name)
        # src_response = s3_src.generate_presigned_url('get_object',
        #                                             Params={'Bucket': request.src_bucket,
        #                                                     'Key': request.file_name},
        #                                             ExpiresIn=expiration)
    

    # Upload S3 to Destination:
    s3_dest = boto3.client('s3',
                      aws_access_key_id=aws_access_key_id,
                      aws_secret_access_key=aws_secret_access_key)
    
    dest_file_name = f'{request.dest_folder}/{request.src_bucket}/{request.file_name}'

    # Raise except if file has already been transferred
    try:
        # raise client error
        s3_dest.head_object(Bucket=request.dest_bucket, Key=dest_file_name)
        # TODO: Conflict, since wfile exists, can add location if needed
        response.status_code = status.HTTP_409_CONFLICT
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'{request.file_name} already transferred to S3!')
    # Transfer file
    except:
        test = s3_dest.upload_fileobj(src_response['Body'], request.dest_bucket, dest_file_name)
        
        dest_url = f'https://{request.dest_bucket}.s3.amazonaws.com/{dest_file_name}'

        # API Response
        # TODO: 
        return {'Search Method': request.search_method, 'Destination s3 URL': dest_url}



# GET metadata options for 
@app.get("/field_selection", status_code=status.HTTP_200_OK, dependencies=[Depends(auth_bearer.JWTBearer())], tags=['files'])
# @app.get("/field_selection", status_code=status.HTTP_200_OK, tags=['files'])
# def filter(self, table_name, req_value, **input_values):
# util.filter("geos18", 'hour', product='ABI-L1b-RadC', year=year_selected, day_of_year=day_selected)
def filter(request: schemas.Field_Selection):
    # dbUtil.filter(self, table_name, req_value, **input_values)
    # TODO:
    filter_list = dbUtil.filter(request.table_name, request.req_value, **request.input_values)

    # return list of filter options
    # TODO:
    return {'Filter List': filter_list}



@app.post('/user/register', tags = ['user'])
def register(user: schemas.UserRegisterSchema):
    if not dbUtil.check_user_registered('users', user.email):
        dbUtil.insert('users', ['first_name', 'last_name', 'email', 'password_hash'], [(user.first_name, user.last_name, user.email, auth.get_password_hash(user.password))])
    else:
        raise HTTPException(status_code=409, detail='Invalid username and/or password')
    return auth.signJWT(user.email)


@app.post('/user/login', tags = ['user'])
def login(user: schemas.UserLoginSchema):
    if dbUtil.check_user('users', user.email, user.password):
        return auth.signJWT(user.email)
    else:
        raise HTTPException(status_code=401, detail='Invalid username and/or password')


