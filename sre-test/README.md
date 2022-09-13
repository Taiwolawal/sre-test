## sre-test
The task of the SRE-challenge is it to ensure that all images moved from legacy-s3 to production-s3 are updated with there paths in the database. All objects in the legacy bucket/path are correctly moved to the new production bucket/path.

# Development Setup
* Ensure your IAM user setting up the database and S3 bucket has the necessary permission to work with the AWS services.

* Create your database on AWS using PostgreSQL, with the username, password and security group settings needed to access the database.

* Create your S3 buckets for legacy and production with a global unique name respectively for each buckets.

