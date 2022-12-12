import boto3
from botocore.exceptions import ClientError

from constants import DATA_BUCKET_NAME


s3_client = boto3.client('s3')
sm_client = boto3.client('secretsmanager')


def get_s3_obj(key):
  return s3_client.get_object(Bucket=DATA_BUCKET_NAME, Key=key)


def get_secret(name):
  try:
    get_secret_value_response = sm_client.get_secret_value(
        SecretId=name
    )
  except ClientError as e:
    # For a list of exceptions thrown, see
    # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    raise e

  # Decrypts secret using the associated KMS key.
  return get_secret_value_response['SecretString']

