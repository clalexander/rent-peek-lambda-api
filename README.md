# rent-peek-lambda-api

## Description

Lambda + API Gateway handler for a rent peek email function.  Rent peek generation provided by client, modified to work on Lambda.

## How to Use

### Get Invoke URL

Get the `apiGatewayInvokeURL` output value from the Lambda API Gateway stack outputs.  (See 'Setup' below for stack instructions.)

### Request

```js
{
  url: '<invokeURL>',
  method: 'POST', // or other method if configured differently
  data: {
    zipcode: 12345,                 // int
    rent: 1234,                     // int
    beds: 1,                        // int
    baths: 1.5,                     // float
    email: 'user_email@domain.com'  // string
  }
}
```

** Note: request body requires types as indicated above

### Success Response

```json
// Status code 201
{
  "message": "Success"
}
```

### Bad Request Response

```json
// Status code 400
{
  "message": "<Error message>"
}
```

Error message may be a validation error or may be an internal error if there is a bad configuration.

## Setup

### Step 0: Development Environment

Install python if not already installed.

Set up repository:
```bash
> git clone <repo> [<dir>]
> cd <dir>
```

Optional: Create virtual environment
```bash
# https://docs.python.org/3/library/venv.html
# linux/mac
> python3 -m venv .venv
> source .venv/bin/activate

# windows
> python -m venv .venv
> .venv\Scripts\activate
```

Optional: Install requirements
```bash
# linux/mac
> python3 -m pip install -r requirements.txt

# windows
> python -m pip install -r requirements.txt
```

### Step 1: Archive Lambda and Layer Code

Create archives of the lambda code and the dependencies layer code. (Skip this step if you have been provided with the archives.)

** **This only works on linux**

```bash
# pack lambda archive
> scripts/pack.sh
# ...
# output: dist/lambda.zip

# pack dependencies archive
# installs dependencies in folder for use in lambda layer
> scripts/pack_deps.sh
# ...
# output dist/lambda_deps.zip
```

### Step 2: Add Email Credentials Secret

From the AWS Console:

1. Navigate to AWS Secrets Manager
1. Click "Store a new secret"
1. Select "Other type of secret"
1. Enter "user" as the first key and the smtp email as the first value
1. Click "+ Add row" to add another key/value pair
1. Enter "pw" as the key and the smtp password as the value
1. Click "Next"
1. Enter any name for the secret name (ex. "prod/RentPeek/EmailCreds") and **take note of this name**
1. Click "Next"
1. Click "Next" again
1. Click "Store"

### Step 3: Create Buckets Stack

From the AWS Console:

1. Navigate to CloudFormation
1. Click "Create stack"
1. Under "Specify template" click "Upload a template file"
1. Click "Choose file" and select the `stacks/buckets.yml` file from your project
1. Click "Next"
1. Enter a stack name (ex. "RentPeekBuckets")
1. Enter stack parameters
1. Click "Next"
1. Click "Next" again
1. Click "Submit"

### Step 4: Add Resources to New Bucket

From the AWS Console:

1. Navigate to S3
1. Open the newly created bucket
1. Create two new folders: "archives" and "data"
1. In the "archives" folder, upload the `lambda.zip` and `lambda_deps.zip` archives
1. In the "data" folder, upload the `rental_data.csv` and `zipcode_coverage.zip` files
1. Take note of the names of all the uploaded files

### Step 5: Create Lambda API Gateway Stack

From the AWS Console:

1. Navigate to CloudFormation
1. Click "Create stack"
1. Under "Specify template" click "Upload a template file"
1. Click "Choose file" and select the `stacks/lambda-api-gateway.yml` file from your project
1. Click "Next"
1. Enter a stack name (ex. "RentPeekLambdaAPIGateway")
1. Enter stack parameters, entering correct names for the bucket, bucket resource keys, and secret name
1. Click "Next"
1. Click "Next" again
1. Check "I acknowledge that AWS CloudFormation might create IAM resources."
1. Click "Submit"
1. Wait until CloudFormation completes adding the resources
1. Click the "Outputs" tab
1. Copy the `apiGatewayInvokeURL` output value; this is your invoke URL

### Step 6: Test Endpoint

Follow usage instructions above to test the endpoint.

## How to Update Resources

### Updating S3 Reources

This works for both data and archive resources.

From the AWS Console:

1. Navigate to S3
1. Click the associated bucket
1. Navigate to the parent folder of the resource.
1. Upload the new file

### Updating Lambda Code

#### Option 1

Best way so as not to accidentally lose code.

1. Update the code in the repository
1. Create a new lambda archive (Setup Step 1)
1. Update the lambda archive in S3 (above)
1. Copy the "Object URL"
1. Navigate to AWS Lambda
1. Select the Lambda function
1. From the Code tab, click "Upload from"
1. Select "Amazon S3 location"
1. Enter the object URL
1. Click "Save"

#### Option 2

Good for quick testing, but be sure to update the repository when done.

1. Navigate to AWS Lambda
1. Select the Lambda function
1. From the Code tab, select the file to edit and edit in place
1. Click "Deploy" when ready

### Updating Dependencies

1. Update `requirements.txt` in the repository
1. Create a new dependencies archive (Setup Step 1)
1. Update the dependencies archive in S3 (above)
1. Copy the "Object URL"
1. Navigate to AWS Lambda
1. Select "Layers" (on the left)
1. Select the layer
1. Click "Create version"
1. Select "Upload a file from "Amazon S3"
1. Enter the object URL
1. Click "Create"
1. Wait until create process is complete
1. Navigate to the Lambda function
1. From the Code tab at the bottom of the page in the Layers section, click "Edit"
1. Select the most recent layer version
1. Click "Save"

### Updating CloudFormation Stacks

From the AWS Console:

1. Navigate to CloudFormation
1. Select the stack you want to update
1. Click "Update"
1. Follow the prompts to update the stack