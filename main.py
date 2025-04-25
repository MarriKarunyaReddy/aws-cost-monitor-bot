import boto3
from datetime import datetime, timezone
import json
import csv

now = datetime.now(timezone.utc)

client = boto3.client('ce', region_name='us-east-1')

start = now.replace(day=1).strftime('%Y-%m-%d')
end = now.strftime('%Y-%m-%d')

response = client.get_cost_and_usage(
    TimePeriod={'Start': start, 'End': end},
    Granularity='MONTHLY',
    Metrics=['UnblendedCost'],
    GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
)

# Calculate total cost from group data
total_cost = 0.0
for group in response['ResultsByTime'][0]['Groups']:
    amount = float(group['Metrics']['UnblendedCost']['Amount'])
    total_cost += amount


# Send alert based on cost threshold
sns = boto3.client('sns')

if total_cost > 1.00:
    sns.publish(
        TopicArn='arn:aws:sns:us-east-1:xxxxxxxxxx:xxxxxxxxxx',
        Subject='AWS Free Tier Alert!',
        Message=f"Your total AWS cost this month is ${total_cost:.2f} — you've exceeded the $1 limit!"
    )
else:
    sns.publish(
        TopicArn='arn:aws:sns:us-east-1:137068226726:cost-sns-topic-arn',
        Subject='AWS Free Tier Alert!',
        Message=f"Current total cost is ${total_cost:.2f}. You're safe!"
    )


# Print service-wise breakdown
if 'Groups' in response['ResultsByTime'][0] and response['ResultsByTime'][0]['Groups']:
    print("Service-wise cost breakdown:")
    for group in response['ResultsByTime'][0]['Groups']:
        service = group['Keys'][0]
        service_cost = group['Metrics']['UnblendedCost']['Amount']
        print(f"{service}: ${service_cost}")
else:
    print("No service breakdown data available.")

# Export to CSV
with open('aws_cost_report.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Service', 'Cost (USD)'])

    if 'Groups' in response['ResultsByTime'][0] and response['ResultsByTime'][0]['Groups']:
        for group in response['ResultsByTime'][0]['Groups']:
            service = group['Keys'][0]
            service_cost = group['Metrics']['UnblendedCost']['Amount']
            writer.writerow([service, service_cost])

print("\n✅ Exported to aws_cost_report.csv")
