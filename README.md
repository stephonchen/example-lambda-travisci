# example-lambda-travisci
* Lambda deployment using TravisCI as Example

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

# Note
* (Beta) Travis CI deployment to AWS Lambda is still in Beta, and use at your own risk.

# References
* https://docs.travis-ci.com/user/deployment-v2/providers/lambda/
