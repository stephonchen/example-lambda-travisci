# example-lambda-travisci
* Lambda deployment using Travis CI as Example
* Lambda function
  * Start/Stop/Reboot EC2 instances with tag:Environment=Staging

# Travis CI Configuration
* Please configure these environment variables in Travis CI:
```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_BUCKET_REGION
AWS_LAMBDA_FUNCTION_NAME
AWS_LAMBDA_HANDLER_NAME
AWS_IAM_ROLE
```
* Example
  * AWS_LAMBDA_FUNCTION_NAME: lamdba-blah
  * AWS_LAMBDA_HANDLER_NAME: lambda_function.lambda_handler
    * Please refer to src/lambda/lambda_function.py for details
  * AWS_IAM_ROLE: arn:aws:BLAHBLAH
    * Note: in ARN format

# AWS Configuration
* Create an IAM user for TravisCI deployment
* Create an IAM policy for TravisCI deployment
```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ListExistingRolesAndPolicies",
      "Effect": "Allow",
      "Action": [
        "iam:ListRolePolicies",
        "iam:ListRoles"
      ],
      "Resource": "*"
    },
    {
      "Sid": "CreateAndListFunctions",
      "Effect": "Allow",
      "Action": [
        "lambda:CreateFunction",
        "lambda:ListFunctions"
      ],
      "Resource": "*"
    },
    {
      "Sid": "DeployCode",
      "Effect": "Allow",
      "Action": [
        "lambda:GetFunction",
        "lambda:UpdateFunctionCode",
        "lambda:UpdateFunctionConfiguration"
      ],
      "Resource": [
        "arn:aws:lambda:<region>:<account-id>:function:<name-of-function>"
      ]
    },
    {
     "Sid": "SetRole",
      "Effect": "Allow",
      "Action": [
        "iam:PassRole"
      ],
      "Resource": "arn:aws:iam::<account-id>:role/*"
    }
  ]
}
```
* Create an IAM role and attach policy above

# API gateway
* Example JSON data for stopping EC2 instances with tag:Environment=Staging
```
{
    "tag": "Environment",
    "tag_value": "Staging",
    "EC2Action": "stop"
}
```

# Note
* (Beta) Travis CI deployment to AWS Lambda is still in Beta, and use at your own risk.
* Tests of Lambda function are not well-defined yet.

# References
* https://docs.travis-ci.com/user/deployment-v2/providers/lambda/
