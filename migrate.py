#!/usr/bin/env python

import sys
import os
import logging
import psycopg2
import boto3

#database & S3 bucket
DB_CONN_STRING = os.getenv('DB_CONN_STRING', 'postgres://postgres:mysecretpassword@database-1.cxpqgzfn1lf4.us-east-1.rds.amazonaws.com/proddatabase')
S3_LEGACY_BUCKET = os.getenv('S3_LEGACY_BUCKET', 'legacy-s3-bucket2022')
S3_PRODUCTION_BUCKET = os.getenv('S3_PRODUCTION_BUCKET', 'production-s3-2022')

# S3 connection details
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', 'AKIAR27JRZKSG2VXQLMV')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', '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')
AWS_DEFAULT_REGION = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')