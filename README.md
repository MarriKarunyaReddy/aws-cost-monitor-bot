# AWS Cost Monitor Bot (Boto3 + SNS)

A simple Python script to monitor AWS costs using **AWS Cost Explorer** and **SNS**. It fetches the current month’s usage cost from AWS, displays it, and sends an email alert via SNS when a set cost threshold is reached. This project is perfect for practicing AWS SDK (`boto3`) and automating cost management on AWS.

## Features
- Fetches AWS cost data via the **AWS Cost Explorer** API
- Monitors cost for specific AWS services (e.g., EC2, S3, etc.)
- Sends **email notifications** via **AWS SNS** when usage exceeds a defined threshold
- Displays the unblended cost in USD for the current billing period
- Compatible with AWS **Free Tier** and lightweight usage

## Tech Stack
- **Python 3**: Scripting and automation
- **boto3**: AWS SDK for Python, used to interact with AWS services
- **AWS SNS**: To send notifications when a cost threshold is exceeded
- **AWS Cost Explorer API**: To retrieve usage and billing data

## Setup

1. **Install dependencies**:
   ```bash
   pip install boto3
   
## Setup

-Create AWS Credentials: Ensure your AWS credentials are properly set up. If you're running this script locally, ensure that AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_DEFAULT_REGION are configured (either through environment variables or in the AWS credentials file).

-Create an SNS Topic:

-Go to the Amazon SNS Console.

-Create a new SNS Topic and copy the Topic ARN.

-Subscribe your email to the topic to receive notifications when usage crosses thresholds.

-Update the Script:

-Replace 'arn:aws:sns:us-east-1:xxxxxxxxxx:xxxxxxxxxxx' in the script with your own SNS Topic ARN.

Optionally, adjust the cost threshold and the service you want to track (e.g., EC2, Lambda, etc.).

Run the Bot:

To track your AWS usage and receive notifications, simply run the main.py script:
