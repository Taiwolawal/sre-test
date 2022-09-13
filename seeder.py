#!/usr/bin/env python

import sys
import os
import logging
import argparse
import psycopg2
import boto3

# Env variables for script configuration

# Connection string for the postgreSQL database. The database and schema must exist
# you can create the db and schema using
# --------------------------
# CREATE DATABASE proddatabase;
# CREATE TABLE IF NOT EXISTS avatars (
#   id SERIAL PRIMARY KEY,
#   path VARCHAR
# );
# --------------------------
DB_CONN_STRING = os.getenv('DB_CONN_STRING', 'postgres://postgres:mysecretpassword@127.0.0.1/proddatabase')

# filename to use for seeding the S3 bucket. If ommitted it will use the dummy avatar
AVATAR_FILE = os.getenv('AVATAR_FILE', False)

# S3 bucket name to use. It should exist and be accessible to your AWS credentials
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME', 'legacy-s3')

# S3 connection details
S3_ENDPOINT_URL = os.getenv('S3_ENDPOINT_URL', 'http://localhost:9000')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', 'minioadmin')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', 'minioadmin')
AWS_DEFAULT_REGION = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')


DUMMY_AVATAR=b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x14\x00\x00\x00\x14\x08\x06\x00\x00\x00\x8d\x89\x1d\r\x00\x00\x00\x01sRGB\x00\xae\xce\x1c\xe9\x00\x00\x00\x84eXIfMM\x00*\x00\x00\x00\x08\x00\x05\x01\x12\x00\x03\x00\x00\x00\x01\x00\x01\x00\x00\x01\x1a\x00\x05\x00\x00\x00\x01\x00\x00\x00J\x01\x1b\x00\x05\x00\x00\x00\x01\x00\x00\x00R\x01(\x00\x03\x00\x00\x00\x01\x00\x02\x00\x00\x87i\x00\x04\x00\x00\x00\x01\x00\x00\x00Z\x00\x00\x00\x00\x00\x00\x00H\x00\x00\x00\x01\x00\x00\x00H\x00\x00\x00\x01\x00\x03\xa0\x01\x00\x03\x00\x00\x00\x01\x00\x01\x00\x00\xa0\x02\x00\x04\x00\x00\x00\x01\x00\x00\x00\x14\xa0\x03\x00\x04\x00\x00\x00\x01\x00\x00\x00\x14\x00\x00\x00\x00A\xe7\x9d\xfe\x00\x00\x00\tpHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x01YiTXtXML:com.adobe.xmp\x00\x00\x00\x00\x00<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="XMP Core 6.0.0">\n   <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">\n      <rdf:Description rdf:about=""\n            xmlns:tiff="http://ns.adobe.com/tiff/1.0/">\n         <tiff:Orientation>1</tiff:Orientation>\n      </rdf:Description>\n   </rdf:RDF>\n</x:xmpmeta>\n\x19^\xe1\x07\x00\x00\x04<IDAT8\x11\xd5\x94ml\x14E\x18\xc7\xff3\xbb\xb7\xdd\xbb\xde\xedmm{G\xdbkKK+P,\x84\x16\x9aR\x82\xbc\x88U\x081\x12r\x1f\xb4\xc4\xa4Q\xe3\x0b\x81\x84\x90\xf8\x01M<\x8dZ\x8c!\xa8\x81\xa0QQ"&X\x90\x82\t\xd1\x14b\x8a\x14[\x8dP"\x14\xae\xa9\x05l\x9b\xb4\xa5w\xbd^\xaf\xbd\x97\xdd\x9b\x1d\xe7\n$$\xc6\x0fF\xbf8\xd9Iv^\x9e\xdf\xf3\xff\xcf\xe4\x19\xe0\xff\xd8\xc8\x7f%\x9ap\x8eYXk\xab_\xfa\xb7\xd0\xfbU\xcd\xc2z[\xfd\xca?\x85\xf2@\x80\xce\xaa"\x04\\\x04\xd3\xce7W~\x99\xeb\x92\x1e\x1dI\xf0\xcd\xebv\x9f\xbfp\x17\x98I\x96Y\xff\xdb\x96qv\x97\x01\xf9\xde\x0f\xa0\x96V\x16\xabO+b\xa2{0\xf9UGK\xe3\x81\xf4\xd4\xe0\xa1\xf5-\xc1\xb0 \xfd\x05\xca9\x17\x10"D\xad\x11\x8c\x8e\xf4\xa7-[\x1fO\x8d\xf5\xe5\xe2\xc3\x9dKv\x01+\xec\xa7\xdeX\xd3t\xec\x95\x1a\xbe\xbaB2\xbaZV\xf2\xe41?GmSuF\xd6\xe7\x815\xea\xfd\xf22\xb0{c\xce\xef\x9c\xf7P\xdb\xaa\xef\xc7\xce\xecH\xd0u\xab\\\x9b\x9b\x9b|O\x94\xe6Y\x07\x96U8\xf1\xc9\xae\xb5RQn\x92\xdd\x98\x98\xb2~}\xe6\xc2q\x11X\xd6\x1c\xe8H\xb6\xfa\xef\x04n\xdf\xbe!+\xa3\xac\xf9\xa9\xe6\xd5G\xdem\xf2\x11r\x8c]9\xba\xe5-\x9fW{\x8c\xbbj\x14\x12<\xb5 \x187\x9d\xc3\x03\x03\xd2\x89\ng\xf4=\rA\xc7\x8c\xba\x99\x17+m\\\xf2\xbcJ\xcf\xa7jo\xb7\x9f>\xe2\xff\xe0\xe3\x13?\x06\x02\x01Y\xf4tF\xdd\x95\xb6\xa6\x9e\xaf/\x86wn}\xc8\xe1/+\xe3/\x87\xa2n\x96\x8aG8\x19;7\xd7\x82\xe9$\xaf\xef\xc7\x8d\xe7\x1a\xae\x96\xf96\xfe@n\xc45X\xc3\xbf\xc0S\xb9<y\xf0\xb3\xa3j\xfb\xd1\xbd=\xbd\xa3\xa8\x11V\xa9PW\xfd[\xfb\xbe\xe7\xe7\xb9/m\xbb\xde\xdf\xdf]\xbb4\xbf>\xd8G\x98Se\x92\xafx\x91E5\xb7\xdd\xfa)h\xe0\xa3\x93W\xcbC\xd9\xcd\xc4\xca\xa9@C\xdd2|wq\x181SR\xf6\x1d\xfa\x16R\x8eG>\xfb~\xdd\xee\xc6\x1aw\x17\xe0\xbc|\xfc\xf4\xc9m\x91\xe8\xb8\xb5d\xa1^?\x12N\xb1y\x85\xa6T\x90\xcb\x91\x98\x18\xe0r,.\xe3\xa5=\xa3\x19\x17Vx\xec:5\xe21<\xd2\xf4"\xce\xbd\xfd\x0e\xfc\xcb\x9d\xf4\x9b\xbd\xcf\xf2\xc5\xf2\xe1\xea\xc9\x99P\xf5\x99\x9e\x19\xb1\x8dY.z\x93;\xf5E\xd2@H\xb5\x1e\xf4j\x12a\xa3\x88\xa74\x18,I\xe4\xe0\xcd\x10\x19\x1d\x8e\x88\x8ds\xa8ft\xc3vm?^k,\x80k)P2\xb9\x1b%Y \xaa\xa3\xc2JL3\xb6c\x03\xa3\x85\xf9s\xe9\xa6\xf5\x8b\xa9;\xdb\x03\x9a\x8eR"{\xc0L\tFb\x1c\xaa\x8dCv\xe7\xd4\tX\xa7\xe8\xa3\xf0y\x17\xc2\x119\x88\xca\x180`\xbe\x80Kq\'J\xe8\xcf<\x9b\xdd\xa6\xf9\x9aB\xb7=\xb9\x88YyEd\xae\xc7\x01\x9e\xb2\xe0\xd2u\xc0F \xb1\x19\xe8z\x14H3\x90\xf6=\x1b\xd9\xe0\xad(\xd5\x1dCx\xb8\xca\x86\x94\xe9\x00\x93,L\xdf\xd4pvpAz\xd0+\xc9\xc5\xe1\x8e\x16#\xaf\xb0oKc\xd1\x17\xa5\x05\x94[\x02\xc6!\x9cZ!\xdc\x1aJ\xc1&\xe7 M%\x14\xe7Y\x96<\':\x8c\xf9\xe5vD\xe2\x0e\x8c\x8e\x98P\x94\x04\xb2$\nw\xd18\xeam]d~ZG\xee\xda\x86j"+\xde\xf2|S\x94\x0ce\xd1\x14\x97\x15\x1aC(\xe1E_x\x1e\xe23\x11\xa8.\r\x93)@\x96JryL\xb1\x90\xb6\x860\x15R\xa1\x11\n\xea\xa2bL\xe0\xf3TI\xbaA8U\xcdM\xbaN\x10\x9d\x8cr=G\x93\x99\xb0&\xdbMd)&\xd6\xaf(\x81+\xbb\x0c\xe1\x89\x08:{os\xd9@\x8cd\nZq\x01v)\r\x85Q\xc0\x14\x9f\xb8P\x96`\xe0\xdc"\x13\xb6\xdfy\xb6+\x9f\xb8\x90&0&ER\r\xd3F\x01\x86\'\x1c\x90c\x83\xf0\xe8\x14\x91\xa9(\xe4\xa1~"\xcbDe\xca\xb4\t\x83\xc8\x9c\x8az\x87#\xcd\xedvJLC\xbc\x08\x160\x1d\x03w{\xabP\xa0\xfd\x013!^\'\xc1\xbc|-\xc6\xc9P\x16)(\x9c\xe6I\x1a!Q\x91V2S\xa4\xee\x81\x14\xfb\x13\x98\xa5\xd1\xcf\xf3\\\xed\xcf\x00\x00\x00\x00IEND\xaeB`\x82'


def generate_path(n):
    num = 0
    while num < n:
        yield f"image/avatar-{num}.png"
        num += 1


def insert_db_row(connection, path):
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO avatars (path) VALUES (%s)", (path,))
        conn.commit()
    except Exception as e:
        logging.error(f"Error inserting to the database: {e}")
        sys.exit(1)


def create_s3_object(s3_conn, bucket, path):
    try:
        if AVATAR_FILE:
            s3_conn.Bucket(bucket).upload_file(Key=f"{path}", Filename=AVATAR_FILE)
        else:
            s3_conn.Bucket(bucket).put_object(Key=f"{path}", Body=DUMMY_AVATAR)
    except Exception as e:
        logging.error(f"Error while creating an s3 object: {e}")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='This script seeds the database and s3 bucket with the number of legacy avatars passed as a first argument.')
    parser.add_argument('number_of_avatars', type=int, help='Number of legacy avatars to create')
    args = parser.parse_args()

    # Connect to db
    try:
        conn = psycopg2.connect(DB_CONN_STRING)
    except Exception as e:
        logging.error(f"Error while connecting to the database: {e}")
        sys.exit(1)


    # Initialize s3 resource
    try:
        s3 = boto3.resource('s3',
                            endpoint_url=S3_ENDPOINT_URL,
                            aws_access_key_id=AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                            region_name=AWS_DEFAULT_REGION
                            )
    except Exception as e:
        logging.error(f"Error while connecting to S3: {e}")
        sys.exit(1)

    # Generate as many legacy avatars as requested
    for path in generate_path(args.number_of_avatars):
        insert_db_row(conn, path)
        create_s3_object(s3, S3_BUCKET_NAME, path)

    print(f"Created {args.number_of_avatars} legacy avatars")