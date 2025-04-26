from flask import Flask, render_template
import boto3
from datetime import datetime, timezone

app = Flask(__name__)

@app.route('/')
def index():
    now = datetime.now(timezone.utc)
    start = now.replace(day=1).strftime('%Y-%m-%d')
    end = now.strftime('%Y-%m-%d')

    client = boto3.client('ce', region_name='us-east-1')

    response = client.get_cost_and_usage(
        TimePeriod={'Start': start, 'End': end},
        Granularity='MONTHLY',
        Metrics=['UnblendedCost'],
        GroupBy=[{
            'Type': 'DIMENSION',
            'Key': 'SERVICE'
        }]
    )

    services = []
    total = 0.0

    for group in response['ResultsByTime'][0]['Groups']:
        service = group['Keys'][0]
        cost = float(group['Metrics']['UnblendedCost']['Amount'])
        services.append({'name': service, 'cost': f"{cost:.4f}"})
        total += cost

    return render_template('index.html', services=services, total=f"{total:.2f}")

if __name__ == '__main__':
    app.run(debug=True)
# app.py
# This is a simple Flask application that fetches AWS cost data and displays it on a web page.  ss