import io
import json
import pandas as pd
from aws import get_s3_obj, get_secret

from constants import RENTAL_DATA_KEY, ZIPCODE_COVERAGE_KEY, EMAIL_CREDS_SECRET_NAME

def get_csv_df(key):
  csv_obj = get_s3_obj(key)
  body = csv_obj['Body']
  read_body = body.read()
  # hack because windows is encoding the file differently
  try:
    csv_str = read_body.decode('windows-1252')
  except:
    csv_str = read_body.decode('utf-8')
  return pd.read_csv(io.StringIO(csv_str))


def get_rental_data():
  return get_csv_df(RENTAL_DATA_KEY)


def get_zipcode_coverage_data():
  return get_csv_df(ZIPCODE_COVERAGE_KEY)


def get_email_creds():
  secret = get_secret(EMAIL_CREDS_SECRET_NAME)
  return json.loads(secret)