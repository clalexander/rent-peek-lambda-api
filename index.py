from __future__ import print_function

import json
from rent_peek_generation import get_data, send_user_email


def handler(event, context):
  try:
    # parse data
    user_data = parse_user_data(event)
    get_data(user_data)
    print('user data:', user_data)
    send_user_email(user_data)
    # invoke function try/catch
  except Exception as e:
    print('EXCEPTION:', e)
    return http_response(400, str(e))

  return http_response(201, 'Success')



def parse_user_data(event):
  body_raw = event['body']
  if body_raw is None:
    raise Exception('No body data provided')
  
  body = json.loads(body_raw)
  
  if 'zipcode' not in body:
    raise Exception('Property \'zipcode\' not provided')
  
  if 'rent' not in body:
    raise Exception('Property \'rent\' not provided')
  
  if 'beds' not in body:
    raise Exception('Property \'beds\' not provided')
  
  if 'baths' not in body:
    raise Exception('Property \'baths\' not provided')
  
  if 'email' not in body:
    raise Exception('Property \'email\' not provided')
  
  # full validation
  # if 'zipcode' not in body or not isinstance(body['zipcode'], int):
  #   raise Exception('Property \'zipcode\' not provided or is not of type int')
  
  # if 'rent' not in body or not isinstance(body['rent'], int):
  #   raise Exception('Property \'rent\' not provided or is not of type int')
  
  # if 'beds' not in body or (not isinstance(body['beds'], int) and not isinstance(body['beds'], str)):
  #   raise Exception('Property \'beds\' not provided or is not of type int or str')
  
  # if 'baths' not in body or (not isinstance(body['baths'], float) and not isinstance(body['baths'], int)):
  #   raise Exception('Property \'baths\' not provided or is not of type float or int')
  
  # if 'email' not in body or not isinstance(body['email'], str):
  #   raise Exception('Property \'email\' not provided or is not of type str')
  
  return body



def http_response(code, message):
  return {
    'body': json.dumps({
      'message': message
    }),
    'headers': {
      'Content-Type': 'application/json'
    },
    'statusCode': code
  }