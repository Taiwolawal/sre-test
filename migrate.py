#!/usr/bin/env python

import sys
import os
import logging
import psycopg2
import boto3

#database & S3 bucket
DB_CONN_STRING = os.getenv('DB_CONN_STRING', '<>')
S3_LEGACY_BUCKET = os.getenv('S3_LEGACY_BUCKET', '<>')
S3_PRODUCTION_BUCKET = os.getenv('S3_PRODUCTION_BUCKET', 'production-s3-2022')

# S3 connection details
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', '<>')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', '<>')
AWS_DEFAULT_REGION = os.getenv('AWS_DEFAULT_REGION', '<>')

#Connecting to S3
try:
    s3 = boto3.resource('s3',
                        aws_access_key_id=AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                        region_name=AWS_DEFAULT_REGION
                        )
except Exception as e:
    logging.error(f"Error while connecting to S3: {e}")
    sys.exit(1)

# Connect to db
try:
    conn = psycopg2.connect(DB_CONN_STRING)
except Exception as e:
    logging.error(f"Error while connecting to the database: {e}")
    sys.exit(1)


#Connecting to legacy S3 objetcs
legacy_bucket = s3.Bucket(S3_LEGACY_BUCKET)

#
for file in legacy_bucket.objects.all():
    new_key = file.key.split("/")
    new_key = 'avatar/' + new_key[-1]
    copy_source = {
        'Bucket': file.bucket_name,
        'Key': file.key
    }
    try:
        #Copy an object from one S3 location to another
        s3.meta.client.copy(copy_source, S3_PRODUCTION_BUCKET, new_key)
        update_row(conn, file.key, new_key)
        s3.Object(file.bucket_name, file.key).delete()
    except Exception as e:
        logging.error(f"Something went wrong: {e}")