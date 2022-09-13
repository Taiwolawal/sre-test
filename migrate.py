#!/usr/bin/env python

import sys
import os
import logging
import psycopg2
import boto3

DB_CONN_STRING = os.getenv('DB_CONN_STRING', 'postgres://postgres:mysecretpassword@database-1.cxpqgzfn1lf4.us-east-1.rds.amazonaws.com/proddatabase')
S3_LEGACY_BUCKET = os.getenv('S3_LEGACY_BUCKET', 'legacy-s3-bucket2022')
S3_PRODUCTION_BUCKET = os.getenv('S3_PRODUCTION_BUCKET', 'production-s3-2022')