## sre-test
The task of the SRE-challenge is it to ensure that all images moved from legacy-s3 to production-s3 are updated with there paths in the database. All objects in the legacy bucket/path are correctly moved to the new production bucket/path.

# Development Setup
* Using Python programming language to execute the task

* Ensure your IAM user setting up the database and S3 bucket has the necessary permission to work with the AWS services.

* Create database on AWS using PostgreSQL, with username, password and security group settings needed to access the database.

* Create your S3 buckets for legacy and production with a global unique name respectively for each buckets.

* Create database named 'proddatabase' in the PostgreSQL created and create table "avatar" in prodatabase.

* To interact with the AWS service (Database, S3), we make use of boto3 

* In the seeder.py file enter the necessary credentials and details needed and run the file with number of avatar images required.

* R

# Performance and Scalability
* The program is highly scalable irrespective of the volume of files needed to be transfered from one S3 to another.
* For performance, since file are transferred from one S3 to another S3 within the same AWS account, it will be very efficient

# Privileges
* Postgres user need the following priviliges to perform the task
CONNECT: Allows the grantee to connect to the database
SELECT:  This privilege is needed to reference existing column values in.
UPDATE: Allows UPDATE of any column, or specific column(s) of a table

* S3 user need the following priviliges to perform the task
Setup bucketpolicy with allow permission on the following
CreateBucket - To Create legacy and production bucket
ListBucket - To list out all buckets created
GetObject - To get objects in the buckets
CopyObject - Creates a copy of an object that is already stored in Legacy S3 to production
PutObject - Put object from legacy S3 to Production S3
DeleteObject - Delete object from Legacy S3.
