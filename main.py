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
    GroupBy=[{
        'Type': 'DIMENSION',
        'Key': 'SERVICE'
    }]
)

# Try getting total cost
try:
    total_cost = float(response['ResultsByTime'][0]['Total']['UnblendedCost']['Amount'])
except (KeyError, ValueError, TypeError):
    total_cost = 0.0
    print("Error fetching cost or invalid value: 'UnblendedCost'")

# Export to CSV
with open('aws_cost_report.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Service', 'Cost (USD)'])

    for group in response['ResultsByTime'][0]['Groups']:
        service = group['Keys'][0]
        cost = group['Metrics']['UnblendedCost']['Amount']
        writer.writerow([service, cost])
        print(f"{service}: ${cost}")

print("\n✅ Exported to aws_cost_report.csv")
print(f"Total Cost So Far: ${total_cost}")
