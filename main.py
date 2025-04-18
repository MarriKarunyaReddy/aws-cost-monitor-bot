import boto3
from datetime import datetime, timezone

now = datetime.now(timezone.utc)


client = boto3.client('ce', region_name='us-east-1')

start = now.replace(day=1).strftime('%Y-%m-%d')
end = now.strftime('%Y-%m-%d')

response = client.get_cost_and_usage(
    TimePeriod={'Start': start, 'End': end},
    Granularity='MONTHLY',
    Metrics=['UnblendedCost'],
    
)
import json
print(json.dumps(response, indent=2))

print("Cost so far:", response['ResultsByTime'][0]['Total']['UnblendedCost']['Amount'])

sns = boto3.client('sns')

cost = float(response['ResultsByTime'][0]['Total']['UnblendedCost']['Amount'])

if cost >= 0.90:  # Alert threshold based on $0.9s0 free-tier cap
    sns.publish(
        TopicArn='arn:aws:sns:us-east-1:xxxxxxxxxx:xxxxxxxxxx',
        Subject='AWS Free Tier Alert!',
        Message=f"Your EC2 cost this month is ${cost} — you're nearing the free tier limit!"
    )
else:
    sns.publish(
    TopicArn='arn:aws:sns:us-east-1:137068226726:cost-sns-topic-arn',
    Subject='AWS Free Tier Alert!',
    Message= f"Current Cost ${cost} is below the threshold.You're Safe."
    )
